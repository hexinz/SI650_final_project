from django.shortcuts import render
from django.http import HttpResponse
#from BM25 import Retrival_Interface
from LTR import BM25, FastRank
from Filter import Item_Item_Filter
from question_answer import get_answer
import pickle
# Create your views here.
from searchengine.models import Episode, Fav
def index(request):
    return render(request, 'searchengine/form.html')

def search(request):
    template_name = "searchengine/line_list.html"
    if request.method == 'GET':
        if request.GET.get("textfield"):
            query = request.GET.get('textfield', None)
            # query = 'Can the trophy system protect me against bullets?' # for test
            try:
                # RI = Retrival_Interface(10)
                # results = RI.Retrival(query)
                results = FastRank(query)
            except:
                results = []
            return render(request, template_name, {'results': results})

def episodeListView(request):
    # if request.user.is_authenticated:
    episode_list = Episode.objects.all()
    ratings = list()
    recommend_episode_list = []
    if request.user.is_authenticated:
        # rows = [{'id': 2}, {'id': 4} ... ]  (A list of rows)
        rows = request.user.favorite_episodes.values('id')
        # favorites = [2, 4, ...] using list comprehension
        ratings = [row['id'] for row in rows]
        result = Item_Item_Filter(request.user.username)
        for i in result:
            recommend_episode_list.append(Episode.objects.get(pk=i))
    return render(request, 'searchengine/episode_list.html', {'episode_list' : episode_list, 'ratings': ratings, 'recommend_episode_list': recommend_episode_list})

def answerView(request):
    if request.method == 'GET':
        if request.GET.get("question"):
            query = request.GET.get('question', None)
            print(query)
            # query = 'Can the trophy system protect me against bullets?' # for test
            try:
                result = get_answer(query)
                print(result)
            except:
                result = None
            return render(request, "searchengine/answer_list.html", {'result': result})

def QAView(request):
    return render(request, "searchengine/question_answer.html")

# csrf exemption in class based views
# https://stackoverflow.com/questions/16458166/how-to-disable-djangos-csrf-validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404

@method_decorator(csrf_exempt, name='dispatch')
class AddRating(LoginRequiredMixin, View):
    def post(self, request, pk, rating) :
        print("Add PK", pk, 'with rating',rating)
        t = get_object_or_404(Episode, id=pk)
        fav = Fav(user=request.user, episode=t, rating=rating)
        try:
            fav.save()  # In case of duplicate key
            print('successfully saved!')
        except IntegrityError as e:
            pass
        return HttpResponse()

@method_decorator(csrf_exempt, name='dispatch')
class DeleteRating(LoginRequiredMixin, View):
    def post(self, request, pk) :
        print("Delete PK",pk)
        t = get_object_or_404(Episode, id=pk)
        try:
            fav = Fav.objects.get(user=request.user, episode=t).delete()
        except Fav.DoesNotExist as e:
            pass

        return HttpResponse()
