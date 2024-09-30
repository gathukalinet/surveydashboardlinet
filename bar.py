#importing the necessary libraries
import pandas as pd
import plotly.express as px  
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output 
app = Dash(__name__)

# Import and clean data 
df = pd.read_csv("Dataset/intro_bees.csv")

# Grouping the features by the mean of percentages of colonies impacted
df = df.groupby(['State', 'ANSI', 'Year', 'state_code', 'Affected by','Period'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

print(df.head())



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Bees Survey Dashboard", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_period",
                 options=[
                     {'label': 'Jan-Mar', 'value':'JAN THRU MAR'},
                    {'label': 'Apr-Jun', 'value':'APR THRU JUN'},
                    {'label': 'Jul-Sep', 'value':'JUL THRU SEP'},
                    {'label': 'Oct-Dec', 'value':'OCT THRU DEC'}],
                 multi=False,
                 value='JAN THRU MAR',
                 style={'width': "50%"}
                 ),
  
    html.Div(id='output_container', children=[]),
    html.Br(),
    dcc.Graph(id='period_analysis', figure={})

])


# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='period_analysis', component_property='figure')],
    [Input(component_id='slct_period', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The period chosen by user was: {}".format(option_slctd)


    dff = df.copy()
    dff = dff[dff["Period"] == option_slctd]
    dff = dff[dff["Affected by"] == "Pests_excl_Varroa"]


      # Plotly Express
    fig = px.bar(dff, x='State', y='Pct of Colonies Impacted'
    )
    
    
    return container, fig


# # ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)