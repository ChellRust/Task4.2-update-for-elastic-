from fastapi import APIRouter, Request    #Importing fastapi modules  
import json    #Importing JSON
from fastapi.templating import Jinja2Templates   #Importing jinja2 for html hadnling
from fastapi.responses import HTMLResponse   #HTMLResponse is fore returning an HTML page
from datetime import datetime   #Importing datetime module
from elasticsearch import Elasticsearch  #Importing Elasticsearch module

#Initializization of the database
url = "https://22c217337fe648d4992332d6ca32bb31.europe-west3.gcp.cloud.es.io:443"
api_key = "LTgtMGk1TUJZOVZYcVhrUnYwa3I6Zl91X2dqWjVTdFdiWElRT3NDWmEtdw=="
client = Elasticsearch(url, api_key=api_key)

router_get_all = APIRouter(tags=['Tag for /get/all'])    #Assigning route variable
templates = Jinja2Templates(directory="src/templates")   #Assigning route variable to HTML file

#Filtering CVE by date range from Elasticsearch
def date_range(start_date_str, end_date_str):
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    
    #Elasticsearch query for extracting specific data
    response = client.search(
        index="mydb",  
        body={
            "query": {
                "range": {
                    "dateAdded": {
                        "gte": start_date_str,
                        "lte": end_date_str,
                        "format": "yyyy-MM-dd"
                    }
                }
            },
            "_source": ["cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded", 
                        "shortDescription", "requiredAction", "dueDate", "knownRansomwareCampaignUse", 
                        "notes", "cwes"]
        }
    )

    vulnerabilities = response['hits']['hits']
    
    filtered_vulnerabilities = [
        vuln['_source'] for vuln in vulnerabilities      #from every part of index mydb data extracting _source
    ]
    return filtered_vulnerabilities

#filtered data by date range
filtered = date_range("2024-11-21", "2024-11-25")

extracted_data = []#preparing varuable with list

#Extracting by loop for in data in enumerated format where max results equel 40
for idx, entry in enumerate(filtered[:40], start=1):    
    extracted_data.append({
        'Number': idx,
        'cveID': entry.get('cveID', ''),
        'vendorProject': entry.get('vendorProject', ''),
        'product': entry.get('product', ''),
        'vulnerabilityName': entry.get('vulnerabilityName', ''),
        'dateAdded': entry.get('dateAdded', ''),
        'shortDescription': entry.get('shortDescription', ''),
        'requiredAction': entry.get('requiredAction', ''),
        'dueDate': entry.get('dueDate', ''),
        'knownRansomwareCampaignUse': entry.get('knownRansomwareCampaignUse', ''),
        'notes': entry.get('notes', ''),
        'cwes': entry.get('cwes', [])
    })


@router_get_all.get("/get/all/json")   #assigned get request to the "/get/all/json" of the API
def read_json():
    return {"Data": extracted_data}  #return extracted data

@router_get_all.get("/get/all", response_class=HTMLResponse)     #assigned get request to the "/get/all" of the API
def read_html(request: Request):
    return templates.TemplateResponse(     #templateresponse return html page "get_all.html"
        "get_all.html", 
        {"request": request, "data": extracted_data}  #return extracted data
    )
