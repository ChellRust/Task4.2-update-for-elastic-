from fastapi import APIRouter, Request      #Importing fastapi modules
from fastapi.templating import Jinja2Templates    #Importing jinja2 for html hadnling
from fastapi.responses import HTMLResponse    #HTMLResponse is fore returning an HTML page

router_info = APIRouter(tags=['tag for /info'])   #Assigning route varuable
templates = Jinja2Templates(directory="src/templates")  #varuable that assigned directory where html page is stored

@router_info.get("/info/json")   #assigned get request to the "/info/json" of the API
def read_root():
    return {"Follow": "your own way"}   #return extracted data 

@router_info.get("/info", response_class=HTMLResponse)   #assigned get request to the "/info" of the API
def read_html(request: Request):
    return templates.TemplateResponse(    #templateresponse return html page "/info.html"
        "info.html", 
        {"request": request} 
    )