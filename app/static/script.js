// JavaScript personalizado para Cotações API

document.addEventListener('DOMContentLoaded', function() {
    console.log('Cotações API carregado com sucesso!');
    
    // Inicializar tooltips do Bootstrap
    initializeTooltips();
    
    // Configurar auto-refresh (opcional)
    setupAutoRefresh();
    
    // Configurar busca em tempo real
    setupLiveSearch();
    
    // Configurar animações
    setupAnimations();
});

/**
 * Inicializa todos os tooltips do Bootstrap na página
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Configura atualização automática das cotações
 */
function setupAutoRefresh() {
    const refreshInterval = 300000; // 5 minutos em millisegundos
    
    // Só ativar auto-refresh se houver cotações na página
    const cotacoesContainer = document.getElementById('cotacoes-container');
    if (!cotacoesContainer || cotacoesContainer.children.length === 0) {
        return;
    }
    
    let autoRefreshEnabled = false;
    
    // Criar botão de toggle para auto-refresh
    const toggleButton = createAutoRefreshToggle();
    
    // Função para atualizar automaticamente
    function autoRefresh() {
        if (!autoRefreshEnabled) return;
        
        console.log('Auto-refresh executado');
        updateTimestamp();
        
        // Recarregar a página mantendo os parâmetros atuais
        window.location.reload();
    }
    
    // Configurar intervalo
    let refreshTimer;
    
    function startAutoRefresh() {
        autoRefreshEnabled = true;
        refreshTimer = setInterval(autoRefresh, refreshInterval);
        toggleButton.classList.replace('btn-outline-secondary', 'btn-success');
        toggleButton.innerHTML = '<i class="bi bi-pause me-1"></i>Auto-refresh ON';
        showNotification('Auto-refresh ativado (5 min)', 'success');
    }
    
    function stopAutoRefresh() {
        autoRefreshEnabled = false;
        if (refreshTimer) {
            clearInterval(refreshTimer);
        }
        toggleButton.classList.replace('btn-success', 'btn-outline-secondary');
        toggleButton.innerHTML = '<i class="bi bi-play me-1"></i>Auto-refresh OFF';
        showNotification('Auto-refresh desativado', 'info');
    }
    
    // Event listener para o botão
    toggleButton.addEventListener('click', function() {
        if (autoRefreshEnabled) {
            stopAutoRefresh();
        } else {
            startAutoRefresh();
        }
    });
}

/**
 * Cria botão de toggle para auto-refresh
 */
function createAutoRefreshToggle() {
    const button = document.createElement('button');
    button.className = 'btn btn-outline-secondary btn-sm ms-2';
    button.innerHTML = '<i class="bi bi-play me-1"></i>Auto-refresh OFF';
    button.title = 'Ativar/desativar atualização automática';
    
    // Adicionar ao container de badges no topo
    const badgeContainer = document.querySelector('.badge.bg-info').parentElement;
    if (badgeContainer) {
        badgeContainer.appendChild(button);
    }
    
    return button;
}

/**
 * Configura busca em tempo real no campo de ativos
 */
function setupLiveSearch() {
    const ativosInput = document.getElementById('ativos-input');
    if (!ativosInput) return;
    
    let searchTimeout;
    
    // Adicionar sugestões de ativos populares
    const suggestions = [
        'PETR4', 'VALE3', 'ITUB4', 'BBDC4', 'BBAS3', 'ABEV3',
        'MGLU3', 'WEGE3', 'RENT3', 'LREN3', 'JBSS3', 'BEEF3',
        'HAPV3', 'RADL3', 'SUZB3', 'TOTS3', 'VIVT3', 'TIMS3'
    ];
    
    // Criar datalist para autocomplete
    const datalist = document.createElement('datalist');
    datalist.id = 'ativos-suggestions';
    
    suggestions.forEach(ticker => {
        const option = document.createElement('option');
        option.value = ticker;
        datalist.appendChild(option);
    });
    
    ativosInput.setAttribute('list', 'ativos-suggestions');
    ativosInput.parentElement.appendChild(datalist);
    
    // Validação em tempo real
    ativosInput.addEventListener('input', function(e) {
        clearTimeout(searchTimeout);
        
        const value = e.target.value;
        const isValid = validateTickerInput(value);
        
        // Feedback visual
        if (value && !isValid) {
            ativosInput.classList.add('is-invalid');
            ativosInput.classList.remove('is-valid');
        } else if (value && isValid) {
            ativosInput.classList.add('is-valid');
            ativosInput.classList.remove('is-invalid');
        } else {
            ativosInput.classList.remove('is-valid', 'is-invalid');
        }
        
        // Busca automática após 2 segundos de inatividade (opcional)
        searchTimeout = setTimeout(() => {
            if (value && isValid && value.length > 3) {
                console.log('Busca automática seria executada para:', value);
                // Implementar busca automática se necessário
            }
        }, 2000);
    });
}

/**
 * Valida entrada de tickers
 */
