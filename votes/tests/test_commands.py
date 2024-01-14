from datetime import date
from django.core.management import call_command
from django.test import TestCase

from votes.models import Vote, Result

class TestDate_Create_Test(TestCase):
  def test_testdata_create_command(self):
    call_command("testdata_create",  2023, 1, 1, 2023, 1, 2)
    votes = Vote.objects.filter(test_vote_date__gte=date(2023, 1, 1))
    self.assertEqual(votes.count(), 2000)
        
class Vote_Result_Test(TestCase):
  def test_result_create_command(self):
    call_command("testdata_create",  2024, 1, 1, 2024, 1, 2)
    call_command("vote_result",  "-s 2024-01-01", "-e 2024-01-02")
    vote1 = Vote.objects.filter(test_vote_date="2024-01-01").filter(party_name="自民")
    result1 = Result.objects.filter(vote_date="2024-01-01").get(party_name="自民")
    self.assertEqual(vote1.count(), result1.num_votes)
    vote2 = Vote.objects.filter(test_vote_date="2024-01-02").filter(party_name="立民")
    result2 = Result.objects.filter(vote_date="2024-01-02").get(party_name="立民")
    self.assertEqual(vote2.count(), result2.num_votes)