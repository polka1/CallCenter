from django.db import models

from django.contrib.auth.models import User

"""
    (
    время начала, время окончания, телефон, 
    тип звонка (входящий/исходящий)), 
    которая при нажатии соответствующей кнопки сохранится в базу данных.
"""


class CallInfo(models.Model):
    TYPE_CALL_CHOICES = (
        ('Вхiдний', 'Вхiдний'),
        ('Вихiдний', 'Вихiдний')
    )
    # author = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.CASCADE,
    # )
    created_at = models.DateTimeField(auto_now_add=True)
    time_start = models.DateTimeField()
    time_end = models.DateTimeField()
    number = models.CharField(max_length=13)
    type_call = models.CharField(max_length=9, choices=TYPE_CALL_CHOICES)
    interval = models.CharField(max_length=16)
