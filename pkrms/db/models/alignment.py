from django.db import models
from django.core.exceptions import ValidationError
from .link import Link
class Alignment(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255,null=False, blank=False, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE,null=True, blank=True, db_column='linkNo',to_field='link_no')
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
        # Validate required fields
        errors = {}
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:
            errors['link_no'] = 'This field is required.'
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
                if abs(chainage_value - link_length_m) > 50:
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
        return f"{self.link_no}"  

    class Meta:
        db_table = 'Alignment'
        verbose_name = 'Alignment'
        verbose_name_plural = 'Alignments'


