from django import forms
from django.forms import ModelForm, TextInput, Textarea
from .models import Animal, Quantidade, Fazenda,  Movimento


class RebanhoForm(forms.ModelForm):
    class Meta:
        model = Quantidade
        exclude = ()
        # fields = ['cliente', 'data_entrega','fpag','author']
        # widgets = {
        #     'cliente': forms.Select(attrs={'class': 'form-control', 'style':'color:#ccc; Background-color:#27293d;'}),
        #     'un_medida': forms.Select(attrs={'class': 'form-control', 'style':'color:#ccc; Background-color:#27293d;'}),
        #
        #
        # }
        fields = ['tipo_movimento','fazenda','animal','entrada', 'saida','obs']
        # ANIMAL = [
        #         ('Bezerra', ('Bza')),
        #         ('Bezerro', ('Bzo')),
        #         ('Boi', ('Boi')),
        #         ('Vaca', ('Vac')),
        #         ]
        # animal = forms.ChoiceField(choices=ANIMAL, default='Bezerra')
        widgets = {
                    'tipo_movimento': forms.Select(attrs={'class': 'form-control', 'id':'validationTooltip01'}),
                    'fazenda': forms.Select(attrs={'class': 'form-control', 'id':'validationTooltip01'}),
                    'animal': forms.Select(attrs={'class': 'form-control', 'id':'validationTooltip01'}),
                    }
# PedidoFormSet = inlineformset_factory(Pedido, form=PedidoForm, extra=1,
#                                       widgets={'cliente':TextInput(attrs={'class':'base'}),
#                                                 'artigo':TextInput(attrs={'class':'base'}),
#                                                 'classe':TextInput(attrs={'class':'qt'}),
#                                                 'qt_pedido':TextInput(attrs={'class':'qt'}),
#                                                 'qt_entrega':TextInput(attrs={'class':'qt'}),
#                                             } )

# class Nf_eForm(forms.ModelForm):
#     class Meta:
#         model = Financeiro
#         exclude = ()
#         fields = '__all__'

