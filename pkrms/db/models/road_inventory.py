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
    row = models.CharField(max_length=255, db_column='row')
    pave_width = models.CharField(max_length=255, db_column='paveWidth')
    pave_type = models.CharField(max_length=255, db_column='paveType')
    
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
        required_fields = [
            self.admin_code,
            self.link_no,
            self.chainagefrom,
            self.chainageto,
            self.pave_width,
            self.row,
            self.pave_type,
        ]   
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")
        
        # Validate that chainagefrom is less than chainageto
        if self.chainagefrom >= self.chainageto:
            raise ValidationError("ChainageFrom must be less than ChainageTo")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'roadinventory'
        verbose_name = 'Road Inventory'
        verbose_name_plural = 'Road Inventories'

