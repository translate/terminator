# -*- coding: UTF-8 -*-
from django import forms


class SearchForm(forms.Form):
    search_string = forms.CharField(max_length=100, min_length=2, required=False)


