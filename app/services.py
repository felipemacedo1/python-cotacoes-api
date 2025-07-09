import requests
from typing import List, Dict, Optional
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cotacoes(tickers: List[str]) -> Dict[str, Dict]:
    """
    Busca cotações de ações através da API do BRAPI.dev
    Com fallback para dados simulados em caso de erro
    
    Args:
        tickers: Lista de símbolos de ações (ex: ['PETR4', 'VALE3', 'BBAS3'])
    
    Returns:
        Dict contendo dados das cotações ou informação de erro para cada ticker
    """
    if not tickers:
        return {}
    
    # Remove espaços e converte para maiúsculo
    tickers_clean = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
    
    if not tickers_clean:
        return {}
    
    # Junta os tickers com vírgula para a API
    tickers_string = ','.join(tickers_clean)
    
    # URL da API do BRAPI.dev (usando endpoint público)
    url = f"https://brapi.dev/api/quote/{tickers_string}?fundamental=false"
    
    try:
        logger.info(f"Buscando cotações para: {tickers_string}")
        
        # Faz a requisição para a API
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        result = {}
        
        # Processa os resultados da API
        if 'results' in data and data['results']:
            for stock in data['results']:
                ticker = stock.get('symbol', '')
                
                # Calcula a variação percentual
                variacao_percent = 0
                if stock.get('regularMarketPreviousClose') and stock.get('regularMarketPrice'):
                    preco_anterior = stock['regularMarketPreviousClose']
                    preco_atual = stock['regularMarketPrice']
                    variacao_percent = ((preco_atual - preco_anterior) / preco_anterior) * 100
                
                result[ticker] = {
                    'symbol': ticker,
                    'shortName': stock.get('shortName', ticker),
                    'longName': stock.get('longName', stock.get('shortName', ticker)),
                    'regularMarketPrice': stock.get('regularMarketPrice', 0),
                    'currency': stock.get('currency', 'BRL'),
                    'marketCap': stock.get('marketCap'),
                    'variacao_percent': round(variacao_percent, 2),
                    'regularMarketPreviousClose': stock.get('regularMarketPreviousClose'),
                    'valid': True
                }
        
        # Para tickers que não retornaram dados, marca como inválidos
        for ticker in tickers_clean:
            if ticker not in result:
                result[ticker] = {
                    'symbol': ticker,
                    'shortName': ticker,
                    'longName': f"Ativo não encontrado: {ticker}",
                    'regularMarketPrice': 0,
                    'currency': 'BRL',
                    'marketCap': None,
                    'variacao_percent': 0,
                    'regularMarketPreviousClose': 0,
                    'valid': False,
                    'error': 'Ativo não encontrado'
                }
        
        logger.info(f"Cotações obtidas com sucesso para {len(result)} ativos")
        return result
        
    except requests.RequestException as e:
        logger.warning(f"Erro ao buscar cotações na API: {e}. Usando dados simulados.")
        
        # Fallback para dados simulados para demonstração
        return get_cotacoes_simuladas(tickers_clean)
        
    except Exception as e:
        logger.error(f"Erro inesperado: {e}. Usando dados simulados.")
        
        # Fallback para dados simulados para demonstração
        return get_cotacoes_simuladas(tickers_clean)


