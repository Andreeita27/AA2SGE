from django import forms
from .models import Cliente, Producto

#Formulario de producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto #A qué modelo está vinculado
        fields = ['sku', 'nombre', 'precio', 'stock'] #Campos que aparecen en el formulario
        help_texts = {
            'stock': 'No puede ser inferior a 0.', #Texto de ayuda 
        }

    #Valida que el stock no sea negativo
    def clean_stock(self): #Metodo especial de Django para validar un campo concreto
        stock = self.cleaned_data.get('stock') #Obtiene el valor que ha introducido el usuario
        if stock is not None and stock < 0: #Si el valor existe y es negativo ->
            raise forms.ValidationError("El stock no puede ser inferior a 0.") # <- error
        return stock #Sino devuelve el valor

#Formulario de cliente    
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente #Modelo asocciado
        fields = ['nif', 'nombre', 'email'] #Campos del formulario
        help_texts = {
            'email': 'Debe pertenecer al dominio corporativo @svalero.com', # Texto de ayuda
        }

    #Valida que el email sea corporativo
    def clean_email(self): #Método de validacion especifico del campo email
        email = self.cleaned_data.get('email') #Obtiene el valor introducido

        if not email: #Si el usuario no introduce nada ->
            raise forms.ValidationError("El email es obligatorio.") # <- error
        
        if not email.lower().endswith('@svalero.com'): #Convierte a minusculas y comprueba el dominio
            raise forms.ValidationError( # error si no cumple la regla
                "El email debe pertenecer al dominio corporativo @svalero.com."
            )
        
        return email #Sino devuelve el valor