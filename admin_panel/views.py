from django.shortcuts import render, redirect
from django.contrib import admin

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.http import HttpResponse

from admin_panel.forms import AddCallForm, CheckCallForm
from admin_panel.models import CallInfo

import time
import datetime
import pandas as pd


GROUP_INSER = 'Внесення даних'
GROUP_CHECK = 'Перегляд даних'


def is_member(user, group):
    return user.groups.filter(name=group).exists()


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('[signup]: reg success')
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            group = Group.objects.get(name='Внесення даних')
            user.groups.add(group)
            return redirect('profile')
    else:
        print('[signup]: reg error')
        form = UserCreationForm()
    return render(request, 'signup.html', context={'form': form})


def index(request):
    return render(request, 'base.html')


def profile(request):
    if request.user.is_authenticated():
        context_dict = {
            'in_check_group': is_member(request.user, GROUP_CHECK)
        }
        print('[context_dict]: ', context_dict)
        print('[GROUP_INSER]: ', is_member(request.user, GROUP_INSER))
        print('[request.user]: ', request.user)
        return render(request, 'profile.html', context=context_dict)
    return render(request, 'base.html')


def insert_data(request):
    if request.user.is_authenticated() and is_member(request.user, GROUP_INSER):
        if request.method == 'POST':
            form = AddCallForm(request.POST)
            if form.is_valid():
                ft_start = time.mktime(time.strptime(str(form.instance.time_start.time()), "%H:%M:%S"))
                ft_end = time.mktime(time.strptime(str(form.instance.time_end.time()), "%H:%M:%S"))
                interval = (datetime.timedelta(seconds=ft_end - ft_start))
                form.instance.interval = interval
                form.save(request)
            else:
                print(form.errors)
        else:
            form = AddCallForm()
        return render(request, 'insert_data.html', {'form': form})
    return render(request, 'base.html')


def check_data(request):
    search_form = False
    if request.user.is_authenticated() and is_member(request.user, GROUP_CHECK):
        if request.method == 'POST':
            form = CheckCallForm(request.POST)

            if form.is_valid():
                # TODO Ajax
                formated_formDatetime = str(form.instance.time_start.strftime("%Y-%m-%d %H:%M:%S %Z"))
                formated_pd_formDatetime = pd.to_datetime(formated_formDatetime).to_pydatetime()

                formated_datetimeNow = datetime.datetime.now().replace(microsecond=0).isoformat(' ')
                formated_pd_datetimeNow = pd.to_datetime(formated_datetimeNow).to_pydatetime()
                print(formated_pd_formDatetime, '\n', formated_pd_datetimeNow)
                print('update_time_sec: ', form.cleaned_data.get('update_time_sec'))
                requested_form = CallInfo.objects.filter(time_start__range=[
                    formated_pd_formDatetime, formated_pd_datetimeNow
                ])
                print(time_sum(requested_form))
                search_form = requested_form
        else:
            form = CheckCallForm()

        return render(request, 'check_data.html', {'form': form, 'search_form': search_form})
    return render(request, 'base.html')


def time_sum(query_set):
    total_time = datetime.timedelta(hours=0, minutes=0, seconds=0)
    for i in query_set:
        query_time = pd.to_datetime(i.interval).to_pydatetime()
        total_time = total_time + datetime.timedelta(
            hours=query_time.hour, minutes=query_time.minute, seconds=query_time.second
        )
    return total_time


def i18n_javascript(request):
    return admin.site.i18n_javascript(request)


def ajax_data_gen(request):
    if request.method == 'GET':
        data = request.GET
        form_datetime = data['date_time']
        interval = data['interval']

        pd_formDatetime = pd.to_datetime(form_datetime).to_pydatetime()

        datetimeNow = datetime.datetime.now().replace(microsecond=0).isoformat(' ')
        pd_datetimeNow = pd.to_datetime(datetimeNow).to_pydatetime()

        print('[ajax_return_search_data] dates :\n', pd_datetimeNow, '\n', datetimeNow)
        print('[ajax_return_search_data] interval:  ', interval)

        unfiltered_callInfo_data = CallInfo.objects.filter(time_start__range=[
            pd_formDatetime, pd_datetimeNow
        ])
        incoming_calls = unfiltered_callInfo_data.filter(type_call='Вхiдний')
        incoming_interval_sum = time_sum(incoming_calls)
        incoming_count = incoming_calls.count()

        outcoming_calls = unfiltered_callInfo_data.filter(type_call='Вихiдний')
        outcaming_interval_sum = time_sum(outcoming_calls)
        outcaming_count = outcoming_calls.count()

        all_interval_sum = time_sum(unfiltered_callInfo_data)
        sum_count_calls = unfiltered_callInfo_data.count()

        html = render(request, 'search_form.html', {
            'incoming_calls': incoming_calls,
            'incoming_interval_sum': incoming_interval_sum,
            'incoming_count': incoming_count,
            'outcoming_calls': outcoming_calls,
            'outcoming_interval_sum': outcaming_interval_sum,
            'outcoming_count': outcaming_count,
            'all_interval_sum': all_interval_sum,
            'sum_count_calls': sum_count_calls
        })
        return HttpResponse(html)
    else:
        print('[ajax_data_gen] error')
        html = render(request, 'search_form.html', {})
        return HttpResponse(html)
