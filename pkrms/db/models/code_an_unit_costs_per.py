from django.db import models
from django.core.exceptions import ValidationError

class CODE_AN_UnitCostsPER(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=True, blank=True,db_column='adminCode')

    overlay_thick = models.CharField(max_length=255, null=True, blank=True, db_column='overlayThick')
    per_unitcost = models.CharField(max_length=255, null=True, blank=True, db_column='perUnitcost')

    def clean(self):
        # Validate required fields
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.overlay_thick:
            errors['overlay_thick'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)   
    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'code_an_unitcostsper'
        verbose_name = 'Code An Unitcostsper'
        verbose_name_plural = 'Code An Unitcostspers'
