import json
import re


from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import loader
from .models import King, Servant, TestCase, Kingdom, TestAnswer
from .forms import ServantForm, TestForm, SignInForm
# Create your views here.
def choose(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render(request=request))

def start(request):
    template = loader.get_template("king/index.html")
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
        "accepted_servants": [
            {
                "id": servant.id,
                'name': servant.name,
                'age': servant.age,
                'pigeon': servant.mail
            } for servant in servants if servant.accepted
        ],
        "not_accepted_servants": [
            {
                "id": servant.id,
                'name': servant.name,
                'age': servant.age,
                'pigeon': servant.mail
            } for servant in servants if not servant.accepted
        ]
    }
    return HttpResponse(template.render(context, request))

def king_accept(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        print(data)
        id = data['id']
        if Servant.objects.filter(pk=id).exists():
            servant = Servant.objects.get(pk=id)
            if not servant.accepted:
                servant.accepted = True
                servant.save()
            return HttpResponse('')
        else:
            return HttpResponseNotFound('No Such ID')
    

def servant(request):
    template = loader.get_template("servant/index.html")
    return HttpResponse(template.render(context={"sign_in_form": SignInForm()}, request=request))

def servant_sign_in(request):
    if request.method == "POST":
        if Servant.objects.filter(mail=request.POST['email']).exists():
            mail = request.POST['email']
            print(mail)
            servant = Servant.objects.get(mail=mail).id
            return HttpResponseRedirect(f'/servant/{servant}/')
        else:
            return HttpResponseNotFound('')
        
def servant_info(request, servant_id):
    if Servant.objects.filter(pk=servant_id).exists():
        template = loader.get_template("servant/servant.html")
        servant = Servant.objects.get(pk=servant_id)
        context = {
            "name": servant.name,
            "kingdom": "?" if servant.kingdom is None else servant.kingdom.name,
            "age": servant.age,
            "pigeon": servant.mail,
            "accepted": servant.accepted
        }
        return HttpResponse(template.render(context, request))
    else:
        return HttpResponseNotFound('')


def servant_add_html(request):
    template = loader.get_template("servant/new.html")
    if request.method == 'POST':
        form_data = ServantForm(request.POST)
        if form_data.is_valid():
            if Servant.objects.filter(mail=request.POST['email']).exists():
                return HttpResponse(template.render(context={"form_data": form_data, "user_exists": True}, request=request))
            else:
                tests = TestCase.objects.filter(kingdom=request.POST['kingdom']).values('id', 'question')
                form_test = TestForm(question_list=tests)    
                return HttpResponse(template.render(context={"form_data": form_data, "form_test": form_test}, request=request))
    else:
        form = ServantForm()
        return HttpResponse(template.render(context={"form_data": form}, request=request))


def servant_create(request):
    if request.method == 'POST':
        template = loader.get_template('servant/created.html')
        post_data = request.POST
        servant_data = {}
        test_data = {}
        for key in post_data.keys():
            if 'question-' not in key:
                servant_data[key] = post_data[key]
            else:
                test_data[key] = post_data[key]

        servant = Servant(
            name=servant_data['name'],
            age=servant_data['age'],
            mail=servant_data['email'],
            kingdom=Kingdom.objects.filter(
                pk = servant_data['kingdom']
            ).get()
        )
        if servant:
            for key, val in test_data.items():
                id = re.search('question-(?P<ID>\d+)', key).group("ID")
                answer = TestAnswer(
                    servant=servant,
                    test=TestCase.objects.get(pk=id),
                    answer=(val=='1')
                )
                servant.save()
                answer.save()
        return HttpResponse(template.render(request=request))


def stats(request):
    template = loader.get_template("stats/index.html")
    print(template.origin)
    kings = King.objects.all()
    kingdoms = []
    for king in kings:
        kingdom_ = {}
        kingdom_['name'] = king.kingdom.name
        kingdom_['king'] = king.name
        servants = Servant.objects.filter(kingdom=king.kingdom)
        kingdom_['applied'] = len(servants.filter(accepted=True))
        kingdom_['pending'] = len(servants.filter(accepted=False))
        kingdoms.append(kingdom_)
    return HttpResponse(template.render(context={'kingdoms': kingdoms}, request=request))