import json
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from pyevmasm import disassemble_hex, assemble_hex


# Create your views here.
def disassembler(request):
    return render(request, "disassembler.html")


def etherscansync(request):
    return render(request, "etherscan.html")


def disassembler_ajax_handle(request):
    # ajax 汇编处理
    bincode = request.POST.get("bincode")
    if bincode[:10] == '0x60806040' or bincode[:8] == '60806040':
        opcode_from_bytecode = disassemble_hex(bincode)
        return JsonResponse({"res": 1, "opcode": opcode_from_bytecode})
    elif bincode[:4] == 'PUSH':
        opcode_inline = "\n".join(bincode.splitlines())
        bytecode_from_opcode = assemble_hex(opcode_inline)
        return JsonResponse({"res": 2, "runtime": bytecode_from_opcode})
    else:
        # 用户名和密码错误
        return JsonResponse({"res": 0})
