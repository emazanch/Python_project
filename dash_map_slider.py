import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv("https://raw.githubusercontent.com/emazanch/Python_project/main/for_appli2.csv")
geodata = {'type':'FeatureCollection', 'features': []}
sources = df.loc[:,["Production éolienne (GWh)", "Production solaire (GWh)", "Vitesse du vent à 100m (m/s)", "Rayonnement solaire global (W/m2)"]]

app.layout = html.Div([
     html.Div([
        dcc.RadioItems(
            id="choice",
            options=[{'label': i, 'value': i} for i in sources],
            value="Production éolienne (GWh)")
    ]),
    dcc.Graph(id ='map-with-slider'),
    dcc.Slider(
            id ='year-slider',
            min = df['Year'].min(), 
            max = df['Year'].max(),
            value = df['Year'].min(),
            marks = {str(year) : str(year) for year in df['Year'].unique()},
            #marks = {str(i):str(j) for i,j in zip(range(len(data['Mois'])), data['Mois'].unique())} #pour ds avec Mois
            step = None
    )
])


@app.callback(
    Output('map-with-slider', 'figure'),
    [Input('choice','value'),
    Input('year-slider', 'value')]
)

def update_figure(input1, input2):
    filtered_df = df[df["Year"] == input2]

    for row in filtered_df.itertuples():
        region_code = row[2]
        coord = eval(row[13])
        temp_d = {}
        temp_d['type'] = 'Feature'
        temp_d['geometry'] = coord
        temp_d['id'] = region_code
        geodata['features'].append(temp_d)

    fig = px.choropleth_mapbox(filtered_df, geojson = geodata, 
                               locations = 'Région', color = filtered_df[input1],
                               color_continuous_scale = "Reds", 
                               #range_color = [filtered_df[input1].min(),filtered_df[input1].max()],
                               mapbox_style = "carto-positron",
                               zoom = 5, center = {"lat": 47, "lon": 1.7},opacity = 0.5)
    fig.update_layout(height=600, margin={"r":0,"t":0,"l":0,"b":0})
       
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
