from django.shortcuts import render_to_response
from django.views.generic.edit import CreateView

from citizens.models import citizen
from citizens.forms import CitizenForm


def indexView(request):
    global projectDescription
    c = {'title': 'blockchainpassport'}
    return render_to_response('index.html', c)

##
#def list_and_create(request):
    #form = CitizenForm(request.POST or None)
    #if request.method == 'POST':
        #form.save()

##    # notice this comes after saving the form to pick up new objects
    #objects = YourModel.objects.all()
    #return render(request, 'your-template.html',
        #{'objects': objects, 'form': form})


class CitizenCreateView(CreateView):
    model = citizen
    fields = ['name', 'lastname', 'photo', 'social']
    #success_url = '/id/citizen.pk'

    def form_valid(self, form):
        print self.object
        print self.request
        print self.model

    def form_valid(self, form):
        self.object.save()
        return super(CitizenCreateView, self).form_valid(form)