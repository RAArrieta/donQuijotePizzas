from django import forms
from . import models

class ProveedoresForm(forms.ModelForm):
    class Meta:
        model = models.Proveedores
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }

class InsumosForm(forms.ModelForm):
    class Meta:
        model = models.Insumos
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "precio": forms.NumberInput(attrs={"class": "form-control"}),
            "unidad": forms.Select(attrs={"class": "form-control"}),  
            "proveedor": forms.Select(attrs={"class": "form-control"}), 
            "observacion": forms.TextInput(attrs={"class": "form-control"}),
        }

class ProductoCategoriaForm(forms.ModelForm):
    class Meta:
        model = models.ProductoCategoria
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = "__all__"
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "descripcion": forms.TextInput(attrs={"class": "form-control"}),
            "precio_unit": forms.TextInput(attrs={"class": "form-control"}),
            "precio_media": forms.TextInput(attrs={"class": "form-control"}),
            "precio_doc": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-control"}),
            "precio_rec": forms.TextInput(attrs={"class": "form-control"}),
        }
        
# class CantProductoForm(forms.ModelForm):
#     class Meta:
#         model = models.Producto
#         fields = ['cantidad', 'stock']
#         widgets = {
#             'cantidad': forms.NumberInput(attrs={'class': 'producto-cant', 'min': 0}),
#             'stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
#         }
  
class CantProductoForm(forms.ModelForm):
    class Meta:
        model = models.Producto
        fields = ['cantidad', 'stock']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'producto-cant',
                'min': 0,
            }),
            'stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        producto = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if producto and producto.categoria.nombre != 'Pizzas':
            # Mostrar entero
            self.fields['cantidad'].widget.attrs['step'] = 1

            if producto.cantidad is not None:
                self.initial['cantidad'] = int(producto.cantidad)
        else:
            # Pizzas → decimal
            self.fields['cantidad'].widget.attrs['step'] = '0.01'

class CantCategoriaForm(forms.ModelForm):
    class Meta:
        model = models.ProductoCategoria
        fields = ['cantidad', 'stock']
        widgets = {
            'cantidad': forms.NumberInput(attrs={
                'class': 'cat-cant-opc',
                'min': 0,
            }),
            'stock': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        categoria = kwargs.get('instance')
        super().__init__(*args, **kwargs)

        if str(categoria.nombre) != 'Pizzas':
            self.fields['cantidad'].widget.attrs['step'] = 1
            
            if categoria.cantidad is not None:
                self.initial['cantidad'] = int(categoria.cantidad)
        else:
            self.fields['cantidad'].widget.attrs['step'] = '0.01'

            # if categoria and categoria.cantidad is not None:
            #     self.initial['cantidad'] = int(categoria.cantidad)


# class CantCategoriaForm(forms.ModelForm):
#     class Meta:
#         model = models.ProductoCategoria
#         fields = ['cantidad', 'stock']
#         widgets = {
#             'cantidad': forms.NumberInput(attrs={
#                 'class': 'cat-cant-opc',
#                 'min': 0,
#                 'step': 1,   # SIEMPRE entero
#             }),
#             'stock': forms.CheckboxInput(attrs={
#                 'class': 'form-check-input'
#             }),
#         }














      
class CantCategoriaForm(forms.ModelForm):
    class Meta:
        model = models.ProductoCategoria
        fields = ['cantidad', 'stock']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'cat-cant', 'min': 0}),
            'stock': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }