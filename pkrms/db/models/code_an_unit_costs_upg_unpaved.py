from django.db import models
from django.core.exceptions import ValidationError

class CODE_AN_UnitCostsUPGUnpaved(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=True, blank=True,db_column='adminCode')
    pave_width1 = models.CharField(max_length=255, null=True, blank=True, db_column='paveWidth1')
    upg_unitcost = models.CharField(max_length=255, null=True, blank=True, db_column='upgUnitcost')

    def clean(self):
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.pave_width1:    
            errors['pave_width1'] = 'This field is required.'
        
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'code_an_unitcostsupgunpaved'
        verbose_name = 'Code An Unitcostsupgunpaved'
        verbose_name_plural = 'Code An Unitcostsupgunpaveds'
