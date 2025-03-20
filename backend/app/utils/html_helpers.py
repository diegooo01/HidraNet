def find_variable_name(html, prefix):
    pattern = f"var {prefix}"
    start_index = html.find(pattern) + 4
    tmp_html = html[start_index:]
    end_index = tmp_html.find(" =") + start_index
    return html[start_index:end_index]


def custom_code(map_variable_name):
    return '''
           var marker;  
           function latLngPop(e) {
               if (marker) {
                   marker.remove(); 
               }
               var lat = e.latlng.lat;
               var lng = e.latlng.lng

               marker = L.marker(
                   [lat, lng],
                   {}
               ).addTo(%s);

               let coordinates = { lat: lat, lng: lng };
               localStorage.setItem('coordinates', JSON.stringify(coordinates));
               console.log('Coordenadas:', coordinates);
           }

    ''' % (map_variable_name)

def inject_button_change_hydrant(polylines):
    options = ""
    for index, polyline in enumerate(polylines):
        options += f'<option value="{index}">ID: {polyline[2]} - {round(polyline[1],2)}m</option>\n'

    return f'''
        <style>
             #polyline-select {{
            position: absolute;
            bottom: 50px;
            right: 10px;  
            z-index: 1000;
            padding: 8px 12px;
            font-size: 14px;
            border-radius: 25px;
            border: 2px solid #4e171c;
            background-color: #4e171c;
            color: white;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            outline: none;
            transition: all 0.3s ease;
        }}

        #polyline-select:hover {{
            background-color: #fdf3f3;
            color: #4e171c;
        }}

        #polyline-select:focus {{
            box-shadow: 0px 0px 8px rgba(78, 23, 28, 0.8);
        }}

        #polyline-select option {{
            background-color: white;
            color: black;
            padding: 5px;
        }}

        #polyline-select option {{
            background-color: white;
            color: black;
            padding: 5px;
        }}
        </style>

       <select id="polyline-select" onchange="togglePolyline(this.value)">
            <option value="" disabled selected>Seleccione un Hidrante</option>
            {options}
        </select>
    '''

def inject_script_to_button_change_hydrant(polylines):
    return f'''
            var currentPolyline = 0;
            var poylines_len = {len(polylines)};
            var polylines = document.getElementsByClassName('leaflet-interactive');

            for (let i = 1; i < poylines_len; i++) {{
                polylines[i].style.display = "none";
            }}

            function togglePolyline(value) {{
                polylines[currentPolyline].style.display = "none";
                currentPolyline = value;
                polylines[value].style.display = "block";
            }}
    '''