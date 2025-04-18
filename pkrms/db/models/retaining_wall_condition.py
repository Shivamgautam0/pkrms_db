from django.db import models
from django.forms import ValidationError
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
        required_fields = [
            self.year,
            self.admin_code,
            self.link_no,
            self.wall_number
        ]
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'retainingwallcondition' 
        verbose_name = 'RetainingWallCondition'
        verbose_name_plural = 'RetainingWallConditions' 