function validateTickerInput(input) {
    if (!input) return true;
    
    // Remove espaços e divide por vírgula
    const tickers = input.split(',').map(t => t.trim().toUpperCase());
    
    // Verifica se todos os tickers são válidos (3-6 caracteres alfanuméricos)
    return tickers.every(ticker => /^[A-Z0-9]{3,6}$/.test(ticker));
}

/**
 * Configura animações da página
 */
function setupAnimations() {
    // Animação de entrada para cards
    const cards = document.querySelectorAll('.cotacao-card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Animação de hover para badges de variação
    const badges = document.querySelectorAll('.badge');
    badges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        
        badge.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

/**
 * Atualiza o timestamp de última atualização
 */
function updateTimestamp() {
    const element = document.getElementById('last-update');
    if (element) {
        const now = new Date();
        element.innerHTML = `<i class="bi bi-clock me-1"></i>Atualizado às ${now.toLocaleTimeString('pt-BR')}`;
    }
}

/**
 * Atualiza uma ação específica via AJAX
 */
function refreshStock(ticker) {
    const card = document.querySelector(`[data-ticker="${ticker}"]`);
    if (!card) return;
    
    // Adicionar estado de loading
    card.classList.add('loading');
    
    // Fazer requisição para a API
    fetch(`/api/cotacoes?tickers=${ticker}`)
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data[ticker]) {
                updateStockCard(ticker, data.data[ticker]);
                showNotification(`${ticker} atualizado com sucesso`, 'success');
            } else {
                showNotification(`Erro ao atualizar ${ticker}`, 'danger');
            }
        })
        .catch(error => {
            console.error('Erro ao atualizar ação:', error);
            showNotification(`Erro ao atualizar ${ticker}`, 'danger');
        })
        .finally(() => {
            card.classList.remove('loading');
        });
}

/**
 * Atualiza um card de ação com novos dados
 */
function updateStockCard(ticker, data) {
    const card = document.querySelector(`[data-ticker="${ticker}"]`);
    if (!card) return;
    
    // Atualizar preço
    const priceElement = card.querySelector('.display-6');
    if (priceElement) {
        priceElement.textContent = formatCurrency(data.regularMarketPrice, data.currency);
        
        // Atualizar cor baseada na variação
        priceElement.className = `display-6 fw-bold ${data.variacao_percent >= 0 ? 'text-success' : 'text-danger'}`;
    }
    
    // Atualizar badge de variação
    const badge = card.querySelector('.badge');
    if (badge) {
        const icon = data.variacao_percent >= 0 ? 'bi-arrow-up' : 'bi-arrow-down';
        const colorClass = data.variacao_percent >= 0 ? 'bg-success' : 'bg-danger';
        
        badge.className = `badge ${colorClass} fs-6`;
        badge.innerHTML = `<i class="bi ${icon}"></i> ${formatPercentage(data.variacao_percent)}`;
    }
    
    // Atualizar fechamento anterior
    const prevCloseElement = card.querySelector('.row .col-6:first-child .fw-semibold');
    if (prevCloseElement) {
        prevCloseElement.textContent = formatCurrency(data.regularMarketPreviousClose, data.currency);
    }
    
    // Adicionar efeito visual de atualização
    card.style.background = '#e8f5e8';
    setTimeout(() => {
        card.style.background = '';
    }, 1000);
}

/**
 * Formata valor monetário
 */
function formatCurrency(value, currency = 'BRL') {
    if (currency === 'BRL') {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    }
    return `${currency} ${value.toFixed(2)}`;
}

/**
 * Formata porcentagem
 */
function formatPercentage(value) {
    const sign = value >= 0 ? '+' : '';
    return `${sign}${value.toFixed(2)}%`;
}

/**
 * Mostra notificação toast
 */
function showNotification(message, type = 'info') {
    // Criar elemento de toast se não existir
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Criar toast
    const toastId = `toast-${Date.now()}`;
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="bi bi-info-circle text-${type} me-2"></i>
                <strong class="me-auto">Cotações API</strong>
                <small>${new Date().toLocaleTimeString('pt-BR')}</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    // Inicializar e mostrar toast
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, {
        autohide: true,
        delay: 3000
    });
    
    toast.show();
    
    // Remover element após esconder
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

/**
 * Copia texto para área de transferência
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copiado para área de transferência!', 'success');
    }).catch(() => {
        showNotification('Erro ao copiar', 'danger');
    });
}

/**
 * Compartilha URL atual
 */
function shareCurrentPage() {
    if (navigator.share) {
        navigator.share({
            title: 'Cotações API',
            text: 'Confira as cotações das ações em tempo real',
            url: window.location.href
        });
    } else {
        copyToClipboard(window.location.href);
        showNotification('Link copiado para compartilhamento!', 'info');
    }
}

// Exportar funções para uso global
window.refreshStock = refreshStock;
window.updateTimestamp = updateTimestamp;
window.showNotification = showNotification;
window.copyToClipboard = copyToClipboard;
window.shareCurrentPage = shareCurrentPage;
