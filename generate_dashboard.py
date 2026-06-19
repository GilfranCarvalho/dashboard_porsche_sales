import json
import os

def generate():
    # Load JSON data
    data_path = 'data.json'
    if not os.path.exists(data_path):
        print("data.json not found!")
        return

    with open(data_path, 'r', encoding='utf-8') as f:
        sales_data = json.load(f)

    # Format JSON string for embedding
    js_data = json.dumps(sales_data, indent=2, ensure_ascii=False)

    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Porsche Analytics - Dashboard de Vendas</title>
    <meta name="description" content="Dashboard interativo de vendas da Porsche, baseado na identidade visual e refinamento da marca.">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <!-- Chart.js via CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        /* CSS Variables - Porsche Visual Identity */
        :root {
            --bg-primary: #0b0b0c;
            --bg-secondary: #111112;
            --bg-card: #161618;
            --bg-hover: #1e1e21;
            --border-color: #242428;
            --text-primary: #ffffff;
            --text-secondary: #8a8a93;
            --text-muted: #5e5e65;
            --brand-red: #d5001c; /* Porsche Guards Red */
            --brand-gold: #c5a059; /* Porsche Crest Gold */
            --accent-green: #00b050;
            --font-primary: 'Inter', sans-serif;
            --font-display: 'Outfit', sans-serif;
            --transition-speed: 0.3s;
            --shadow-premium: 0 10px 30px rgba(0, 0, 0, 0.5);
        }

        /* Light Theme Options */
        body.light-theme {
            --bg-primary: #f8f9fa;
            --bg-secondary: #ffffff;
            --bg-card: #ffffff;
            --bg-hover: #f1f3f5;
            --border-color: #e9ecef;
            --text-primary: #1c1c1e;
            --text-secondary: #6c757d;
            --text-muted: #adb5bd;
            --shadow-premium: 0 10px 30px rgba(0, 0, 0, 0.05);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: var(--font-primary);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            transition: background-color var(--transition-speed), color var(--transition-speed);
            overflow-x: hidden;
        }

        /* Scrollbar styling */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: var(--bg-primary);
        }
        ::-webkit-scrollbar-thumb {
            background: var(--border-color);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: var(--text-muted);
        }

        /* Header Layout */
        header {
            background-color: var(--bg-secondary);
            border-bottom: 1px solid var(--border-color);
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .porsche-logo {
            font-family: var(--font-display);
            font-weight: 800;
            font-size: 1.5rem;
            letter-spacing: 0.35em;
            text-transform: uppercase;
            color: var(--text-primary);
            text-decoration: none;
            display: inline-block;
            transition: color var(--transition-speed);
        }
        
        .porsche-logo span {
            color: var(--brand-red);
        }

        .subtitle {
            font-family: var(--font-display);
            font-size: 0.75rem;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--text-secondary);
            border-left: 1px solid var(--border-color);
            padding-left: 1rem;
            display: flex;
            align-items: center;
            height: 1.5rem;
        }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 1.5rem;
        }

        .theme-toggle {
            background: none;
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.5rem 1rem;
            border-radius: 4px;
            font-size: 0.8rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all var(--transition-speed);
            font-family: var(--font-primary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .theme-toggle:hover {
            background-color: var(--bg-hover);
            border-color: var(--text-muted);
        }

        /* Main Workspace */
        .dashboard-container {
            display: flex;
            flex: 1;
            position: relative;
        }

        /* Sidebar Filters */
        aside {
            width: 320px;
            background-color: var(--bg-secondary);
            border-right: 1px solid var(--border-color);
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 1.75rem;
            overflow-y: auto;
            height: calc(100vh - 70px);
            position: sticky;
            top: 70px;
            z-index: 90;
        }

        .filter-section-title {
            font-family: var(--font-display);
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 0.75rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .filter-section-title .reset-icon {
            cursor: pointer;
            font-size: 0.75rem;
            color: var(--brand-red);
            text-transform: none;
            letter-spacing: 0;
            font-weight: 400;
        }

        .filter-group {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .filter-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .custom-select, .custom-input {
            width: 100%;
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem;
            font-size: 0.85rem;
            border-radius: 4px;
            outline: none;
            transition: border-color var(--transition-speed);
            font-family: var(--font-primary);
        }

        .custom-select:focus, .custom-input:focus {
            border-color: var(--brand-red);
        }

        /* Date inputs */
        .date-range {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.5rem;
        }

        /* Multi-select tag display */
        .multi-select-container {
            position: relative;
        }

        .search-results {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            max-height: 200px;
            overflow-y: auto;
            z-index: 110;
            display: none;
            box-shadow: var(--shadow-premium);
        }

        .search-item {
            padding: 0.6rem 0.8rem;
            font-size: 0.85rem;
            cursor: pointer;
            transition: background-color var(--transition-speed);
        }

        .search-item:hover {
            background-color: var(--bg-hover);
        }

        .search-item.selected {
            color: var(--brand-red);
            font-weight: 600;
        }

        .active-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
            margin-top: 0.5rem;
        }

        .tag {
            background-color: var(--bg-hover);
            border: 1px solid var(--border-color);
            padding: 0.25rem 0.6rem;
            border-radius: 20px;
            font-size: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
            color: var(--text-primary);
        }

        .tag-remove {
            cursor: pointer;
            color: var(--brand-red);
            font-weight: bold;
        }

        .btn-reset-all {
            margin-top: auto;
            background-color: transparent;
            border: 1px solid var(--brand-red);
            color: var(--text-primary);
            padding: 0.8rem;
            font-size: 0.8rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            cursor: pointer;
            border-radius: 4px;
            transition: all var(--transition-speed);
            font-family: var(--font-display);
        }

        .btn-reset-all:hover {
            background-color: var(--brand-red);
            color: white;
            box-shadow: 0 0 15px rgba(213, 0, 28, 0.4);
        }

        /* Content Area */
        main {
            flex: 1;
            padding: 2rem;
            display: flex;
            flex-direction: column;
            gap: 2rem;
            overflow-y: auto;
            height: calc(100vh - 70px);
        }

        /* Top Bar Info */
        .dashboard-header-summary {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }

        .page-title {
            font-family: var(--font-display);
            font-size: 1.75rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        .page-title span {
            font-weight: 300;
            color: var(--text-secondary);
        }

        .data-period-badge {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            font-size: 0.8rem;
            border-radius: 20px;
            color: var(--text-secondary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .data-period-badge::before {
            content: '';
            display: inline-block;
            width: 8px;
            height: 8px;
            background-color: var(--brand-red);
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                transform: scale(0.9);
                opacity: 0.8;
            }
            50% {
                transform: scale(1.2);
                opacity: 1;
            }
            100% {
                transform: scale(0.9);
                opacity: 0.8;
            }
        }

        /* KPI Cards Grid */
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
        }

        .kpi-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            position: relative;
            overflow: hidden;
            transition: transform var(--transition-speed), border-color var(--transition-speed), box-shadow var(--transition-speed);
            box-shadow: var(--shadow-premium);
        }

        .kpi-card::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--border-color), transparent);
            transition: background var(--transition-speed);
        }

        .kpi-card:hover {
            transform: translateY(-5px);
            border-color: var(--text-muted);
        }

        .kpi-card:hover::after {
            background: linear-gradient(90deg, transparent, var(--brand-red), transparent);
        }

        .kpi-title {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        .kpi-value {
            font-family: var(--font-display);
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--text-primary);
            line-height: 1.2;
        }

        .kpi-desc {
            font-size: 0.7rem;
            color: var(--text-muted);
        }

        /* Dashboard Charts Grid */
        .charts-grid {
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 1.5rem;
        }

        @media (max-width: 1100px) {
            .charts-grid {
                grid-template-columns: 1fr;
            }
        }

        .chart-card {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            box-shadow: var(--shadow-premium);
            transition: border-color var(--transition-speed);
        }

        .chart-card:hover {
            border-color: rgba(255, 255, 255, 0.05);
        }

        .chart-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .chart-title {
            font-family: var(--font-display);
            font-size: 1rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            color: var(--text-primary);
        }

        .chart-subtitle {
            font-size: 0.75rem;
            color: var(--text-secondary);
        }

        .chart-container {
            position: relative;
            width: 100%;
            height: 320px;
        }

        /* Full Width Row */
        .full-width-row {
            grid-column: 1 / -1;
        }

        /* Business Insights Panel */
        .insights-section {
            background-color: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 2rem;
            box-shadow: var(--shadow-premium);
        }

        .section-header-premium {
            border-left: 3px solid var(--brand-red);
            padding-left: 1rem;
            margin-bottom: 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .section-title-premium {
            font-family: var(--font-display);
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: var(--text-primary);
        }

        .insights-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 1.5rem;
        }

        .insight-card {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 6px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1rem;
            transition: all var(--transition-speed);
        }

        .insight-card:hover {
            border-color: var(--brand-gold);
            transform: translateY(-2px);
        }

        .insight-title-group {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .insight-icon-badge {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            background-color: var(--bg-hover);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            color: var(--brand-gold);
            border: 1px solid var(--border-color);
        }

        .insight-title {
            font-family: var(--font-display);
            font-size: 0.9rem;
            font-weight: 600;
            color: var(--text-primary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .insight-content {
            font-size: 0.85rem;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        .insight-highlight {
            color: var(--text-primary);
            font-weight: 600;
            border-bottom: 1px dashed var(--brand-gold);
            padding-bottom: 1px;
        }

        .insight-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.6rem;
            margin-top: 0.5rem;
        }

        .insight-list-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.4rem;
        }

        .insight-list-item span:first-child {
            color: var(--text-secondary);
        }

        .insight-list-item span:last-child {
            color: var(--text-primary);
            font-weight: 600;
        }

        /* Table Design */
        .premium-table-container {
            max-height: 250px;
            overflow-y: auto;
            border: 1px solid var(--border-color);
            border-radius: 4px;
        }

        .premium-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 0.8rem;
            text-align: left;
        }

        .premium-table th {
            background-color: var(--bg-hover);
            color: var(--text-secondary);
            font-weight: 600;
            padding: 0.75rem 1rem;
            text-transform: uppercase;
            font-size: 0.7rem;
            letter-spacing: 0.05em;
            position: sticky;
            top: 0;
            border-bottom: 1px solid var(--border-color);
        }

        .premium-table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-secondary);
        }

        .premium-table tr:hover td {
            background-color: var(--bg-hover);
            color: var(--text-primary);
        }

        .premium-table tr:last-child td {
            border-bottom: none;
        }

        /* No Data State */
        .no-data {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 4rem 2rem;
            color: var(--text-secondary);
            gap: 1rem;
            grid-column: 1 / -1;
        }

        .no-data-icon {
            font-size: 3rem;
            color: var(--text-muted);
        }

        /* Responsive Layouts */
        @media (max-width: 900px) {
            .dashboard-container {
                flex-direction: column;
            }

            aside {
                width: 100%;
                height: auto;
                position: relative;
                top: 0;
                border-right: none;
                border-bottom: 1px solid var(--border-color);
                padding: 1.5rem;
            }

            main {
                height: auto;
                padding: 1.5rem;
            }
        }

        /* Footer styling */
        footer {
            background-color: var(--bg-secondary);
            border-top: 1px solid var(--border-color);
            padding: 1.5rem 2rem;
            text-align: center;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: auto;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo-container">
            <a href="#" class="porsche-logo">PORSCHE<span>.</span></a>
            <div class="subtitle">Brasil | Analytics</div>
        </div>
        <div class="header-actions">
            <button class="theme-toggle" id="themeToggle" onclick="toggleTheme()">
                <span id="themeToggleIcon">☀️</span> <span id="themeToggleText">Modo Claro</span>
            </button>
        </div>
    </header>

    <div class="dashboard-container">
        <!-- Sidebar Filters -->
        <aside>
            <div class="filter-section-title">
                <span>Filtros Corporativos</span>
                <span class="reset-icon" onclick="resetAllFilters()">Limpar tudo</span>
            </div>

            <!-- Porsche Model Filter -->
            <div class="filter-group">
                <label class="filter-label" for="modelFilter">Modelo da Porsche</label>
                <div class="multi-select-container">
                    <input type="text" id="modelFilterInput" class="custom-input" placeholder="Pesquisar modelo..." onfocus="showModelResults()" oninput="filterModels()">
                    <div id="modelSearchResults" class="search-results">
                        <!-- Items populated dynamically -->
                    </div>
                </div>
                <div class="active-tags" id="activeModelTags">
                    <!-- Dynamic tags -->
                </div>
            </div>

            <!-- Model Year Filter -->
            <div class="filter-group">
                <label class="filter-label" for="yearFilter">Ano do Modelo</label>
                <select id="yearFilter" class="custom-select" onchange="applyFilters()">
                    <option value="">Todos os Anos</option>
                    <!-- Populated dynamically -->
                </select>
            </div>

            <!-- City Filter -->
            <div class="filter-group">
                <label class="filter-label" for="cityFilter">Cidade</label>
                <div class="multi-select-container">
                    <input type="text" id="cityFilterInput" class="custom-input" placeholder="Pesquisar cidade..." onfocus="showCityResults()" oninput="filterCities()">
                    <div id="citySearchResults" class="search-results">
                        <!-- Items populated dynamically -->
                    </div>
                </div>
                <div class="active-tags" id="activeCityTags">
                    <!-- Dynamic tags -->
                </div>
            </div>

            <!-- Payment Method Filter -->
            <div class="filter-group">
                <label class="filter-label" for="payMethodFilter">Forma de Pagamento</label>
                <select id="payMethodFilter" class="custom-select" onchange="applyFilters()">
                    <option value="">Todas as Formas</option>
                    <!-- Populated dynamically -->
                </select>
            </div>

            <!-- Date range Filter -->
            <div class="filter-group">
                <label class="filter-label">Período de Venda</label>
                <div class="date-range">
                    <input type="date" id="dateStartFilter" class="custom-input" onchange="applyFilters()">
                    <input type="date" id="dateEndFilter" class="custom-input" onchange="applyFilters()">
                </div>
            </div>

            <button class="btn-reset-all" onclick="resetAllFilters()">Resetar Dashboard</button>
        </aside>

        <!-- Main Content Workspace -->
        <main>
            <div class="dashboard-header-summary">
                <h1 class="page-title">Relatório de Performance <span>de Vendas</span></h1>
                <div class="data-period-badge" id="periodBadge">Todos os registros</div>
            </div>

            <!-- KPIs Cards -->
            <section class="kpi-grid">
                <div class="kpi-card">
                    <span class="kpi-title">Faturamento Total</span>
                    <span class="kpi-value" id="kpiRevenue">R$ 0,00</span>
                    <span class="kpi-desc" id="kpiRevenueSub">Faturamento bruto das vendas filtradas</span>
                </div>
                <div class="kpi-card">
                    <span class="kpi-title">Veículos Vendidos</span>
                    <span class="kpi-value" id="kpiCount">0</span>
                    <span class="kpi-desc" id="kpiCountSub">Unidades faturadas no período</span>
                </div>
                <div class="kpi-card">
                    <span class="kpi-title">Ticket Médio</span>
                    <span class="kpi-value" id="kpiAvgPrice">R$ 0,00</span>
                    <span class="kpi-desc" id="kpiAvgPriceSub">Preço médio de faturamento</span>
                </div>
                <div class="kpi-card">
                    <span class="kpi-title">Quilometragem Média</span>
                    <span class="kpi-value" id="kpiAvgMileage">0 km</span>
                    <span class="kpi-desc" id="kpiAvgMileageSub">Média de rodagem dos veículos faturados</span>
                </div>
            </section>

            <!-- Dashboard Charts Area -->
            <section class="charts-grid">
                <!-- Monthly Sales Line Chart -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Evolução Mensal de Vendas</div>
                            <div class="chart-subtitle">Histórico de carros vendidos por mês</div>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="salesTrendChart"></canvas>
                    </div>
                </div>

                <!-- Model Year distribution Pie Chart -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Distribuição de Anos</div>
                            <div class="chart-subtitle">Representação por ano do modelo</div>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="modelYearChart"></canvas>
                    </div>
                </div>

                <!-- Main Models sold by City horizontal Bar Chart -->
                <div class="chart-card full-width-row">
                    <div class="chart-header">
                        <div>
                            <div class="chart-title">Modelos Líderes por Cidades com Maior Volume</div>
                            <div class="chart-subtitle">Unidades vendidas por modelo nas principais praças comerciais</div>
                        </div>
                    </div>
                    <div class="chart-container">
                        <canvas id="citySalesChart"></canvas>
                    </div>
                </div>
            </section>

            <!-- Business Questions and Insights Panel -->
            <section class="insights-section">
                <div class="section-header-premium">
                    <h2 class="section-title-premium">Perguntas de Negócios & KPIs Inteligentes</h2>
                </div>

                <div class="insights-grid">
                    <!-- Insight 1: Principais Modelos por Cidade -->
                    <div class="insight-card">
                        <div class="insight-title-group">
                            <div class="insight-icon-badge">📍</div>
                            <div class="insight-title">Modelos por Cidade</div>
                        </div>
                        <div class="insight-content">
                            <p style="margin-bottom: 0.75rem;">Distribuição das vendas por praça e o modelo mais comercializado em cada localidade:</p>
                            <div class="premium-table-container">
                                <table class="premium-table" id="modelsByCityTable">
                                    <thead>
                                        <tr>
                                            <th>Cidade</th>
                                            <th>Modelo Líder</th>
                                            <th>Vendidos</th>
                                            <th>Faturamento</th>
                                        </tr>
                                    </thead>
                                    <tbody id="modelsByCityBody">
                                        <!-- Populated dynamically -->
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </div>

                    <!-- Insight 2: Ano do Modelo Mais Vendido -->
                    <div class="insight-card">
                        <div class="insight-title-group">
                            <div class="insight-icon-badge">📅</div>
                            <div class="insight-title">Ano do Modelo em Destaque</div>
                        </div>
                        <div class="insight-content" id="modelYearInsight">
                            <!-- Populated dynamically -->
                        </div>
                    </div>

                    <!-- Insight 3: Perfil e Insights de Carros Populares -->
                    <div class="insight-card">
                        <div class="insight-title-group">
                            <div class="insight-icon-badge">💡</div>
                            <div class="insight-title">Insights de Carros Populares por Cidade</div>
                        </div>
                        <div class="insight-content" id="popularCarInsight">
                            <!-- Populated dynamically -->
                        </div>
                    </div>
                </div>
            </section>
        </main>
    </div>

    <footer>
        <p>© 2026 Porsche Brasil. Todos os direitos reservados. Projeto interno de Business Intelligence.</p>
    </footer>

    <!-- JS Logic and Data -->
    <script>
        // Data injected from backend
        const rawSalesData = {js_data};

        // State variables
        let filteredData = [...rawSalesData];
        let selectedModels = [];
        let selectedCities = [];
        let uniqueModelsList = [];
        let uniqueCitiesList = [];

        // Chart instances
        let salesTrendChartInstance = null;
        let modelYearChartInstance = null;
        let citySalesChartInstance = null;

        // Initialize Application
        window.addEventListener('DOMContentLoaded', () => {
            initializeFilterOptions();
            applyFilters();
            setupOutsideClickHandlers();
        });

        // Setup drop down lists values
        function initializeFilterOptions() {
            const modelsSet = new Set();
            const yearsSet = new Set();
            const citiesSet = new Set();
            const payMethodsSet = new Set();

            rawSalesData.forEach(item => {
                if (item.PorscheModelSanitized) modelsSet.add(item.PorscheModelSanitized);
                if (item.ModelYearSanitized) yearsSet.add(item.ModelYearSanitized);
                if (item.CitySanitized) citiesSet.add(item.CitySanitized);
                if (item.PayMethodSanitized) payMethodsSet.add(item.PayMethodSanitized);
            });

            uniqueModelsList = Array.from(modelsSet).sort();
            uniqueCitiesList = Array.from(citiesSet).sort();

            // Populate Year select
            const yearSelect = document.getElementById('yearFilter');
            // clear existing options but keep the first one
            yearSelect.innerHTML = '<option value="">Todos os Anos</option>';
            Array.from(yearsSet).sort((a,b) => b - a).forEach(year => {
                const opt = document.createElement('option');
                opt.value = year;
                opt.textContent = year;
                yearSelect.appendChild(opt);
            });

            // Populate Pay Method select
            const paySelect = document.getElementById('payMethodFilter');
            paySelect.innerHTML = '<option value="">Todas as Formas</option>';
            Array.from(payMethodsSet).sort().forEach(method => {
                const opt = document.createElement('option');
                opt.value = method;
                opt.textContent = method;
                paySelect.appendChild(opt);
            });

            renderModelSearchResults(uniqueModelsList);
            renderCitySearchResults(uniqueCitiesList);
        }

        // Dropdown Search logic for Models
        function renderModelSearchResults(list) {
            const container = document.getElementById('modelSearchResults');
            container.innerHTML = '';
            list.forEach(model => {
                const div = document.createElement('div');
                div.className = `search-item ${selectedModels.includes(model) ? 'selected' : ''}`;
                div.textContent = model;
                div.onclick = (e) => {
                    e.stopPropagation();
                    toggleModelSelect(model);
                };
                container.appendChild(div);
            });
        }

        function showModelResults() {
            document.getElementById('modelSearchResults').style.display = 'block';
            document.getElementById('citySearchResults').style.display = 'none';
        }

        function filterModels() {
            const query = document.getElementById('modelFilterInput').value.toLowerCase();
            const filtered = uniqueModelsList.filter(m => m.toLowerCase().includes(query));
            renderModelSearchResults(filtered);
        }

        function toggleModelSelect(model) {
            const index = selectedModels.indexOf(model);
            if (index > -1) {
                selectedModels.splice(index, 1);
            } else {
                selectedModels.push(model);
            }
            updateModelTags();
            applyFilters();
            
            // Re-render query results
            filterModels();
        }

        function updateModelTags() {
            const container = document.getElementById('activeModelTags');
            container.innerHTML = '';
            selectedModels.forEach(model => {
                const tag = document.createElement('div');
                tag.className = 'tag';
                tag.innerHTML = `${model} <span class="tag-remove" onclick="toggleModelSelect('${model}')">×</span>`;
                container.appendChild(tag);
            });
        }

        // Dropdown Search logic for Cities
        function renderCitySearchResults(list) {
            const container = document.getElementById('citySearchResults');
            container.innerHTML = '';
            list.forEach(city => {
                const div = document.createElement('div');
                div.className = `search-item ${selectedCities.includes(city) ? 'selected' : ''}`;
                div.textContent = city;
                div.onclick = (e) => {
                    e.stopPropagation();
                    toggleCitySelect(city);
                };
                container.appendChild(div);
            });
        }

        function showCityResults() {
            document.getElementById('citySearchResults').style.display = 'block';
            document.getElementById('modelSearchResults').style.display = 'none';
        }

        function filterCities() {
            const query = document.getElementById('cityFilterInput').value.toLowerCase();
            const filtered = uniqueCitiesList.filter(c => c.toLowerCase().includes(query));
            renderCitySearchResults(filtered);
        }

        function toggleCitySelect(city) {
            const index = selectedCities.indexOf(city);
            if (index > -1) {
                selectedCities.splice(index, 1);
            } else {
                selectedCities.push(city);
            }
            updateCityTags();
            applyFilters();

            // Re-render query results
            filterCities();
        }

        function updateCityTags() {
            const container = document.getElementById('activeCityTags');
            container.innerHTML = '';
            selectedCities.forEach(city => {
                const tag = document.createElement('div');
                tag.className = 'tag';
                tag.innerHTML = `${city} <span class="tag-remove" onclick="toggleCitySelect('${city}')">×</span>`;
                container.appendChild(tag);
            });
        }

        // Close dropdowns on outer click
        function setupOutsideClickHandlers() {
            document.addEventListener('click', (e) => {
                if (!e.target.closest('.multi-select-container')) {
                    document.getElementById('modelSearchResults').style.display = 'none';
                    document.getElementById('citySearchResults').style.display = 'none';
                    document.getElementById('modelFilterInput').value = '';
                    document.getElementById('cityFilterInput').value = '';
                }
            });
        }

        // Apply filters
        function applyFilters() {
            const yearVal = document.getElementById('yearFilter').value;
            const payVal = document.getElementById('payMethodFilter').value;
            const dateStartVal = document.getElementById('dateStartFilter').value;
            const dateEndVal = document.getElementById('dateEndFilter').value;

            filteredData = rawSalesData.filter(item => {
                // Model Filter
                if (selectedModels.length > 0 && !selectedModels.includes(item.PorscheModelSanitized)) {
                    return false;
                }
                // Year Filter
                if (yearVal && item.ModelYearSanitized.toString() !== yearVal) {
                    return false;
                }
                // City Filter
                if (selectedCities.length > 0 && !selectedCities.includes(item.CitySanitized)) {
                    return false;
                }
                // Payment Method Filter
                if (payVal && item.PayMethodSanitized !== payVal) {
                    return false;
                }
                // Date Range Filter
                if (dateStartVal && item.SaleDateSanitized < dateStartVal) {
                    return false;
                }
                if (dateEndVal && item.SaleDateSanitized > dateEndVal) {
                    return false;
                }
                return true;
            });

            updatePeriodBadge(dateStartVal, dateEndVal);
            calculateKPIs();
            renderCharts();
            generateInsights();
        }

        // Update period text badge
        function updatePeriodBadge(start, end) {
            const badge = document.getElementById('periodBadge');
            if (start && end) {
                badge.textContent = `Período: ${formatDateBR(start)} a ${formatDateBR(end)}`;
            } else if (start) {
                badge.textContent = `Desde: ${formatDateBR(start)}`;
            } else if (end) {
                badge.textContent = `Até: ${formatDateBR(end)}`;
            } else {
                badge.textContent = `Todos os registros (${rawSalesData.length} vendas)`;
            }
        }

        function formatDateBR(dateStr) {
            if (!dateStr) return '';
            const parts = dateStr.split('-');
            if (parts.length !== 3) return dateStr;
            return `${parts[2]}/${parts[1]}/${parts[0]}`;
        }

        // Reset all filters
        function resetAllFilters() {
            selectedModels = [];
            selectedCities = [];
            document.getElementById('yearFilter').value = '';
            document.getElementById('payMethodFilter').value = '';
            document.getElementById('dateStartFilter').value = '';
            document.getElementById('dateEndFilter').value = '';
            document.getElementById('modelFilterInput').value = '';
            document.getElementById('cityFilterInput').value = '';
            
            updateModelTags();
            updateCityTags();
            initializeFilterOptions();
            applyFilters();
        }

        // KPI Calculations
        function calculateKPIs() {
            const revenueEl = document.getElementById('kpiRevenue');
            const countEl = document.getElementById('kpiCount');
            const avgPriceEl = document.getElementById('kpiAvgPrice');
            const avgMileageEl = document.getElementById('kpiAvgMileage');

            if (filteredData.length === 0) {
                revenueEl.textContent = 'R$ 0,00';
                countEl.textContent = '0';
                avgPriceEl.textContent = 'R$ 0,00';
                avgMileageEl.textContent = '0 km';
                return;
            }

            let totalRev = 0;
            let totalMileage = 0;

            filteredData.forEach(item => {
                totalRev += item.SalesPriceSanitized;
                totalMileage += item.VehicleMileageSanitized;
            });

            const count = filteredData.length;
            const avgPrice = totalRev / count;
            const avgMileage = totalMileage / count;

            revenueEl.textContent = formatCurrency(totalRev);
            countEl.textContent = `${count} ${count === 1 ? 'veículo' : 'veículos'}`;
            avgPriceEl.textContent = formatCurrency(avgPrice);
            avgMileageEl.textContent = `${Math.round(avgMileage).toLocaleString('pt-BR')} km`;
        }

        function formatCurrency(value) {
            return value.toLocaleString('pt-BR', {
                style: 'currency',
                currency: 'BRL',
                minimumFractionDigits: 2
            });
        }

        // Themes
        function toggleTheme() {
            const body = document.body;
            const toggleIcon = document.getElementById('themeToggleIcon');
            const toggleText = document.getElementById('themeToggleText');

            if (body.classList.contains('light-theme')) {
                body.classList.remove('light-theme');
                toggleIcon.textContent = '☀️';
                toggleText.textContent = 'Modo Claro';
                localStorage.setItem('theme', 'dark');
            } else {
                body.classList.add('light-theme');
                toggleIcon.textContent = '🌙';
                toggleText.textContent = 'Modo Escuro';
                localStorage.setItem('theme', 'light');
            }

            // Re-render charts to update grid colors
            renderCharts();
        }

        // Check theme preference in localStorage
        if (localStorage.getItem('theme') === 'light') {
            document.body.classList.add('light-theme');
            document.getElementById('themeToggleIcon').textContent = '🌙';
            document.getElementById('themeToggleText').textContent = 'Modo Escuro';
        }

        // Render Canvas Charts
        function renderCharts() {
            const isDark = !document.body.classList.contains('light-theme');
            const gridColor = isDark ? '#242428' : '#e9ecef';
            const tickColor = isDark ? '#8a8a93' : '#6c757d';
            const primaryTextColor = isDark ? '#ffffff' : '#1c1c1e';

            // --- Chart 1: Monthly Sales Trend (Line/Area) ---
            const trendCtx = document.getElementById('salesTrendChart').getContext('2d');
            if (salesTrendChartInstance) salesTrendChartInstance.destroy();

            // Process data for trend
            const monthlyData = {};
            filteredData.forEach(item => {
                // Parse date YYYY-MM
                const date = new Date(item.SaleDateSanitized);
                const year = date.getFullYear();
                const month = String(date.getMonth() + 1).padStart(2, '0');
                const key = `${year}-${month}`;
                monthlyData[key] = (monthlyData[key] || 0) + 1;
            });

            // Sort months chronologically
            const sortedMonths = Object.keys(monthlyData).sort();
            const monthlyCounts = sortedMonths.map(m => monthlyData[m]);
            const monthLabels = sortedMonths.map(m => {
                const parts = m.split('-');
                const monthNames = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez'];
                return `${monthNames[parseInt(parts[1])-1]}/${parts[0].slice(-2)}`;
            });

            salesTrendChartInstance = new Chart(trendCtx, {
                type: 'line',
                data: {
                    labels: monthLabels.length > 0 ? monthLabels : ['Sem dados'],
                    datasets: [{
                        label: 'Vendas Mensais',
                        data: monthlyCounts.length > 0 ? monthlyCounts : [0],
                        borderColor: '#d5001c', // Guards Red
                        backgroundColor: 'rgba(213, 0, 28, 0.15)',
                        borderWidth: 2,
                        pointBackgroundColor: '#c5a059', // Dourado nos pontos
                        pointBorderColor: '#ffffff',
                        pointHoverRadius: 7,
                        pointRadius: 4,
                        fill: true,
                        tension: 0.35
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            padding: 12,
                            backgroundColor: isDark ? '#161618' : '#ffffff',
                            titleColor: primaryTextColor,
                            bodyColor: tickColor,
                            borderColor: gridColor,
                            borderWidth: 1,
                            callbacks: {
                                label: function(context) {
                                    return `Vendas: ${context.raw} unidades`;
                                }
                            }
                        }
                    },
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: tickColor, font: { family: 'Inter', size: 10 } }
                        },
                        y: {
                            grid: { color: gridColor },
                            ticks: { 
                                color: tickColor, 
                                font: { family: 'Inter', size: 10 },
                                stepSize: 1,
                                precision: 0
                            }
                        }
                    }
                }
            });


            // --- Chart 2: Model Year Distribution (Doughnut) ---
            const yearCtx = document.getElementById('modelYearChart').getContext('2d');
            if (modelYearChartInstance) modelYearChartInstance.destroy();

            const yearCounts = {};
            filteredData.forEach(item => {
                yearCounts[item.ModelYearSanitized] = (yearCounts[item.ModelYearSanitized] || 0) + 1;
            });

            const sortedYears = Object.keys(yearCounts).sort((a,b) => a - b);
            const yearLabels = sortedYears.map(y => `Modelo ${y}`);
            const yearValues = sortedYears.map(y => yearCounts[y]);

            // Visual palette for years - gradient tones of grey, silver, white, and a highlight red/gold
            const yearPalette = [
                '#1c1c1e', '#2c2c2e', '#3a3a3c', '#5e5e65', '#8a8a93', '#c5a059', '#d5001c'
            ];

            modelYearChartInstance = new Chart(yearCtx, {
                type: 'doughnut',
                data: {
                    labels: yearLabels.length > 0 ? yearLabels : ['Sem dados'],
                    datasets: [{
                        data: yearValues.length > 0 ? yearValues : [1],
                        backgroundColor: yearValues.length > 0 ? yearPalette.slice(0, yearValues.length) : ['#242428'],
                        borderWidth: isDark ? 2 : 1,
                        borderColor: isDark ? '#161618' : '#ffffff',
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                color: tickColor,
                                font: { family: 'Inter', size: 10 },
                                boxWidth: 12
                            }
                        },
                        tooltip: {
                            padding: 12,
                            backgroundColor: isDark ? '#161618' : '#ffffff',
                            titleColor: primaryTextColor,
                            bodyColor: tickColor,
                            borderColor: gridColor,
                            borderWidth: 1,
                            callbacks: {
                                label: function(context) {
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const value = context.raw;
                                    const pct = ((value / total) * 100).toFixed(1);
                                    return ` ${context.label}: ${value} (${pct}%)`;
                                }
                            }
                        }
                    },
                    cutout: '65%'
                }}
            });


            // --- Chart 3: Main Car Models by Top Cities (Horizontal Bar) ---
            const cityCtx = document.getElementById('citySalesChart').getContext('2d');
            if (citySalesChartInstance) citySalesChartInstance.destroy();

            // Group by city to find top cities by volume
            const cityVolume = {};
            filteredData.forEach(item => {
                cityVolume[item.CitySanitized] = (cityVolume[item.CitySanitized] || 0) + 1;
            });

            // Take top 8 cities by volume to make chart readable
            const topCities = Object.keys(cityVolume)
                .sort((a, b) => cityVolume[b] - cityVolume[a])
                .slice(0, 8);

            // Get top models overall in these cities
            const cityModelData = {}; // city -> model -> count
            const allModelsSet = new Set();

            filteredData.forEach(item => {
                const city = item.CitySanitized;
                if (!topCities.includes(city)) return;
                
                const model = item.PorscheModelSanitized;
                allModelsSet.add(model);

                if (!cityModelData[city]) cityModelData[city] = {};
                cityModelData[city][model] = (cityModelData[city][model] || 0) + 1;
            });

            const topModelsOverall = Array.from(allModelsSet);

            // Prepare datasets: one dataset per model
            // Porsche palette: high contrast greys, golden yellow, custom silver, guards red
            const colors = [
                '#d5001c', '#c5a059', '#3a3a3c', '#8a8a93', '#5e5e65', '#2c2c2e', 
                '#b392ac', '#735d78', '#90dbf4', '#f1c0e8', '#cfbaf0', '#a3c4f3'
            ];

            const datasets = topModelsOverall.map((model, idx) => {
                const data = topCities.map(city => {
                    return cityModelData[city] && cityModelData[city][model] ? cityModelData[city][model] : 0;
                });

                return {
                    label: model,
                    data: data,
                    backgroundColor: colors[idx % colors.length],
                    borderWidth: 0,
                    stack: 'Stack 0'
                };
            });

            citySalesChartInstance = new Chart(cityCtx, {
                type: 'bar',
                data: {
                    labels: topCities.length > 0 ? topCities : ['Sem dados'],
                    datasets: datasets.length > 0 ? datasets : [{ label: 'Sem dados', data: [0] }]
                },
                options: {
                    indexAxis: 'y', // Makes the bar chart horizontal
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom',
                            labels: {
                                color: tickColor,
                                font: { family: 'Inter', size: 9 },
                                boxWidth: 10,
                                padding: 12
                            }
                        },
                        tooltip: {
                            padding: 12,
                            backgroundColor: isDark ? '#161618' : '#ffffff',
                            titleColor: primaryTextColor,
                            bodyColor: tickColor,
                            borderColor: gridColor,
                            borderWidth: 1
                        }
                    },
                    scales: {
                        x: {
                            stacked: true,
                            grid: { color: gridColor },
                            ticks: { 
                                color: tickColor, 
                                font: { family: 'Inter', size: 10 },
                                stepSize: 1,
                                precision: 0
                            }
                        },
                        y: {
                            stacked: true,
                            grid: { display: false },
                            ticks: { color: tickColor, font: { family: 'Inter', size: 10 } }
                        }
                    }
                }
            });
        }

        // Generate dynamic answers and insights
        function generateInsights() {
            const tableBody = document.getElementById('modelsByCityBody');
            const yearInsightEl = document.getElementById('modelYearInsight');
            const popularInsightEl = document.getElementById('popularCarInsight');

            if (filteredData.length === 0) {
                tableBody.innerHTML = '<tr><td colspan="4" style="text-align: center;">Nenhum dado encontrado para os filtros atuais.</td></tr>';
                yearInsightEl.innerHTML = '<p>Selecione outros filtros para gerar insights de período.</p>';
                popularInsightEl.innerHTML = '<p>Selecione outras localidades para verificar a popularidade de modelos.</p>';
                return;
            }

            // --- Insight 1: Principais Modelos Vendidos por Cidade ---
            // Calculate sales count per city and model
            const cityModelSales = {}; // city -> model -> { count, revenue }
            filteredData.forEach(item => {
                const city = item.CitySanitized;
                const model = item.PorscheModelSanitized;
                const price = item.SalesPriceSanitized;

                if (!cityModelSales[city]) cityModelSales[city] = {};
                if (!cityModelSales[city][model]) {
                    cityModelSales[city][model] = { count: 0, revenue: 0 };
                }

                cityModelSales[city][model].count += 1;
                cityModelSales[city][model].revenue += price;
            });

            tableBody.innerHTML = '';
            
            // For each city, find the main model (highest count, tie breaker: revenue)
            const citySummaries = [];
            Object.keys(cityModelSales).forEach(city => {
                let leaderModel = '';
                let leaderCount = 0;
                let leaderRevenue = 0;
                let cityTotalRevenue = 0;

                Object.keys(cityModelSales[city]).forEach(model => {
                    const mData = cityModelSales[city][model];
                    cityTotalRevenue += mData.revenue;
                    if (mData.count > leaderCount || (mData.count === leaderCount && mData.revenue > leaderRevenue)) {
                        leaderModel = model;
                        leaderCount = mData.count;
                        leaderRevenue = mData.revenue;
                    }
                });

                citySummaries.push({
                    city: city,
                    leaderModel: leaderModel,
                    leaderCount: leaderCount,
                    leaderRevenue: leaderRevenue,
                    cityTotalRevenue: cityTotalRevenue
                });
            });

            // Sort cities by total revenue descending
            citySummaries.sort((a,b) => b.cityTotalRevenue - a.cityTotalRevenue);

            // Populate table with top cities
            citySummaries.forEach(summary => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><strong>${summary.city}</strong></td>
                    <td><span style="color: var(--brand-gold); font-weight: 500;">${summary.leaderModel}</span></td>
                    <td>${summary.leaderCount} ${summary.leaderCount === 1 ? 'unidade' : 'unidades'}</td>
                    <td>${formatCurrency(summary.leaderRevenue)}</td>
                `;
                tableBody.appendChild(tr);
            });


            // --- Insight 2: Ano do Modelo Mais Vendido no Período ---
            const yearCounts = {};
            filteredData.forEach(item => {
                yearCounts[item.ModelYearSanitized] = (yearCounts[item.ModelYearSanitized] || 0) + 1;
            });

            let topYear = '';
            let topYearCount = 0;
            Object.keys(yearCounts).forEach(yr => {
                if (yearCounts[yr] > topYearCount) {
                    topYear = yr;
                    topYearCount = yearCounts[yr];
                }
            });

            const yearPct = ((topYearCount / filteredData.length) * 100).toFixed(1);
            
            // Find total revenue of this top year
            const topYearRev = filteredData
                .filter(item => item.ModelYearSanitized.toString() === topYear)
                .reduce((acc, item) => acc + item.SalesPriceSanitized, 0);

            yearInsightEl.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <p>O ano de fabricação que registrou o maior volume de saída no período selecionado foi o ano modelo <span class="insight-highlight">${topYear}</span>.</p>
                    <div style="display: flex; align-items: center; gap: 1rem; margin: 0.5rem 0;">
                        <div style="font-size: 2.2rem; font-family: var(--font-display); font-weight: 800; color: var(--brand-red);">${topYear}</div>
                        <div>
                            <div style="font-size: 0.9rem; font-weight: 700; color: var(--text-primary);">${topYearCount} unidades vendidas</div>
                            <div style="font-size: 0.75rem; color: var(--text-secondary);">Representa ${yearPct}% de participação nas vendas</div>
                        </div>
                    </div>
                    <ul class="insight-list">
                        <li class="insight-list-item">
                            <span>Receita deste ano modelo:</span>
                            <span>${formatCurrency(topYearRev)}</span>
                        </li>
                        <li class="insight-list-item">
                            <span>Ticket médio do modelo:</span>
                            <span>${formatCurrency(topYearRev / topYearCount)}</span>
                        </li>
                    </ul>
                </div>
            `;


            // --- Insight 3: Insights de Carros Populares por Cidade ---
            // "Popular" refers to the model that drove the highest volume relative to price (often the entry or mid-range volume drivers like Cayman, Macan or standard Cayenne vs expensive ones).
            // Let's analyze: what are the high volume / popular options in the database?
            // Group by model overall to see average pricing
            const modelAverages = {}; // model -> { total_price, count }
            filteredData.forEach(item => {
                const model = item.PorscheModelSanitized;
                if (!modelAverages[model]) modelAverages[model] = { total_price: 0, count: 0 };
                modelAverages[model].total_price += item.SalesPriceSanitized;
                modelAverages[model].count += 1;
            });

            // Find the most sold model overall
            let topVolModel = '';
            let topVolCount = 0;
            Object.keys(modelAverages).forEach(model => {
                if (modelAverages[model].count > topVolCount) {
                    topVolModel = model;
                    topVolCount = modelAverages[model].count;
                }
            });

            const topVolModelPrice = modelAverages[topVolModel] ? (modelAverages[topVolModel].total_price / modelAverages[topVolModel].count) : 0;

            // Generate some localized city specific insight (e.g. for the highest volume city)
            const topCitySummary = citySummaries[0]; // The city with highest faturamento
            let popularCityText = '';
            if (topCitySummary) {
                popularCityText = `Na praça de maior representatividade financeira (<span class="insight-highlight">${topCitySummary.city}</span>), o modelo líder é o <span class="insight-highlight">${topCitySummary.leaderModel}</span>, somando um faturamento de ${formatCurrency(topCitySummary.leaderRevenue)} para ${topCitySummary.leaderCount} unidades.`;
            }

            // Let's identify entry-level popular cars (lower than average price, higher volume)
            // Average price across all sales
            const overallAverage = filteredData.reduce((acc, item) => acc + item.SalesPriceSanitized, 0) / filteredData.length;
            
            const entryPopularModels = Object.keys(modelAverages)
                .map(model => ({
                    name: model,
                    count: modelAverages[model].count,
                    avgPrice: modelAverages[model].total_price / modelAverages[model].count
                }))
                .filter(m => m.avgPrice < overallAverage && m.count >= 2) // Cheaper than average and sold at least twice
                .sort((a,b) => b.count - a.count); // sorted by volume

            let entryInsightText = '';
            if (entryPopularModels.length > 0) {
                const bestEntry = entryPopularModels[0];
                entryInsightText = `O modelo <span class="insight-highlight">${bestEntry.name}</span> desponta como uma excelente opção 'popular' (de volume de entrada) nas cidades pesquisadas, com preço médio de ${formatCurrency(bestEntry.avgPrice)} e ${bestEntry.count} unidades vendidas.`;
            } else {
                entryInsightText = `O modelo mais frequente do portfólio no período é o <span class="insight-highlight">${topVolModel}</span>, com ticket médio de ${formatCurrency(topVolModelPrice)}.`;
            }

            popularInsightEl.innerHTML = `
                <div style="display: flex; flex-direction: column; gap: 1rem;">
                    <p style="font-size: 0.85rem; line-height: 1.5;">${popularCityText}</p>
                    <p style="font-size: 0.85rem; line-height: 1.5; margin-top: 0.5rem;">${entryInsightText}</p>
                    <div style="background-color: var(--bg-primary); padding: 1rem; border-radius: 4px; border: 1px solid var(--border-color); margin-top: 0.5rem;">
                        <div style="font-size: 0.75rem; color: var(--text-secondary); text-transform: uppercase; font-weight: 700; margin-bottom: 0.5rem; color: var(--brand-gold);">Resumo de Ticket Médio Geral</div>
                        <div style="font-size: 1.25rem; font-family: var(--font-display); font-weight: 700;">${formatCurrency(overallAverage)}</div>
                        <div style="font-size: 0.7rem; color: var(--text-muted); margin-top: 0.2rem;">Modelos abaixo desta linha são considerados de entrada/volume de vendas (ex. Cayman, Macan).</div>
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>
"""

    # Do replacements safely
    html_content = html_content.replace("{js_data}", js_data)

    output_path = 'dashboard.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Successfully generated dashboard in: {output_path}")

if __name__ == '__main__':
    generate()
