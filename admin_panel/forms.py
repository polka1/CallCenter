from django import forms
from django.contrib.admin.widgets import AdminSplitDateTime, AdminDateWidget, AdminTimeWidget
from django.forms import widgets
from admin_panel.models import CallInfo


class AddCallForm(forms.ModelForm):
    TYPE_CALL_CHOICES = (
        ('Вхiдний', 'Вхiдний'),
        ('Вихiдний', 'Вихiдний')
    )
    time_start = forms.SplitDateTimeField(label='Початок дзвiнка', widget=AdminSplitDateTime)
    time_end = forms.SplitDateTimeField(label='Кiнець дзвiнка',  widget=AdminSplitDateTime)
    number = forms.CharField(label='Номер телефону', max_length=13, widget=widgets.TextInput)
    type_call = forms.ChoiceField(label='Тип дзвiнка', widget=forms.RadioSelect, choices=TYPE_CALL_CHOICES)
    interval = forms.CharField(max_length=16, required=False, widget=forms.HiddenInput())
    # author_id = forms.HiddenInput()

    class Meta:
        model = CallInfo
        fields = ('time_start', 'time_end', 'number', 'type_call', 'interval')
        # widgets = {
        #     'time_start': AdminSplitDateTime(),
        #     'time_end': AdminSplitDateTime()
        # }
        # exclude = ['author_id']


class CheckCallForm(forms.ModelForm):
    time_start = forms.SplitDateTimeField(label='Початок дзвiнка', widget=AdminSplitDateTime)
    update_time_sec = forms.IntegerField(label='Iнтервал обовлення')

    class Meta:
        model = CallInfo
        fields = {'time_start', 'update_time_sec'}
