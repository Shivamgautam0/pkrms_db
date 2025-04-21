from django.db import models
from django.core.exceptions import ValidationError

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
        # Validate required fields
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:    
            errors['link_no'] = 'This field is required.'   
        if not self.culvert_number:
            errors['culvert_number'] = 'This field is required.'
        if not self.chainage:
            errors['chainage'] = 'This field is required.'
        
        if errors:
            raise ValidationError(errors)

        # Validate chainage if provided
        if self.chainage:
            try:
                chainage_value = float(self.chainage)
                # Get link length in meters (assuming it's stored in kilometers)
                link_length_km = float(self.link_no.link_length_actual)
                link_length_m = link_length_km * 1000  # Convert km to meters
                
                # Check if the chainage is within 50 meters of the link length
                if chainage_value > link_length_m + 50:
                    error_msg = (
                        f"⚠️ Chainage Length Mismatch: Your chainage ({chainage_value:.1f}m) "
                        f"exceeds the actual road length ({link_length_m:.1f}m) by more than 50m. "
                        f"Please ensure the chainage is within 50m of the actual road length."
                    )
                    raise ValidationError(error_msg)
            except (ValueError, TypeError, AttributeError) as e:
                raise ValidationError(f"Invalid chainage value: {str(e)}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.culvert_number}"
    
    class Meta:
        db_table = 'culvertinventory'
        verbose_name = 'Culvert Inventory'
        verbose_name_plural = 'Culvert Inventories'
