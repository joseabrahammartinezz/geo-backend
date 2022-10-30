from django.db import models
import datetime
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import geopandas as gpd
import os
import glob
import zipfile
from sqlalchemy import *
from geoalchemy2 import Geometry, WKTElement
from geo.Geoserver import Geoserver
from pathlib import Path

# Initialize the library
#db = Db(dbname='ide_nuevatel', user='postgres', password='postgres', host='10.40.35.101', port='5432')
#geo = Geoserver('http://10.40.35.101:8080/geoserver', username='admin', password='geoserver')
geo = Geoserver('http://3.217.17.20:8080/geoserver', username='admin', password='geoserver')


# Modelo de BD
class AdmMapa(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=1000, blank=True)
    archivo = models.FileField(upload_to = '%Y/%m/%d')
    uploaded_date = models.DateField(default=datetime.date.today, blank=True)

    def __str__(self):
        return self.nombre 

@receiver(post_save, sender=AdmMapa)
def publish_data(sender, instance, created, **kwargs):
    file = instance.archivo.path
    file_format = os.path.basename(file).split('.')[-1]
    file_name = os.path.basename(file).split('.')[0]
    file_path = os.path.dirname(file)
    nombre_capa = instance.nombre
    conn_str = 'postgresql://postgres:acer56xxx@52.86.173.62:5432/ide_prueba'
    #conn_str = 'postgresql://postgres:postgres@52.86.173.62:5432/ide_nuevatel'

    print (file, 'archivo')
    print (file_name)
    print (file_path)

    #extraer zip
    with zipfile.ZipFile(file, 'r') as zip_ref:
        zip_ref.extractall(file_path)

    os.remove (file)

    shp = glob.glob(r'{}/**/*.shp'.format(file_path), recursive=True)[0] # obtener shp
    print('---------------------')
    print (shp, 'shape')
    print('---------------------')
   # from sqlalchemy import create_engine
   # engine = create_engine("postgresql://scott:tiger@localhost:5432/mydatabase")

   
   # gdf = gpd.read_file("C:/viva/pando/PND.shp")
    gdf = gpd.read_file(shp)
    # crs_name = str(gdf.crs.init)
    #print (crs_name, 'crs_name')
   # epsg = int(crs_name.replace('epsg:',''))

    #if epsg is None:
     #   epsg=4326

    epsg=32719
    geom_type = gdf.geom_type[1]
    print('----------GDF--------------')
    print (gdf)
    print('---------------------------')

    engine = create_engine(conn_str) # crea  el SSQL Alchemy engine
    gdf['geom'] = gdf['geometry'].apply (lambda x: WKTElement(x.wkt, srid=epsg))
    gdf.drop('geometry', 1, inplace = True)  #drop  the geometry column (since we already backup this column with geom)
    gdf.to_sql(nombre_capa, engine, 'public', if_exists='replace', 
              index=false, dtype={'geom': Geometry('Geometry', srid=epsg)}) # a postgres

    for f in Path(file_path).glob('*.*'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s: %s" % (f, e.strerror)) #removemos archivos

    #Publicar mapa en geoserver usando geoserer -rest

    # geo.create_featurestore(store_name='nuevatel_postgis', workspace='nuevatel', db='ide_nuevatel', host='10.40.35.101', pg_user='postgres',
    #                     pg_password='postgres', schema='public')
    # geo.publish_featurestore(workspace='nuevatel', store_name='nuevatel_postgis', pg_table=nombre_capa)

    geo.create_featurestore(store_name='BDColcapirhua', workspace='Colcapirhua', db='ide_prueba', host='52.86.173.62', pg_user='postgres',
                        pg_password='acer56xxx', schema='public')
    geo.publish_featurestore(workspace='Colcapirhua', store_name='BDColcapirhua', pg_table=nombre_capa)

    geo.create_outline_featurestyle('estilo1',color='#3579b1', workspace='Colcapirhua')
    #geo.create_catagorized_featurestyle(style_name='categorizado', column_name='RSRP',column_distinct_values=[-120, -110, -105, -100, -94, -86,-80, -50, null],  workspace='nuevatel')
    #geo.create_classified_featurestyle(style_name='clasificado', column_name='SECTOR_ID', column_distinct_values=[1,2,3,4,5,6,7], workspace='nuevatel')
    geo.publish_style(layer_name=nombre_capa, style_name='estilo1', workspace='Colcapirhua')

@receiver(post_delete, sender=AdmMapa)
def delete_data(sender, instance,  **kwargs):
    #db.delete_table(table_name= instance.nombre, schema='public', dbname='ide_nuevatel')
    #hay que ver la opcion de cambiar codigo para borrar tablas
   # geo.delete_layer(instance.nombre,'nuevatel')
    pass
