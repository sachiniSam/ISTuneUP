import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import numpy as np

from configparser import ConfigParser


from ResultAnalyzer import ResultAnaylzer

external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4',
        'crossorigin': 'anonymous'
    }
]

external_scripts = [
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/solid.js',
        'integrity': 'sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js',
        'integrity': 'sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://code.jquery.com/jquery-3.3.1.slim.min.js',
        'integrity': 'sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js',
        'integrity': 'sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js',
        'integrity': 'sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm',
        'crossorigin': 'anonymous'
    }
]

# initialize an instance of the object resultAnalyzer to get the analysed performancec data
analyzeD = ResultAnaylzer()

app = dash.Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets)

app.config.suppress_callback_exceptions = True




index_page = html.Div([])

app.index_string = '''<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <link rel="stylesheet" href="https://bootstrapious.com/tutorial/sidebar/style.css">
        <link href="assets/dashStylesheet.css" rel="stylesheet">

        
    </head>
    <body>
        <div class="wrapper" >
            <nav id="sidebar" class="navsideBar" style="background: #3b638e;">
                <div class="sidebar-header">
                    <h3>ISTuneUP</h3>
                </div>
                <ul class="list-unstyled components">
                    
                    <li class="active">
                        <li>
                            <a href="/PerfTestPage">Performance Test Results</a>
                        </li>
                        <li>
                            <a href="/setConfigPage">Set configurations</a>
                        </li>
                        <li>
                            <a href="/analysisPage">Performance Analysis</a>
                        </li>
                        
                        
                        

                    </li>
                </ul>
            </nav>
            <div id="content">
                {%app_entry%}
                {%config%}
                {%scripts%}
                {%renderer%}
                
            </div>
            
            <footer>    
            </footer>
        </div>
    </body>
</html>'''
app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

# read data from the result analyzer class
finalResult = analyzeD.importResultData()
configData = analyzeD.importConfigData()
tableData = analyzeD.analyseCategory()

features = finalResult.columns[1:-1]
opts = [{'label' : i.replace('_', ' ').title(), 'value' : i} for i in features]


# Step 3. Create a plotly figure
trace_1 = go.Scatter(x = finalResult['iterations'], y = finalResult[analyzeD.getTargetMetric()],
                    name = '99%',
                    line = dict(width = 2,color = 'rgb(229, 151, 50)'))
layout = go.Layout(title={
        'text': "Performance Optimization Plot",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},hovermode = 'closest',
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number of Iterations',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text=analyzeD.getTargetMetric(),
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
                        )
fig = go.Figure(data = [trace_1], layout = layout)




