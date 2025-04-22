from django.db import models
from django.core.exceptions import ValidationError
from .link import Link
class CulvertCondition(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    year = models.CharField(max_length=255, db_column='year')
    admin_code = models.CharField(max_length=255, db_column='adminCode')    
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
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
        # Validate required fields
        errors = {}
        if not self.year:
            errors['year'] = 'This field is required.'
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:
            errors['link_no'] = 'This field is required.'
        if not self.culvert_number:
            errors['culvert_number'] = 'This field is required.'

        if errors:
            raise ValidationError(errors)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.year}"
    
    class Meta:
        db_table = 'culvertcondition'
        verbose_name = 'Culvertcondition'
        verbose_name_plural = 'Culvertconditions'
