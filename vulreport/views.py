import time

from django.shortcuts import render

# Create your views here.
from vulscan.models import SolAddList


def vulreport(request):
    rcount = 0
    r_list = []
    report_datas = SolAddList.objects.all()[::-1]
    for replistware in report_datas:
        report_data = {
            'id': replistware.id,
            'fname': replistware.fname,
            'fpath': replistware.fpath,
            'add': replistware.add,
            'scantype': replistware.scantype,
            'result': replistware.result,
            'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(replistware.time))),
        }
        r_list.append(report_data)
        rcount += 1
    data = r_list
    return render(request, "vulreport.html", {"data": data})
