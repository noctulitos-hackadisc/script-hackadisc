# HACKADISC - LOS NOCTULITOS

## Descripción

Este script de Python analiza un archivo dataset.xlsx para identificar compañías principales y subsidiarias. Luego, genera un archivo companies_and_subcompanies.xlsx que puede ser utilizado como seeder para una base de datos.

## Requisitos

- Python 3.x
- pandas
- openpyxl

## Instalación

1. Clona este repositorio.
2. Instala las dependencias con:
   bash
   pip install pandas openpyxl
   

## Uso

1. Asegúrate de tener el archivo dataset.xlsx en el mismo directorio que el script.
2. Ejecuta el script:
   bash
   python script.py
   
3. Se generará el archivo companies_and_subcompanies.xlsx con las compañías principales y subsidiarias identificadas.

## Estructura del Dataset

- *multicompanies*: Contiene información sobre compañías principales y subsidiarias.
- *workers*: Contiene información sobre trabajadores y sus compañías.

## Salida

El script genera un archivo Excel con dos hojas:

- *Companies*: Compañías sin coincidencias en 'multicompanies'.
- *SubCompanies*: Subsidiarias con coincidencias en 'sub_company_id'.

## Licencia

Este proyecto está bajo la Licencia MIT.
