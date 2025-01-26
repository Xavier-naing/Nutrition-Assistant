from django.shortcuts import render
from .models import TodoItem
from .forms import searchForm 

import http.client
import json

import os
from dotenv import load_dotenv


load_dotenv()

conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")
a = os.getenv("API_KEY")

headers = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }


# Create your views here.
def home(request):
    form = searchForm(request.POST)
    return render(request, "home.html", {'form' : form})

def todosView(request):
    return render(request, "todos.html", {"todos": TodoItem.objects.all()})

def search(request, *args, **kwargs):
    name, current = "", 0
    form = searchForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            if form.cleaned_data['name']:
                name = form.cleaned_data['name']
    if request.method == "GET":
        name = kwargs['name']
        current = request.GET.get('current')

    current = int(current)
    conn.request("GET", f"/recipes/complexSearch?query={name}&instructionsRequired=true&fillIngredients=false&addRecipeInformation=false&addRecipeInstructions=false&addRecipeNutrition=false&sort=max-used-ingredients&offset={current * 10}&number=10", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    maximum = data["totalResults"] // 10
    totalResult = list(range( max(current-2, 0), min(current+6, maximum+1)))

    return render(request, "result.html", {"search" : name ,"result": data['results'], "totalResult" : totalResult, "current" : current, "maximum": maximum })
