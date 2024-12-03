from fastapi import APIRouter, Request    #Importing fastapi modules 
from fastapi.templating import Jinja2Templates    #Importing jinja2 for html hadnling
from fastapi.responses import HTMLResponse    #HTMLResponse is fore returning an HTML page
from elasticsearch import Elasticsearch  #Importing Elasticsearch module

#Initializization of the database
url = "https://22c217337fe648d4992332d6ca32bb31.europe-west3.gcp.cloud.es.io:443"
api_key = "LTgtMGk1TUJZOVZYcVhrUnYwa3I6Zl91X2dqWjVTdFdiWElRT3NDWmEtdw=="
client = Elasticsearch(url, api_key=api_key)

router_get_known = APIRouter(tags=['Tag for /get/known'])   #Assigning route variable
templates = Jinja2Templates(directory="src/templates")  #Variable for directory where HTML page is stored

#Filtering CVE by date range from Elasticsearch
def ransomekey():
    #Elasticsearch query for extracting specific data
    response = client.search(
        index="mydb",  
        body={
            "query": {
                "match": {  
                    "knownRansomwareCampaignUse": "known"  
                }
            },
            "_source": [
                "cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded",
                "shortDescription", "requiredAction", "dueDate", "knownRansomwareCampaignUse",
                "notes", "cwes"
            ]
        }
    )

    vulnerabilities = response['hits']['hits']
    

    filtered_vulnerabilities = [
        vuln['_source'] for vuln in vulnerabilities   #from every part of index mydb data extracting _source
    ]
    
    return filtered_vulnerabilities

#filtered data by key
filtered = ransomekey()

extracted_data = []   #preparing varuable with list

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



@router_get_known.get("/get/known/json")  #assigned get request to the "/get/known/json" of the API
def read_json():
    if not extracted_data:
        return {"message": "No data found for the given filter."}
    return {"Data": extracted_data}  #return extracted data


@router_get_known.get("/get/known", response_class=HTMLResponse)   #assigned get request to the "/get/known" of the API
def read_html(request: Request):
    if not extracted_data:
        return templates.TemplateResponse(
            "get_known.html", 
            {"request": request, "message": "No data found for the given filter."}
        )
    return templates.TemplateResponse(
        "get_known.html", 
        {"request": request, "data": extracted_data}  #templateresponse return html page "get_known.html"
    )
