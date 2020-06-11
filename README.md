# Accesibilidad a espacios verdes

Este proyecto junta algunas herramientas para analizar la accesibilidad a espacios verdes en el area urbana buenos aires.

El archivo `notebooks/espacios_verdes_caba.ipynb` utiliza informacion oficial del Gobierno de la Ciudad de Buenos Aires y limita su analisis a este area administrativa.

El archivo `notebooks/accesibilidad_amba.ipynb` utiliza como fuente OpenSreetMap. Por un lado [este repo](https://github.com/alephcero/ba_grafo) contiene como bajar la red de calles y esquinas para los partidos del AMBA utilizando [osmnx](https://github.com/gboeing/osmnx). Luego se realiza una query en OSM para los parques utilizando `query_parques_osm.py`. Finalmente el notebook realiza el analisis.

  
