from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from votes.models import Vote, Result

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


class SelectViewTests(TestCase):
  def test_context_data(self):
    response = self.client.get(reverse('votes:select'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, "votes/select.html")
    for list in (party_list, age_list, gender_list):
      for context in list:
        print("test")
        self.assertContains(response, context)
        
class ConfirmViewTests(TestCase):
  def test_context_data(self):
    response = self.client.get(reverse('votes:confirm'),
                               {"party": party_list[0],
                                "age": age_list[0],
                                "gender": gender_list[0]})
    print(response)
    self.assertTemplateUsed(response, "votes/confirm.html")
    self.assertContains(response, party_list[0])
    self.assertNotContains(response, party_list[1])
    
class VoteViewTests(TestCase):
  def test_not_voted_today(self):
    response = self.client.post(reverse('votes:vote',
                               kwargs={"party": party_list[0],
                                       "age": age_list[0],
                                       "gender": gender_list[0]}))
    self.assertEqual(response.status_code, 302)
    vote = Vote.objects.all().first()
    self.assertEqual(vote.party_name, party_name[party_list[0]])
    self.assertEqual(vote.age_group, age_list[0])
    self.assertEqual(vote.gender, gender_list[0])
    response = self.client.get(response.url)
    self.assertTemplateUsed(response, "votes/index.html")
    
  def test_already_voted_today(self):
    Vote.objects.create(party_name=party_name[party_list[0]],
                        age_group=age_list[0],
                        gender=gender_list[0],
                        ip_address="127.0.0.1",)
    response = self.client.post(reverse('votes:vote',
                               kwargs={"party": party_list[1],
                                       "age": age_list[1],
                                       "gender": gender_list[1]}))
    self.assertEqual(response.status_code, 302)
    vote = Vote.objects.all()
    self.assertEqual(vote.count(), 1)
    self.assertEqual(vote.first().party_name, party_name[party_list[0]])
    self.assertEqual(vote.first().age_group, age_list[0])
    self.assertEqual(vote.first().gender, gender_list[0])
    self.assertEqual(vote.first().ip_address, "127.0.0.1")
    response = self.client.get(response.url)
    self.assertTemplateUsed(response, "votes/index.html")
    
  def test_multi_people_voted(self):
    Vote.objects.create(party_name=party_name[party_list[0]],
                        age_group=age_list[0],
                        gender=gender_list[0],
                        ip_address="127.0.0.0",)
    response = self.client.post(reverse('votes:vote',
                               kwargs={"party": party_list[1],
                                       "age": age_list[1],
                                       "gender": gender_list[1]}))
    self.assertEqual(response.status_code, 302)
    vote = Vote.objects.all()
    self.assertEqual(vote.count(), 2)
    self.assertEqual(vote.first().party_name, party_name[party_list[0]])
    self.assertEqual(vote.first().age_group, age_list[0])
    self.assertEqual(vote.first().gender, gender_list[0])
    self.assertEqual(vote.first().ip_address, "127.0.0.0")
    self.assertEqual(vote.last().party_name, party_name[party_list[1]])
    self.assertEqual(vote.last().age_group, age_list[1])
    self.assertEqual(vote.last().gender, gender_list[1])
    self.assertEqual(vote.last().ip_address, "127.0.0.1")
    response = self.client.get(response.url)
    self.assertTemplateUsed(response, "votes/index.html")
  
  def test_voted_2days(self):
    date = datetime(2022, 1, 1)
    Vote.objects.create(party_name=party_name[party_list[-1]],
                        age_group=age_list[-1],
                        gender=gender_list[-1],
                        ip_address="127.0.0.1",)
    
    Vote.objects.filter(party_name=party_name[party_list[-1]]).update(vote_datetime=date)
    response = self.client.post(reverse('votes:vote',
                               kwargs={"party": party_name[party_list[-2]],
                                       "age": age_list[-2],
                                       "gender": gender_list[-2]}))
    self.assertEqual(response.status_code, 302)
    vote = Vote.objects.all()
    self.assertEqual(vote.count(), 2)
    self.assertEqual(vote.first().ip_address, vote.last().ip_address)
    self.assertEqual(vote.first().party_name, party_name[party_list[-1]])
    self.assertEqual(vote.first().age_group, age_list[-1])
    self.assertEqual(vote.first().gender, gender_list[-1])
    self.assertEqual(vote.last().party_name, party_name[party_list[-2]])
    self.assertEqual(vote.last().age_group, age_list[-2])
    self.assertEqual(vote.last().gender, gender_list[-2])
    response = self.client.get(response.url)
    self.assertTemplateUsed(response, "votes/index.html")