import sys
import os
from flask import Flask, request,jsonify,send_from_directory
from flask_cors import CORS
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster,Fullscreen
import osmnx as ox
import random
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from backend.app.utils.calculation import calculate_distance
from backend.app.utils.html_helpers import find_variable_name, custom_code, inject_button_change_hydrant, inject_script_to_button_change_hydrant
from backend.app.models.GraphPrim import GraphPrim
from backend.app.models.Hydrant import Hydrant
from backend.app.models.GraphRoutes import GraphRoutes


ox.settings.log_console = False
ox.settings.use_cache = False


app = Flask(__name__ ,static_folder = "../../dist")
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1.0/hydrants_map')
def hydrants_map():
    gdf = gpd.read_file("../data/HIDRANTES_PROVCALLAO.geojson")
    num_hydrants = 1500
    num_hydrants = min(num_hydrants, len(gdf))
    sampled_gdf = gdf.sample(n=num_hydrants, random_state=1)  
    sampled_gdf = sampled_gdf.reset_index(drop=True)
    m = folium.Map(location=[-12.050, -77.120], zoom_start=13)
    marker_cluster = MarkerCluster().add_to(m)
    Fullscreen(position='topright').add_to(m)

    hydrants_cola = []
    graph = GraphPrim(num_hydrants)

    hydrant_icon_url = [
    '../../public/map-icons/hidrant-icon-low-level.png',
    '../../public/map-icons/hidrant-icon-mid-level.png',
    '../../public/map-icons/hidrant-icon-high-level.png',
    ]

    for index, row in sampled_gdf.iterrows():
        lon, lat = row['geometry'].coords[0]
        level = random.randint(0, 2)
        hydrant = Hydrant(level, lon, lat, index)

        icon = folium.CustomIcon(hydrant_icon_url[level], icon_size=(30, 30)) 

        folium.Marker(location=hydrant.getLocation(),
                      tooltip=f'ID {index}',
                      icon=icon).add_to(marker_cluster)

        for other in hydrants_cola:
            if hydrant.isNear(other,600):
                graph.addEdge(index, other.getIndex(), calculate_distance(hydrant.getLocation(), other.getLocation()))

        hydrants_cola.append(hydrant)

    connections,cost = graph.PrimMST()

    for edge in connections:
        u, v, distance = edge
        folium.PolyLine(locations=[hydrants_cola[u].getLocation(), hydrants_cola[v].getLocation()], color='blue', weight=2, opacity=0.5,tooltip=f'{round(distance,2)}').add_to(m)

    map_html = m._repr_html_()

    return jsonify({"map": map_html,
                    "cost": cost})

@app.route('/api/v1.0/nearHydrants_map', methods=['GET'])
def nearHydrants_map():

    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    lvl = request.args.get('level', type=int)

    if lat and lng:
        current_hydrant = Hydrant(None, lng, lat, None)
        routes_to_nearHydrants = []
    else:
        current_hydrant = None

    geojson_url = "../data/HIDRANTES_PROVCALLAO.geojson"
    gdf = gpd.read_file(geojson_url)
    num_hydrants = 1500
    num_hydrants = min(num_hydrants, len(gdf))
    sampled_gdf = gdf.sample(n=num_hydrants, random_state=1) 
    sampled_gdf = sampled_gdf.reset_index(drop=True)
    if(current_hydrant): m = folium.Map(location=current_hydrant.getLocation(), zoom_start=18)
    else: m = folium.Map(location=[-12.050, -77.120], zoom_start=16)
    marker_cluster = MarkerCluster().add_to(m)
    if current_hydrant:
       custom_icon = folium.CustomIcon(icon_image='../../public/map-icons/fire-alert-icon.png', icon_size=(32, 32))
       folium.Marker(
           location=current_hydrant.getLocation(),
           tooltip='Incendio',
           icon=custom_icon
       ).add_to(m)

    Fullscreen(position='topright').add_to(m)


    hydrant_icon_url = [
    '../../public/map-icons/hidrant-icon-low-level.png',
    '../../public/map-icons/hidrant-icon-mid-level.png',
    '../../public/map-icons/hidrant-icon-high-level.png',
    ]

    if current_hydrant:
        G = ox.graph_from_point((current_hydrant.getLocation()[0],current_hydrant.getLocation()[1]), dist=1000, network_type='walk',simplify=False)
        graphTemp = GraphRoutes(G)

    random.seed(45) 

    for index, row in sampled_gdf.iterrows():
        lon, lat = row['geometry'].coords[0]
        level = random.randint(1, 3)
        hydrant = Hydrant(level, lon, lat, index)


        icon = folium.CustomIcon(hydrant_icon_url[level-1], icon_size=(30, 30)) 

        folium.Marker(location=hydrant.getLocation(),
                     tooltip=f'ID: {index}',
                     icon=icon).add_to(marker_cluster)

        if current_hydrant:

            if hydrant.isNear(current_hydrant,300) and hydrant.isLevelRequired(lvl):

                orig_node = ox.distance.nearest_nodes(G, current_hydrant.getLocation()[1],current_hydrant.getLocation()[0])
                dest_node = ox.distance.nearest_nodes(G, hydrant.getLocation()[1], hydrant.getLocation()[0]) 
                route , distance = graphTemp.dijkstra(orig_node, dest_node)
                line = folium.PolyLine(locations=route, color='blue', weight=5, opacity=0.7,tooltip=f"{round(distance,2)} metros")   
                routes_to_nearHydrants.append([line,distance,hydrant.getIndex()])


    if current_hydrant:
        routes_to_nearHydrants.sort(key=lambda x: x[1])
        for route in routes_to_nearHydrants:
            route[0].add_to(m)

    folium.LatLngPopup().add_to(m)
    map_html = m._repr_html_()
    map_variable_name = find_variable_name(map_html, "map_")
    if current_hydrant:
        m.get_root().html.add_child(folium.Element(inject_button_change_hydrant(routes_to_nearHydrants)))
        m.get_root().script.add_child(folium.Element(inject_script_to_button_change_hydrant(routes_to_nearHydrants)))

    m.get_root().script.add_child(folium.Element(custom_code(map_variable_name)))

    map_html = m._repr_html_()

    return map_html



@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')
    
if __name__ == '__main__':
    app.run(debug=True)