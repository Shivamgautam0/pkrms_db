from django.db import models
from django.core.exceptions import ValidationError
from .link import Link

class RetainingWallCondition(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    year = models.CharField(max_length=255, db_column='year')
    admin_code = models.CharField(max_length=255,db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
    wall_number = models.CharField(max_length=255,db_column='wallNumber')
    wall_mortar_m2 = models.CharField(max_length=255, null=True, blank=True, db_column='wallMortarM2')
    wall_repair_m3 = models.CharField(max_length=255, null=True, blank=True, db_column='wallRepairM3')
    wall_rebuild_m = models.CharField(max_length=255, null=True, blank=True, db_column='wallRebuildM')
    analysis_base_year = models.CharField(max_length=255, null=True, blank=True, db_column='analysisBaseYear')
    survey_by = models.CharField(max_length=255, null=True, blank=True, db_column='surveyBy')

# Year, Province_Code, Kabupaten_Code, Link_No, Wall_Number, 
    def clean(self):
        # Validate required fields
        errors = {}
        if not self.year:
            errors['year'] = 'This field is required.'
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:
            errors['link_no'] = 'This field is required.'
        if not self.wall_number:
            errors['wall_number'] = 'This field is required.'

        if errors:
            raise ValidationError(errors)
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'retainingwallcondition' 
        verbose_name = 'RetainingWallCondition'
        verbose_name_plural = 'RetainingWallConditions' 


