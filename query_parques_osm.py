import pandana as pdna
from OSMPythonTools.overpass import overpassQueryBuilder, Overpass
from OSMPythonTools.nominatim import Nominatim
from shapely.geometry import Polygon
import pandas as pd
import geopandas as gpd


def create_poly(g):
    return Polygon([(d['lon'], d['lat']) for d in g])


def parse_element_poly(element):
    df = pd.DataFrame({
        'id': element['id'],
        'geometry': create_poly(element['geometry'])
    }, index=[0])
    return df


def parse_element_csv(element):
    df = pd.DataFrame({'nodes': [node for node in element['nodes']],
                       'x': [e['lon'] for e in element['geometry']],
                       'y': [e['lat'] for e in element['geometry']]
                       })
    df['id'] = element['id']
    return df


def query_osm_area(string):
    nominatim = Nominatim()
    areaId = nominatim.query(string).areaId()
    overpass = Overpass()
    query = overpassQueryBuilder(area=areaId, elementType='way',
                                 selector='"leisure"="park"', out='geom')
    result = overpass.query(query)
    return result


def osm_result_to_gdf(result):
    parks = pd.concat([parse_element_poly(element)
                       for element in result.toJSON()['elements']])
    parks = gpd.GeoDataFrame(parks, geometry=parks.geometry, crs='EPSG:4326')
    return parks


def osm_result_to_csv(result):
    parks = pd.concat([parse_element_csv(element)
                       for element in result.toJSON()['elements']])
    parks = parks.reset_index(drop=True)
    return parks


def osm_parks(string, polygon_out=True):
    result = query_osm_area(string)
    if polygon_out:
        parks = osm_result_to_gdf(result)
    else:
        parks = osm_result_to_csv(result)
    return parks


partidos = pd.read_csv('data/partidos.csv', sep=';')

parks_poly = gpd.GeoDataFrame()
parks_csv = pd.DataFrame()

for i, (nominatim, nombre) in partidos.iterrows():
    # obtener parques con polygonos y nodos
    gdf = osm_parks(nominatim)
    df = osm_parks(nominatim, polygon_out=False)

    # asignar nombre del partido
    gdf['nombre'] = nombre
    df['nombre'] = nombre

    # calcular area
    gdf['area'] = gdf.geometry.to_crs('EPSG:3857').area
    df = df.merge(gdf.reindex(columns=['id', 'area']), on='id', how='left')

    # appenderar
    parks_poly = parks_poly.append(gdf)
    parks_csv = parks_csv.append(df)


parks_poly.to_file('carto/parks_poly.geojson', driver='GeoJSON')
parks_csv.to_csv('carto/parks_point.csv', index=False)
