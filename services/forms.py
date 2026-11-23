from django import forms
from services.models import Garage, Service, GarageReview

class GarageBaseForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = (
            'name',
            'description',
            'city',
            'address',
            'phone_number',
            'email',
            'services',
        )

        labels = {
            'name': 'Garage Name',
            'description': 'Description',
            'city': 'City',
            'address': 'Address',
            'phone_number': 'Phone Number',
            'email': 'Email',
            'services': 'Services that are offered at the Garage',
        }

        help_texts = {
            'name': 'Provide the name of the garage',
            'description': 'Provide a short description of the garage',
            'city': 'Provide the city location of the garage',
            'address': 'Provide the address of the garage',
            'phone_number': 'Provide a phone number for contact',
            'email': 'Provide an email address for contact',
            'services': 'Select all services offered at this garage',

        }

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter the name of the garage'}),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Provide a short description of the garage'}),
            'city': forms.TextInput(attrs={'placeholder': 'Provide the city location of the garage'}),
            'address': forms.TextInput(attrs={'placeholder': 'Provide the address of the garage'}),
            'phone_number': forms.TextInput(attrs={'placeholder': 'Provide a phone number for contact'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Provide an email address for contact'}),
            'services': forms.CheckboxSelectMultiple(),
        }

        error_messages = {
            'name':{
                'required': 'Garage name shall be provided',
                'unique': 'Garage name shall be unique',
                'max_length': 'Garage name can not be more than 100 characters',
            },

            'description':{
                'required': 'Garage description shall be provided',
                'min_length': 'Garage description shall be at least 20 characters',
                'max_length': 'Garage description can not be more than 1000 characters',
            },

            'city':{
                'required': 'Please, provide a city for the garage location',
                'min_length': 'Name of the city shall be at least 3 characters',
                'max_length': 'Name of the city shall not be more than 100 characters',
            },

            'address':{
                'required': 'Please, provide an address for the garage',
                'min_length': 'Address of the garage shall be at least 10 characters',
                'max_length': 'Address of the garage shall not be more than 200 characters',
            },

            'phone_number':{
                'required': 'Please, provide a phone number for contact',
            },

            'email':{
                'invalid': 'Please, provide a valid email address for contact',
            },

            'services':{
                'required': 'At least one service offered by the garage shall be selected',
            }

        }




class GarageCreateForm(GarageBaseForm):
    pass

class GarageEditForm(GarageBaseForm):
    pass

class GarageDeleteForm(GarageBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.disabled = True



class GarageReviewBaseForm(forms.ModelForm):
    class Meta:
        model = GarageReview

        fields = ('garage', 'rating', 'comment')

        labels = {
            'garage': 'Garage',
            'rating': 'Rating',
            'comment': 'Review of the garage',
        }

        help_texts = {
            'garage': 'Choose the garage to provide review for',
            'rating': 'Provide a rating for the garage from 1 to 5',
            'comment': 'Provide a short review for the garage',
        }

        widgets = {
            'garage': forms.Select(),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5,}),
            'comment': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Provide a short review for the garage and services provide to you'}),
        }

        error_messages = {
            'garage': {'required': 'Garage, shall be selected',
                       'invalid_choice': 'Please, select a valid garage'},
            'rating': {'required': 'Rating from 1 to 5 shall be provided',
                       'invalid': 'Please, provide valid rating from 1 to 5'},
            'comment': {'max_length': 'Review can not be more than 500 characters',}
        }


class GarageReviewCreateForm(GarageReviewBaseForm):
    pass

class GarageReviewEditForm(GarageReviewBaseForm):
    pass

class GarageReviewDeleteForm(GarageReviewBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True
