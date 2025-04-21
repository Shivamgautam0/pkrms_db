from django.db import models
from django.core.exceptions import ValidationError

class CODE_AN_UnitCostsRM(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=True, blank=True,db_column='adminCode')
    rm_activity = models.CharField(max_length=100, null=True, blank=True, db_column='rmActivity')
    terrain = models.CharField(max_length=255, null=True, blank=True, db_column='terrain')
    unit = models.CharField(max_length=100, null=True, blank=True, db_column='unit')
    rm_networkelement = models.CharField(max_length=255, null=True, blank=True, db_column='rmNetworkElement')
    rm_category = models.CharField(max_length=100, null=True, blank=True, db_column='rmCategory')
    rm_priority = models.CharField(max_length=255, null=True, blank=True, db_column='rmPriority')
    rm_quantity = models.CharField(max_length=255, null=True, blank=True, db_column='rmQuantity')
    rm_unitcost = models.CharField(max_length=255, null=True, blank=True, db_column='rmUnitcost')
    rm_onoff = models.CharField(max_length=100, null=True, blank=True, db_column='rmOnoff')
    rm_reportcategory = models.CharField(max_length=100, null=True, blank=True, db_column='rmReportCategory')

    def clean(self):
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.rm_activity:
            errors['rm_activity'] = 'This field is required.'
        if not self.terrain:
            errors['terrain'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'code_an_unitcostsrm'
        verbose_name = 'Code An Unitcostsrm'
        verbose_name_plural = 'Code An Unitcostsrms'
