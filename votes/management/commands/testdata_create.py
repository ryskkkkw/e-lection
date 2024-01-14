from datetime import date, timedelta
import random

from django.core.management.base import BaseCommand, CommandError

from votes.models import Vote


class Command(BaseCommand):
  help = "Create test data of votes for monthly"
  
  def add_arguments(self, parser):
    parser.add_argument('days', nargs='+', type=int)
  
  def handle(self, *args, **options):
    days = options['days']
    start_day = date(days[0], days[1], days[2])
    end_day = date(days[3], days[4], days[5])
    
    days = []
    while True:
      if start_day > end_day:
        break
      days.append(start_day)
      start_day += timedelta(days=1)
    
    def create_datas():
      party_list = [
        '自民', '立民', '維新', '公明',
        '国民', '共産', 'その他', '白紙',
        ]
      age_list = [
          '10代', '20代', '30代', '40代',
          '50代', '60代', '70代', '80代以上',
        ]   
      gender_list = [
        '男', '女', 'LGBTQ', '回答しない',]

      parties = random.choices(party_list,
                              [20,3,4,4,1,1,2,65],
                              k=1000)
      ages = random.choices(age_list,
                            [3,7,7,4,4,2,1,1],
                            k=1000)
      genders = random.choices(gender_list,
                            [45,45,6,4], 
                            k=1000)
      
      datas = []
      for data in zip(parties, ages, genders):
        datas.append(data)
      print('datas', datas)
      
      return datas
      
    for day in days:
      datas = create_datas()
      print(datas)
      for data in datas:
        Vote.objects.create(
        party_name=data[0],
        age_group=data[1],
        gender=data[2],
        test_vote_date=day,
        ip_address='test',
      )  