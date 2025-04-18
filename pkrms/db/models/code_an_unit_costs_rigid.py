from django.db import models

class CODE_AN_UnitCostsRIGID(models.Model):
    # id = models.AutoField(primary_key=True,db_column='id')
    admin_code = models.CharField(max_length=255, null=True, blank=True,db_column='adminCode')
    code = models.CharField(max_length=255, null=True, blank=True, db_column='code')
    perunitcost = models.CharField(max_length=255, null=True, blank=True, db_column='perUnitcost')
    rehunitcost = models.CharField(max_length=255, null=True, blank=True, db_column='rehUnitcost')

    def __str__(self):
        return f"{self.admin_code}"
    
    class Meta:
        db_table = 'code_an_unitcostsrigid'
        verbose_name = 'Code An Unitcostsrigid'
        verbose_name_plural = 'Code An Unitcostsrigids'
