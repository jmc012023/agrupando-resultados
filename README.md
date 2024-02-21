# Descripcion

Se utiliza la libreria Pandas para extraer los datos de los resultados de admision de la pagina web de la unt, limpiar los datos y dejarlos en columnas. El archivo main.ipynb tiene la transformacion de todos los resultados encontrados en la pagina web, mientras que el archivo demo.ipynb tiene como finalidad mostrar el paso a paso de la transformacion de los datos es por ello que en dicho archivo se utiliza como maximo solo dos urls de la pagina web. El archivo unt_results.csv es el resultado final de main.ipynb

# Objetivo

Limpiar y agrupar todos los resultados de admision de la unt encontrados en su pagina web

# Resultados

- En el archivo unt_results.csv se encuentran limpios y agrupados todos los resultados de admision encontrados en la pagina web, contiene 64235 filas y 12 columnas
- Algunas columnas como: tipo_postulante contiene el tipo de dato NaN, que es un tipo de dato propio de Pandas, y otras columnas como: area contiene el tipo de dato ''. La desicion de dejar esos datos se hizo con la finalidad de ver como se comportan estos tipos de datos al convertirlos a .csv y llevarlos a Power BI
- El archivo .cvs se llevara a Power BI para continuar el analisis
