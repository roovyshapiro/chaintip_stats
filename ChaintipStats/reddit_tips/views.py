from django.http.response import HttpResponse
from django.shortcuts import render

def main(request):
    from .tasks import get_tips
    get_tips()
    return HttpResponse('Testing!')
