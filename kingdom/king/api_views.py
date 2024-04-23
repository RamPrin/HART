import json

from django.http import HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from .models import King, Servant, TestAnswer

def start_api(request):
    if request.method == "GET":
        return HttpResponse(
            json.dumps(
                [
                    {
                        "id": k.id,
                        "name": k.name,
                        "kingdom": {
                            "id": k.kingdom.id,
                            "name": k.kingdom.name
                        }
                    } for k in King.objects.all()
                ]
            ).encode(),
            content_type="application/json"
        )
    else:
        return HttpResponseNotAllowed(['GET'])
    
def api_king(request, king_id):
    if request.method == "GET":
        king = King.objects.filter(pk=king_id).get()
        servants = Servant.objects.filter(kingdom=king.kingdom.id)
        context = {
            "name": king.name,
            "kingdom": {
                "name": king.kingdom.name,
                "id": king.kingdom.id
            },
            "accepted_servants": [
                {
                    "id": servant.id,
                    'name': servant.name,
                    'age': servant.age,
                    'pigeon': servant.mail,
                    'answers': [
                        {
                            'question': ans.test.question,
                            'answer': 'Yes' if ans.answer else 'No'
                        } for ans in TestAnswer.objects.filter(servant=Servant.objects.get(id=servant.id))
                    ]
                } for servant in servants if servant.accepted
            ],
            "not_accepted_servants": [
                {
                    "id": servant.id,
                    'name': servant.name,
                    'age': servant.age,
                    'pigeon': servant.mail,
                    'answers': [
                        {
                            'question': ans.test.question,
                            'answer': 'Yes' if ans.answer else 'No'
                        } for ans in TestAnswer.objects.filter(servant=Servant.objects.get(id=servant.id))
                    ]
                } for servant in servants if not servant.accepted
            ]
        }
        return HttpResponse(
            json.dumps(
               context
            ).encode(),
            content_type='application/json'
        )
    else:
        return HttpResponseNotAllowed(["GET"])

def api_servant(request, servant_id):
    if Servant.objects.filter(pk=servant_id).exists():
        servant = Servant.objects.get(pk=servant_id)
        context = {
            "id": servant.id,
            "name": servant.name,
            "kingdom": {
                "id": servant.kingdom.id,
                "name": servant.kingdom.name,
            },
            "age": servant.age,
            "pigeon": servant.mail,
            "accepted": servant.accepted
        }
        return HttpResponse(
            json.dumps(
                context
            ).encode(),
            content_type='application/json'
        )
    else:
        return HttpResponseNotFound('No servant with such ID')
    
def api_stats(request):
    if request.method == "GET":
        kings = King.objects.all()
        kingdoms = []
        for king in kings:
            kingdom_ = {}
            kingdom_['name'] = king.kingdom.name
            kingdom_['id'] = king.kingdom.id
            kingdom_['king'] = king.name
            servants = Servant.objects.filter(kingdom=king.kingdom)
            kingdom_['applied'] = len(servants.filter(accepted=True))
            kingdom_['pending'] = len(servants.filter(accepted=False))
            kingdoms.append(kingdom_)
        return HttpResponse(json.dumps({'kingdoms': kingdoms}).encode(), content_type='application/json')
    else:
        return HttpResponseNotAllowed(['GET'])