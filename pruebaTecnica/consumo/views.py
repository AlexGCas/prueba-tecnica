from django.shortcuts import render
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json
from django.http import HttpResponse
import pymongo
from django.conf import settings
client = pymongo.MongoClient()

url = 'https://pro-api.coinmarketcap.com/v1/'
parameters = {
  'start':'1',
  'limit':'5000'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '21721843-7f6d-4320-8b3f-ffff25cc1c5e',
}

# Create your views here.
def index(request):
    endpoint = '/cryptocurrency/map'
    # tomar la informacion
    data = getInfo(endpoint)
    os.system('clear')
    print(data['name'])
    return HttpResponse("<h1>escribe una url para acceder a un endpoint </h1> <br/> <h2>ej:</h2> http://127.0.0.1:8000/consumo/cryptocurrency/map")
# acceso a los endpoint
def endpoint(request, endpointLocation, endpointResource):
    endpoint = endpointLocation + "/" + endpointResource

    # Lista de 5000 diccionarios con toda la información de un endpoint
    data = getInfo(endpoint)
    os.system('clear')
    # aniadir los datos a una base de datos en pymongo
    insertedData = conexion(endpointLocation, endpointResource, data)
    return HttpResponse(len(data))
# borrado de las colecciones
def drop(request, endpointLocation, endpointResource):
    mydb = client[endpointLocation]
    mycol = mydb[endpointResource]
    mycol.drop()
    print(mydb.list_collection_names)
    print("aaaaasaa")
    return HttpResponse("drop")

# conexion a la API
def getInfo(endpoint):
    fullUrl = url + endpoint
    session = Session()
    session.headers.update(headers)
    try:
        response = session.get(fullUrl, params=parameters)
        data = json.loads(response.text)
        print(data.keys())
        print(data['data'][0])
        session.close
        return data['data']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
        session.close
        return e
# conexion a la base de datos
def conexion(databaseName, collectionName, data):
    db = client[databaseName]
    collection = db[collectionName]
    insertedData = collection.insert_many(data)
    return insertedData