from fastapi import APIRouter, Request  #Importing fastapi modules 
from fastapi.templating import Jinja2Templates  #Importing jinja2 for html hadnling
from fastapi.responses import HTMLResponse  #HTMLResponse is fore returning an HTML page
from elasticsearch import Elasticsearch  #Importing Elasticsearch module

#Initializization of the database
url = "https://22c217337fe648d4992332d6ca32bb31.europe-west3.gcp.cloud.es.io:443"
api_key = "LTgtMGk1TUJZOVZYcVhrUnYwa3I6Zl91X2dqWjVTdFdiWElRT3NDWmEtdw=="
client = Elasticsearch(url, api_key=api_key)

router_get_new = APIRouter(tags=['Tag for /get/all'])   #Assigning route variable
templates = Jinja2Templates(directory="src/templates")   #Assigning route variable

#Filtering CVE by date range from Elasticsearch
def get_data():
    #Elasticsearch query for extracting specific data limited to 10 results
    response = client.search(
        index="mydb",  
        body={
            "query": {
                "match_all": {}  
            },
            "size": 10,  
            "_source": [
                "cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded",
                "shortDescription", "requiredAction", "dueDate", "knownRansomwareCampaignUse",
                "notes", "cwes"
            ]
        }
    )
    
    vulnerabilities = response['hits']['hits']
    
   
    extracted_data = []
    for idx, entry in enumerate(vulnerabilities, start=1): #from every part of index mydb data extracting _source
        source = entry['_source']
        extracted_data.append({
            'Number': idx,
            'cveID': source.get('cveID', ''),
            'vendorProject': source.get('vendorProject', ''),
            'product': source.get('product', ''),
            'vulnerabilityName': source.get('vulnerabilityName', ''),
            'dateAdded': source.get('dateAdded', ''),
            'shortDescription': source.get('shortDescription', ''),
            'requiredAction': source.get('requiredAction', ''),
            'dueDate': source.get('dueDate', ''),
            'knownRansomwareCampaignUse': source.get('knownRansomwareCampaignUse', ''),
            'notes': source.get('notes', ''),
            'cwes': source.get('cwes', [])
        })
    return extracted_data

extracted_data = get_data()   #preparing varuable with list

@router_get_new.get("/get/new/json") #assigned get request to the "/get/new/json" of the API
def read_json():
    return {"Data": extracted_data}  #return extracted data

@router_get_new.get("/get/new", response_class=HTMLResponse)   #assigned get request to the "/get/new" of the API
def read_html(request: Request):
    return templates.TemplateResponse(  #templateresponse return html page "get_new.html"
        "get_new.html", 
        {"request": request, "data": extracted_data}   #return extracted data
    )
