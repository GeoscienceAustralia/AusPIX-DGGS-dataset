from flask import Blueprint, request, Response, render_template
from auspixDGGS.model.dggs_data import DGGS_data
import os
from auspixDGGS._conf import APP_DIR
import folium
print(__name__)
routes = Blueprint('controller', __name__)

DEFAULT_ITEMS_PER_PAGE=150


@routes.route('/', strict_slashes=True)
def home():
    return render_template('/home.html')


@routes.route('/index.ttl', strict_slashes=True)
def dataset_ttl():
    file = 'auspix.ttl'
    ttl_txt = open(os.path.join(APP_DIR, 'view', file), 'rb').read().decode('utf-8')
    return Response(ttl_txt, mimetype='text/turtle')


@routes.route('/collections/auspix/')
def ausPIX():
    search_string = request.values.get('search')
    return render_template('ausPIX.html',
                           search_query=search_string,
                           search_enabled=True
                           )

@routes.route('/collections/auspix/items/<string:auspix_cell_id>')
def auspix_cell(auspix_cell_id):
    auspix_cell = DGGS_data(request, request.base_url)
    return auspix_cell.render()


@routes.route('/map')
def show_map():
    '''
    Function to render a map around the specified coordinates
    '''

    auspix='Cell nucleus on ellipsoid'

    corners = (request.values.get('location')).split('),')

    #corners is straight from database via auspix_location.py and auspix_location.html
    # convert the corner information  into a list for the leaflet map
    longLatsList = list()
    for thing in corners:
        thing = thing.replace("{", "")
        thing = thing.replace("}", "")
        thing = thing.replace("[", "")
        thing = thing.replace("]", "")
        thing = thing.replace("(", "")
        thing = thing.replace(")", "")
        split_thing = thing.split(',')
        # needs latitude first
        latLongs = [split_thing[1], split_thing[0]]
        coords = list()
        # convert to floats
        for item in latLongs:
            coords.append(float(item))
        longLatsList.append(coords)

    x = float(request.values.get('x'))
    y = float(request.values.get('y'))
    # algorithm designed to make it map properly . . .
    min_long = min(longLatsList[0][1], longLatsList[1][1], longLatsList[2][1], longLatsList[3][1])
    max_long = max(longLatsList[0][1], longLatsList[1][1], longLatsList[2][1], longLatsList[3][1])

    print()

    if (max_long - min_long) > 120:
        print('warning', (max_long - min_long))

        # fix to suit leaflet
        # find the one that is wrong
        print('minLong', min_long, 'maxlong', max_long)
        ll_list = list()
        for item in longLatsList:
            print(item[1])
            if abs(item[1] - x)> 90:  # find any that are more than 180 from centroid x
                gap = (item[1] - x)
                print('a large gap is', gap)
                if gap < 0: #ie when gap is negative
                    myItem = float(item[1]) + 360  # make come closer to x, the centroid
                else:# when gap is positive
                    myItem = float(item[1]) - 360  # make come closer to x, the centroid

                print('360 transform is', myItem)
                ll_list.append((item[0], myItem))
            else:
                ll_list.append(item)
        longLatsList = ll_list

    # create a new map object
    tooltip = 'Click for more information'
    folium_map = folium.Map(location=[y, x], zoom_start=7)
    # create markers
    folium.Marker([y, x],
        popup = auspix,
        tooltip=tooltip).add_to(folium_map)

    # create polygon
    folium.vector_layers.Polygon(locations=longLatsList,
                                 popup=auspix,
                                 tooltip='tooltip',
                                 ).add_to(folium_map)
    folium.vector_layers.path_options(line=True,
                                      radius=5,
                                      color='#FF6347')

    return folium_map.get_root().render()

