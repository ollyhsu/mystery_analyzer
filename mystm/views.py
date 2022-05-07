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


def bad_request(request):
    return render(request, 'errors/page_400.html')


def permission_denied(request):
    return render(request, 'errors/page_403.html')


def page_not_found(request):
    return render(request, 'errors/page_404.html')


def server_error(request):
    return render(request, 'errors/page_500.html')
