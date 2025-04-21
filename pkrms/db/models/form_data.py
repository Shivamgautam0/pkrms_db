from django.db import models
from django.core.exceptions import ValidationError

class FormData(models.Model):
    # id = models.AutoField(primary_key=True, db_column='id')
    status = models.CharField(max_length=50, db_column='status')
    admin_code = models.CharField(max_length=100, null=True, blank=True, db_column='adminCode')
    lg_name = models.CharField(max_length=100, db_column='lgName')
    email = models.EmailField(db_column='email')
    phone = models.CharField(max_length=19, db_column='phone')

    def clean(self):
        required_fields = [
            self.status,
            self.admin_code,
            self.lg_name,
            self.email,
            self.phone
        ]
        if any(field is None or field == '' for field in required_fields):
            raise ValidationError("All required fields must be filled")

        # Check if this admin_code and email combination already exists
        if self.admin_code and self.email:
            existing_record = FormData.objects.filter(
                admin_code=self.admin_code,
                email=self.email
            ).exclude(pk=self.pk).first()
            
            if existing_record:
                # If we're updating an existing record, that's fine
                if self.pk and self.pk == existing_record.pk:
                    return
                # If we're creating a new record with existing admin_code and email, that's also fine
                # as the save() method will handle updating the existing record
                return

    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Check if a record with this admin_code and email already exists
        existing_record = FormData.objects.filter(
            admin_code=self.admin_code,
            email=self.email
        ).exclude(pk=self.pk).first()

        if existing_record:
            # Update the existing record with new data
            existing_record.status = self.status
            existing_record.lg_name = self.lg_name
            existing_record.phone = self.phone
            existing_record.save()
            return existing_record

        super().save(*args, **kwargs)
        return self

    def __str__(self):
        return f"{self.lg_name} - {self.admin_code}"

    class Meta:
        db_table = 'form_data'
        verbose_name = 'Form Data'
        verbose_name_plural = 'Form Data'
        unique_together = ('admin_code', 'email')