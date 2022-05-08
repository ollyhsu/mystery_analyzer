import json
import time

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from mystery.utils.report.json_report import get_slither_report, get_mythril_report
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


@login_required
def get_report(request):
    rid = request.GET.get('rid')
    if rid:
        uid = request.user.id
        obj = SolAddList.objects.get(id=rid)
        if obj.uid:
            if uid == obj.uid:
                # json处理result
                result = obj.result
                # print(result)
                data_result = get_report_json(result)
                report_data = {
                    'id': obj.id,
                    'fname': obj.fname,
                    'fpath': obj.fpath,
                    'add': obj.add,
                    'scantype': obj.scantype,
                    'result': data_result,
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


# 处理slither报告
def get_slither_report_s(dict_data):
    slither_data = dict_data['Slither']

    # 判断slither_data的success属性是否为True
    if slither_data['success'] and slither_data['error'] is None:
        # print('Slither success')
        # print(slither_data['results']['detectors'])
        # 循环遍历slither_data['results']['detectors']
        data = ''
        for detector in slither_data['results']['detectors']:
            # "SWC ID:" + '\n' + \
            sldata = detector['check'] + '\n' + \
                     detector['impact'] + '\n' + \
                     detector['first_markdown_element'] + '\n' + \
                     detector['description'] + '\n'
                     # "Suggestion: " + 'suggestion' + '\n\n'
            data += sldata
        return data

        # print("SWC ID:")
        # print(detector['check'])
        # print(detector['impact'])  # 漏洞等级
        # # print(detector['confidence'])  # 可信度
        # print(detector['first_markdown_element'])
        # print(detector['description'])
        # print("Suggestion: " + 'suggestion')
    else:
        print('Slither Result Error.')


# 处理mythril报告
def get_mythril_report_s(dict_data):
    myth_data = dict_data['Mythril']
    # print(json.dumps(myth_data))
    # 判断myth_data的success属性是否为True
    if myth_data['success'] and myth_data['error'] is None:
        # print('Myth success')
        # 循环遍历myth_data['issues']
        data = ''
        for issue in myth_data['issues']:
            mydata = issue['title'] + '\n' + \
                     issue['swc-id'] + '\n' + \
                     "Name:" + '\n' + \
                     issue['severity'] + '\n' + \
                     issue['function'] + '\n' + \
                     issue['description'] + '\n' + \
                     str(issue['filename']).split('/')[-1] + "#" + str(issue['lineno']) + '\n' + \
                     "Suggestion: " + 'suggestion' + '\n\n'
            data += mydata
        return data
    else:
        print('Myth Result Error.')


def json_to_dict(my_json: str) -> dict:
    return json.loads(my_json)


def get_report_json(data):
    # 转成json格式
    json_data = json.dumps(data)
    # 转成字典格式
    dict_datas = eval(json_to_dict(json_data))
    # 获取slither数据
    s_data = get_slither_report_s(dict_datas)
    # m_data = get_mythril_report_s(dict_datas)
    return s_data
    # if s_data is not None or m_data is not None:
    #     rdata = s_data + m_data
    #     return rdata
    # else:
    #     rdata = "No Vulnerable Code"
    #     return rdata
