import os
import dash
from dash import html

from Graficos import Graficos

app = dash.Dash(__name__)

gr = Graficos()

# Função para criar uma linha de gráfico
def linha_grafico(descricao, grafico, texto_esquerda=True):
    if texto_esquerda:
        return html.Div([
            html.Div(descricao, style={
                'flex': '1',
                'padding': '20px',
                'backgroundColor': '#ecf0f1',
                'color': '#34495e',
                'borderRadius': '8px',
                'fontFamily': 'Verdana, sans-serif',
                'fontWeight': 'bold',
                'display': 'flex',
                'alignItems': 'center'
            }),
            html.Div(grafico, style={'flex': '2'})
        ], style={'display': 'flex', 'marginBottom': '50px'})
    else:  # centralizado com descrição abaixo
        return html.Div([
            grafico,
            html.Div(descricao, style={
                'textAlign': 'center',
                'marginTop': '10px',
                'color': '#34495e',
                'fontFamily': 'Verdana, sans-serif',
                'fontWeight': 'bold'
            })
        ], style={'marginBottom': '50px', 'textAlign': 'center'})

app.layout = html.Div([
    # Título e subtítulo
    html.Div([
        html.H1("Desigualdade de Gênero no Mercado de Trabalho Brasileiro", style={
            'textAlign': 'center',
            'fontFamily': 'Arial, sans-serif',
            'color': '#2c3e50'
        }),
        html.H3("Uma análise baseada nos microdados da PNAD Contínua (IBGE).", style={
            'textAlign': 'center',
            'color': '#7f8c8d',
            'fontFamily': 'Verdana, sans-serif'
        })
    ], style={'marginBottom': '50px'}),

    # Gráficos com texto à esquerda
    linha_grafico("Mulheres representam quase metade da força de trabalho no Brasil, mas ainda recebem menos que homens. O gráfico ao lado mostra a diferença no último ano disponível.", gr.homensXmulheres()),
    linha_grafico("A diferença vem diminuindo nos últimos anos, mas lentamente.", gr.empoderamentoRegional()),
    linha_grafico("Mesmo em áreas com predominância feminina, como saúde e educação, a desigualdade persiste.", gr.empoderamentoPorSetor()),
    linha_grafico("A disparidade varia pelo território nacional. Onde ela é maior?", gr.mapaGeografico()),
    linha_grafico("Nem o diploma elimina a diferença. Mulheres com ensino superior ainda recebem menos que homens com a mesma formação.", gr.distribuicaoEscolaridade()),

    # Gráficos centralizados com descrição abaixo
    
    linha_grafico("“Se a tendência atual continuar, pode levar décadas para mulheres alcançarem igualdade salarial plena no Brasil.”", gr.projecaoIgualdade(), texto_esquerda=False),

], style={'width': '90%', 'margin': '0 auto', 'backgroundColor': '#f8f9fa', 'padding': '20px'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
