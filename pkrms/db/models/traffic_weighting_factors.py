from django.db import models
from django.forms import ValidationError

class TrafficWeightingFactors(models.Model):
    veh_type = models.CharField(max_length=255, null=False, blank=False, db_column='vehType')
    wti_factor = models.CharField(max_length=255, null=True, blank=True, db_column='wtiFactor')
    vdf_factor = models.CharField(max_length=255, null=True, blank=True, db_column='vdfFactor')

    def clean(self):
        required_fields = [
            self.veh_type,
        ]
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)   

    def __str__(self):
        return self.veh_type
    
    class Meta:
        db_table = 'traffic_weighting_factors'
        verbose_name = 'Traffic Weighting Factors'
        verbose_name_plural = 'Traffic Weighting Factors'
