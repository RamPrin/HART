from django.http import HttpResponse
from django.template import loader
from .models import King, Servant, TestCase
from .forms import ServantForm, TestForm
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

def servant(request):
    template = loader.get_template("servant/index.html")
    return HttpResponse(template.render(request=request))

def servant_info(request, servant_id):
    template = loader.get_template("servant/servant.html")
    servant = Servant.objects.filter(pk=servant_id).get()
    context = {
        "name": servant.name,
        "kingdom": "?" if servant.kingdom is None else servant.kingdom.name,
        "age": servant.age,
        "pigeon": servant.mail

    }
    return HttpResponse(template.render(context, request))

def servant_add_html(request):
    template = loader.get_template("servant/new.html")
    if request.method == 'POST':
        form_data = ServantForm(request.POST)
        if form_data.is_valid():
            tests = TestCase.objects.filter(kingdom=request.POST['kingdom']).values('question')
            form_test = TestForm(question_list=tests)    
            return HttpResponse(template.render(context={"form_data": form_data, "form_test": form_test}, request=request))
    else:
        form = ServantForm()
        return HttpResponse(template.render(context={"form_data": form}, request=request))


def servant_create(request):
    if request.method == 'POST':
        print(request.POST)
        return HttpResponse("pong")
