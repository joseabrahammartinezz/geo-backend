# Import the library
from geo.Geoserver import Geoserver

# Initialize the library
geo = Geoserver('http://3.217.17.20:8080/geoserver', username='admin', password='geoserver')

# For creating workspace
#geo.create_workspace(workspace='demo')

# For uploading raster data to the geoserver
#geo.create_coveragestore(layer_name='layer1', path=r'path\to\raster\file.tif', workspace='demo')

# For creating postGIS connection and publish postGIS table

##### funciona!!!!
# geo.create_featurestore(store_name='BDColcapirhua', workspace='Colcapirhua', 
#                         db='ide_prueba', host='52.86.173.62',
#                         pg_user='postgres',pg_password='acer56xxx')

# geo.publish_featurestore(workspace='Colcapirhua', store_name='BDColcapirhua', pg_table='manzanos')

# For uploading SLD file and connect it with layer
# geo.upload_style(path=r'D:\geoserver-rest\data\estilos\manzanos.sld', workspace='Colcapirhua') 
# geo.publish_style(layer_name='manzanos', style_name='manzanos', workspace='Colcapirhua')

#geo.create_outline_featurestyle(style_name='poligono', workspace='Colcapirhua')
#geo.publish_style(layer_name='manzanos', style_name='poligono', workspace='Colcapirhua')