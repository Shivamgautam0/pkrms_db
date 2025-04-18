from django.db import models
from django.forms import ValidationError

from .link import Link

class CulvertInventory(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255,db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
    culvert_number = models.CharField(max_length=255,db_column='culvertNumber')
    chainage = models.CharField(max_length=255,db_column='chainage')
    drp_from = models.CharField( max_length=255,null=True, blank=True, db_column='drpFrom')
    offset_from = models.CharField( max_length=255,null=True, blank=True, db_column='offsetFrom')
    culvert_length = models.CharField( max_length=255,null=True, blank=True, db_column='culvertLength')
    culvert_type = models.CharField( max_length=255,null=True, blank=True, db_column='culvertType')
    number_opening = models.CharField(max_length=255, null=True, blank=True, db_column='numberOpening')
    culvert_width = models.CharField(max_length=255, null=True, blank=True, db_column='culvertWidth')
    culvert_heigth = models.CharField(max_length=255, null=True, blank=True, db_column='culvertHeight')
    inlet_type = models.CharField( max_length=255,null=True, blank=True, db_column='inletType')
    outlet_type = models.CharField(max_length=255, null=True, blank=True, db_column='outletType')

# admin_code, Link_No, Culvert_Number, Chainage
    def clean(self):
        required_fields = [
            self.admin_code,
            self.link_no,
            self.culvert_number,
            self.chainage
        ]
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.culvert_number}"
    
    class Meta:
        db_table = 'culvertinventory'
        verbose_name = 'Culvert Inventory'
        verbose_name_plural = 'Culvert Inventories'
