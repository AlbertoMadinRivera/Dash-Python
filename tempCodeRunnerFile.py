import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import yfinance as yf
import pandas as pd
from datetime import datetime

# Obtener la fecha actual
current_date = datetime.today().strftime('%Y-%m-%d')

# Obtener datos de Yahoo Finance
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
start_date = '2020-01-01'
end_date = current_date
dfs = {ticker: yf.download(ticker, start=start_date, end=end_date) for ticker in tickers}

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/styles.css'])  # Ruta al archivo CSS

# Estilo CSS personalizado para la tabla
table_style = {
    'width': '100%',
    'border-collapse': 'collapse',
    'border': '1px solid #ddd',
    'font-size': '14px',
    'text-align': 'left',
    'margin-top': '10px',
    'margin-bottom': '10px',
}

# Estilo para las celdas de la tabla
cell_style = {
    'border': '1px solid #ddd',
    'padding': '8px',
}

# Crear dropdown para seleccionar la empresa
dropdown_options = [{'label': ticker, 'value': ticker} for ticker in tickers]
dropdown = dcc.Dropdown(
    id='company-dropdown',
    options=dropdown_options,
    value='AAPL',  # Valor inicial seleccionado
    style={'width': '100%'}
)

app.layout = dbc.Container([
    html.H1("Trading by Alberto Madin Rivera", className='custom-header text-center mb-4'),  # Agregar la clase custom-header aquí
    dbc.Row([
        dbc.Col([
            html.Label('Select Stocks'),
            dropdown
        ], width=3),
        dbc.Col([
            html.Label('Select dates'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=start_date,
                end_date=end_date
            )
        ], width=9)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Current Price", className="card-title"),
                    html.P(id='current-price', className="card-text")
                ], id='current-price-card')
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Change", className="card-title"),
                    html.P(id='price-change', className="card-text")
                ], id='price-change-card')
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Percent Change", className="card-title"),
                    html.P(id='percent-change', className="card-text")
                ], id='percent-change-card')
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='price-history',
                figure={'data': [], 'layout': {}}
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='candlestick-chart',
                figure={'data': [], 'layout': {}}
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Table(id='stock-table', style=table_style)
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Button("Download CSV", id="btn_csv", className="btn btn-primary"),
            dcc.Download(id="download-dataframe-csv")
        ], width=12)
    ])
], fluid=True)

######################################
# Contenido del código Dash para ser mostrado/ocultado
dash_code = """
app.layout = dbc.Container([
    html.H1("Trading by Alberto Madin Rivera", className='custom-header text-center mb-4'),  # Agregar la clase custom-header aquí
    dbc.Row([
        dbc.Col([
            html.Label('Select Stocks'),
            dropdown
        ], width=3),
        dbc.Col([
            html.Label('Select dates'),
            dcc.DatePickerRange(
                id='date-picker-range',
                start_date=start_date,
                end_date=end_date
            )
        ], width=9)
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Current Price", className="card-title"),
                    html.P(id='current-price', className="card-text")
                ], id='current-price-card')
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Change", className="card-title"),
                    html.P(id='price-change', className="card-text")
                ], id='price-change-card')
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Percent Change", className="card-title"),
                    html.P(id='percent-change', className="card-text")
                ], id='percent-change-card')
            ])
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='price-history',
                figure={'data': [], 'layout': {}}
            )
        ], width=6),
        dbc.Col([
            dcc.Graph(
                id='candlestick-chart',
                figure={'data': [], 'layout': {}}
            )
        ], width=6)
    ]),
    dbc.Row([
        dbc.Col([
            html.Table(id='stock-table', style=table_style)
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            html.Button("Download CSV", id="btn_csv", className="btn btn-primary"),
            dcc.Download(id="download-dataframe-csv")
        ], width=12)
    ])
], fluid=True)
"""

# Componente Collapse para mostrar/ocultar el código
collapse = dbc.Collapse(
    dbc.Card(dbc.CardBody(html.Pre(dash_code, style={'overflowX': 'scroll'}))),
    id='collapse-code',
    is_open=False,
)
######################################


@app.callback(
    Output('current-price', 'className'),
    Output('price-change', 'className'),
    Output('percent-change', 'className'),
    Input('company-dropdown', 'value')
)
def update_color(ticker):
    df = dfs[ticker]
    current_price_change = df['Close'][-1] - df['Close'][0]
    percent_change = (df['Close'][-1] - df['Close'][0]) / df['Close'][0] * 100

    current_price_class = 'green-bg' if current_price_change > 0 else 'red-bg'
    price_change_class = 'green-bg' if current_price_change > 0 else 'red-bg'
    percent_change_class = 'green-bg' if percent_change > 0 else 'red-bg'

    return current_price_class, price_change_class, percent_change_class


@app.callback(
    Output('current-price', 'children'),
    Output('price-change', 'children'),
    Output('percent-change', 'children'),
    Input('company-dropdown', 'value')
)
def update_stock_data(ticker):
    df = dfs[ticker]
    current_price = "${:.2f}".format(df['Close'][-1])
    price_change = "${:.2f}".format(df['Close'][-1] - df['Close'][0])
    percent_change = "{:.2f}%".format((df['Close'][-1] - df['Close'][0]) / df['Close'][0] * 100)
    return current_price, price_change, percent_change


@app.callback(
    Output('price-history', 'figure'),
    Output('candlestick-chart', 'figure'),
    Input('company-dropdown', 'value'),
    State('date-picker-range', 'start_date'),
    State('date-picker-range', 'end_date')
)
def update_graphs(ticker, start_date, end_date):
    df = yf.download(ticker, start=start_date, end=end_date)

    price_history_figure = {
        'data': [
            go.Scatter(
                x=df.index,
                y=df['Close'],
                mode='lines',
                name='Price'
            )
        ],
        'layout': go.Layout(
            title='Price history',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price'}
        )
    }

    candlestick_figure = {
        'data': [
            go.Candlestick(
                x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                name='Candlestick'
            )
        ],
        'layout': go.Layout(
            title='Candlestick Chart',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price'}
        )
    }

    return price_history_figure, candlestick_figure


@app.callback(
    Output('stock-table', 'children'),
    Input('company-dropdown', 'value')
)
def update_table(ticker):
    df = dfs[ticker]

    table_content = [
        html.Thead(html.Tr([
            html.Th("Category", style=cell_style),
            html.Th("Value", style=cell_style)
        ]))
    ]

    categories = ['Open', 'High', 'Low', 'Close', 'Volume']
    for category in categories:
        table_content.append(
            html.Tr([
                html.Td(category, style=cell_style),
                html.Td("${:.2f}".format(df[category][-1]), style=cell_style)
            ])
        )

    return table_content


@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    State('company-dropdown', 'value'),
    prevent_initial_call=True,
)
def download_data(n_clicks, ticker):
    df = dfs[ticker]
    return dcc.send_data_frame(df.to_csv, f"{ticker}_stock_data.csv")


if __name__ == '__main__':
    app.run_server(debug=True)