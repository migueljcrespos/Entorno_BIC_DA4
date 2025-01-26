# Importar modulo de geoprocesado de QGIS
import processing

# Definir capas de entrada y superposicion.
BienesDA = QgsProject.instance().mapLayersByName('Bienes')[0]
SueloUrbano = QgsProject.instance().mapLayersByName('SueloUrbano')[0]
SueloUrbanizable = QgsProject.instance().mapLayersByName('SueloUrbanizable')[0]
SueloRustico = QgsProject.instance().mapLayersByName('SueloRustico')[0]

# Geoproceso Buffer. Crear un buffer de 50 m, geometría completa.
# Definición de los parametros del geoproceso
Buffer50Solido_parametros={'INPUT':BienesDA,'DISTANCE':50,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'SEPARATE_DISJOINT':False,'OUTPUT':'memory:'}
# Ejecutar este geoproceso
Buffer50Solido_resultado= processing.run('native:buffer', Buffer50Solido_parametros)
# Obtención de la capa temporal resultante
Buffer50Solido= Buffer50Solido_resultado['OUTPUT']

# Geoproceso Buffer. Crear un buffer de 200 m, geometría completa.
Buffer200Solido_parametros= {'INPUT':BienesDA,'DISTANCE':200,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'SEPARATE_DISJOINT':False,'OUTPUT':'memory:'}
# Ejecutar este geoproceso
Buffer200Solido_resultado= processing.run('native:buffer', Buffer200Solido_parametros)
# Obtención de la capa temporal resultante
Buffer200Solido= Buffer200Solido_resultado['OUTPUT']

# Geoproceso Diferencia Simetrica. Crear un buffer de 50 m eliminando el perímetro de los Bienes Culturales.
Buffer50Anillo_parametros= {'INPUT':Buffer50Solido,'OVERLAY':BienesDA,'OVERLAY_FIELDS_PREFIX':'','OUTPUT':'memory:','GRID_SIZE':None}
# Ejecutar este geoproceso
Buffer50Anillo_resultado= processing.run('native:symmetricaldifference', Buffer50Anillo_parametros)
# Obtención de la capa temporal resultante
Buffer50Anillo= Buffer50Anillo_resultado['OUTPUT']

# Geoproceso Diferencia Simetrica. Crear un buffer de 200 m eliminando el perímetro de los Bienes Culturales.
Buffer200Anillo_parametros= {'INPUT':Buffer200Solido,'OVERLAY':BienesDA,'OVERLAY_FIELDS_PREFIX':'','OUTPUT':'memory:','GRID_SIZE':None}
# Ejecutar este geoproceso
Buffer200Anillo_resultado= processing.run('native:symmetricaldifference', Buffer200Anillo_parametros)
# Obtención de la capa temporal resultante
Buffer200Anillo= Buffer200Anillo_resultado['OUTPUT']

# Geoproceso Cortar. Crear un Entorno de 50 m en Suelo Urbano.
Entorno50Urbano_parametros= {'INPUT':Buffer50Anillo,'OVERLAY':SueloUrbano,'OUTPUT':'memory:'}
# Ejecutar este geoproceso
Entorno50Urbano_resultado= processing.run('native:clip', Entorno50Urbano_parametros)
# Obtención de la capa temporal resultante
Entorno50Urbano= Entorno50Urbano_resultado['OUTPUT']

# Geoproceso Cortar. Crear un Entorno de 50 m en Suelo Urbanizable.
Entorno50Urbanizable_parametros= {'INPUT':Buffer50Anillo,'OVERLAY':SueloUrbanizable,'OUTPUT':'memory:'}
# Ejecutar este geoproceso
Entorno50Urbanizable_resultado= processing.run('native:clip', Entorno50Urbanizable_parametros)
# Obtención de la capa temporal resultante
Entorno50Urbanizable= Entorno50Urbanizable_resultado['OUTPUT']

