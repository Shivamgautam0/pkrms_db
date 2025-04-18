from django.db import models
from django.forms import ValidationError
from .link import Link
class RoadHazard(models.Model):
    year = models.CharField(max_length=255, null=False, blank=False, db_column='year')
    admin_code = models.CharField(max_length=255, null=False, blank=False, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo')
    chainage_from = models.CharField(max_length=255, null=False, blank=False, db_column='chainageFrom')
    chainage_to = models.CharField(max_length=255, null=False, blank=False, db_column='chainageTo')
    hazard_type = models.CharField(max_length=255, null=False, blank=False, db_column='hazardType')
    hazard_rating = models.CharField(max_length=255, null=False, blank=False, db_column='hazardRating')
    length = models.CharField(max_length=255, null=True, blank=True, db_column='length')
    x_start_dd = models.CharField(max_length=255, null=True, blank=True, db_column='xStartDd')
    y_start_dd = models.CharField(max_length=255, null=True, blank=True, db_column='yStartDd')
    x_end_dd = models.CharField(max_length=255, null=True, blank=True, db_column='xEndDd')
    y_end_dd = models.CharField(max_length=255, null=True, blank=True, db_column='yEndDd')
    
    def clean(self):
        required_fields = [
            self.admin_code,
            self.link_no,
            self.chainage_from,
            self.chainage_to,
            self.hazard_type,
            self.hazard_rating
        ]
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'RoadHazard'
        verbose_name = 'Road Hazard'
        verbose_name_plural = 'Road Hazards'
