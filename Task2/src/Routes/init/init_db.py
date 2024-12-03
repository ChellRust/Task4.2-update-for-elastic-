from elasticsearch import Elasticsearch  #Importing Elasticsearch module
import json   #Importing JSON
from fastapi import APIRouter, Request   #Importing fastapi modules 
from fastapi.templating import Jinja2Templates     #Importing jinja2 for html hadnling
from fastapi.responses import HTMLResponse    #HTMLResponse is fore returning an HTML page

templates = Jinja2Templates(directory="src/templates")
router_init_db = APIRouter(tags=['tag for /init_db'])

#your api key and provided url
url = "https://22c217337fe648d4992332d6ca32bb31.europe-west3.gcp.cloud.es.io:443"
api_key = "LTgtMGk1TUJZOVZYcVhrUnYwa3I6Zl91X2dqWjVTdFdiWElRT3NDWmEtdw=="

#Initializization of the database
client = Elasticsearch(url, api_key=api_key)

#Adding data to Elasticsearch
def add_data_mydb():
    #Checks ofr existing index
    if client.indices.exists(index="mydb"):
        print("Index 'cve' already exists, skipping data addition.")
        return  #exit if exist


    with open("src/known_exploited_vulnerabilities.json", "r") as file:   #open and loading json data
        data = json.load(file)

    #Adding data from the json file to index mydb
    for item in data["vulnerabilities"]:
        response = client.index(index="mydb", document=item)
        
        if response.get("result") == "created":
            print(f"Document created successfully: {response['_id']}")
        else:
            print(f"Failed to index document: {response}")

    print("Data addition to 'mydb' index completed.")

@router_init_db.get("/init_db", response_class=HTMLResponse) #assigned get request to the "/init_db" of the API
def read_html(request: Request):
    add_data_mydb()  #executing of add_Data_mydb after opening 
    return templates.TemplateResponse("init_db.html", {"request": request}) #templateresponse return html page "init_db.html"
