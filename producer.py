from kafka import KafkaProducer
from kafka.errors import KafkaError
from flask import make_response, abort
from datetime import datetime
import requests
import json, os

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

def create_msg(msg):
    try:
        texto = msg.get("texto", None)
        #topico = os.environ('meu-topico') #recebe do Dockerfile ENV TOPICO=meu-topico
        #broker = os.environ('0.0.0.0') + ":" + os.environ('9092') #"192.168.10.133:9092" recebe do Dockerfile ENV HOST=0.0.0.0 e ENV PORTA=9092
        #print(broker)

        # --------
        # USAGE: https://kafka-python.readthedocs.io/en/master/usage.html
        producer = KafkaProducer(bootstrap_servers='0.0.0.0:9092')

        # Asynchronous by default
        future = producer.send('meu-topico', texto.encode('utf-8'))
        # Block for 'synchronous' sends
        record_metadata = future.get(timeout=10)
        
    except Exception as e:
        # Decide what to do if produce request failed...
        print(repr(e))
        abort(
            406,
            "Erro ao enviara msg pro Kafka: "+repr(e),
        )

    # Successful result returns assigned partition and offset
    print ('Sucesso no envio. Topico: '+str(record_metadata.topic)+' Particao :' + str(record_metadata.partition) + ' Offset: ' + str(record_metadata.offset))
    postMSG_criada_para_o_slack(texto)
    return make_response(
        "Mensagem criada: "+str(texto), 201
    )
    
def postMSG_criada_para_o_slack(msg):
    # format payload for slack
    sdata = formatForSlack(msg)
    #url = os.environ('https://hooks.slack.com/services/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') #recebe do Dockerfile ENV SLACK=https....
    r = requests.post('https://hooks.slack.com/services/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', sdata, headers={'Content-Type': 'application/json'})
    if r.status_code == 200:
      print('SUCCEDED: Sent slack webhook')
    else:
      print('FAILED: Send slack webhook')

def formatForSlack(msg):
  #canal = os.environ('lab-produtor') #recebe do Dockerfile ENV CANAL=lab-produtor
  payload = {
    "channel":'lab-produtor',
    "username":'app_kafka_producer',
    "text": msg,
    "icon_emoji":':mailbox_with_mail:'
  }
  return json.dumps(payload)