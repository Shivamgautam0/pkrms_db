from django.db import models
from django.forms import ValidationError
from .link import Link

class RetainingWallInventory(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255,db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
    wall_number = models.CharField(max_length=255, null=True, blank=True, db_column='wallNumber')
    wall_side = models.CharField(max_length=255, null=True, blank=True, db_column='wallSide')
    chainagefrom = models.CharField( max_length=255,null=True, blank=True, db_column='chainageFrom')
    drp_from = models.CharField( max_length=255,null=True, blank=True, db_column='drpFrom')
    offset_from = models.CharField(max_length=255,null=True, blank=True, db_column='offsetFrom')
    length = models.CharField( max_length=255,null=True, blank=True, db_column='length')
    wall_material = models.CharField(max_length=255, null=True, blank=True, db_column='wallMaterial')
    wall_height = models.CharField( max_length=255,null=True, blank=True, db_column='wallHeight')
    wall_type = models.CharField(max_length=255, null=True, blank=True, db_column='wallType')

# admin_code , Link_No, Wall_Number
    def clean(self):
        required_fields = [
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
        db_table = 'retainingwallinventory'
        verbose_name = 'Retainingwallinventory'
        verbose_name_plural = 'Retainingwallinventorys'
