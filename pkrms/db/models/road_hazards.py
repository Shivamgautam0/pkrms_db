from django.db import models
from django.core.exceptions import ValidationError
from .link import Link

class RoadHazard(models.Model):
    year = models.CharField(max_length=255, null=False, blank=False, db_column='year')
    admin_code = models.CharField(max_length=255, null=False, blank=False, db_column='adminCode')
    link_no = models.ForeignKey(Link, on_delete=models.CASCADE, null=True, blank=True, db_column='linkNo',to_field='link_no')
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
        errors = {}
        if not self.year:
            errors['year'] = 'This field is required. Please enter a valid year.'  # More descriptive message
        if not self.admin_code:
            errors['admin_code'] = 'This field is required.'
        if not self.link_no:
            errors['link_no'] = 'This field is required.'
        if not self.chainage_from:
            errors['chainage_from'] = 'This field is required.'
        if not self.chainage_to:
            errors['chainage_to'] = 'This field is required.'
        if errors:
            raise ValidationError(errors)       
        # Validate that chainage_from is less than chainage_to
        if float(self.chainage_from) >= float(self.chainage_to):
            raise ValidationError("ChainageFrom must be less than ChainageTo")

        # Get all existing records for this link_no
        existing_records = RoadHazard.objects.filter(link_no=self.link_no)
        if not existing_records.exists():
            # First record for this link, no need to check overlaps
            return

        # Check for overlaps with existing records
        current_from = float(self.chainage_from)
        current_to = float(self.chainage_to)
        
        for record in existing_records:
            if record.pk == self.pk:
                continue  # Skip self
                
            existing_from = float(record.chainage_from)
            existing_to = float(record.chainage_to)
            
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

        # Get the maximum chainage value from all records (including this one)
        all_chainage_values = [float(r.chainage_to) for r in existing_records] + [current_to]
        max_chainage = max(all_chainage_values)
        
        # Only check link length if this is the last record for this link_no
        # or if this record's chainage_to is the highest among all records
        if current_to == max_chainage:
            try:
                # Get link length in meters (assuming it's stored in kilometers)
                link_length_km = float(self.link_no.link_length_actual)
                link_length_m = link_length_km * 1000  # Convert km to meters
                
                # Check if the difference is more than 50 meters
                difference = abs(max_chainage - link_length_m)
                if difference > 50:
                    error_msg = (
                        f"⚠️ Chainage Length Mismatch: Your total chainage ({max_chainage:.1f}m) "
                        f"differs from the actual road length ({link_length_m:.1f}m) by {difference:.1f}m. "
                        f"Please ensure all segments are properly connected and the total length is within 50m of the actual road length."
                    )
                    raise ValidationError(error_msg)
            except (ValueError, TypeError, AttributeError) as e:
                raise ValidationError(f"Invalid link length value: {str(e)}")
        else:
            # This is not the last record, so we don't need to check the link length
            pass

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'RoadHazard'
        verbose_name = 'Road Hazard'
        verbose_name_plural = 'Road Hazards'
