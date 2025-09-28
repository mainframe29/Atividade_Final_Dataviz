import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from sklearn.linear_model import LinearRegression
from dash import dcc, html

from GerenciarArquivos import GerenciarArquivos

class Graficos():

    def __init__(self):
        self.df_regional = self.ler_csv('Datasets/EmpoderamentoEconomico_HomensMulheres_PorRegiao.csv')
        self.df_cargo = self.ler_csv('Datasets/EmpoderamentoEconomico_HomensMulheres_PorCargo.csv')

    def ler_csv(self, caminho):
        try:
            return pd.read_csv(caminho)
        except FileNotFoundError:
            GerenciarArquivos()
            return pd.read_csv(caminho)
        
    def homensXmulheres(self):
        df_brasil = self.df_regional[self.df_regional['Indicadores'] == 'Brasil']
        df_brasil = df_brasil.drop(columns=['Indicadores'])
        df_brasil_ano = df_brasil.groupby('Ano').mean()

        df_brasil_ano = df_brasil_ano.reset_index()

        df = pd.DataFrame(df_brasil_ano)

        # Criando o gráfico de barras interativo
        fig = go.Figure()

        # Barras para Homens
        fig.add_trace(go.Bar(
            x=df['Ano'],
            y=df['Homens'],
            name='Homens',
            marker_color='blue'
        ))

        # Barras para Mulheres
        fig.add_trace(go.Bar(
            x=df['Ano'],
            y=df['Mulheres'],
            name='Mulheres',
            marker_color='red'
        ))

        # Layout do gráfico
        fig.update_layout(
            title='Empoderamento Econômico - Homens vs Mulheres',
            xaxis_title='Ano',
            yaxis_title='Valor',
            barmode='group',  # barras lado a lado
            template='plotly_white',
        )

        return dcc.Graph(figure=fig, style={
        'border': '2px solid #2980b9',
        'borderRadius': '10px',
        'padding': '10px',
        'height': '300px'
        })
    
    def empoderamentoRegional(self):
        df_media = self.df_regional.groupby(['Ano', 'Indicadores'], as_index=False).mean()
        df = pd.DataFrame(df_media)

        # Listagem das regiões disponíveis
        regioes = df['Indicadores'].unique()

        # Cria a figura
        fig = go.Figure()

        # Adiciona as linhas de todas as regiões, mas inicialmente só mostra a primeira
        for i, regiao in enumerate(regioes):
            df_regiao = df[df['Indicadores'] == regiao]
            visible = True if i == 0 else False
            fig.add_trace(go.Scatter(
                x=df_regiao['Ano'],
                y=df_regiao['Homens'],
                mode='lines+markers',
                name=f'Homens - {regiao}',
                line=dict(color='blue'),
                visible=visible
            ))
            fig.add_trace(go.Scatter(
                x=df_regiao['Ano'],
                y=df_regiao['Mulheres'],
                mode='lines+markers',
                name=f'Mulheres - {regiao}',
                line=dict(color='red'),
                visible=visible
            ))

        # Botões dropdown para escolher a região
        buttons = []
        for i, regiao in enumerate(regioes):
            visibilidade = [False] * len(fig.data)
            visibilidade[i*2] = True   # Homem
            visibilidade[i*2+1] = True # Mulher
            buttons.append(dict(label=regiao,
                                method='update',
                                args=[{'visible': visibilidade},
                                    {'title': {'text': f'Empoderamento Econômico - {regiao}'}}]))

        fig.update_layout(
            title=f'Empoderamento Econômico - {regioes[0]}',
            xaxis_title='Ano',
            yaxis_title='Valor',
            updatemenus=[dict(active=0, buttons=buttons, x=1.1, y=1.6)],
            template='plotly_white'
        )

        return dcc.Graph(figure=fig, style={
        'border': '2px solid #2980b9',
        'borderRadius': '10px',
        'padding': '10px',
        'height': '300px'
        })
    
    def empoderamentoPorSetor(self):
        df_cargo_filtrado = self.df_cargo[~self.df_cargo['Indicadores'].str.contains(r'\d')]

        abreviacoes = {
            'Diretores e gerentes': 'Diretores/Gerentes',
            'Profissionais das ciências e intelectuais': 'Científicos/Intelectuais',
            'Técnicos e profissionais de nível médio': 'Técnicos/Nível Médio',
            'Trabalhadores de apoio administrativo': 'Apoio Administrativo',
            'Trabalhadores dos serviços, vendedores dos comércios e mercados': 'Serviços/Vendas',
            'Trabalhadores qualificados da agropecuária, florestais, da caça e da pesca': 'Agropecuária/Florestal/Pesca',
            'Trabalhadores qualificados, operários e artesões da construção, das artes mecânicas e outros ofícios': 'Construção/Ofícios',
            'Operadores de instalações e máquinas e montadores': 'Operadores/Máquinas',
            'Ocupações elementares': 'Ocupações Elementares',
            'Membros das forças armadas, policiais e bombeiros militares': 'Forças Armadas/Polícia/Bombeiros'
        }

        # Aplica as abreviações no dataset
        df_cargo_filtrado['Indicadores_curto'] = df_cargo_filtrado['Indicadores'].replace(abreviacoes)

        df = pd.DataFrame(df_cargo_filtrado)

        # Lista de anos disponíveis
        anos = df['Ano'].unique()

        # Cria a figura
        fig = go.Figure()

        # Adiciona barras para cada ano, mas apenas o primeiro ano visível inicialmente
        for i, ano in enumerate(anos):
            df_ano = df[df['Ano'] == ano]
            visible = True if i == 0 else False
            fig.add_trace(go.Bar(
                x=df_ano['Indicadores_curto'],
                y=df_ano['Homens'],
                name='Homens',
                marker_color='blue',
                visible=visible
            ))
            fig.add_trace(go.Bar(
                x=df_ano['Indicadores_curto'],
                y=df_ano['Mulheres'],
                name='Mulheres',
                marker_color='red',
                visible=visible
            ))

        # Botões dropdown para escolher o ano
        buttons = []
        for i, ano in enumerate(anos):
            vis = [False] * len(fig.data)
            vis[i*2] = True   # Homens
            vis[i*2+1] = True # Mulheres
            buttons.append(dict(label=str(ano),
                                method='update',
                                args=[{'visible': vis},
                                    {'title': {'text': f'Empoderamento Econômico por Setor - {ano}'}}]))

        fig.update_layout(
            title=f'Empoderamento Econômico por Setor - {anos[0]}',
            xaxis_title='Setor',
            yaxis_title='Valor',
            barmode='group',
            updatemenus=[dict(active=0, buttons=buttons, x=1.1, y=1.6)],
            template='plotly_white'
        )

        return dcc.Graph(figure=fig, style={
        'border': '2px solid #2980b9',
        'borderRadius': '10px',
        'padding': '10px',
        'height': '300px'
        })
    
    def mapaGeografico(self):

        df_media = self.df_regional.groupby(['Ano', 'Indicadores'], as_index=False).mean()

        df = pd.DataFrame(df_media)

        # Calcula diferença percentual
        df['Dif_percent'] = ((df['Homens'] - df['Mulheres']) / df['Homens'] * 100).round(2)

        # Dicionário para mapear regiões para códigos das UFs
        # (para Plotly usar o mapa do Brasil)
        regioes_uf = {
            'Norte': ['AC','AP','AM','PA','RO','RR','TO'],
            'Nordeste': ['AL','BA','CE','MA','PB','PE','PI','RN','SE'],
            'Sudeste': ['ES','MG','RJ','SP'],
            'Sul': ['PR','RS','SC'],
            'Centro-Oeste': ['DF','GO','MT','MS'],
            'Brasil': ['BR']  # pode ser usado para destacar todo o país
        }

        # Expandindo dataframe para cada UF
        rows = []
        for _, row in df.iterrows():
            for uf in regioes_uf[row['Indicadores']]:
                rows.append({'UF': uf,
                            'Homens': row['Homens'],
                            'Mulheres': row['Mulheres'],
                            'Dif_percent': row['Dif_percent'],
                            'Ano': row['Ano']})
        df_map = pd.DataFrame(rows)

        # Lista de anos disponíveis
        anos = df_map['Ano'].unique()

        # Cria a figura
        fig = go.Figure()

        # Adiciona barras para cada ano, mas apenas o primeiro ano visível inicialmente
        for i, ano in enumerate(anos):
            df_ano = df_map[df_map['Ano'] == ano]
            visible = True if i == 0 else False
            fig.add_trace(go.Choropleth(
                geojson="https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson",
                locations=df_ano['UF'],
                z=df_ano['Dif_percent'],
                featureidkey="properties.sigla",
                colorscale="RdBu_r",
                zmin=0,
                zmax=df_map['Dif_percent'].max(),
                visible=visible,
                hovertext=[
                    f"Homens: {h:.2f}<br>Mulheres: {m:.2f}<br>Dif: {d:.2f}%"
                    for h, m, d in zip(df_ano['Homens'], df_ano['Mulheres'], df_ano['Dif_percent'])
                ],
                hoverinfo="text"
            ))

        # Botões dropdown para escolher o ano
        buttons = []
        for i, ano in enumerate(anos):
            vis = [False] * len(fig.data)
            vis[i] = True  # Ativa só o ano selecionado
            buttons.append(dict(label=str(ano),
                                method='update',
                                args=[{'visible': vis},
                                    {'title': {'text': f'Diferença percentual entre Homens e Mulheres por Região - {ano}'}}]))


        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(title=f'Diferença percentual entre Homens e Mulheres por Região - {anos[0]}',
                          updatemenus=[dict(active=0, buttons=buttons, x=1.1, y=1.6)],
                          template='plotly_white')

        return dcc.Graph(figure=fig, style={
        'border': '2px solid #2980b9',
        'borderRadius': '10px',
        'padding': '10px',
        'height': '300px'
        })
    

    def mapaGeografico2(self):

        df_media = self.df_regional.groupby(['Ano', 'Indicadores'], as_index=False).mean()
        df = pd.DataFrame(df_media)

        # Calcula diferença percentual
        df['Dif_percent'] = ((df['Homens'] - df['Mulheres']) / df['Homens'] * 100).round(2)

        # Dicionário para mapear regiões para códigos das UFs
        regioes_uf = {
            'Norte': ['AC','AP','AM','PA','RO','RR','TO'],
            'Nordeste': ['AL','BA','CE','MA','PB','PE','PI','RN','SE'],
            'Sudeste': ['ES','MG','RJ','SP'],
            'Sul': ['PR','RS','SC'],
            'Centro-Oeste': ['DF','GO','MT','MS'],
            'Brasil': ['BR']
        }

        return html.Div([
            dcc.Dropdown(
                id='filtro-ano',
                options=[{'label': str(ano), 'value': ano} for ano in df['Ano'].unique()],
                value=df['Ano'].min(),
                clearable=False,
                style={'margin-bottom': '10px'}
            ),
            dcc.Graph(id='grafico-mapa',
                    style={
                        'border': '2px solid #2980b9',
                        'borderRadius': '10px',
                        'padding': '10px',
                        'height': '300px'
                    })
        ])

    
    def distribuicaoEscolaridade(self):
        df = pd.DataFrame(self.df_cargo)

        # Mapear cargos para escolaridade
        nivel_escolaridade = {
            'Diretores e gerentes': 'Superior',
            'Profissionais das ciências e intelectuais': 'Superior',
            'Técnicos e profissionais de nível médio': 'Médio',
            'Trabalhadores de apoio administrativo': 'Médio',
            'Trabalhadores dos serviços, vendedores dos comércios e mercados': 'Fundamental'
        }

        df['Escolaridade'] = df['Indicadores'].map(nivel_escolaridade)

        # Transformar dados para formato long (uma linha por valor)
        df_long = df.melt(id_vars=['Escolaridade'], value_vars=['Homens','Mulheres'],
                        var_name='Sexo', value_name='Salário')

        fig = px.box(df_long, x='Escolaridade', y='Salário', color='Sexo',
                    color_discrete_map={'Homens':'blue','Mulheres':'red'},
                    points='all')  # mostra todos os pontos

        fig.update_layout(title='Distribuição Salarial por Escolaridade',
                        template='plotly_white')

        return dcc.Graph(figure=fig, style={
        'border': '2px solid #2980b9',
        'borderRadius': '10px',
        'padding': '10px',
        'height': '300px'
        })

    def projecaoIgualdade(self):
        df_brasil = self.df_regional[self.df_regional['Indicadores'] == 'Brasil']
        df_brasil = df_brasil.drop(columns=['Indicadores'])
        df_brasil_ano = df_brasil.groupby('Ano').mean()

        df_brasil_ano = df_brasil_ano.reset_index()

        df = pd.DataFrame(df_brasil_ano)

        # Garantir que 'Ano' seja numérico
        df['Ano'] = df['Ano'].astype(int)

        # Diferença salarial
        df['Dif'] = df['Homens'] - df['Mulheres']

        # Regressão sobre a diferença
        anos = df['Ano'].values.reshape(-1, 1)
        model_dif = LinearRegression().fit(anos, df['Dif'])

        texto = ""

        if model_dif.coef_[0] >= 0:
            texto = "Diferença não está diminuindo. Igualdade não ocorrerá."
            Ano_eq = None
        else:
            Ano_eq = -model_dif.intercept_ / model_dif.coef_[0]
            texto = f"Projeção indica igualdade em {Ano_eq:.1f}"

        # Modelos lineares para salários
        model_h = LinearRegression().fit(anos, df['Homens'])
        model_m = LinearRegression().fit(anos, df['Mulheres'])

        # Dados reais
        anos_reais = df['Ano'].values
        homens_reais = df['Homens'].values
        mulheres_reais = df['Mulheres'].values

        # Projeção a partir do último ano real
        ultimo_ano = df['Ano'].max()
        if Ano_eq:
            anos_proj = np.arange(ultimo_ano+1, int(Ano_eq)+1, 1)
        else:
            anos_proj = np.arange(ultimo_ano+1, ultimo_ano+4, 1)  # projeta 3 anos se não houver Ano_eq

        homens_proj = model_h.predict(anos_proj.reshape(-1,1))
        mulheres_proj = model_m.predict(anos_proj.reshape(-1,1))

        # Criar gráfico
        fig = go.Figure()

        # Linhas reais
        fig.add_trace(go.Scatter(x=anos_reais, y=homens_reais, mode='lines+markers', name='Homens (reais)', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=anos_reais, y=mulheres_reais, mode='lines+markers', name='Mulheres (reais)', line=dict(color='red')))

        # Linhas de projeção
        fig.add_trace(go.Scatter(x=anos_proj, y=homens_proj, mode='lines+markers', name='Homens (projeção)', line=dict(color='blue', dash='dash')))
        fig.add_trace(go.Scatter(x=anos_proj, y=mulheres_proj, mode='lines+markers', name='Mulheres (projeção)', line=dict(color='red', dash='dash')))

        # Ponto de igualdade
        if Ano_eq:
            fig.add_trace(go.Scatter(
                x=[Ano_eq],
                y=[model_h.predict([[Ano_eq]])[0]],
                mode='markers+text',
                name=texto,
                text=['Igualdade'],
                textposition='top center',
                marker=dict(color='green', size=12)
            ))

        fig.update_layout(title='Projeção de Igualdade Salarial Homens x Mulheres',
                        xaxis_title='Ano',
                        yaxis_title='Salário Médio',
                        template='plotly_white')

        return dcc.Graph(figure=fig, style={
        'border': '2px solid #2980b9',
        'borderRadius': '10px',
        'padding': '10px',
        'height': '300px'
        })
