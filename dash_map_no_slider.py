import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data = pd.read_csv("D:/Work/PythonWorkshop/Project/for_appli_fix.csv")
geodata = {'type':'FeatureCollection', 'features': []}

data = data.loc[data["Mois"] == '2020-12']

for row in data.itertuples():
    region_code = row[2]
    coord = eval(row[3])
    temp_d = {}
    temp_d['type'] = 'Feature'
    temp_d['geometry'] = coord
    temp_d['id'] = region_code
    geodata['features'].append(temp_d)
    
fig1 = px.choropleth_mapbox(data, geojson = geodata, 
                           locations = 'Région', color = 'Production éolienne (GWh)',
                           color_continuous_scale = "Aggrnyl", 
                           mapbox_style = "carto-positron",
                           zoom = 5, center = {"lat": 47, "lon": 1.7},opacity = 0.5,
                           labels = {'Production éolienne (GWh)'})
fig1.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})

fig2 = px.choropleth_mapbox(data, geojson = geodata, 
                           locations = 'Région', color = 'Production solaire (GWh)',
                           color_continuous_scale = "Reds", 
                           mapbox_style = "carto-positron",
                           zoom = 5, center = {"lat": 47, "lon": 1.7},opacity = 0.5,
                           labels = {'Production solaire'})
fig2.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})

fig3 = px.choropleth_mapbox(data, geojson = geodata, 
                           locations = 'Région', color = 'Vitesse du vent à 100m (m/s)',
                           color_continuous_scale = "Aggrnyl", 
                           mapbox_style = "carto-positron",
                           zoom = 5, center = {"lat": 47, "lon": 1.7},opacity = 0.5,
                           labels = {'Vitesse du vent à 100m (m/s)'})
fig3.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})

fig4 = px.choropleth_mapbox(data, geojson = geodata, 
                           locations = 'Région', color = 'Rayonnement solaire global (W/m2)',
                           color_continuous_scale = "Reds", 
                           mapbox_style = "carto-positron",
                           zoom = 5, center = {"lat": 47, "lon": 1.7},opacity = 0.5,
                           labels = {'Rayonnement solaire global (W/m2)'})
fig4.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})

app.layout = html.Div(
    children=[
        html.H3(
            id="title",
            children='Data for 2020-12:'),
        dcc.RadioItems(
            id="choice",
            options=[
                {'label': 'Production éolienne', 'value': 1},
                {'label': 'Production solaire', 'value': 2},
                {'label': 'Vitesse du vent à 100m (m/s)', 'value': 3},
                {'label': 'Rayonnement solaire global', 'value': 4}
            ], value=1
        ),
        dcc.Graph(
            id='graph',
            figure=fig1,
        )
         
])

@app.callback(
    Output('graph','figure'),
    Input('choice','value')

)
def update_graph(choice_value):
    if choice_value == 1:
        updated_fig = fig1
    elif choice_value == 2:
        updated_fig = fig2
    elif choice_value == 3:
        updated_fig = fig3
    elif choice_value == 4:
        updated_fig = fig4

    return updated_fig

if __name__ == '__main__':
    app.run_server(debug=True)