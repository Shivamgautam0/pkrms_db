from django.db import models
from django.forms import ValidationError
from .link import Link
class CulvertCondition(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    year = models.CharField(max_length=255, db_column='year')
    admin_code = models.CharField(max_length=255, db_column='adminCode')    
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo')
    culvert_number = models.CharField(max_length=100, db_column='culvertNumber')
    cond_barrel = models.CharField(max_length=255, null=True, blank=True, db_column='condBarrel')
    cond_inlet = models.CharField( max_length=255,null=True, blank=True, db_column='condInlet')
    cond_outlet = models.CharField(max_length=100,null=True, blank=True, db_column='condOutlet')
    silting = models.CharField( max_length=255,null=True, blank=True, db_column='silting')
    overtopping = models.CharField(max_length=100,null=True, blank=True, db_column='overtopping')
    analysisbaseyear = models.CharField(max_length=255, null=True, blank=True, db_column='analysisBaseYear')
    surveyby = models.CharField(max_length=255, null=True, blank=True, db_column='surveyBy')
#  year,admin_code, Link_No, Culvert_Number
    def clean(self):
        required_fields = [
            self.year,
            self.admin_code,
            self.link_no,
            self.culvert_number
        ]
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year}"
    
    class Meta:
        db_table = 'culvertcondition'
        verbose_name = 'Culvertcondition'
        verbose_name_plural = 'Culvertconditions'
