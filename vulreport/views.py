import json
import os
import time

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
# Create your views here.
from pyevmasm import disassemble_hex

from mystery_analyzer import settings
from vulreport.models import VulDeatilList
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
            'status': replistware.status,
        }
        r_list.append(report_data)
        rcount += 1
    data = r_list
    return render(request, "vulreport.html", {"data": data, })


@login_required
def get_report(request):
    global opcodes
    rid_get = request.GET.get('rid')
    uid = request.user.id
    try:
        dcount = 0
        d_list = []
        obj = SolAddList.objects.get(id=rid_get)
        # 若runtime
        if obj.runtime:
            bincode = obj.runtime
            if bincode[:10] == '0x60806040' or bincode[:8] == '60806040':
                opcodes = disassemble_hex(bincode)
        else:
            opcodes = ''
        sol_code = get_sol_code_file(obj.fpath)
        try:
            if obj.cfg:
                cfg_path = json.loads(obj.cfg)
            else:
                cfg_path = ''
        except Exception as e:
            print(e)
            cfg_path = ''

        if obj.uid == uid:
            report_data = {
                'id': obj.id,
                'fname': obj.fname,
                'fpath': obj.fpath,
                'add': obj.add,
                'scantype': obj.scantype,
                'result': obj.result,
                'time': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(float(obj.time))),
                'uid': obj.uid,
                'status': obj.status,
                'check_time': obj.check_time,
                'runtime': obj.runtime,
                'opcodes': opcodes,
                'sol_code': sol_code,
                'cfg': cfg_path,
            }
            dreport_datas = VulDeatilList.objects.filter(rid=rid_get)
            for deatillistware in dreport_datas:
                detail_data = {
                    'swcid': deatillistware.swcid,
                    'title': deatillistware.title,
                    'impact': deatillistware.impact,
                    'lines': deatillistware.lines,
                    'description': deatillistware.description,
                }
                d_list.append(detail_data)
                dcount += 1
            detail = d_list
            return render(request, "get_report.html", {"data": report_data, "detail": detail})
        else:
            return HttpResponse("没有权限查看该报告")
    except SolAddList.DoesNotExist:
        return HttpResponse('当前报告不存在')


@login_required
def del_report(request):
    rid_get = request.POST.get('rid')
    uid = request.user.id
    try:
        dreport_datas = VulDeatilList.objects.filter(rid=rid_get)
        for deatillistware in dreport_datas:
            deatillistware.delete()
        obj = SolAddList.objects.get(id=rid_get)
        # 循环获取obj.cfg文件路径
        cfg_path = obj.cfg
        for i in json.loads(obj.cfg):
            cfg_path = os.path.join(settings.MEDIA_ROOT, i)
            # delete file
            if os.path.exists(cfg_path):
                os.remove(cfg_path)
        file_path = os.path.join(settings.MEDIA_ROOT, obj.fpath)
        # print(file_path)
        if os.path.exists(file_path):
            os.remove(file_path)
        obj.delete()
        return JsonResponse({"res": 1})
    except Exception as e:
        print(e)
        return JsonResponse({"res": 0})


def get_report_json(data, rid):
    try:
        # # 转成字典格式
        dict_datas = json.loads(data)
        myth_data = dict_datas[0].get('Mythril')
        sli_data = dict_datas[1].get('Slither')

        if myth_data is not None:
            if myth_data['success'] and myth_data['error'] is None:
                # myth_info = "Mythril has detected the vulnerability.\n"
                for issue in myth_data['issues']:
                    try:
                        VulDeatilList.objects.create(rid=rid, swcid=issue['swc-id'], title=issue['title'],
                                                     impact=issue['severity'], lines=issue['lineno'],
                                                     description=issue['description'])
                    except Exception as e:
                        print(e)
            elif myth_data['success'] is False:
                # myth_status = "failed"
                print(myth_data['error'])
            else:
                myth_info = "Mythril has detected the vulnerability.\n"
        else:
            myth_info = "Mythril does not detect vulnerabilities.\n"

        if sli_data is not None:
            if sli_data['success'] and sli_data['error'] is None:
                # sli_info = "Slither has detected the vulnerability.\n"
                for detector in sli_data['results']['detectors']:
                    if detector['impact'] not in ['Informational', 'Optimization']:
                        try:
                            VulDeatilList.objects.create(rid=rid, title=detector['check'],
                                                         impact=detector['impact'],
                                                         lines=detector['first_markdown_element'].split("#")[1],
                                                         description=detector['description'])
                        except Exception as e:
                            print(e)
            elif sli_data['success'] is False:
                # sli_status = "failed"
                print(sli_data['error'])
            else:
                sli_info = "Slither has detected the vulnerability.\n"
        else:
            sli_info = "Slither does not detect vulnerabilities.\n"

        # if myth_status == "failed" and sli_status == "failed":
        #     obj = SolAddList.objects.get(id=rid)
        #     obj.status = "failed"
        #     obj.save()
        # result_info = myth_info + "\n" + sli_info
        # return True
    except Exception as e:
        print(e)


def get_sol_code_file(fpath):
    abs_path = "%s/%s" % (settings.MEDIA_ROOT, fpath)
    # Read File Content from abs_path
    with open(abs_path, 'r') as f:
        content = f.read()
    return content
