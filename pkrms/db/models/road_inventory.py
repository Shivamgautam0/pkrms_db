from django.db import models
from django.core.exceptions import ValidationError
from .link import Link

class RoadInventory(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, db_column='adminCode')
    # link_code = models.ForeignKey(Link, on_delete=models.CASCADE, db_column='linkCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
    chainagefrom = models.CharField(max_length=255, db_column='chainageFrom')
    chainageto = models.CharField(max_length=255, db_column='chainageTo')
    row = models.CharField(max_length=255,null=True, blank=True, db_column='row')
    pave_width = models.CharField(max_length=255,null=True, blank=True, db_column='paveWidth')
    pave_type = models.CharField(max_length=255,null=True, blank=True, db_column='paveType')
    
    drp_from = models.CharField(max_length=255, null=True, blank=True, db_column='drpFrom')
    offset_from = models.CharField(max_length=255, null=True, blank=True, db_column='offsetFrom')
    drp_to = models.CharField(max_length=255, null=True, blank=True, db_column='drpTo')
    offset_to = models.CharField(max_length=255, null=True, blank=True, db_column='offsetTo')
    should_width_l = models.CharField(max_length=255, null=True, blank=True, db_column='shoulderWidthL')
    should_width_r = models.CharField(max_length=255, null=True, blank=True, db_column='shoulderWidthR')
    should_type_l = models.CharField(max_length=255, null=True, blank=True, db_column='shoulderTypeL')
    should_type_r = models.CharField(max_length=255, null=True, blank=True, db_column='shoulderTypeR')
    drain_type_l = models.CharField(max_length=255, null=True, blank=True, db_column='drainTypeL')
    drain_type_r = models.CharField(max_length=255, null=True, blank=True, db_column='drainTypeR')
    terrain = models.CharField(max_length=255, null=True, blank=True, db_column='terrain')
    land_use_l = models.CharField(max_length=255, null=True, blank=True, db_column='landUseL')
    land_use_r = models.CharField(max_length=255, null=True, blank=True, db_column='landUseR')
    impassable = models.CharField(max_length=255, null=True, blank=True, db_column='impassable')
    impassablereason = models.CharField(max_length=255, null=True, blank=True, db_column='impassableReason')

    # @classmethod
    # def create_with_admin_code(cls, province_code, kabupaten_code, **kwargs):
    #     admin_code = int(f"{province_code}{kabupaten_code:02d}")
    #     return cls(admin_code=admin_code, **kwargs)

    def clean(self):
        # Validate required fields
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:    
            errors['link_no'] = 'This field is required.'       
        if not self.chainagefrom:
            errors['chainagefrom'] = 'This field is required.'
        if not self.chainageto:
            errors['chainageto'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)
        # Validate that chainagefrom is less than chainageto
        if float(self.chainagefrom) >= float(self.chainageto):
            raise ValidationError("ChainageFrom must be less than ChainageTo")

        # Get all existing records for this link_no
        existing_records = RoadInventory.objects.filter(link_no=self.link_no)
        if not existing_records.exists():
            # First record for this link, no need to check overlaps
            return

        # Check for overlaps with existing records
        current_from = float(self.chainagefrom)
        current_to = float(self.chainageto)
        
        for record in existing_records:
            if record.pk == self.pk:
                continue  # Skip self
                
            existing_from = float(record.chainagefrom)
            existing_to = float(record.chainageto)
            
            # Check for true overlaps (not exact matches or continuous ranges)
            if (current_from < existing_to and current_to > existing_from and
                not (current_from == existing_from and current_to == existing_to)):
                # Create a more user-friendly error message
                error_msg = (
                    f"⚠️ Chainage Overlap Error: Your segment ({current_from:.1f}m to {current_to:.1f}m) "
                    f"overlaps with an existing segment ({existing_from:.1f}m to {existing_to:.1f}m). "
                    f"Please adjust your segment to start after {existing_to:.1f}m or end before {existing_from:.1f}m."
                )
                raise ValidationError(error_msg)


        else:
            # This is not the last record, so we don't need to check the link length
            pass

    def save(self, *args, **kwargs):
        # For new records, check if this is the first record for this link
        if not self.pk:
            existing_records = RoadInventory.objects.filter(link_no=self.link_no).exists()
            if not existing_records:
                # First record for this link, skip chainage validation
                self.full_clean(exclude=['chainagefrom'])
            else:
                # Not the first record, run full validation
                self.full_clean()
        else:
            # Existing record, run full validation
            self.full_clean()
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'roadinventory'
        verbose_name = 'Road Inventory'
        verbose_name_plural = 'Road Inventories'

