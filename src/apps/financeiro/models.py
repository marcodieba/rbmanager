from django.db import models
from django.contrib.auth.models import User
from apps.rebanho.models import Fazenda

class Financeiro(models.Model):
    author = models.ForeignKey('auth.User', null=True, blank=True, on_delete=models.CASCADE)
    data_criacao = models.DateField(('Data Criação'), auto_now_add=True, null=True)
    modificado = models.DateField(('Modificado em'), auto_now=True)
    fazenda = models.ForeignKey(Fazenda, null=False, blank=True, on_delete=models.CASCADE)
    nr_nota = models.IntegerField("Numero NF-e")
    data = models.DateField(('Data'), null=False, blank=True)
    entrada = models.DecimalField(('Entrada'), default=("0.00"), max_digits=19, decimal_places=2)
    saida = models.DecimalField(('Saida'), default=("0.00"), max_digits=19, decimal_places=2)
    descricao = models.CharField(('Descrição'), max_length=255, null=True, blank=True)
    def __str__(self):
        return u"%s" % self.fazenda


    class Meta:
        verbose_name = "Financeiro"
        verbose_name_plural = "Financeiros"