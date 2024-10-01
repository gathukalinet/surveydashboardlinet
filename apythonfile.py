
import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
df = pd.read_csv("Dataset/intro_bees.csv")
#df = pd.read_csv("https://raw.githubusercontent.com/LubangaD/beesurveydashboard/refs/heads/main/Dataset/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df.head())

#App Layout

app.layout = html.Div([
    html.H1("Bees Survey Dashboard",style={'text-align': 'center'}),
    dcc.Dropdown(id='slct_year',
                 options=[
                    {'label': '2015', 'value':2015},
                    {'label': '2016', 'value':2016},
                    {'label': '2017', 'value':2017},
                    {'label': '2018', 'value':2018},
                    {'label': '2019', 'value':2019}],
                multi=False,
                value=2015,
                style={'width': '40%'}
    ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='my_bee_map', figure={})
    
    ])

#Connect the Plotly graphs with the Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Year"] == option_slctd]
    dff = dff[dff["Affected by"] == "Varroa_mites"]

    # Plotly Express
    fig = px.line(dff, x='Year', y='Pct of Colonies Impacted')
    
    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)