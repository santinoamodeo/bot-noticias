import azure.functions as func
import requests
import json
import os

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="obtener-noticias")
def obtener_noticias(req: func.HttpRequest) -> func.HttpResponse:
    
    tema = req.params.get("tema", "tecnologia")
    api_key = os.environ.get("NEWS_API_KEY")
    
    url = f"https://newsapi.org/v2/everything?q={tema}&language=es&pageSize=5&apiKey={api_key}"
    
    response = requests.get(url)
    data = response.json()
    
    articulos = []
    for articulo in data.get("articles", []):
        articulos.append({
            "titulo": articulo["title"],
            "descripcion": articulo["description"],
            "url": articulo["url"],
            "fuente": articulo["source"]["name"]
        })
    
    return func.HttpResponse(
        json.dumps(articulos, ensure_ascii=False),
        mimetype="application/json",
        status_code=200
    )