# Geoproceso Cortar. Crear un Entorno de 200 m en Suelo Urbanizable.
Entorno200Urbanizable_parametros= {'INPUT':Buffer200Anillo,'OVERLAY':SueloUrbanizable,'OUTPUT':'memory:'}
# Ejecutar este geoproceso
Entorno200Urbanizable_resultado= processing.run('native:clip', Entorno200Urbanizable_parametros)
# Obtención de la capa temporal resultante
Entorno200Urbanizable= Entorno200Urbanizable_resultado['OUTPUT']

# Geoproceso Cortar. Crear un Entorno de 200 m en Suelo Rústico.
Entorno200Rustico_parametros= {'INPUT':Buffer200Anillo,'OVERLAY':SueloRustico,'OUTPUT':'memory:'}
# Ejecutar este geoproceso
Entorno200Rustico_resultado= processing.run('native:clip', Entorno200Rustico_parametros)
# Obtención de la capa temporal resultante
Entorno200Rustico= Entorno200Rustico_resultado['OUTPUT']

# Geoproceso Diferencia Simetrica. Crea un Entorno en Suelo Urbanizable que es la diferencia entre 200 m y 50 m.
Entorno150Urbanizable_parametros= {'INPUT':Entorno200Urbanizable,'OVERLAY':Entorno50Urbanizable,'OVERLAY_FIELDS_PREFIX':'','OUTPUT':'memory:','GRID_SIZE':None}
# Ejecutar este geoproceso
Entorno150Urbanizable_resultado= processing.run('native:symmetricaldifference', Entorno150Urbanizable_parametros)
# Obtención de la capa temporal resultante
Entorno150Urbanizable= Entorno150Urbanizable_resultado['OUTPUT']

# Geoproceso Unir Capas Vectoriales. Crea un Entorno unificiando 50m Urbano, 50m Urbanizable y 200m Rustico, polígono multiparte.
EntornoRusticoUrbano_parametros= {'LAYERS':[Entorno200Rustico,Entorno50Urbanizable,Entorno50Urbano],'CRS':QgsCoordinateReferenceSystem('EPSG:25830'),'OUTPUT':'memory:'}
# Ejecutar este geoproceso
EntornoRusticoUrbano_resultado= processing.run('native:mergevectorlayers', EntornoRusticoUrbano_parametros)
# Obtención de la capa temporal resultante
EntornoRusticoUrbano= EntornoRusticoUrbano_resultado['OUTPUT']

# Geoproceso Disolver. Crea un Entorno unificando 50m Urbano, 50m Urbanizable y 200m Rustico, polígono único por atributo.
# La capa donde están los BIC debe tener un atributo único para cada BIC. Por defecto está programado con ID, cambiado si es otro.
EntornoMinimo_parametros= {'INPUT':EntornoRusticoUrbano,'FIELD':['ID'],'SEPARATE_DISJOINT':False,'OUTPUT':'memory:'}
# Ejecutar este geoproceso
EntornoMinimo_resultado= processing.run('native:dissolve', EntornoMinimo_parametros)
# Obtención de la capa temporal resultante
EntornoMinimo= EntornoMinimo_resultado['OUTPUT']

# Geoproceso Unir Capas Vectoriales - Entorno Minimo (1 geometria por atributo) con entorno 150m Urbanbizable
EntornoAutomatico_parametros= {'LAYERS':[Entorno150Urbanizable,EntornoMinimo],'CRS':QgsCoordinateReferenceSystem('EPSG:25830'),'OUTPUT':'memory:'}
# Ejecutar este geoproceso
EntornoAutomatico_resultado= processing.run('native:mergevectorlayers', EntornoAutomatico_parametros)
# Obtención de la capa temporal resultante
EntornoAutomatico= EntornoAutomatico_resultado['OUTPUT']

# Geoproceso recopilar geometria - unir mismo codigo en poligono multiparte
# La capa donde están los BIC debe tener un atributo único para cada BIC. Por defecto está programado con ID, cambiado si es otro.
EntornoDA_parametros= {'INPUT':EntornoAutomatico,'FIELD':['ID'],'OUTPUT':'memory:'}
# Ejecutar este geoproceso
EntornoDA_resultado= processing.run('native:collect', EntornoDA_parametros)
# Obtención de la capa temporal resultante
EntornoDA= EntornoDA_resultado['OUTPUT']
QgsProject.instance().addMapLayer(EntornoDA)