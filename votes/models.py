from django.db import models

class Vote(models.Model):
  party_name = models.CharField('political party name', max_length=50)
  vote_datetime = models.DateTimeField('datetime voted', auto_now_add=True)
  age_group = models.CharField("age group from teens to over 80s", 
                               blank=True, max_length=50)
  gender = models.CharField('man or woman or no answer', 
                            blank=True, max_length=50)
  ip_address = models.GenericIPAddressField()
  test_vote_date = models.DateField(
    'test date for test data', null=True)
  
  def __str__(self):
    return f'{self.party_name}/{self.test_vote_date}'
  
  
class Result(models.Model):
  vote_date = models.DateField('test_vote_date')
  party_name = models.CharField('political party name', max_length=50)
  num_votes = models.IntegerField()
  
  def __str__(self):
    return f'{self.vote_date}/{self.party_name}/{self.num_votes}'