from django.db import models
from django.core.exceptions import ValidationError

class TrafficWeightingFactors(models.Model):
    veh_type = models.CharField(max_length=255, null=False, blank=False, db_column='vehType')
    wti_factor = models.CharField(max_length=255, null=True, blank=True, db_column='wtiFactor')
    vdf_factor = models.CharField(max_length=255, null=True, blank=True, db_column='vdfFactor')

    def clean(self):
        # Validate required fields
        errors = {}
        if not self.veh_type:
            errors['veh_type'] = 'This field is required.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)   

    def __str__(self):
        return self.veh_type
    
    class Meta:
        db_table = 'traffic_weighting_factors'
        verbose_name = 'Traffic Weighting Factors'
        verbose_name_plural = 'Traffic Weighting Factors'
