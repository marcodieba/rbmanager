# Generated by Django 4.2.13 on 2024-06-19 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rebanho', '0002_remove_saldo_animal_remove_saldo_fazenda_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Financeiro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_criacao', models.DateField(auto_now_add=True, null=True, verbose_name='Data Criação')),
                ('modificado', models.DateField(auto_now=True, verbose_name='Modificado em')),
                ('nr_nota', models.IntegerField(verbose_name='Numero NF-e')),
                ('data', models.DateField(blank=True, verbose_name='Data')),
                ('entrada', models.DecimalField(decimal_places=2, default='0.00', max_digits=19, verbose_name='Entrada')),
                ('saida', models.DecimalField(decimal_places=2, default='0.00', max_digits=19, verbose_name='Saida')),
                ('descricao', models.CharField(blank=True, max_length=255, null=True, verbose_name='Descrição')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('fazenda', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='rebanho.fazenda')),
            ],
            options={
                'verbose_name': 'Financeiro',
                'verbose_name_plural': 'Financeiros',
            },
        ),
    ]
