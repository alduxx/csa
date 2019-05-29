import hashlib

from datetime import datetime

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.hashers import make_password

from financeiro.models import Registro


IGNORAR_STATUS = ['Anotacao De Credito']


def processa_linha(cnt, linha):
    """
    extrai os dados do extrato da linha passada
    """
    possui_data_e_num_doc = False

    ano=mes=dia=num_doc=historico=origem=_txt=saldo_no_dia = None

    retorno = ""

    try:
        ano, mes, dia = int(linha[6:10]), int(linha[3:5]), int(linha[0:2])
        data = datetime(ano, mes, dia).strftime('%Y-%m-%d')
        num_doc = int(linha[60:71].replace('.', ''))
        possui_data_e_num_doc = True
    except ValueError:
        pass

    if(possui_data_e_num_doc):
        historico = linha[20:48].strip()
        if(historico not in IGNORAR_STATUS):
            origem = linha[50:56].strip()
            num_doc = int(linha[60:71].replace('.', ''))
            valor = float(linha[73:87].replace(',', '#').replace('.', '') \
                                      .replace('#', '.'))
            saldo_no_dia = float(linha[89:].replace(',', '#').replace('.', '') \
                                           .replace('#', '.'))
            _txt = data+historico+origem+str(num_doc)+str(valor)+str(saldo_no_dia)
            # retorno = f"data: {data} | hist: {historico} | orig: {origem} | num: {num_doc} | vlr: {valor} | sld: {saldo_no_dia}"
            retorno = f"{dia}.{mes}.{ano}   {historico:28} {origem: >6} {num_doc: >11}  {valor: >14}"

            m = Registro()
            m.posicao=data
            m.historico=historico
            m.origem=origem
            m.numero_documento=num_doc
            m.valor=valor
            m.saldo_no_dia=saldo_no_dia
            m.hash = hashlib.md5(_txt.encode()).hexdigest()

            if(Registro.objects.filter(hash=m.hash)):
                retorno = '[  ] ' + retorno
            else:
                retorno = '[ok] ' + retorno
                m.save()

        return retorno

def upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        results = []
        with open(fs.path(filename)) as arq:
            for cnt, line in enumerate(arq):
                r = processa_linha(cnt, line)
                if r != None:
                    results.append(r)

        return render(request, 'financeiro/upload_receipts.html', {
            'uploaded_file_url': uploaded_file_url,
            'results': results
        })
    return render(request, 'financeiro/upload_receipts.html')
