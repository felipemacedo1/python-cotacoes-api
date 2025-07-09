# Configuração para desenvolvimento local
export FLASK_APP=app
export FLASK_ENV=development
export FLASK_DEBUG=1

# Instalar dependências
pip install -r requirements.txt

# Executar aplicação
python -m app
