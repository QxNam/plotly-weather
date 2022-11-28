import plotly.express as px
import pandas as pd
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = 'plotly_dark'

app = Dash(external_stylesheets=[dbc.themes.SLATE])

# đọc data
df = pd.read_csv('weather-history.csv', parse_dates =["date"], index_col ="date")
df.fillna(method='bfill', inplace=True)
ele = {'tmin': 'Nhiệt độ thấp nhất', 'tmax': 'Nhiệt độ cao nhất', 'prcp': 'Lượng mưa', 'snwd': 'Lượng tuyết rơi', 'awnd': 'Tốc độ gió trung bình'}

tabs_styles = {
    'height': '35px'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# --------MAIN-----------
app.layout = html.Div([
    html.Div(html.H2(children='Thông tin thời tiết ở sân bay quốc tế Raleigh Durham'), id='topic'),
    html.Div(dcc.Tabs(id="tabs-styled-with-inline", value=1, children=[
        dcc.Tab(label='Dash 1', value=1, style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Dash 2', value=2, style=tab_style, selected_style=tab_selected_style)
    ], style=tabs_styles), id = 'tab'),
    html.Div(id="tabs-content-inline")
])
@app.callback(Output('tabs-content-inline', 'children'),
            Input('tabs-styled-with-inline', 'value'))
def render_content(tab):
    if tab==1:
        return html.Div([
    dbc.Row([
        html.Div(
            dcc.RadioItems(id="val", 
                options = [{"label": "Nhỏ nhất", "value": "min"},
                            {"label": "Lớn nhất", "value": "max"},
                            {"label": "Tổng", "value": "sum"},
                            {"label": "Trung bình", "value": "mean"},
                            {"label": "Trung vị", "value": "median"}],
                            value="sum"),
        id = 'radioItems')
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.P("Lượng mưa", className='title'),
                dcc.Graph(id="prcp_year")
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                html.P("Nhiệt độ", className='title'),
                dcc.Graph(id="hist_temp")
            ])
        ], width=6)
    ], className='row1'),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.P("Tốc độ gió trung bình", className='title'),
                dcc.Graph(id="awnd_year")
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.P("Tuyết rơi và độ dày", className='title'),
                dcc.Graph(id="snow_year")
            ])
        ], width=8)
    ], className='row2')
])
    else:
        return html.Div([
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(id="val", 
                options = [{"label": "Nhỏ nhất", "value": "min"},
                            {"label": "Lớn nhất", "value": "max"},
                            {"label": "Tổng", "value": "sum"},
                            {"label": "Trung bình", "value": "mean"},
                            {"label": "Trung vị", "value": "median"}],
                value="sum")],id = 'radioItems'),
        dbc.Col([
            dcc.Dropdown(id="year", 
            options=[{"label": "2017", "value": 2017},
                        {"label": "2018", "value": 2018},
                        {"label": "2019", "value": 2019},
                        {"label": "2020", "value": 2020},
                        {"label": "2021", "value": 2021},
                        {"label": "2022", "value": 2022}],
            multi=False,
            value=2021)], id = 'radioItems')
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.P("Biểu đồ nhiệt độ", className='title'),
                dcc.Graph(id="temp_month")
            ])
        ], width=6),
        dbc.Col([
            dbc.Card([
                html.P("Biểu đồ lượng mưa", className='title'),
                dcc.Graph(id="prcp_month")
            ])
        ], width=6)
    ], className='row1'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.P("Biểu đồ hộp nhiệt độ", className='title'),
                dcc.Graph(id="temp_box")
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.P("Biểu đồ tốc độ gió", className='title'),
                dcc.Graph(id="wind_month")
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.P("Biểu đồ hộp lượng mưa", className='title'),
                dcc.Graph(id="prcp_box")
            ])
        ], width=4)
    ], className='row2')
])

@app.callback([Output("prcp_year", "figure"),
            Output("hist_temp", "figure"),
            Output("awnd_year", "figure"),
            Output("snow_year", "figure")],
            Input("val", "value"))
