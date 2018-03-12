from django import forms
# from django.forms.extras.widgets import SelectDateWidget
from django.contrib.admin.widgets import AdminSplitDateTime, AdminDateWidget, AdminTimeWidget
from django.forms import widgets


from admin_panel.models import CallInfo

from django.contrib.auth.models import User
from admin_panel.models import CallInfo


class AddCallForm(forms.ModelForm):
    TYPE_CALL_CHOICES = (
        ('Вхiдний', 'Вхiдний'),
        ('Вихiдний', 'Вихiдний')
    )
    time_start = forms.SplitDateTimeField(label='Початок дзвiнка', widget=AdminSplitDateTime)
    time_end = forms.SplitDateTimeField(label='Кiнець дзвiнка',  widget=AdminSplitDateTime )
    number = forms.CharField(label='Номер телефону', max_length=13, widget=widgets.TextInput)
    type_call = forms.ChoiceField(label='Тип дзвiнка', widget=forms.RadioSelect, choices=TYPE_CALL_CHOICES)
    # author_id = forms.HiddenInput()

    class Meta:
        model = CallInfo
        fields = ('time_start', 'time_end', 'number', 'type_call')
        widgets = {
            # 'time_start': AdminSplitDateTime(),
            # 'time_end': AdminSplitDateTime()
        }
        # exclude = ['author_id']


class CheckCallForm(forms.ModelForm):
    time_start = forms.SplitDateTimeField(label='Початок дзвiнка', widget=AdminSplitDateTime)
    interval = forms.IntegerField()

    class Meta:
        model = CallInfo
        fields = {'time_start', 'interval'}
