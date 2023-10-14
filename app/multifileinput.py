from django import forms
from django.forms.widgets import ClearableFileInput
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class MultiFileInput(ClearableFileInput):
    template_name = 'index.html'  # カスタムテンプレートを指定

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['value'] = value
        return context
