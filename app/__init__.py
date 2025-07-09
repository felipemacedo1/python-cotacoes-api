from flask import Flask, render_template, request, jsonify
from app.services import get_cotacoes, format_currency, format_market_cap
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações da aplicação
    app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'
    
    # Filtros Jinja2 personalizados
    @app.template_filter('currency')
    def currency_filter(value, currency='BRL'):
        """Filtro para formatação de moeda"""
        return format_currency(value, currency)
    
    @app.template_filter('market_cap')
    def market_cap_filter(value):
        """Filtro para formatação de valor de mercado"""
        return format_market_cap(value)
    
    @app.template_filter('percentage')
    def percentage_filter(value):
        """Filtro para formatação de porcentagem"""
        if value > 0:
            return f"+{value:.2f}%"
        else:
            return f"{value:.2f}%"
    
    @app.route('/')
    def index():
        """
        Rota principal que exibe as cotações de ações
        Aceita parâmetros:
        - ativos: lista de tickers separados por vírgula (ex: ?ativos=PETR4,VALE3,BBAS3)
        - busca: termo de busca individual (ex: ?busca=PETR4)
        """
        # Obtém os ativos da URL
        ativos_param = request.args.get('ativos', '')
        busca_param = request.args.get('busca', '')
        
        # Lista padrão de ativos para exibir quando não há parâmetros
        ativos_padrao = ['PETR4', 'VALE3', 'BBAS3', 'ITUB4', 'BBDC4', 'ABEV3']
        
        # Determina quais ativos buscar
        if busca_param:
            # Se há busca, adiciona à lista de ativos
            tickers = [busca_param.strip()]
            search_query = busca_param.strip()
        elif ativos_param:
            # Se há ativos específicos na URL
            tickers = [ticker.strip() for ticker in ativos_param.split(',') if ticker.strip()]
            search_query = ''
        else:
            # Usa ativos padrão
            tickers = ativos_padrao
            search_query = ''
        
        # Busca as cotações
        cotacoes = {}
        error_message = ''
        
        if tickers:
            try:
                cotacoes = get_cotacoes(tickers)
                logger.info(f"Buscando cotações para: {', '.join(tickers)}")
            except Exception as e:
                error_message = f"Erro ao buscar cotações: {str(e)}"
                logger.error(error_message)
        
        # Separa ativos válidos e inválidos
        ativos_validos = {k: v for k, v in cotacoes.items() if v.get('valid', False)}
        ativos_invalidos = {k: v for k, v in cotacoes.items() if not v.get('valid', False)}
        
        return render_template(
            'index.html',
            cotacoes=ativos_validos,
            ativos_invalidos=ativos_invalidos,
            search_query=search_query,
            error_message=error_message,
            total_ativos=len(cotacoes)
        )
    
    @app.route('/api/cotacoes')
    def api_cotacoes():
        """
        API endpoint para buscar cotações
        Aceita parâmetro 'tickers' com lista separada por vírgula
        """
        tickers_param = request.args.get('tickers', '')
        
        if not tickers_param:
            return jsonify({
                'error': 'Parâmetro tickers é obrigatório',
                'example': '/api/cotacoes?tickers=PETR4,VALE3,BBAS3'
            }), 400
        
        tickers = [ticker.strip() for ticker in tickers_param.split(',') if ticker.strip()]
        
        try:
            cotacoes = get_cotacoes(tickers)
            return jsonify({
                'success': True,
                'data': cotacoes,
                'total': len(cotacoes)
            })
        except Exception as e:
            logger.error(f"Erro na API: {e}")
            return jsonify({
                'success': False,
                'error': str(e)
            }), 500
    
    @app.route('/health')
    def health():
        """Endpoint para verificação de saúde da aplicação"""
        return jsonify({
            'status': 'healthy',
            'service': 'cotacoes-api'
        })
    
    @app.errorhandler(404)
    def not_found(error):
        """Handler para páginas não encontradas"""
        return render_template('error.html', 
                             error_code=404,
                             error_message="Página não encontrada"), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handler para erros internos do servidor"""
        return render_template('error.html',
                             error_code=500,
                             error_message="Erro interno do servidor"), 500
    
    return app


# Cria a instância da aplicação
app = create_app()

if __name__ == '__main__':
    # Executa em modo de desenvolvimento
    app.run(host='0.0.0.0', port=5000, debug=True)