def display_graph(val):
    def get_data(val, tp = 'Y'):
        yearly = None
        if val == 'sum':
            yearly = df.resample(tp).sum()
        elif val == 'min': 
            yearly = df.resample(tp).min()
        elif val == 'max':
            yearly = df.resample(tp).max()
        elif val == 'mean': 
            yearly = df.resample(tp).mean()
        else: 
            yearly = df.resample(tp).median()
        return yearly
    yearly = get_data(val)
    # prcp_year
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(y = yearly.index.year, x=yearly.prcp, text = yearly.prcp, textposition='auto', orientation='h'))
    fig1.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5, opacity=0.8)
    fig1.update_layout(
        title={
            'xanchor': 'center',
            'yanchor': 'top'},
        title_font_color="red",
        font_color="yellow",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="gray",
            font_size=16,
            font_family="Rockwell")
    )
    fig1.update_layout(yaxis_title=None, xaxis_title=None, margin={"r": 5, "t": 5, "l": 5, "b": 5}, height=300)
    # hist_temp
    fig2 = go.Figure()
    fig2.add_trace(go.Histogram(x = df['tmin'], name = ele['tmin']))
    fig2.add_trace(go.Histogram(x = df['tmax'], name = ele['tmax']))
    fig2.update_traces(opacity=0.75)
    fig2.update_layout(
        barmode='overlay',
        title_font_color="red",
        font_color="yellow",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="gray",
            font_size=16,
            font_family="Rockwell"),
        showlegend = False
    )
    fig2.update_layout(yaxis_title=None, xaxis_title=None, margin={"r": 5, "t": 5, "l": 5, "b": 5}, height=300)
    # awnd_year
    fig3 = go.Figure(go.Barpolar(
        r=yearly.awnd,
        theta=list(map(lambda x: str(x), yearly.index.year.values)),
        width=[0.8, 0.6, 0.4, 0.5, 0.3, 0.2],
        marker_color=["#4618DF", '#709BFF', '#2AC93A', '#FFAA70', '#D50909', '#FFDF70'],
        marker_line_color="yellow",
        marker_line_width=2,
        opacity=0.8
    ))
    fig3.update_layout(yaxis_title=None, xaxis_title=None, margin={"r": 2, "t": 5, "l": 2, "b": 5})
    # snow_year1
    m = get_data(val, 'M') # m = df.resample('M').sum()
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=m.index, y=m.snow, fill='tozeroy', mode='none',
                            name = 'Lượng tuyết rơi'))
    fig4.add_trace(go.Scatter(x=m.index, y=m.snwd, fill='tozeroy', mode='none',
                            name = 'Độ dày tuyết'))
    fig4.update_layout(
        barmode='overlay',
        title_font_color="red",
        font_color="yellow",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="gray",
            font_size=16,
            font_family="Rockwell"),
        showlegend = False
    )
    fig4.update_layout(yaxis_title=None, xaxis_title=None, margin={"r": 5, "t": 5, "l": 5, "b": 5})
    return fig1, fig2, fig3, fig4

@app.callback([Output("temp_month", "figure"),
               Output("prcp_month", "figure"),
               Output("temp_box", "figure"),
               Output("wind_month", "figure"),
               Output("prcp_box", "figure")],
               [(Input("val", "value")),
               (Input("year", "value"))])
def display_graph(val, year):
    yearly = df[df.index.year == year]
    monthly = None
    if val == 'sum':
        monthly = yearly.resample('M').sum()
    elif val == 'min': 
        monthly = yearly.resample('M').min()
    elif val == 'max':
        monthly = yearly.resample('M').max()
    elif val == 'mean': 
        monthly = yearly.resample('M').mean()
    else: 
        monthly = yearly.resample('M').median()
    
    # temp
    y_m = monthly.tmax.max()
    x_m = monthly.loc[monthly.tmax == y_m].index.month[0]
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=monthly.index.month, y=monthly['tmin'],
        name=ele['tmin'],
        connectgaps=True)
    )

    fig1.add_trace(go.Scatter(x=monthly.index.month, y=monthly['tmax'],
        name=ele['tmax'],
        connectgaps=True,)
    )
    fig1.update_layout(
        barmode='overlay',
        title_font_color="red",
        font_color="yellow",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="gray",
            font_size=16,
            font_family="Rockwell"),
        showlegend = False
    )
    fig1.add_annotation(
            x=x_m,
            y=y_m,
            xref="x",
            yref="y",
            text=f"max: {y_m}",
            showarrow=True,
            font=dict(
                family="Courier New, monospace",
                size=16,
                color="#ffffff"
                ),
            align="center",
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="#00e600",
            ax=20,
            ay=-30,
            bordercolor="#c7c7c7",
            borderwidth=2,
            borderpad=4,
            bgcolor="#ff7f0e",
            opacity=0.8
            )
    fig1.update_layout(yaxis_title=None, xaxis_title=None, margin=dict(l=5, r=5, t=5, b=5), height=300)
    
    # prcp
    fig2 = px.bar(x = monthly.index.month, y=monthly['prcp'],
                text_auto=True,
                labels={
                    "x": "",
                    "y": ""
                    })
    fig2.update_layout(
        barmode='overlay',
        title_font_color="red",
        font_color="yellow",
        showlegend = False,
        plot_bgcolor='black'
    )
    fig2.update_layout(yaxis_title=None, xaxis_title=None, margin=dict(l=5, r=5, t=5, b=5), height=300)

    #box
    fig3 = go.Figure()
    fig3.add_trace(go.Box(
        y=monthly.tmax,
        name='',
        jitter=0.3,
        pointpos=-1.8,
        boxpoints='all',
        marker_color='#66ff33',
        line_color='#ff66cc'
    ))
    fig3.update_layout(yaxis_title=None, xaxis_title=None, margin=dict(l=5, r=5, t=5, b=5))
    #awnd
    fig4 = px.line_polar(monthly, r = 'awnd', theta=list(map(lambda x: str(x), monthly.index.month.values)),
                labels={
                    "awnd": "Tốc độ gió",
                    "theta": "Tháng"},
                line_close=True,
                
                )
    fig4.update_layout(
        barmode='overlay',
        font_color="yellow",
        showlegend = False
    )
    fig4.update_traces(fill='toself')
    fig4.update_traces(mode="markers+lines")

    # box prcp
    fig5 = go.Figure()
    fig5.add_trace(go.Box(
        y=monthly.prcp,
        name='',
        jitter=0.3,
        pointpos=-1.8,
        boxpoints='all',
        marker_color='#66ff33',
        line_color='#ff66cc'
    ))
    fig5.update_layout(yaxis_title=None, xaxis_title=None, margin=dict(l=5, r=5, t=5, b=5))
    return fig1, fig2, fig3, fig4, fig5
if __name__ == '__main__':
    app.run_server(debug = False)

