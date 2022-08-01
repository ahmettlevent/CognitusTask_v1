from django.db import models

# Create your models here.

class LabeledData(models.Model):
    text  = models.CharField(max_length=100)
    label = models.CharField(max_length=40)

    class Meta:
        managed = True
        db_table = 'labeled_data'
    
    def __str__(self) :
        return self.text