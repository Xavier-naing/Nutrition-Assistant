from django.shortcuts import render, HttpResponse
from .models import TodoItem
from .forms import searchForm 

import http.client
import json

import os
from dotenv import load_dotenv

load_dotenv()

conn = http.client.HTTPSConnection("spoonacular-recipe-food-nutrition-v1.p.rapidapi.com")
a = os.getenv("API_KEY")
print(a)

headers = {
    'x-rapidapi-key': os.environ.get('API_KEY'),
    'x-rapidapi-host': "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com"
    }

# Create your views here.
def home(request):
    form = searchForm(request.POST)

    return render(request, "home.html", {'form' : form})


def todosView(request):

    return render(request, "todos.html", {"todos": TodoItem.objects.all()})

def search(request):
    search_url = ""
    form = searchForm(request.POST)

    name = ""
    if form.is_valid():
        if form.cleaned_data['name']:
            name = form.cleaned_data['name']
        # if form.cleaned_data['']
        print(name)

    
    conn.request("GET", f"/recipes/complexSearch?query={name}&instructionsRequired=true&fillIngredients=false&addRecipeInformation=false&addRecipeInstructions=false&addRecipeNutrition=false&sort=max-used-ingredients&offset=0&number=10", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    data = json.loads(data.decode("utf-8"))
    print(data)

    return render(request, "result.html", {"result": data['results']})
