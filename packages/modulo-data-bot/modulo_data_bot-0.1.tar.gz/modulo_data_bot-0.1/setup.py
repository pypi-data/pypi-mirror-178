from setuptools import setup

setup(
    name="modulo_data_bot", #nombre del paquete
    version="0.1", #version del paquete
    description="Modulo para crear la base de datos de KCK_BOT_SV", # descripcion del paquete
    author="Gerardo Loucel", #autor del paquete
    packages=['data_source'], #nombre del archivo que haremos paquete
    zip_saage=False) #le decimos a python que al instalar el paqueteno puede ser ejecutado directamente desde un archivo zip