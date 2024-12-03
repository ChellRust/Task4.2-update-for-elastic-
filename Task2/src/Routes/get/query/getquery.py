from fastapi import APIRouter, Request, Query  #Importing fastapi modules 
from fastapi.templating import Jinja2Templates  #Importing jinja2 for html hadnling
from fastapi.responses import HTMLResponse   #HTMLResponse is fore returning an HTML page
from elasticsearch import Elasticsearch  #Importing Elasticsearch module

#Initializization of the database
url = "https://22c217337fe648d4992332d6ca32bb31.europe-west3.gcp.cloud.es.io:443"
api_key = "LTgtMGk1TUJZOVZYcVhrUnYwa3I6Zl91X2dqWjVTdFdiWElRT3NDWmEtdw=="
client = Elasticsearch(url, api_key=api_key)

router_query_filter = APIRouter(tags=['Tag for /get'])   #Assigning route variable
templates = Jinja2Templates(directory="src/templates")  #Assigning route variable to HTML file


def filter_by_keyword(keyword: str):   #filtering by keyword
    keyword_lower = keyword.lower()  #case insensative

    response = client.search(
        index="mydb",  
        body={
            "query": {
                "multi_match": {
                    "query": keyword_lower,
                    "fields": ["cveID", "vendorProject", "product", "vulnerabilityName",
                               "shortDescription", "notes", "cwes"]
                }
            },
            "_source": [
                "cveID", "vendorProject", "product", "vulnerabilityName", "dateAdded",
                "shortDescription", "requiredAction", "dueDate", "knownRansomwareCampaignUse",
                "notes", "cwes"
            ],
            "size": 50  
        }
    )

    vulnerabilities = response['hits']['hits']

    #Extracting by loop for in data in enumerated format
    filtered_results = []
    for idx, entry in enumerate(vulnerabilities, start=1):
        source = entry['_source']
        filtered_results.append({
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

    return filtered_results


@router_query_filter.get("/get/json")  #assigned get request to the "/get/json" of the API
def filter_json(query: str = Query("", description="Keyword to search in the vulnerabilities")):
    if not query:
        return {"Query": query, "Data": []}  
    filtered_data = filter_by_keyword(query)
    return {"Query": query, "Data": filtered_data}  #return extracted data


@router_query_filter.get("/get", response_class=HTMLResponse)  #assigned get request to the "/get" of the API
def filter_query(request: Request, query: str = Query("", description="Keyword to search in the vulnerabilities")):
    if not query:
        return templates.TemplateResponse(
            "get_query.html",
            {"request": request, "data": [], "query": query}
        )  

    filtered_data = filter_by_keyword(query)
    return templates.TemplateResponse(
        "get_query.html",
        {"request": request, "data": filtered_data, "query": query}
    )
