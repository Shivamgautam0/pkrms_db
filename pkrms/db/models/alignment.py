from django.db import models
from django.forms import ValidationError
from .link import Link
class Alignment(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255,null=False, blank=False, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE,null=True, blank=True, db_column='linkNo')
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
        required_fields = [
            self.admin_code,
            self.link_no,
            self.chainage
        ] 
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled") 

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.link_no}"  

    class Meta:
        db_table = 'Alignment'
        verbose_name = 'Alignment'
        verbose_name_plural = 'Alignments'


