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

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if not email:
            raise forms.ValidationError("El email es obligatorio.")
        
        if not email.lower().endswith('@svalero.com'):
            raise forms.ValidationError(
                "El email debe pertenecer al dominio corporativo @svalero.com."
            )
        
        return email