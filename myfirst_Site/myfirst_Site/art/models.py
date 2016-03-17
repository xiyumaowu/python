from django.db import models

# Create your models here.
class TB1(models.Model):
	content = models.CharField(max_length = 500)
	submit_date = models.DateTimeField('auto_now_add')