# Step 4. Create a Dash layout
page_1_layout = html.Div([


                # adding a header and a paragraph
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.Img(src='assets/perficon4.png', id="improveIcon")
                                ],width="2"),
                                dbc.Col([
                                    html.Div([html.H5("Performance Improvement"),
                                    html.H5(str(analyzeD.performanceImprovement()) + "%")
                                    ],className="impro_box_text")
                                    
                                ],width="10")  
                            ],className="impro_box"),
                            dbc.Row([
                                dbc.Col([
                                    html.Img(src='assets/perficon3.png', id="improveIcon")
                                ],width="2"),
                                dbc.Col([
                                    html.Div([
                                    html.H5("Factorial Performance Improvement"),
                                    html.H5(str(analyzeD.improvementByFactor() ) + "x")
                                    ],className="impro_box_text")
                                ],width="10")
                                
                             ],className="impro_box")
                        ],width="5"),

                         dbc.Col([
                             dbc.Row([
                                 #html.H5("Optimum Configuration parameters"),dbc.Button("Set Configurations", outline=True, color="success", className="mr-1",id="btn-collapse"),
                                 dbc.Col([html.H5("Optimum Configuration Parameters")],width="9"),
                                 dbc.Col([ dbc.Button("Set Configurations", outline=True, color="success", className="mr-1",id="btn-collapse", href="/setConfigPage")],width="3")
                             ]),
                            
                         dash_table.DataTable(
                                    id='table',
                                    #columns=[{"name": i, "id": i} for i in rowTrans2.columns],
                                    columns=[{'name': 'parameters', 'id': 'parameters'},
                                    {'name': 'values', 'id': 'values'}],
                                    data=tableData.to_dict('rows')[1:-3],
                                    style_as_list_view=True,
                                    style_cell={'padding': '5px',
                                    'fontFamily': 'Open Sans',
                                    'textAlign': 'center'
                                    },
                                    style_header={
                                        'backgroundColor': 'white',
                                        'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                        {
                                            'textAlign': 'left'
                                        } 
                                    ],
                                    # style data
                                    style_data_conditional=[
                                        {
                                        # stripped rows
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                        }
                
                                    ]
                                ),
                                # html.Div(dbc.Button("Set Configurations", outline=True, color="success", className="mr-1"), id="btn-collapse")ebf7f7
                         ],style = {'padding' : '40px' , 
                             'backgroundColor' : '#e5ecf6', 'margin': '10px',})] ),

                ]),

                #optmized parameters
                 dbc.Row([
                     dbc.Col([ html.Div(
                    [html.H6("99th percentile Decreasement"),html.H6(str(analyzeD.latencyImprovement()) + "%")],className="improvement_box")
                     ]),
                      dbc.Col([
                          html.Div(
                    [html.H6("Throughput Improvement"),html.H6(str(analyzeD.throughputImprovement()) + "%")],className="improvement_box")
                      ]),

                      dbc.Col([
                          html.Div(
                    [html.H6("Average Latency Decreasement"),html.H6(str(analyzeD.averageImprovement()) + "%")],className="improvement_box")
                      ])

                 ]),

                html.Div([
                    dbc.Row([
                        dbc.Col([
                            # adding a plot
                            dcc.Graph(id = 'plot', figure = fig),
                        ], width="10"),
                        dbc.Col([
                            dbc.Row([
                                html.P([
                                html.Label("Choose a feature"),
                                dcc.Dropdown(id = 'opt', 
                                            options = opts,
                                            #value = opts[0]['value']
                                            value = "99%_Line",
                                            clearable=False
                                            )
                                    ], id="sidePanel")
                            ]),
                            dbc.Row([
                                html.Div(
                                    [html.H6("Optimization Type"),
                                    dbc.Badge(configData[configData[0] == 'optimizationType'][1].item() + " objective", color="primary", className="mr-1")],
                                    className="param_box"),
                                html.Div(
                                    [html.H6("Target Metric"),
                                    dbc.Badge(analyzeD.getTargetMetric() , color="primary", className="mr-1")
                                    ],
                                    className="param_box"
                                )
                                ]),
                            dbc.Row([
                                html.Div([html.Div(
                                    dbc.Button(
                                        "Performance Test Configs",
                                        id="collapse-button",
                                        #className="mb-3",
                                        #color="primary",
                                        outline="True",
                                        color="primary",
                                        className="mr-1"
                                    ),id="btn-collapse"
                                )
                                    ,
                                    dbc.Collapse(
                                        dbc.Card(dbc.CardBody([
                                            html.H6("Perf Test time"),
                                            html.H6(configData[configData[0] == 'testTime'][1].item()),
                                            html.H6("Perf Warmup time"),
                                            html.H6(configData[configData[0] == 'warmUpTime'][1].item()),
                                            html.H6("Concurrent Users"),
                                            html.H6(configData[configData[0] == 'testConcurrency'][1].item())
                                        ]
                                            )),
                                        id="collapse",
                                    ),
                                ]
                            )
                            ])
     
                    ],width="2",style = {
                             'backgroundColor' : '#e5ecf6'})
                ])
                ])

                ])              
                
                
# Step 5. Add callback functions
@app.callback(Output('plot', 'figure'),
             [Input('opt', 'value')])

def update_figure(X):
    trace_2 = go.Scatter(x = finalResult['iterations'], y = finalResult[X],
                        name = X,
                        line = dict(width = 2,
                                    color = 'rgb(106, 181, 135)'))
    fig = go.Figure(data = [trace_1,trace_2], layout = layout)
    return fig


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# PAGE2

# Step 2. Import the dataset
#df = pd.read_csv('overallResult2.csv')

