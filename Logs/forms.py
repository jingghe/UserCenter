#-*- coding: utf-8 -*-

from Logs.models import HandlesLog
from django import forms


class LogsAddForm(forms.ModelForm):
    class Meta:
        model = HandlesLog
        fields = ('username', 'log_type', 'source', 'detail', 'component',)

    def __init__(self, *args, **kwargs):
        super(LogsAddForm, self).__init__(*args, **kwargs)
