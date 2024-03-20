from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import King, Kingdom, TestCase, Servant
# Create your views here.
def choose(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render(request=request))

def start(request):
    template = loader.get_template("king/k_list.html")
    data = [{"id": k.id,"name": k.name, "kingdom": k.kingdom.name} for k in King.objects.all()]
    print(data)
    context = {
        "king_list": data
    }
    return HttpResponse(template.render(context, request))

def king(request, king_id):
    template = loader.get_template("king/king.html")
    king = King.objects.filter(pk=king_id).get()
    servants = Servant.objects.filter(kingdom=king.kingdom.id)
    context = {
        "name": king.name,
        "kingdom": king.kingdom.name,
        "servants": [
            {
                'name': servant.name,
                'age': servant.age,
                'pigeon': servant.mail
            } for servant in servants
        ]
    }
    return HttpResponse(template.render(context, request))

def serve(request):
    template = loader.get_template("servant/index.html")
    return HttpResponse(template.render(request=request))