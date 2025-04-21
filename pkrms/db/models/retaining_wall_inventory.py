from django.db import models
from django.core.exceptions import ValidationError
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
        # Validate required fields
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:    
            errors['link_no'] = 'This field is required.'
        if not self.wall_number:
            errors['wall_number'] = 'This field is required.'
        if not self.chainagefrom:
            errors['chainagefrom'] = 'This field is required.'
        
        if errors:
            raise ValidationError(errors)
        # Check if this is not the first record for this link
        if self.pk and self.chainagefrom:  # If this is an existing record with chainage
            # Get the previous record for this link
            previous_record = RetainingWallInventory.objects.filter(
                link_no=self.link_no,
                chainagefrom__lt=self.chainagefrom
            ).order_by('-chainagefrom').first()
            
            if previous_record and float(self.chainagefrom) < float(previous_record.chainagefrom):
                raise ValidationError(f"Starting chainage ({self.chainagefrom}) must not be less than ending chainage ({previous_record.chainagefrom}) of previous record")

    def save(self, *args, **kwargs):
        # Skip chainage validation for the first record of a link
        if not self.pk:  # If this is a new record
            existing_records = RetainingWallInventory.objects.filter(link_no=self.link_no).exists()
            if not existing_records:  # If this is the first record for this link
                self.full_clean(exclude=['chainagefrom'])  # Skip chainage validation
            else:
                self.full_clean()
        else:
            self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'retainingwallinventory'
        verbose_name = 'Retainingwallinventory'
        verbose_name_plural = 'Retainingwallinventorys'
