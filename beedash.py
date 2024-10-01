import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

# ------------------------------------------------------------------------------

# Import and clean data (importing CSV into pandas)
#df = pd.read_csv("Dataset/intro_bees.csv")
df = pd.read_csv("Dataset/intro_bees.csv")
df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)

bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]
years = [2015, 2016, 2017, 2018, 2019]

# ------------------------------------------------------------------------------

# App layout
app.layout = html.Div([

    html.H1("Bee Colonies Impact Dashboard", style={'text-align': 'center'}),

    # Dropdowns for both the bee-killer and year
    html.Div([
        html.Div([
            dcc.Dropdown(id="slct_impact",
                         options=[{"label": x, "value": x} for x in bee_killers],
                         value="Other",
                         multi=False,
                         style={'width': "90%"}),
            html.Br(),
            html.Div(id='output_container_impact', children=[]),
        ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
        
        html.Div([
            dcc.Dropdown(id="slct_year",
                         options=[{"label": str(x), "value": x} for x in years],
                         value=2015,
                         multi=False,
                         style={'width': "90%"}),
            html.Br(),
            html.Div(id='output_container_year', children=[]),
        ], style={'width': '45%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ]),

    html.Br(),

    # Line and Bar Plots displayed side by side
    html.Div([
        html.Div([
            dcc.Graph(id='bee_line_plot', figure={})
        ], style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(id='bee_bar_plot', figure={})
        ], style={'width': '49%', 'display': 'inline-block'})
    ]),

    html.Div([
        dcc.Graph(id='bee_choropleth', figure={})
    ], style={'width': '100%', 'display': 'inline-block', 'padding': '10px'})

])

# ------------------------------------------------------------------------------

# Callback function to update all three plots
@app.callback(
    [Output(component_id='output_container_impact', component_property='children'),
     Output(component_id='output_container_year', component_property='children'),
     Output(component_id='bee_line_plot', component_property='figure'),
     Output(component_id='bee_bar_plot', component_property='figure'),
     Output(component_id='bee_choropleth', component_property='figure')],
    [Input(component_id='slct_impact', component_property='value'),
     Input(component_id='slct_year', component_property='value')]
)
def update_graph(option_slctd_impact, option_slctd_year):

    # Output text for selected dropdowns
    container_impact = f"The bee-killer chosen by the user was: {option_slctd_impact}"
    container_year = f"The year chosen by the user was: {option_slctd_year}"

    # Filter dataframe based on dropdown selections
    dff = df.copy()

    # Line Plot Data - Impact on Colonies over the years for selected bee-killer
    dff_line = dff[dff["Affected by"] == option_slctd_impact]
    dff_line = dff_line[dff_line["State"].isin(["Idaho", "New York", "New Mexico"])]
    fig_line = px.line(
        data_frame=dff_line,
        x='Year',
        y='Pct of Colonies Impacted',
        color='State',
        template='plotly_dark'
    )

    # Bar Plot Data - Bee colony impact for selected year and Varroa mites
    dff_bar = dff[(dff["Year"] == option_slctd_year) & (dff["Affected by"] == "Varroa_mites")]
    fig_bar = px.bar(
        data_frame=dff_bar,
        x='State',
        y='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )

    # Choropleth Data - Bee colony impact across states for selected year and Varroa mites
    dff_choropleth = dff[(dff["Year"] == option_slctd_year) & (dff["Affected by"] == "Varroa_mites")]
    fig_choropleth = px.choropleth(
        data_frame=dff_choropleth,
        locationmode='USA-states',
        locations='state_code',
        scope="usa",
        color='Pct of Colonies Impacted',
        hover_data=['State', 'Pct of Colonies Impacted'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Pct of Colonies Impacted': '% of Bee Colonies'},
        template='plotly_dark'
    )
    return container_impact, container_year, fig_line, fig_bar, fig_choropleth

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
