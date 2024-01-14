from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError

from votes.models import Vote, Result


class Command(BaseCommand):
  help = "Create vote results data from the day before today"
  
  def add_arguments(self, parser):
    parser.add_argument('-s', '--start_day')
    parser.add_argument('-e', '--end_day')
  
  def handle(self, *args, **options):
    parties = [
    "自民", "立民", "維新", "公明",
    "国民", "共産", "その他", "白紙",
    ] 
    
    if options['start_day'] and options['end_day']:
      s_day = options['start_day'].split('-')
      e_day = options['end_day'].split('-')
      
      start_day = date(
        int(s_day[0]), int(s_day[1]), int(s_day[2]))
      end_day = date(
        int(e_day[0]), int(e_day[1]), int(e_day[2]))
      
      while True:
        if not Result.objects.filter(vote_date=start_day):
          votes = Vote.objects.filter(test_vote_date=start_day)
        
          for party in parties:
            count = votes.filter(party_name=party).count()
            result = Result.objects.create(
              vote_date=start_day,
              party_name=party,
              num_votes=count
            )
          
        start_day += timedelta(days=1)
        print('next!')
        if start_day > end_day:
          print('finish!')
          break