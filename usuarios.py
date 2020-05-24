from kafka import KafkaProducer
from kafka.errors import KafkaError
from datetime import datetime
from flask import jsonify, make_response, abort
from producer import create_msg
import requests
import connexion

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    
data = get_timestamp()

USUARIOS = {
    "12345678900": {
        "cpf": "12345678900",
        "nome": "Emerson Jones",
		"ddd": "011",
		"tel": "991910001",
		"placa": "DJE1010",
		"tipoVeiculo": "Rodotrem",
		"carroceria": "Sider",
    },
    "99945678900": {
        "cpf": "99945678900",
        "nome": "Jack Sparrow",
		"ddd": "011",
		"tel": "998880801",
		"placa": "COV1A010",
		"tipoVeiculo": "Carreta",
		"carroceria": "Granaleiro",
    },
    "32145678800": {
        "cpf": "32145678800",
        "nome": "Paulo Snow",
		"ddd": "021",
		"tel": "977990801",
		"placa": "AAA1111",
		"tipoVeiculo": "Bitrem",
		"carroceria": "Granaleiro",
    },
}

class Texto:
    def __init__(self, msg, n):
        self.texto = msg
    def get(self, m, n):
        return self.texto
        
def read_all():
    func_usuarios = [USUARIOS[key] for key in sorted(USUARIOS.keys())]
    usuario = jsonify(func_usuarios)
    qtd = len(func_usuarios)
    content_range = "usuario 0-"+str(qtd)+"/"+str(qtd)
    # Configura headers
    usuario.headers['Access-Control-Allow-Origin'] = '*'
    usuario.headers['Access-Control-Expose-Headers'] = 'Content-Range'
    usuario.headers['Content-Range'] = content_range
    return usuario

def read_one(cpf):
    if cpf in USUARIOS:
        user = USUARIOS.get(cpf)
    else:
        abort(
            404, "Usuario com CPF {cpf} nao encontrado".format(cpf=cpf)
        )
    return user



def create(user):
    cpf = user.get("cpf", None)
    nome = user.get("nome", None)
    ddd = user.get("ddd", None)
    tel = user.get("tel", None)
    placa = user.get("placa", None)
    tipoVeiculo = user.get("tipoVeiculo", None)
    carroceria = user.get("carroceria", None)

    if cpf not in USUARIOS and cpf is not None:
        USUARIOS[cpf] = {
            "cpf": cpf,
            "nome": nome,
			"ddd": ddd,
			"tel": tel,
			"placa": placa,
			"tipoVeiculo": tipoVeiculo,
			"carroceria": carroceria,
        }
        print(str(create_msg(Texto("Usuário {cpf} criado com sucesso em {data}".format(cpf=cpf, data=data),""))))
        
        return make_response(
            "Usuário {cpf} criado com sucesso".format(cpf=cpf), 201
        )
    else:
        abort(
            406,
            "Usuário com CPF {cpf} ja existe".format(cpf=cpf),
        )


def update(cpf, user):
    if cpf in USUARIOS:
        USUARIOS[cpf]["nome"] = user.get("nome")
        USUARIOS[cpf]["ddd"] = user.get("ddd")
        USUARIOS[cpf]["tel"] = user.get("tel")
        USUARIOS[cpf]["placa"] = user.get("placa")
        USUARIOS[cpf]["tipoVeiculo"] = user.get("tipoVeiculo")
        USUARIOS[cpf]["carroceria"] = user.get("carroceria")
        
        print(str(create_msg(Texto("Usuário {cpf} alterado com sucesso em {data}".format(cpf=cpf, data=data),""))))

        return USUARIOS[cpf]
    else:
        abort(
            404, "Usuário com CPF {cpf} nao encontrado".format(cpf=cpf)
        )

def delete(cpf):
    if cpf in USUARIOS:
        del USUARIOS[cpf]
        
        print(str(create_msg(Texto("Usuário {cpf} removido com sucesso em {data}".format(cpf=cpf, data=data),""))))
        
        return make_response(
            "Usuário {cpf} deletado com sucesso".format(cpf=cpf), 200
        )
    else:
        abort(
            404, "Usuário com CPF {cpf} nao encontrada".format(cpf=cpf)
        )