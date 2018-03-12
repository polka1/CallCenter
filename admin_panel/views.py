from django.shortcuts import render, redirect
from django.contrib import admin

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from admin_panel.forms import AddCallForm, CheckCallForm
from admin_panel.models import CallInfo

import time
import datetime
import pandas as pd

from tornado_websockets.websocket import WebSocket


from django.contrib import messages

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
            # messages.success(request, 'Account created successfully')
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
        print('[context_dict]: ',context_dict)
        print('[GROUP_INSER]: ',is_member(request.user, GROUP_INSER))
        print('[request.user]: ',request.user)
        return render(request, 'profile.html', context=context_dict)
    return render(request, 'base.html')


def insert_data(request):
    if request.user.is_authenticated() and is_member(request.user, GROUP_INSER):
        if request.method == 'POST':
            form = AddCallForm(request.POST)
            if form.is_valid():
                print(form.instance.time_start)
                ft_start = time.mktime(time.strptime(str(form.instance.time_start.time()), "%H:%M:%S"))
                ft_end = time.mktime(time.strptime(str(form.instance.time_end.time()), "%H:%M:%S"))
                interval = str(datetime.timedelta(seconds=ft_end - ft_start))
                # form. ('interval', interval)
                form.instance.interval = interval
                print(form.instance.interval)
                # print(form.interval)
                form.save(request)
                # return insert_data(request)
            else:
                print(form.errors)
                # print(form.time_start)
                # print(form.time_end)
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
                requested_form = CallInfo.objects.filter(time_start=formated_pd_formDatetime)#.order_by('-time_start')
                search_form = requested_form
        else:
            form = CheckCallForm()

        return render(request, 'check_data.html', {'form': form, 'search_form': search_form})
    return render(request, 'base.html')


def i18n_javascript(request):
    return admin.site.i18n_javascript(request)
