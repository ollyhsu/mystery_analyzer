# 处理Mythril和Slither json漏洞报告
import json

from .gen_report import gen_report_file


def get_json_data(fname):
    with open(fname) as f:
        data = json.load(f)
    return data


def get_json_data_from_string(data):
    return json.loads(data)


# 处理slither报告
def _get_slither_report(dict_data):
    slither_data = dict_data['Slither']

    # 判断slither_data的success属性是否为True
    if slither_data['success'] and slither_data['error'] is None:
        # print('Slither success')
        # print(slither_data['results']['detectors'])
        # 循环遍历slither_data['results']['detectors']
        data = ''
        for detector in slither_data['results']['detectors']:
            sldata = "SWC ID:" + '\n' + \
                     detector['check'] + '\n' + \
                     detector['impact'] + '\n' + \
                     detector['first_markdown_element'] + '\n' + \
                     detector['description'] + '\n' + \
                     "Suggestion: " + 'suggestion' + '\n\n'
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
def _get_mythril_report(dict_data):
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


# 保存报告至本地
def save_report_txt(sol_path, json_file):
    try:
        dict_datas = get_json_data(json_file)
        s_data = _get_slither_report(dict_datas)
        m_data = _get_mythril_report(dict_datas)
        txt_data = s_data + m_data
        # print(txt_data)
        gen_report_file(sol_path, txt_data)
    except TypeError:
        print("Data Type Error.")


# save_report_txt('/home/hohin/mystery/examples/calls_report.json')
