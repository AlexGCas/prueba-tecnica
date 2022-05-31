from django.shortcuts import render
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import os
import json
from django.http import HttpResponse
import pymongo
from django.conf import settings
client = pymongo.MongoClient()

def index(request):
    endpoint = '/cryptocurrency/map'
    # tomar la informacion
    data = getInfo(endpoint)
    os.system('clear')
    print(data['name'])
    return HttpResponse("<h1>escribe una url para acceder a un endpoint </h1> <br/> <h2>ej:</h2> http://127.0.0.1:8000/consumo/cryptocurrency/map")

def endpoint(request, endpointLocation, endpointResource):
    print("kkkkkkk")
    endpoint = endpointLocation + "/" + endpointResource

    # Leer los datos de la base de datos
    
    data = conexion(endpointLocation, endpointResource)
    print("aaaaaaaa")
    print(data)
    contador = 0
    for dato in data:
        print(dato)
        contador = contador + 1
        if contador == 10:
            break
    html = visualizacion(data)
    return HttpResponse(html)

def conexion(databaseName, collectionName):
    db = client[databaseName]
    collection = db[collectionName]
    # recolectar todos los datos
    data = collection.find({}, { "_id": 0, "id": 0})
    print(data)
    return data
def visualizacion(data):
    os.system('clear')
    contador = 0
    header = "<table><tr>"
    content  = ""
    for key in keys:
        header = header + "<th>{0}</th>".format(key)
    header = header + "</tr>"
    content = "<tr>"
    for dato in data:
        for key in keys:
            content = content + "<td>{0}</td>".format(dato[key])
        content = content + "</tr>"
    content = content + "</table>"
    html = header + content
    return html

