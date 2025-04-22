from django.db import models
from django.core.exceptions import ValidationError

class CODE_AN_UnitCostsPERUnpaved(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=True, blank=True,db_column='adminCode')
    reg_unitcost = models.CharField(max_length=255, null=True, blank=True, db_column='regUnitcost')
    res_unitcost = models.CharField(max_length=255, null=True, blank=True, db_column='resUnitcost')

    def clean(self):
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'code_an_unitcostsperunpaved'
        verbose_name = 'Code An Unitcostsperunpaved'
        verbose_name_plural = 'Code An Unitcostsperunpaveds'
