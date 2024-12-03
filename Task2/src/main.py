from fastapi import FastAPI, Request        #Importing fastapi modules 
from fastapi.templating import Jinja2Templates     #Importing jinja2 for html
from Routes.info import info       #importing own python code
from Routes.get.all import get_all     #importing own python code
from Routes.get.new import get_new     #importing own python code
from Routes.get.known import get_known    #importing own python code
from Routes.get.query import getquery     #importing own python code
from Routes.init import init_db    #importing own python code



app = FastAPI()   #instance for creating routes in feature
templates = Jinja2Templates(directory="src/templates")    #varuable that assigned directory where html page is stored

@app.get('/')   #assigned get request to the "/" of the API
def home(request: Request):  #request: Request assign Request class which has headers and queries by default
    return templates.TemplateResponse(    #templateresponse return html page "home.html"
        "home.html", 
        {"request": request}
    )
    







app.include_router(info.router_info)         #including info.py
app.include_router(get_all.router_get_all)   #including get_all.py
app.include_router(get_new.router_get_new)   #including get_new.py
app.include_router(get_known.router_get_known)   #including get_known.py
app.include_router(getquery.router_query_filter)  #including getquery.py
app.include_router(init_db.router_init_db)    #including init_db.py