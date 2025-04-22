from django.db import models
from django.core.exceptions import ValidationError  
from .link import Link

class DRP(models.Model):
    admin_code = models.CharField(max_length=255, null=False, blank=False, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
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
        # Validate required fields
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:    
            errors['link_no'] = 'This field is required.'
        if not self.drp_num:
            errors['drp_num'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)
        
        # Validate chainage if provided
    
        try:
            chainage_value = float(self.chainage)
        except (ValueError, TypeError):
            raise ValidationError("Invalid chainage value: Must be a number.")
    
        is_last = getattr(self, 'is_last_in_link', False)
    
        if is_last:
            try:
                link_length_m = float(self.link_no.link_length_actual) * 1000
                if abs(chainage_value - link_length_m) > 50:
                    raise ValidationError(
                        f"⚠️ Chainage Length Mismatch: The Difference Between final chainage : ({chainage_value:.1f}m) and the actual road length : ({link_length_m:.1f}m) "
                        f"exceeds by more than 50m."                    )
            except (ValueError, TypeError, AttributeError) as e:
                raise ValidationError(f"Invalid or missing link length data for validation: {str(e)}")

    @staticmethod
    def _is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.drp_num}"
    
    class Meta:
        db_table = 'DRP'
        verbose_name = 'DRP'
        verbose_name_plural = 'DRP'
