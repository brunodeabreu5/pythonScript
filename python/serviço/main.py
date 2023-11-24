import requests
import time
import json
import logging
from datetime import datetime

 # Defina a URL da API que você deseja chamar

log_format = "%(asctime)s:%(levelname)s:%(message)s"

logging.basicConfig(filename='registroInfo.log',filemode='a',level=logging.INFO,format=log_format)
logging.basicConfig(filename='registroErro.log',filemode='a',level=logging.ERROR,format=log_format)

logger = logging.getLogger('root')

#url = ''
url = 'http://localhost:8080'

urlFila = url+'/verificarFila'
urlLote = url+'/enviaLote_test'
urlVerificarProtocolo = url+'/verificarProtocolo'
urlProtocolo = url+'/verficaLote_test' 

def fazer_verifica_fila():
   
    # Faça a chamada à API usando o método GET, por exemplo
    response = requests.get(urlFila)

    dados = response.json()
    dados_json = json.dumps(dados)
    # Verifique se a resposta da API foi bem-sucedida (código de status 200)
    if response.status_code == 200:
      # Processar os dados da resposta aqui
      envio_lote(dados_json)
      print("Dados da API:", dados)
    elif response.status_code == 201:

        resposta = json.loads(dados_json)
        print(datetime.now(),": ",resposta['resposta'])
        #logger.info(f"{datetime.now()}: {resposta['resposta']}")
        logger.info(f"{resposta['resposta']}")
    else:
        logger.error(datetime.now(),": Erro na chamada à API 1. Código de status:", response.status_code)
        print(datetime.now(),": Erro na chamada à API 1. Código de status:", response.status_code)

def envio_lote(dados_json):
    
    json_analise = json.loads(dados_json)

    for item in json_analise:
        empresa   = item['empresaId']
        razao_social = item['razaoSocial']

        print(datetime.now(),": Formando o envio do Lote =",razao_social)
        logger.info(f'{"Formando o envio do Lote = "+razao_social}')

        json_id = {
		    "id":empresa
        }

        # Converte os dados em formato JSON
        json_data = json.dumps(json_id)

        # Define os cabeçalhos para indicar que você está enviando dados JSON
        headers = {'Content-Type': 'application/json'}

        response = requests.post(urlLote,data=json_data,headers=headers)

        if response.status_code == 200:
            dados = response.json()

            json_data = json.dumps(dados)
            resposta = json.loads(json_data)

            status = resposta['status']
            message = resposta['message']

            mostraResultado = ""

            for x in message:
                mostraResultado += 'Mensagem = '+x['mensagemEnvio']+'\nNota = '+str(x['codigoNota'])+'.'+x['nomeNota']+'\nQuantidade Enviada = '+str(x['quantidade'])+'\n\n'

            logger.info(f'{mostraResultado}')
            print(datetime.now(),": \n",mostraResultado)
        elif response.status_code == 400:
            logger.error(f'{'Xml mal formado. / Webservice da SIFEN esta fora!'}')
            print(datetime.now(),": ",'Xml mal formado. / Webservice da SIFEN esta fora!!!')
        else:
            logger.error(f'{'Erro servidor'}')
            print(datetime.now(),": ",'erro servidor')


def fazer_verificacao_protocolo():
    # Faça a chamada à API usando o método GET
    response = requests.get(urlVerificarProtocolo)

    if response.status_code == 200:
        # Processar os dados da resposta aqui
        dados = response.json()
        dados_json = json.dumps(dados)
        verificar_protocolo(dados_json)
        print("Dados da API:", dados)
    elif response.status_code == 201:

        dados = response.json()
        jsonResposta = json.loads(dados)
        mensagem = jsonResposta['resposta']
        
        logger.info(f'{mensagem}')
        print(datetime.now(),": ",mensagem)

    else:
        logger.error(f'{response.status_code}')
        print(datetime.now(),": Erro na chamada à API 2. Código de status:", response.status_code)

def verificar_protocolo(dados_json):

    json_analise = json.loads(dados_json)
    
    for item in json_analise:
        numero_protocolo = item['numeroProtocolo']
        protocoloId      = item['protocoloId']
        empresaId        = item['empresaProtocolo']

        json_id = {
            "protocoloId":protocoloId,
		    "numeroProtocolo": numero_protocolo,
            "empresaId": empresaId
        }

          # Converte os dados em formato JSON
        json_data = json.dumps(json_id)

        # Define os cabeçalhos para indicar que você está enviando dados JSON
        headers = {'Content-Type': 'application/json'}

        response = requests.post(urlProtocolo,data=json_data,headers=headers)

        if response.status_code == 200:
         
            resposta = response.json()
            respotaString = json.dumps(resposta)
            json_analise = json.loads(respotaString)

            print(datetime.now(),": ",json_analise['message'],'= ',numero_protocolo)

            logger.info(f'{json_analise['message'],"= ",numero_protocolo}')
                
        elif response.status_code == 400:
            logger.error(f'{'Xml mal formado. / Webservice da SIFEN esta fora!!!'}')
            #print(datetime.now(),": ",'Xml mal formado. / Webservice da SIFEN esta fora!!!')
        else:
            logger.error(f'{respotaString}')
            print(datetime.now(),": ",'erro servidor')

   
# Defina o intervalo de tempo em segundos para fazer a requisição (por exemplo, a cada 60 segundos)
intervalo = 20

while True:
    #Função que verifica nota na fila e se tive envia
    #json_id = '[{"empresaId":1,"razaoSocial":"teste"}]'

    fazer_verifica_fila()
    #envio_lote(json_id)
    #Função verifica os protocolo dos lotes se tem na fila
    fazer_verificacao_protocolo()
    # Aguarde o intervalo de tempo antes de fazer a próxima chamada à API
    time.sleep(intervalo)