from django import forms
from .models import *
from django.core.exceptions import ValidationError
from datetime import date, datetime

from django.forms import ModelForm, SplitDateTimeField
from django.forms.widgets import Textarea, TextInput, SplitDateTimeWidget

# Note ตัวเองชื่อตัวแปรในนี้ ต้องตรงกับฟังชันใน views.py
# ex. room_types = form.cleaned_data['types']

class createRoomForm(forms.Form):
    name = forms.CharField(
        label="Room name", 
        max_length=100, 
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter room name'})
        )
    
    price = forms.IntegerField(
        label="Price",
        widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter room price'})
    )

    types = forms.ModelMultipleChoiceField(  
        queryset = RoomTypes.objects.all(),  
        widget = forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    
    # promotion = forms.ModelChoiceField(
    #     queryset = Promotion.objects.all(),
    #     widget = forms.Select(attrs={'class': 'form-control'})
    # )

class createPromotionForm(forms.Form):
    name = forms.CharField(
        label="Promotion name", 
        max_length=100, 
        widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Promotion name'})
        )

    discount_percent = forms.IntegerField(
        label="Discount (%)",
        widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Discount'}))
    
    description = forms.CharField(
        label="Description", 
        max_length=250, 
        widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'})
        )
    
    start_date = forms.DateField(
        label="Start date", 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    
    expire_date = forms.DateField(
        label="Expire date", 
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def clean_expire_date(self):
        start_date = self.cleaned_data.get("start_date")
        expire_date = self.cleaned_data.get("expire_date")  
  
        # ตรวจว่าทั้ง start_date และ expire_date มีค่าไหม
        if start_date and expire_date:  
            if expire_date < start_date: 
                raise ValidationError("expire date can't be set before start date")
        return expire_date


#----------------------------------------------------------------------
# 2B's Zone


class NewBookingForm(ModelForm):

    now = datetime.now().date()
    promotion = forms.ModelChoiceField(
        queryset=Promotion.objects.filter(start_date__lte=now,
                expire_date__gte=now),
        widget = forms.Select(attrs={'class': 'form-select'}),
        required=False  # เผื่อว่าผู้ใช้ไม่ต้องการใช้โปรโมชัน
        )
    
    class Meta:
        model = Bookings
        fields = [
            "start_date", 
            "end_date", 
            "promotion", 
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }


    #validated
    def clean(self):
        cleaned_data = super().clean() 
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        now = datetime.now().date()

        if start_date and now and now > start_date:
            self.add_error(
                'start_date',
                "Can't book from the past"
            )
        if end_date < start_date:
            self.add_error(
                'end_date',
                "End date can't be after Start date"
            )
        return cleaned_data
    
class EditBookingForm(ModelForm):
    room = forms.ModelChoiceField(
        queryset=Rooms.objects.all(),
        widget = forms.Select(attrs={'class': 'form-select'}))
    
    promotion = forms.ModelChoiceField(
        queryset=Promotion.objects.all(),
        widget = forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Bookings
        fields = [
            'room',
            "start_date", 
            "end_date", 
            "promotion", 
        ]
        widgets = {
            'start_date': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

    #validated
    def clean(self):
        cleaned_data = super().clean() 
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if end_date < start_date:
            self.add_error(
                'end_date',
                "End date can't be after Start date"
            )
        return cleaned_data

class EditRoomForm(ModelForm):
    room_types = forms.ModelMultipleChoiceField(  
        queryset = RoomTypes.objects.all(),  
        widget = forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Rooms
        fields = [
            'name',
            "price", 
            "room_types",  
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EditPromotionForm(ModelForm):
    class Meta:
        model = Promotion
        fields = [
            'name',
            "discount_percent", 
            "start_date",
            'expire_date' 
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'discount_percent': forms.NumberInput(attrs={'class': 'form-control'}),  
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
        }

    #validated
    def clean_date(self):
        start_date = self.cleaned_data.get("start_date")
        expire_date = self.cleaned_data.get("expire_date")
        now = datetime.now().date()

        if start_date and now and now > start_date:
            self.add_error(
                'start_date',
                "Can't book from the past"
            )
        elif expire_date < start_date:
            self.add_error(
                'expire_date',
                "End date can't be after Start date"
            )
        return expire_date

class PasswordChangeForm(ModelForm):
    room_types = forms.ModelMultipleChoiceField(  
        queryset = RoomTypes.objects.all(),  
        widget = forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Rooms
        fields = [
            'name',
            "price", 
            "room_types",  
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),  
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }