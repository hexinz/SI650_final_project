from django.shortcuts import render
from django.http import HttpResponse
from BM25 import Retrival_Interface
import pickle
# Create your views here.
def index(request):
    return render(request, 'searchengine/form.html')

def search(request):
    template_name = "searchengine/line_list.html"
    if request.method == 'GET':
        if request.GET.get("textfield"):
            query = request.GET.get('textfield', None)
            # query = 'Can the trophy system protect me against bullets?' # for test
            RI = Retrival_Interface(10)
            results = RI.Retrival(query)
            return render(request, template_name, {'results': results})