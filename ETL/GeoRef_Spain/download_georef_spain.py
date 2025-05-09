import requests

# Municipios
url_muni = "https://public.opendatasoft.com/explore/dataset/georef-spain-municipio/download/?format=geojson&lang=es&timezone=Europe%2FMadrid"
r_muni = requests.get(url_muni)
with open("ETL/GeoRef_Spain/georef-spain-municipio.geojson", "wb") as f:
    f.write(r_muni.content)

# Comunidades Autónomas
url_ccaa = "https://public.opendatasoft.com/explore/dataset/georef-spain-comunidad-autonoma/download/?format=geojson&lang=es"
r_ccaa = requests.get(url_ccaa)
with open("ETL/GeoRef_Spain/georef-spain-comunidad-autonoma.geojson", "wb") as f:
    f.write(r_ccaa.content)

print("Descarga completada.")
