from django.db import models
from datetime import date
from django.contrib.auth.models import User



class Fazenda(models.Model):
    fazenda = models.CharField(('Fazenda'), max_length=15, default=None, null=True, blank=True)

    def __str__(self):
        return u"%s" % self.fazenda
# produto_unid = models.IntegerField(('Prod Un'), default=0, null=True, blank=True)


class Animal(models.Model):
    animal = models.CharField(('Animal'), unique=True, max_length=15, default=None, null=True, blank=True)
    def __str__(self):
        return u"%s" % self.animal


# class Totais(models.Model):
#     data = models.DateField(('Data'), auto_now_add=True, null=True)
#     modificado = models.DateField(('Modificado em'), auto_now=True)
#     fazenda = models.ForeignKey('Fazenda', null=True, blank=True, on_delete=models.CASCADE)
#     animal = models.ForeignKey('Animal', null=True, blank=True, on_delete=models.CASCADE)
#     total_entrada = models.IntegerField(default=None, null=True, blank=False)
#     total_saida = models.IntegerField(default=None, null=True, blank=False)
#     def __str__(self):
#         return u"%s" % self.fazenda

class Movimento(models.Model):
    tipo_movimento = models.CharField(('Movimentação'), unique=True, max_length=15, default=None, null=True, blank=True)
    def __str__(self):
        return u"%s" % self.tipo_movimento


class Quantidade(models.Model):
    tipo_movimento = models.ForeignKey('Movimento', null=False, blank=True, on_delete=models.CASCADE)
    fazenda = models.ForeignKey('Fazenda', null=False, blank=True, on_delete=models.CASCADE)
    animal = models.ForeignKey('Animal', null=False, blank=True, on_delete=models.CASCADE)
    data = models.DateField(('Data'), auto_now_add=True, null=True)
    modificado = models.DateTimeField(('Modificado em'), auto_now=True)
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE)
    entrada = models.IntegerField(('Entrada'), default=0, null=True, blank=True)
    saida = models.IntegerField(('Saida'), default=0, null=True, blank=True)
    obs = models.CharField(('Observação'), max_length=255, null=True, blank=True)
    def __str__(self):
        return u"%s" % self.fazenda


# class Saldo(models.Model):
#     data = models.DateField(('Data'), auto_now_add=True, null=True)
#     modificado = models.DateField(('Modificado em'), auto_now=True)
#     fazenda = models.ForeignKey('Fazenda', null=True, blank=True, on_delete=models.CASCADE)
#     animal = models.ForeignKey('Animal', null=True, blank=True, on_delete=models.CASCADE)
#     total = models.FloatField(default=None, null=True, blank=False)
#     def __str__(self):
#         return u"%s" % self.fazenda

# 
# class Nf_e(models.Model):
#     id = models.AutoField(primary_key=True)
#     author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE)
#     fazenda = models.ForeignKey('Fazenda', null=False, blank=True, on_delete=models.CASCADE)
#     nr_nota = models.IntegerField("Numero NF-e")
#     data = models.DateField(('Data'), null=False, blank=True)
#     def __str__(self):
#         return u"%s" % self.fazenda


