# Crear Entornos de Protección de BIC de forma automática (disposición adicional 4ª Ley 14/2007 LPHA)
Este script permite crear Entornos de Protección de Bienes de Interés Cultural, BIC, de forma automática, según lo establecido en la disposición adicional 4ª Ley 14/2007, de 26 de noviembre, de Patrimonio Histórico de Andalucía.

> **Este script NO es oficial de la Junta de Andalucía**

> **Crea buffer geográfico, no tiene en cuenta parcelas catastrales**

## Funcionalidades:
- Creación de Entornos de 50 y 200 m de buffer alrededor del BIC.
- Características:
    - **100% suelo urbano:**
      - buffer de 50 m.
      - creando un único polígono.
    - **100% suelo urbanizable:**
      - crea un buffer de 50 m y otro de 150 m.
      - creando un multipolígono con dos partes, una parte de 50 m y otra parte de 150 m alrededor del anterior. Motivo: al ser un suelo en transición, mientras sea urbanizable su entorno es de 200 m y cuando pase a ser urbano será de 50 m. El polígono multiparte permite eliminar la parte de 150 m cuando el suelo pase a ser urbano sin necesidad de volver a ejecutar el código.
    - **100% suelo no urbanizable:**
      - buffer de 200 m.
      - creando un único polígono.
    - **Suelo Mixto:**
      - buffer de 50 m y otro de 200 m
      - creando un único polígono uniendo los buffer de 50 m. y 200 m.
      - OJO: cuando hay suelo no urbanizable: se crea un multipolígono con dos partes, una parte para el suelo en urbano y no urbano y otra parte de 150 m (como en el punto anterior). Motivo: al ser un suelo en transición, mientras sea urbanizable su entorno es de 200 m y cuando pase a ser urbano será de 50 m. El polígono multiparte permite eliminar la parte de 150 m cuando el suelo pase a ser urbano sin necesidad de volver a ejecutar el código.

## Características técnicas:
- Lenguaje: R.
- Uso: Para usarse en QGIS dentro de consola de Python.
- Antes de ejecutar hay que definir los siguientes parámetros dentro del código:
    - Indica como se llama la **capa** donde están los polígonos de los **BIC** a los que queremos crear el entorno:
        - Introduce el nombre de capa aquí: ('Bienes').
          - En la línea de código: BienesDA = QgsProject.instance().mapLayersByName('Bienes')[0]
    - Indica como se llama la **capa** donde está el polígono del **suelo urbano**:
        - Introduce el nombre de capa aquí: ('Bienes').
          - En la línea de código: SueloUrbano = QgsProject.instance().mapLayersByName('SueloUrbano')[0]
    - Indica como se llama la **capa** donde está el polígono del **suelo urbanizable**:
        - Introduce el nombre de capa aquí: ('Bienes').
          - SueloUrbanizable = QgsProject.instance().mapLayersByName('SueloUrbanizable')[0]
    - Indica como se llama la **capa** donde está el polígono del **suelo no urbanizable**:
        - Introduce el nombre de capa aquí: ('Bienes').
            - SueloRustico = QgsProject.instance().mapLayersByName('SueloRustico')[0]
    - La capa donde están los BIC debe tener un atributo único para cada BIC. Por defecto está programado con ID, cambiado si es otro.

## ¿Cómo suarlo?:
Carga en QGIS las capas necesarias.

Carga el código en el la consola Python de QGIS.

Modifica el código para indicar como se llaman las capas en tu proyecto QGIS.

El resultado tras ejecutar el script Python es una capa en la memoria de QGIS.

## ¿Cómo tener las capas de suelo urbano, urbanizable y no urbanizable?:
Se necesita disponer de 3 capas, una para cada tipo de suelo. Cada capa deberá tener un único polígono.

La geometría de la capa debe ser poligonal.

La capa de los tipos de suelo debe proceder del planeamiento urbanístico del municipio.

Se recomienda incluir, en la capa suelo no urbanizable, un buffer de 200 m sobre el mar para evitar el corte del entorno en la línea marítima.

En caso de no disponer de la clasificación de suelo digital se puede usar la cartografía de tipo de suelo del [Sistema de Información Urbana](https://www.mivau.gob.es/urbanismo-y-suelo/sistema-de-informacion-urbana)

Se recomienza no usar la cartografía de Catastro debido a que Catastro tiene unido los suelo urbano y urbanizable en la misma capa como suelo urbano.

 ## Licencia:
 Creative Commons Attribution-ShareAlike 4.0 International

 CC BY-SA 4.0

 ## Colaborativa:
 Animamos a la Comunidad para que mejore el código y nos ayude a mejorarlo.