#df2 = pd.read_csv('overallResult2.csv')

# Step 3. Create a plotly figure
PG_2_trace_1 = go.Scatter(x = finalResult['iterations'], y = finalResult['Throughput'],
                    name = 'Throughput',
                    line = dict(width = 2,color = 'rgb(229, 151, 50)'))

Pg2layout = go.Layout(title = 'Performance testing plot',hovermode = 'closest',xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number of Iterations',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='y Axis',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ))
pg2fig = go.Figure(data = [PG_2_trace_1], layout = Pg2layout)




# Step 4. Create a Dash layout

features = finalResult.columns[1:-1]
pg2opts = [{'label' : i.replace('_', ' ').title(), 'value' : i} for i in features]


page_2_layout = html.Div([
                
                    dbc.Row([
                     html.H6("Deployed Database Configuration file")],style = {'padding' : '15px' , 
                           'backgroundColor' : '#c2e0ff', 'padding-bottom': '5px'}),
                    dbc.Row([
                        dcc.Input(
                            value="DeployedDatabase/deployedDB.cnf",
                            id="updatedVal",
                            style = { 'padding' : '10px'}
                        ),
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                dbc.Button("Load New File", color="primary", className="mr-1" ,style = {
                                            'margin' : '5px'})
                            ]),
                            # Allow multiple files to be uploaded
                            multiple=False
                        ),
  
                    ],style = {
                           'backgroundColor' : '#c2e0ff','padding' : '5px'}),
                
                dbc.Row([
                    dbc.Col([
                             dbc.Row([
                                 dbc.Col(html.Div([html.H5("Optimum Configuration Parameters")],style = { 'text-align': 'center'})),
                             ]),
                            
                         dash_table.DataTable(
                                    id='table',
                                    #columns=[{"name": i, "id": i} for i in rowTrans2.columns],
                                    columns=[{'name': 'parameters', 'id': 'parameters'},
                                    {'name': 'values', 'id': 'values'}],
                                    data=tableData.to_dict('rows')[1:-3],
                                    style_as_list_view=True,
                                    style_cell={'padding': '5px',
                                    'fontFamily': 'Open Sans',
                                    'textAlign': 'center'
                                    },
                                    style_header={
                                        'backgroundColor': 'white',
                                        'fontWeight': 'bold'
                                    },
                                    style_cell_conditional=[
                                        {
                                            'textAlign': 'left'
                                        } 
                                    ],
                                    # style data
                                    style_data_conditional=[
                                        {
                                        # stripped rows
                                        'if': {'row_index': 'odd'},
                                        'backgroundColor': 'rgb(248, 248, 248)'
                                        }
                
                                    ]
                                ),
                                html.Div(dbc.Button("Set Configurations", color="success", className="mr-1"), id="successBtn"),
                                dbc.Modal(
                                        [
                                            dbc.ModalHeader("Conifguration update Success"),
                                            dbc.ModalBody("This Deployed Db configurations have been updated"),
                                            dbc.ModalFooter(
                                                dbc.Button(
                                                    "Close", id="close-centered", className="ml-auto"
                                                )
                                            ),
                                        ],
                                        id="modal-centered",
                                        centered=True,
                                    ) 
                                
                                
                                
                                

                                # html.Div(dbc.Button("Set Configurations", outline=True, color="success", className="mr-1"), id="btn-collapse")ebf7f7
                         ],style = {'padding' : '40px' , 
                             'backgroundColor' : '#e5ecf6', 'margin': '10px',})
                ])


            
                      ])


newConfFile = "DeployedDatabase/deployedDB.cnf"


@app.callback(dash.dependencies.Output('updatedVal', 'value'),
             [dash.dependencies.Input('upload-data', 'filename')])
def update_output(filename):
        return filename

