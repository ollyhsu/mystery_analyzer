from django.shortcuts import render

# Create your views here.
def welcome(request):
    # 欢迎页
    return render(request, 'home.html')


def index(request):
    # 首页
    return render(request, 'index.html')

def docs(request):
    '''文档'''
    return render(request, 'docs/docs.html')