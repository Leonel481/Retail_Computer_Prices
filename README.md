<h1>Centro de precios de componentes de computadoras</h1>


La aplicacion se divide en 2 modulos:


1. ScrapingPrices: Codigo scraping de diferentes tiendas de componentes de computadoras. (Actualmente se realizan a 3 tiendas)

El codigo se levanto en AWS lambda configurado cloudwatch que se encargar de ejecutar el scraping cada 8 horas. Posteriormente se envia una base de datos mysql de RDS AWS.

2. APPCPS: Construccion de la aplicacion a partir de la data scrapeada

Se desarrollo una appweb que se encarga de mostrar los diferentes productos con sus caracteristicas.

<h3>Pasos para ejecucion local</h3>
1. Clonar el repositorio

2. Ejecutar los siguientes comandos para (win):

    cd AppCPS <br>
    python -m venv env<br>
    /env/Scripts/activate<br>
    pip install -r requirements.txt<br>
    python manage.py runserver<br>
    
Nota: Si la pagina de  lista de produictos demora en cargar, se deba posiblemente a que la cantidad de data del modelo el scraping se ejecuta cada 8 horas.