@app.callback(
    Output("modal-centered", "is_open"),
    [Input("successBtn", "n_clicks"), Input("close-centered", "n_clicks")],
    [State("modal-centered", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    configNewDb = ConfigParser()
    configNewDb.read(newConfFile)
 
    newBufPool = str(tableData.loc[tableData['parameters'] == 'innodb_buffer_pool_size']['values'].item()) + "M"
    newLogS = str(tableData.loc[tableData['parameters'] == 'innodb_log_file_size']['values'].item()) + "M"
    newFlush = str(tableData.loc[tableData['parameters'] == 'innodb_flush_method']['values'].item())
    newCache = str(tableData.loc[tableData['parameters'] == 'thread_cache_size']['values'].item())
    newSleepD = str(tableData.loc[tableData['parameters'] == 'innodb_thread_sleep_delay']['values'].item())
    newConnec = str(tableData.loc[tableData['parameters'] == 'max_connections']['values'].item())

    configNewDb.set('mysql', 'innodb_buffer_pool_size', value=newBufPool)
    configNewDb.set('mysql', 'innodb_log_file_size', value=newLogS)
    configNewDb.set('mysql', 'innodb_flush_method', value=newFlush)
    configNewDb.set('mysql', 'thread_cache_size', value=newCache)
    configNewDb.set('mysql', 'innodb_thread_sleep_delay', value=newSleepD)
    configNewDb.set('mysql', 'max_connections', value=newConnec)


    with open(newConfFile, 'w') as newConfigfile:
        configNewDb.write(newConfigfile)
    

    if n1 or n2:
        return not is_open
    return is_open
    

    


####################################################PAGE 3 - Performance Analysis#############################################

# read data from the result analyzer class

# OIDC 10 Workload
finalResult1 = pd.read_csv('./AnalysisData/idleBayeoidc10.csv')

featureResult1 = finalResult1.columns[1:-1]
optResult1 = [{'label' : i.replace('_', ' ').title(), 'value' : i} for i in featureResult1]


traceR1 = go.Scatter(x = finalResult1['iterations'], y = finalResult1['99%_Line'],
                    name = '99th Percentile',
                    line = dict(width = 2,color = 'rgb(229, 151, 50)'))

layoutR1 = go.Layout(title={
        'text': "Performance Optimization Plot for OIDC workload",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},hovermode = 'closest',
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number of Iterations',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text='99th Percentile',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ))

figR1 = go.Figure(data = [traceR1], layout = layoutR1)

#SAML 10 workload

# read data from the result analyzer class
finalResult2 = pd.read_csv('./AnalysisData/idleBayesaml10.csv')

featureResult2 = finalResult2.columns[1:-1]
optResult2 = [{'label' : i.replace('_', ' ').title(), 'value' : i} for i in featureResult2]


traceR2 = go.Scatter(x = finalResult2['iterations'], y = finalResult2['99%_Line'],
                    name = '99%',
                    line = dict(width = 2,color = 'rgb(229, 151, 50)'))
layoutR2 = go.Layout(title={
        'text': "Performance Optimization Plot for SAML2 workload",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},hovermode = 'closest',
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number of Iterations',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text=analyzeD.getTargetMetric(),
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
                        )
figR2 = go.Figure(data = [traceR2], layout = layoutR2)


# OIDC 50 workload 


# read data from the result analyzer class
finalResult3 = pd.read_csv('./AnalysisData/idleBayeoidc50.csv')

featureResult3 = finalResult3.columns[1:-1]
optResult3 = [{'label' : i.replace('_', ' ').title(), 'value' : i} for i in featureResult2]


traceR3 = go.Scatter(x = finalResult3['iterations'], y = finalResult3['99%_Line'],
                    name = '99%',
                    line = dict(width = 2,color = 'rgb(229, 151, 50)'))
layoutR3 = go.Layout(title={
        'text': "Performance Optimization Plot for OIDC workload",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},hovermode = 'closest',
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number of Iterations',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text=analyzeD.getTargetMetric(),
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
                        )
figR3 = go.Figure(data = [traceR3], layout = layoutR3)


# OAuth 50 workload

# read data from the result analyzer class
finalResult4 = pd.read_csv('./AnalysisData/idleBayeOauth50.csv')

featureResult4 = finalResult4.columns[1:-1]
optResult4 = [{'label' : i.replace('_', ' ').title(), 'value' : i} for i in featureResult4]


traceR4 = go.Scatter(x = finalResult4['iterations'], y = finalResult4['99%_Line'],
                    name = '99%',
                    line = dict(width = 2,color = 'rgb(229, 151, 50)'))
layoutR4 = go.Layout(title={
        'text': "Performance Optimization Plot for OAuth workload",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},hovermode = 'closest',
    xaxis=go.layout.XAxis(
        title=go.layout.xaxis.Title(
            text='Number of Iterations',
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    ),
    yaxis=go.layout.YAxis(
        title=go.layout.yaxis.Title(
            text=analyzeD.getTargetMetric(),
            font=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
                        )
figR4 = go.Figure(data = [traceR4], layout = layoutR4)

############HORIZONTAL GRAPHS############################

# fig1 Bar
figHR1 = go.Figure(go.Bar(
            x=[20.31,40.64,25.72],
            y=['Average Decreasement', '99% Decreasement', 'Throughput Improvement'],
            orientation='h',
             marker=dict(
                color='rgb(59,99,141)',
            )   
            ))

#fig2 Bar
figHR2 = go.Figure(go.Bar(
            x=[33.4,33.96,51.63],
            y=['Average Decreasement', '99% Decreasement', 'Throughput Improvement'],
            orientation='h',
             marker=dict(
                color='rgb(59,99,141)',
            )   
            ))

#fig3 Bar
figHR3 = go.Figure(go.Bar(
            x=[53.26,55.52,116.6],
            y=['Average Decreasement', '99% Decreasement', 'Throughput Improvement'],
            orientation='h',
             marker=dict(
                color='rgb(59,99,141)',
            )   
            ))

#fig4 Bar
figHR4 = go.Figure(go.Bar(
            x=[41.65,40.54,42.4],
            y=['Average Decreasement', '99% Decreasement', 'Throughput Improvement'],
            orientation='h',
             marker=dict(
                color='rgb(59,99,141)',
            )   
            ))



############# page 3 layout
page_3_layout = html.Div([
    html.Div([
                    dbc.Row([
                        dbc.Col([
                            # adding a plot
                            dcc.Graph(id = 'plot2', figure = figR1),
                        ], width="8"),
                        dbc.Col([
                            html.Div([html.H6("Performance Improvement"),html.H6("1.68X")],
                                                className="param_box_analysis"),
                            dcc.Graph(id = 'plot2a', figure = figHR1,
                            style={
                            'height': 370
                            })], width="4")
                        
                    ]),

                    #SECOND GRAPH
                    dbc.Row([
                        dbc.Col([
                            # adding a plot
                            dcc.Graph(id = 'plot3', figure = figR2),
                        ], width="8"),
                        dbc.Col([
                         html.Div([html.H6("Performance Improvement"),html.H6("1.51X")],
                                                className="param_box_analysis"),
                            dcc.Graph(id = 'plot2a', figure = figHR2,
                            style={
                            'height': 370
                            })], width="4")
                    ]),


                    #GRAPH 3

                    dbc.Row([
                        dbc.Col([
                            # adding a plot
                            dcc.Graph(id = 'plot4', figure = figR3),
                        ], width="8"),
                        dbc.Col([
                            html.Div([html.H6("Performance Improvement"),html.H6("2.24X")],
                                                className="param_box_analysis"),
                            dcc.Graph(id = 'plot2a', figure = figHR3,
                            style={
                            'height': 370
                            })], width="4")
                    ]),

                    #Graph 4
                     dbc.Row([
                        dbc.Col([
                            # adding a plot
                            dcc.Graph(id = 'plot5', figure = figR4),
                        ], width="8"),
                        dbc.Col([
                            html.Div([html.H6("Performance Improvement"),html.H6("1.68X")],
                                                className="param_box_analysis"),
                            dcc.Graph(id = 'plot2a', figure = figHR4,
                            style={
                            'height': 370
                            })], width="4")
                    ]),


            ])
])









# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/PerfTestPage':
        return page_1_layout
    elif pathname == '/setConfigPage':
        return page_2_layout
    elif pathname == '/analysisPage':
        return page_3_layout
    else:
        return page_1_layout




if __name__ == '__main__':
    app.run_server(debug=True)