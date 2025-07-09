# Cotações API

Uma aplicação web completa desenvolvida com Flask e Jinja2 para consultar cotações de ações da B3 em tempo real através da API pública do BRAPI.dev.

## 🚀 Características

- **Interface Responsiva**: Design moderno com Bootstrap 5, adaptado para desktop e mobile
- **API de Cotações**: Integração com BRAPI.dev para dados em tempo real
- **Cards Interativos**: Exibição clara de ticker, nome da empresa, preço atual e variação percentual
- **Busca Flexível**: Consulta múltiplos ativos via URL ou formulário de busca
- **Containerização**: Docker e Docker Compose para fácil deployment
- **Código Comentado**: Estrutura organizada para fácil manutenção e extensão

## 📁 Estrutura do Projeto

```
cotacoes-api/
├── app/
│   ├── __init__.py          # Aplicação Flask principal
│   ├── services.py          # Serviços de integração com API
│   ├── templates/           # Templates Jinja2
│   │   ├── base.html        # Template base
│   │   ├── index.html       # Página principal
│   │   └── error.html       # Página de erro
│   └── static/              # Arquivos estáticos
│       ├── style.css        # CSS personalizado
│       └── script.js        # JavaScript personalizado
├── Dockerfile               # Configuração Docker
├── docker-compose.yml       # Orquestração de containers
├── nginx.conf              # Configuração Nginx (produção)
├── requirements.txt        # Dependências Python
└── README.md              # Este arquivo
```

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11, Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript ES6
- **Framework CSS**: Bootstrap 5.3.0
- **Template Engine**: Jinja2
- **HTTP Client**: Requests
- **Server**: Gunicorn
- **Containerização**: Docker, Docker Compose
- **Proxy**: Nginx (opcional para produção)

## 📋 Pré-requisitos

- Docker e Docker Compose instalados
- Python 3.11+ (para desenvolvimento local)
- Conexão com internet para acessar a API do BRAPI.dev

## 🚀 Como Executar

### Usando Docker (Recomendado)

1. **Clone o repositório:**
   ```bash
   git clone <repository-url>
   cd cotacoes-api
   ```

2. **Execute com Docker Compose:**
   ```bash
   docker-compose up -d
   ```

3. **Acesse a aplicação:**
   - Abra seu navegador em `http://localhost:5000`

### Desenvolvimento Local

1. **Clone o repositório:**
   ```bash
   git clone <repository-url>
   cd cotacoes-api
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # ou
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   python -m app
   ```

5. **Acesse:** `http://localhost:5000`

## 📖 Como Usar

### Interface Web

1. **Acesse a página principal** em `http://localhost:5000`

2. **Consulte ativos específicos** via URL:
   - `/?ativos=PETR4,VALE3,BBAS3` - Múltiplos ativos
   - `/?busca=PETR4` - Busca individual

3. **Use o formulário de busca** na página para consultar ativos

4. **Experimente os links de exemplo** na página inicial

### API Endpoints

- **GET** `/` - Página principal com interface web
- **GET** `/api/cotacoes?tickers=PETR4,VALE3` - API JSON para cotações
- **GET** `/health` - Health check da aplicação

### Exemplos de URLs

```bash
# Ativos do setor de petróleo e mineração
http://localhost:5000/?ativos=PETR4,VALE3,BBAS3

# Principais bancos
http://localhost:5000/?ativos=ITUB4,BBDC4,BBAS3

# Busca individual
http://localhost:5000/?busca=MGLU3

# API JSON
http://localhost:5000/api/cotacoes?tickers=PETR4,VALE3
```

## 🎨 Recursos da Interface

### Cards de Cotações
- **Ticker e Nome**: Código da ação e nome da empresa
- **Preço Atual**: Valor em tempo real com formatação brasileira
- **Variação %**: Indicador colorido (verde/vermelho) com seta
- **Dados Adicionais**: Fechamento anterior e valor de mercado
- **Atualização**: Timestamp da última consulta

### Funcionalidades Extras
- **Busca Avançada**: Formulário com validação em tempo real
- **Links de Exemplo**: Atalhos para setores populares
- **Tratamento de Erros**: Mensagens claras para ativos inválidos
- **Design Responsivo**: Adaptação automática para mobile

## 🔧 Configuração

### Variáveis de Ambiente
```bash
FLASK_ENV=production          # Ambiente de execução
PYTHONUNBUFFERED=1           # Output sem buffer
```

### Customização
- **CSS**: Edite `app/static/style.css` para personalizar o visual
- **JavaScript**: Modifique `app/static/script.js` para novas funcionalidades
- **Templates**: Ajuste os arquivos em `app/templates/` conforme necessário

## 📈 Extensões Futuras

O projeto foi estruturado para fácil extensão:

- **Cache**: Implementar Redis para cache de cotações
- **Banco de Dados**: Adicionar histórico de preços
- **Autenticação**: Sistema de usuários e favoritos
- **WebSocket**: Atualizações em tempo real
- **Gráficos**: Visualizações com Chart.js
- **API Rate Limiting**: Controle de requisições
- **Testes**: Suite de testes automatizados

## 🐳 Docker

### Comandos Úteis

```bash
# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f cotacoes-api

# Parar serviços
docker-compose down

# Rebuild da imagem
docker-compose build --no-cache

# Executar com nginx (produção)
docker-compose --profile production up -d
```

### Produção com Nginx

Para ambiente de produção, use o perfil que inclui Nginx:

```bash
docker-compose --profile production up -d
```

Isso executará:
- Aplicação Flask na porta 5000
- Nginx como proxy reverso na porta 80

## 🔍 Monitoramento

### Health Check
- **Endpoint**: `/health`
- **Docker**: Health check automático configurado
- **Status**: Retorna JSON com status da aplicação

### Logs
```bash
# Logs da aplicação
docker-compose logs cotacoes-api

# Logs do nginx (se usando produção)
docker-compose logs nginx
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- [BRAPI.dev](https://brapi.dev) - API de cotações da B3
- [Bootstrap](https://getbootstrap.com) - Framework CSS
- [Flask](https://flask.palletsprojects.com) - Framework web Python

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs da aplicação
2. Consulte a documentação da API do BRAPI.dev
3. Abra uma issue no repositório

---

Desenvolvido com ❤️ usando Flask e Bootstrap
