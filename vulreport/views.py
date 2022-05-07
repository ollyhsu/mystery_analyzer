import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from vulscan.models import SolAddList


@login_required
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
            'uid': replistware.uid,
        }
        r_list.append(report_data)
        rcount += 1
    data = r_list
    return render(request, "vulreport.html", {"data": data})


# @login_required
# def vuldetail(request):
#     rid = request.POST.get('report_id')
#     return render(request, "vulreport.html", {"rid": rid})

@login_required
def get_report(request):
    rid = request.GET.get('rid')
    if rid:
        uid = request.user.id
        obj = SolAddList.objects.get(id=rid)
        if obj.uid:
            if uid == obj.uid:
                report_data = {
                    'id': obj.id,
                    'fname': obj.fname,
                    'fpath': obj.fpath,
                    'add': obj.add,
                    'scantype': obj.scantype,
                    'result': obj.result,
                    'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(obj.time))),
                    'uid': obj.uid,
                }
                return render(request, "get_report.html", {"data": report_data})
            else:
                # print("无权限")
                return render(request, "errors/page_403.html")
        else:
            return render(request, "errors/page_403.html")
    else:
        return render(request, "errors/page_403.html")

    # obj.fpath = 'etherscan/%s' % filename
    # obj.save()

    # if bincode[:10] == '0x60806040' or bincode[:8] == '60806040':
    #     opcode_from_bytecode = disassemble_hex(bincode)
    #     return JsonResponse({"res": 1, "opcode": opcode_from_bytecode})
    # elif bincode[:4] == 'PUSH':
    #     opcode_inline = "\n".join(bincode.splitlines())
    #     bytecode_from_opcode = assemble_hex(opcode_inline)
    #     return JsonResponse({"res": 2, "runtime": bytecode_from_opcode})
    # else:
    #     # 用户名和密码错误
    #     return JsonResponse({"res": 0})
