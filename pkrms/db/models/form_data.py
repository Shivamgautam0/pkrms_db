from django.db import models
from django.core.exceptions import ValidationError

class FormData(models.Model):
    # id = models.AutoField(primary_key=True, db_column='id')
    status = models.CharField(max_length=50, db_column='status')
    selected_province = models.CharField(max_length=100, db_column='selectedProvince')
    selected_kabupaten = models.CharField(max_length=100, null=True, blank=True, db_column='selectedKabupaten')
    lg_name = models.CharField(max_length=100, db_column='lgName')
    email = models.EmailField(db_column='email')
    phone = models.CharField(max_length=19, db_column='phone')

    def clean(self):
        required_fields = [
            self.status,
            self.selected_province,
            self.lg_name,
            self.email,
            self.phone
        ]
        if any(field is None or field == '' for field in required_fields):
            raise ValidationError("All required fields must be filled")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.lg_name} - {self.selected_province}"

    class Meta:
        db_table = 'form_data'
        verbose_name = 'Form Data'
        verbose_name_plural = 'Form Data'