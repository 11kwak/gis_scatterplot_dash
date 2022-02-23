import pandas as pd
import numpy as np
import dash                     #(version 1.0.0)
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.offline as py     #(version 4.4.1)
import plotly.graph_objs as go

# app initialize
app = dash.Dash(__name__)

# mapbox_access_token = 'insert_your_mapbox_token_here'
mapbox_access_token = " "

# blackbold
blackbold={'color':'black', 'font-weight': 'bold'}

#load data
df = pd.read_csv("./data/data.csv",encoding="cp949")

app.layout = html.Div([
#---------------------------------------------------------------
# Map_legen + Borough_checklist + Recycling_type_checklist + Web_link + Map
    html.Div([
        html.Div([
            # Map-legend
            html.Ul([
                html.Li("2종-내진설계 미적용", className='circle', style={'background': '#f54242','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),  # red 2종-내진설계미적용
                html.Li("1종-내진설계 미적용", className='circle', style={'background': '#f542a7','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}), # pink
                html.Li("2종-내진설계 적용", className='circle', style={'background': '#2500f5','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}),  #blue
                html.Li("1종-내진설계 적용", className='circle', style={'background': '#009bf5','color':'black',
                    'list-style':'none','text-indent': '17px','white-space':'nowrap'}), #하늘색 
               
            ], style={'border-bottom': 'solid 3px', 'border-color':'#00FC87','padding-top': '6px'}
            ),

            # Borough_checklist
            html.Label(children=['광역시: '], style=blackbold),
            dcc.Checklist(id='boro_name',
                    options=[{'label':str(b),'value':b} for b in sorted(df['광역시'].unique())],
                    value=[b for b in sorted(df['광역시'].unique())],
            ),

            # Recycling_type_checklist
            html.Label(children=['교량타입: '], style=blackbold),
            dcc.Checklist(id='recycling_type',
                    options=[{'label':str(b),'value':b} for b in sorted(df['교량타입'].unique())],
                    value=[b for b in sorted(df['교량타입'].unique())],
            ),

            # Web_link
            html.Br(),
            html.Label(['시설물명:'],style=blackbold),
            html.Pre(id='web_link', children=[],
            style={'white-space': 'pre-wrap','word-break': 'break-all',
                 'border': '1px solid black','text-align': 'center',
                 'padding': '12px 12px 12px 12px', 'color':'blue',
                 'margin-top': '3px'}
            ),

        ], className='three columns'
        ),

        # Map
        html.Div([
            dcc.Graph(id='graph', config={'displayModeBar': False, 'scrollZoom': True},
                style={'background':'#00FC87','padding-bottom':'2px','padding-left':'2px','height':'100vh'}
            )
        ], className='nine columns'
        ),

    ], className='row'
    ),

], className='ten columns offset-by-one'
)

#---------------------------------------------------------------
# Output of Graph
@app.callback(Output('graph', 'figure'),
              [Input('boro_name', 'value'),
               Input('recycling_type', 'value')])

def update_figure(chosen_boro,chosen_recycling):
    df_sub = df[(df['광역시'].isin(chosen_boro)) &
                (df['교량타입'].isin(chosen_recycling))]

    # Create figure
    locations=[go.Scattermapbox(
                    lon = df_sub['경도'],
                    lat = df_sub['위도'],
                    mode='markers',
                    marker={'color' : df_sub['색깔']},
                    unselected={'marker' : {'opacity':1}},
                    selected={'marker' : {'opacity':0.5, 'size':25}},
                    hoverinfo='text',
                    hovertext=df_sub['교량정보'],
                    customdata=df_sub['시설물명']
    )]

    # Return figure
    return {
        'data': locations,
        'layout': go.Layout(
            uirevision= 'foo', #preserves state of figure/map after callback activated
            clickmode= 'event+select',
            hovermode='closest',
            hoverdistance=2,
            title=dict(text="scatterplot dash 탬플릿입니다.",font=dict(size=50, color='green')),
            mapbox=dict(
                accesstoken=mapbox_access_token,
                bearing=25,
                style='light',
                center=dict(
                    lat=36.50410,
                    lon=127.26766
                ),
                pitch=40,
                zoom=6.5
            ),
        )
    }
#---------------------------------------------------------------
# callback for Web_link
@app.callback(
    Output('web_link', 'children'),
    [Input('graph', 'clickData')])
def display_click_data(clickData):
    if clickData is None:
        return '시설물을 클릭하세요.'
    else:
        # print (clickData)
        the_link=clickData['points'][0]['customdata']
        if the_link is None:
            return '시설물명이 존재하지 않습니다.'
        else:
            return html.A(the_link, href=the_link, target="_blank")
# #--------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=False)
