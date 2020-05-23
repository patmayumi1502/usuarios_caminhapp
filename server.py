from flask import render_template
import connexion
from flask_cors import CORS
from producer import create_msg
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))
    
data = get_timestamp()

app = connexion.App(__name__, specification_dir='./')

app.add_api('swagger.yml')
CORS(app.app,resources=r'/api/*',methods=['GET', 'POST', 'OPTIONS', 'PUT', 'DELETE'])

@app.route('/')
def home():
    return render_template('usuarios.html')

if __name__ == '__main__':
    with app.app.app_context():
        # Classe definida só para postar uma mensagem inicial, visando criar o tópico
        class Texto:
          def __init__(self, msg, n):
            self.texto = msg
          def get(self, m, n):
            return self.texto
        print(str(create_msg(Texto("Caminhapp ativado em {data}".format(data=data),""))))
        
    app.run(host='0.0.0.0', port=5000, debug=True)