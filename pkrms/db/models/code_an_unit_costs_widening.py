from django.db import models
from django.core.exceptions import ValidationError

class CODE_AN_UnitCostsWidening(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=True, blank=True,db_column='adminCode')
    cumesa1 = models.CharField(max_length=255, null=True, blank=True, db_column='cumesa1')
    cumesa2 = models.CharField(max_length=255, null=True, blank=True, db_column='cumesa2')
    wideningsealed_unitcost = models.CharField(max_length=255, null=True, blank=True, db_column='wideningSealedUnitcost')
    wideningunsealed_unitcost = models.CharField(max_length=255, null=True, blank=True, db_column='wideningUnsealedUnitcost')
    def clean(self):
        # Validate required fields
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.cumesa1:
            errors['cumesa1'] = 'This field is required.'
        if not self.cumesa2:
            errors['cumesa2'] = 'This field is required.'
        
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):    
        self.full_clean()
        super().save(*args, **kwargs)   
        
    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'code_an_unitcostswidening'
        verbose_name = 'Code An Unitcostswidening'
        verbose_name_plural = 'Code An Unitcostswidenings'
