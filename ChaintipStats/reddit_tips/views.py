from django.http.response import HttpResponse
from django.shortcuts import render

def main(request):
    return HttpResponse('Testing!')
