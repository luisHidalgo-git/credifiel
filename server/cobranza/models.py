from django.db import models

class ListaCobroDetalle2022(models.Model):
    idListaCobro = models.IntegerField()
    idCredito = models.IntegerField()
    consecutivoCobro = models.CharField(max_length=20)
    idBanco = models.IntegerField()
    montoExigible = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrar = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fechaCobroBanco = models.DateTimeField(null=True, blank=True)
    idRespuestaBanco = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'ListaCobroDetalle2022'
        
    def __str__(self):
        return f"Lista Cobro {self.idListaCobro} - Crédito {self.idCredito}"

class ListaCobroDetalle2023(models.Model):
    idListaCobro = models.IntegerField()
    idCredito = models.IntegerField()
    consecutivoCobro = models.CharField(max_length=20)
    idBanco = models.IntegerField()
    montoExigible = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrar = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fechaCobroBanco = models.DateTimeField(null=True, blank=True)
    idRespuestaBanco = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'ListaCobroDetalle2023'
        
    def __str__(self):
        return f"Lista Cobro {self.idListaCobro} - Crédito {self.idCredito}"

class ListaCobroDetalle2024(models.Model):
    idListaCobro = models.IntegerField()
    idCredito = models.IntegerField()
    consecutivoCobro = models.CharField(max_length=20)
    idBanco = models.IntegerField()
    montoExigible = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrar = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fechaCobroBanco = models.DateTimeField(null=True, blank=True)
    idRespuestaBanco = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'ListaCobroDetalle2024'
        
    def __str__(self):
        return f"Lista Cobro {self.idListaCobro} - Crédito {self.idCredito}"

class ListaCobroDetalle2025(models.Model):
    idListaCobro = models.IntegerField()
    idCredito = models.IntegerField()
    consecutivoCobro = models.CharField(max_length=20)
    idBanco = models.IntegerField()
    montoExigible = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrar = models.DecimalField(max_digits=10, decimal_places=2)
    montoCobrado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    fechaCobroBanco = models.DateTimeField(null=True, blank=True)
    idRespuestaBanco = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        db_table = 'ListaCobroDetalle2025'
        
    def __str__(self):
        return f"Lista Cobro {self.idListaCobro} - Crédito {self.idCredito}"