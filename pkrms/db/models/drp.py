from django.db import models
from django.forms import ValidationError    
from .link import Link
class DRP(models.Model):
    admin_code = models.CharField(max_length=255, null=False, blank=False, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo')
    drp_num = models.CharField(max_length=255, null=False, blank=False, db_column='drpNum')
    chainage = models.CharField(max_length=255, null=True, blank=True, db_column='chainage')
    drp_order = models.CharField(max_length=255, null=True, blank=True, db_column='drpOrder')
    drp_length = models.CharField(max_length=255, null=True, blank=True, db_column='drpLength')
    drp_north_deg = models.CharField(max_length=255, null=True, blank=True, db_column='drpNorthDeg')
    drp_north_min = models.CharField(max_length=255, null=True, blank=True, db_column='drpNorthMin')
    drp_north_sec = models.CharField(max_length=255, null=True, blank=True, db_column='drpNorthSec')
    drp_east_deg = models.CharField(max_length=255, null=True, blank=True, db_column='drpEastDeg')
    drp_east_min = models.CharField(max_length=255, null=True, blank=True, db_column='drpEastMin')
    drp_east_sec = models.CharField(max_length=255, null=True, blank=True, db_column='drpEastSec')
    drp_type = models.CharField(max_length=255, null=True, blank=True, db_column='drpType')
    drp_desc = models.CharField(max_length=255, null=True, blank=True, db_column='drpDesc')
    drp_comment = models.CharField(max_length=255, null=True, blank=True, db_column='drpComment')
    
    def clean(self):
        required_fields = [
            self.admin_code,
            self.link_no,
            self.drp_num
        ]
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.drp_num}"
    
    class Meta:
        db_table = 'DRP'
        verbose_name = 'DRP'
        verbose_name_plural = 'DRP'
