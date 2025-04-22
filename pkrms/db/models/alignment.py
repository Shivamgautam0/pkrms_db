from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Max
from .link import Link

class Alignment(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=False, blank=False, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo', to_field='link_no')
    chainage = models.CharField(max_length=255, null=False, blank=False, db_column='chainage')
    chainage_rb = models.CharField(max_length=255, null=True, blank=True, db_column='chainageRb')
    gps_point_north_deg = models.CharField(max_length=255, null=True, blank=True, db_column='gpsPointNorthDeg')
    gps_point_north_min = models.CharField(max_length=255, null=True, blank=True, db_column='gpsPointNorthMin')
    gps_point_north_sec = models.CharField(max_length=255, null=True, blank=True, db_column='gpsPointNorthSec')
    gps_point_east_deg = models.CharField(max_length=255, null=True, blank=True, db_column='gpsPointEastDeg')
    gps_point_east_min = models.CharField(max_length=255, null=True, blank=True, db_column='gpsPointEastMin')
    gps_point_east_sec = models.CharField(max_length=255, null=True, blank=True, db_column='gpsPointEastSec')
    section_wkt_line_string = models.CharField(max_length=500, null=True, blank=True, db_column='sectionWKTLineString')
    east = models.CharField(max_length=255, null=True, blank=True, db_column='east')
    north = models.CharField(max_length=255, null=True, blank=True, db_column='north')
    hemis_ns = models.CharField(max_length=255, null=True, blank=True, db_column='hemisNS')


    def clean(self):
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:
            errors['link_no'] = 'This field is required.'
        if not self.chainage:
            errors['chainage'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)
    
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
                        f" exceeds by more than 50m."
                    )
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
        return f"{self.link_no}"  

    class Meta:
        db_table = 'Alignment'
        verbose_name = 'Alignment'
        verbose_name_plural = 'Alignments'