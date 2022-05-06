from django.shortcuts import render

# Create your views here.
def disassembler(request):
    return render(request, "disassembler.html")

def etherscansync(request):
    return render(request, "etherscan.html")