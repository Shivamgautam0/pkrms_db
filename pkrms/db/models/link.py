from django.db import models
from django.forms import ValidationError

class Link(models.Model):
    id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.IntegerField(null=True, blank=True,db_column='adminCode')
    link_no = models.BigIntegerField(null=False, blank=False,db_column='linkNo')
    link_code = models.IntegerField(null=False, blank=False, db_column='linkCode')
    link_name = models.CharField(max_length=255, db_column='linkName')
    status = models.CharField(max_length=255, null=True, blank=True, db_column='status')
    function = models.CharField(max_length=255, null=True, blank=True, db_column='function')
    class_field = models.CharField(max_length=255,db_column='class')
    link_length_official = models.FloatField(null=True, blank=True, db_column='linkLengthOfficial')
    link_length_actual = models.FloatField(db_column='linkLengthActual')
    wti = models.IntegerField(null=True, blank=True, db_column='wti')
    mca2 = models.IntegerField(null=True, blank=True, db_column='mca2')
    mca3 = models.IntegerField(null=True, blank=True, db_column='mca3')
    mca4 = models.IntegerField(null=True, blank=True, db_column='mca4')
    mca5 = models.IntegerField(null=True, blank=True, db_column='mca5')
    project_number = models.FloatField(null=True, blank=True, db_column='projectNumber')
    cumesa = models.FloatField(null=True, blank=True, db_column='cumesa')
    esa0 = models.FloatField(null=True, blank=True, db_column='esa0')
    aadt = models.IntegerField(null=True, blank=True, db_column='aadt')
    accessstatus = models.FloatField(null=True, blank=True, db_column='accessStatus')

    # @classmethod
    # def create_with_admin_code(cls, province_code, kabupaten_code, **kwargs):
    #     admin_code = int(f"{province_code}{kabupaten_code:02d}")
    #     return cls(Province_Code=province_code, Kabupaten_Code=kabupaten_code, **kwargs)

    def clean(self):
        required_fields = [
            self.admin_code,
            self.link_no,
            self.link_code,
            self.link_name,
            # self.class_field,
            self.link_length_actual
        ]
        if any(field is None for field in required_fields):
            raise ValidationError("All required fields must be filled")
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.link_no}"
    
    class Meta:
        db_table = 'link'
        verbose_name = 'Link'
        verbose_name_plural = 'Links'