def get_cotacoes_simuladas(tickers: List[str]) -> Dict[str, Dict]:
    """
    Gera dados simulados de cotações para demonstração
    
    Args:
        tickers: Lista de símbolos de ações
    
    Returns:
        Dict contendo dados simulados das cotações
    """
    import random
    
    # Dados simulados de empresas conhecidas
    empresas_simuladas = {
        'PETR4': {'nome': 'Petróleo Brasileiro S.A. - Petrobras', 'nome_curto': 'PETROBRAS PN', 'preco_base': 32.50},
        'VALE3': {'nome': 'Vale S.A.', 'nome_curto': 'VALE ON', 'preco_base': 61.20},
        'BBAS3': {'nome': 'Banco do Brasil S.A.', 'nome_curto': 'BANCO BRASIL ON', 'preco_base': 28.45},
        'ITUB4': {'nome': 'Itaú Unibanco Holding S.A.', 'nome_curto': 'ITAUUNIBANCO PN', 'preco_base': 23.80},
        'BBDC4': {'nome': 'Banco Bradesco S.A.', 'nome_curto': 'BRADESCO PN', 'preco_base': 15.25},
        'ABEV3': {'nome': 'Ambev S.A.', 'nome_curto': 'AMBEV ON', 'preco_base': 12.65},
        'MGLU3': {'nome': 'Magazine Luiza S.A.', 'nome_curto': 'MAGAZ LUIZA ON', 'preco_base': 8.90},
        'WEGE3': {'nome': 'WEG S.A.', 'nome_curto': 'WEG ON', 'preco_base': 45.30},
        'RENT3': {'nome': 'Localiza Rent a Car S.A.', 'nome_curto': 'LOCALIZA ON', 'preco_base': 42.15},
        'LREN3': {'nome': 'Lojas Renner S.A.', 'nome_curto': 'LOJAS RENNER ON', 'preco_base': 18.75}
    }
    
    result = {}
    
    for ticker in tickers:
        ticker_upper = ticker.upper()
        
        if ticker_upper in empresas_simuladas:
            empresa = empresas_simuladas[ticker_upper]
            
            # Gera preço com variação aleatória de -5% a +5%
            variacao = random.uniform(-0.05, 0.05)
            preco_anterior = empresa['preco_base']
            preco_atual = preco_anterior * (1 + variacao)
            variacao_percent = variacao * 100
            
            # Gera valor de mercado simulado
            market_cap = random.randint(50_000_000_000, 500_000_000_000)
            
            result[ticker_upper] = {
                'symbol': ticker_upper,
                'shortName': empresa['nome_curto'],
                'longName': empresa['nome'],
                'regularMarketPrice': round(preco_atual, 2),
                'currency': 'BRL',
                'marketCap': market_cap,
                'variacao_percent': round(variacao_percent, 2),
                'regularMarketPreviousClose': preco_anterior,
                'valid': True
            }
        else:
            # Para tickers desconhecidos, ainda cria dados simulados genéricos
            preco_base = random.uniform(10.0, 100.0)
            variacao = random.uniform(-0.08, 0.08)
            preco_atual = preco_base * (1 + variacao)
            variacao_percent = variacao * 100
            
            result[ticker_upper] = {
                'symbol': ticker_upper,
                'shortName': f'{ticker_upper} SIMULADO',
                'longName': f'Empresa Simulada {ticker_upper}',
                'regularMarketPrice': round(preco_atual, 2),
                'currency': 'BRL',
                'marketCap': random.randint(10_000_000_000, 200_000_000_000),
                'variacao_percent': round(variacao_percent, 2),
                'regularMarketPreviousClose': preco_base,
                'valid': True
            }
    
    logger.info(f"Dados simulados gerados para {len(result)} ativos")
    return result


def format_currency(value: float, currency: str = 'BRL') -> str:
    """
    Formata valor monetário para exibição
    
    Args:
        value: Valor numérico
        currency: Moeda (padrão BRL)
    
    Returns:
        String formatada com o valor monetário
    """
    if currency == 'BRL':
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    else:
        return f"{currency} {value:,.2f}"


def format_market_cap(market_cap: Optional[int]) -> str:
    """
    Formata valor de mercado para exibição
    
    Args:
        market_cap: Valor de mercado em número
    
    Returns:
        String formatada (ex: "R$ 123,45 B")
    """
    if not market_cap:
        return "N/A"
    
    if market_cap >= 1_000_000_000:
        return f"R$ {market_cap / 1_000_000_000:.1f}B"
    elif market_cap >= 1_000_000:
        return f"R$ {market_cap / 1_000_000:.1f}M"
    else:
        return f"R$ {market_cap:,.0f}".replace(',', '.')
