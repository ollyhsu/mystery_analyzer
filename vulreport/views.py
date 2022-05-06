from django.shortcuts import render

# Create your views here.
def vulreport(request):
    return render(request, "vulreport.html")
