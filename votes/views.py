from datetime import date, datetime, timedelta
import io

import matplotlib.pyplot as plt

from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View, TemplateView

from .models import Vote, Result


party_list = [
  '自由民主党', '立憲民主党', '日本維新の会', 
  '公明党', '国民民主党', '日本共産党', 
  'その他', '白紙投票',
]

age_list = [
      '10代', '20代', '30代', '40代',
      '50代', '60代', '70代', '80代以上',
    ]
    
gender_list = ['男', '女', 'LGBTQ', '回答しない',]

def check_form(party, age, gender):
  return party in party_list and age in age_list and gender in gender_list


class IndexView(TemplateView):
  template_name = 'votes/index.html'


class SelectView(TemplateView):
  template_name = 'votes/select.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    context['party_list'] = party_list
    context['age_list'] = age_list
    context['gender_list'] = gender_list
    
    return context


class ConfirmView(TemplateView):
  template_name = 'votes/confirm.html'
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    
    party = self.request.GET.get("party")
    age = self.request.GET.get("age")
    gender = self.request.GET.get("gender")
    
    if check_form(party, age, gender): 
      context['party'] = party
      context['age'] = age
      context['gender'] = gender
    
    return context
  

class VoteView(View):  
  def post(self, request, *args, **kwargs):
    party_name = {
      "自由民主党": "自民",
      "立憲民主党": "立民",
      "日本維新の会": "維新",
      "公明党": "公明",
      "国民民主党": "国民",
      "日本共産党": "共産",
      "その他": "その他",
      "白紙投票": "白紙",
    }
    
    forwarded_address = request.META.get(
      'HTTP_X_FORWARDED_FOR')
    
    if forwarded_address:
      ip = forwarded_address.split(',')[0]
    else:
      ip = request.META.get('REMOTE_ADDR')
    
    party = self.kwargs.get("party")
    age = self.kwargs.get("age")
    gender = self.kwargs.get("gender")
    
    if check_form(party, age, gender):
      today = date.today()
      check_votes_today = Vote.objects.filter(vote_datetime__date=today).filter(ip_address=ip)
      
      if check_votes_today:
        raise Exception("voted today already")
      else:
        print('no voted today')
        vote = Vote.objects.create(
        party_name=party_name[party],
        age_group=age,
        gender=gender,
        ip_address=ip,
      )
        vote.save()
      
      return HttpResponseRedirect(
        reverse("votes:index"))


def setPLT_daily(date):
  year, month, day = date.split('-')
  title = f'{year}-{month}-{day}'
  votes = Result.objects.filter(vote_date=date)
  
  party_counts = [
    votes.get(party_name="自民").num_votes,
    votes.get(party_name="立民").num_votes,
    votes.get(party_name="維新").num_votes,
    votes.get(party_name="公明").num_votes,
    votes.get(party_name="国民").num_votes,
    votes.get(party_name="共産").num_votes,
    votes.get(party_name="その他").num_votes,
    votes.get(party_name="白紙").num_votes,
  ]
  
  plt.rcParams['font.family'] = "Hiragino Sans"
  fig, ax = plt.subplots(layout='constrained')
  bar_container = ax.barh(party_list[::-1], party_counts[::-1])
  ax.set(xlabel='得票数', title=title)
  ax.bar_label(bar_container)
  
  vote_date = Result.objects.filter(vote_date=f'{year}-{month}-{day}')
  if not year:
    raise Exception("Please fill in a day!")
  else:
    print('else')
    print(year, month, day)
    title = f'{year}-{month}-{day}'
    vote_date = Result.objects.filter(vote_date=date)
  
  
def setPLT_monthly(month):
  year, month = month.split('-')
  print(year, month)
  votes = Result.objects.filter(vote_date__year=year).filter(vote_date__month=month)
  
  party_counts  = [
    votes.filter(party_name="自民").aggregate(Sum('num_votes'))['num_votes__sum'],
    votes.filter(party_name="立民").aggregate(Sum('num_votes'))['num_votes__sum'],
    votes.filter(party_name="維新").aggregate(Sum('num_votes'))['num_votes__sum'],
    votes.filter(party_name="公明").aggregate(Sum('num_votes'))['num_votes__sum'],
    votes.filter(party_name="国民").aggregate(Sum('num_votes'))['num_votes__sum'],
    votes.filter(party_name="共産").aggregate(Sum('num_votes'))['num_votes__sum'],
    votes.filter(party_name="その他").aggregate(Sum('num_votes'))['num_votes__sum'],
    votes.filter(party_name="白紙").aggregate(Sum('num_votes'))['num_votes__sum'],
  ]
  
  plt.rcParams['font.family'] = "Hiragino Sans"
  fig, ax = plt.subplots(layout='constrained')
  bar_container = ax.barh(party_list[::-1], party_counts[::-1])
  ax.set(xlabel='得票数', title=f'{year}-{month}')
  ax.bar_label(bar_container)
  
  
def setPLT_transition(from_month, to_month):
  votes_counts = {
    "自民": [],
    "立民": [],
    "維新": [],
    "公明": [],
    "国民": [],
    "共産": [],
    "その他": [],
    "白紙": [],
  }
  
  votes_counts_keys = list(votes_counts.keys())
  month_list = []
  from_year, from_month = from_month.split('-')
  to_year, to_month = to_month.split('-')
  
  from_year = int(from_year)
  from_month = int(from_month)
  to_year = int(to_year)
  to_month = int(to_month)
   
  while True:
    a_month = Result.objects.filter(vote_date__year=from_year).filter(vote_date__month=from_month)
    month_list.append(f'{from_year}-{from_month}')
    for key in votes_counts_keys:
      votes_counts[key].append(a_month.filter(
        party_name=key).aggregate(Sum('num_votes'))['num_votes__sum'])
    if from_month == 12:
      from_year += 1
      from_month = 1
    else:
      from_month += 1
    if date(from_year, from_month, 1) > date(to_year, to_month, 1):
      break 

  plt.rcParams['font.family'] = "Hiragino Sans"
  fig, ax = plt.subplots(3, 1, sharex=True)
  for p in votes_counts_keys:
    for a in ax:
      a.plot(month_list, votes_counts[p], label=p) 
    
  ax[0].set_ylim(15000, 22500)
  ax[1].set_ylim(1500, 7000)
  ax[2].set_ylim(0, 1500)
  
  ax[0].set_title('得票数推移(月別）')
  ax[1].legend()
def pltToSvg():
  buf = io.BytesIO()
  plt.savefig(buf, format='svg', bbox_inches='tight')
  s = buf.getvalue()
  buf.close()
  return s


def get_svg_dayly(request):
  date = request.GET.get('date')
  setPLT_daily(date)
  svg = pltToSvg()
  plt.cla()
  response = HttpResponse(svg, content_type='image/svg+xml')
  return response


def get_svg_monthly(request):
  month = request.GET.get('month')
  setPLT_monthly(month)
  svg = pltToSvg()
  plt.cla()
  response = HttpResponse(svg, content_type='image/svg+xml')
  return response


def get_svg_transition(request):
  from_month = request.GET.get('from_month')
  to_month = request.GET.get('to_month')
  setPLT_transition(from_month, to_month)
  svg = pltToSvg()
  plt.cla()
  response = HttpResponse(svg, content_type='image/svg+xml')
  return response