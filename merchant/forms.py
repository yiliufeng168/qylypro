from django import forms
from django.utils import timezone
from .models import Business,Goods,Sell



class EditBusinessInfoForm(forms.ModelForm):
    class Meta:
        model=Business
        fields=(
            'name','location','pic','star','introduct','type'
        )

class GoodsForm(forms.ModelForm):
    class Meta:
        model=Goods
        fields=(
            'name','pic','introduct'
        )

class EditGoodsForm(forms.Form):
    id = forms.UUIDField(label='id')
    name = forms.CharField(max_length=50,label='商品名')
    introduct = forms.CharField(max_length=500)
    # pic = forms.ImageField(label='图片')
    # price = forms.FloatField(label='价格')


class SellForm(forms.ModelForm):
    class Meta:
        model=Sell
        fields=(
            'total','startdatetime','enddatetime','goods','price'
        )