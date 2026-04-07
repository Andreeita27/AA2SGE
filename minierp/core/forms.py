from django import forms
from .models import Cliente, Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'nombre', 'precio', 'stock']
        help_texts = {
            'stock': 'No puede ser inferior a 0.',
        }

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError("El stock no puede ser inferior a 0.")
        return stock
    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nif', 'nombre', 'email']
        help_texts = {
            'email': 'Debe pertenecer al dominio corporativo @svalero.com',
        }

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        nif = cleaned_data.get('nif')

        email_valido = False
        nif_unico = False

        if email and email.lower().endswith('@svalero.com'):
            email_valido = True

        if nif:
            qs = Cliente.objects.filter(nif=nif)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if not qs.exists():
                nif_unico = True

        if not email_valido and not nif_unico:
            raise forms.ValidationError(
                "El cliente debe tener un email corporativo (@svalero.com) o un NIF único."
            )
        
        return cleaned_data