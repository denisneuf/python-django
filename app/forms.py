from django import forms

from .widgets import DatePickerInput, TimePickerInput, DateTimePickerInput


# creating a form
class OrdersForm(forms.Form):
    start_date_time_field = forms.DateField(widget=DatePickerInput)
    end_date_time_field = forms.DateTimeField(widget=DatePickerInput)

    class Meta:
        fields = ['start_date_time_field', 'end_date_time_field']

        widgets = {
            'start_date_time_field': DatePickerInput(),
            'end_date_time_field': DatePickerInput()
        }


class ItemsForm(forms.Form):

    # start_date_time_field = forms.DateTimeField(widget=DateTimePickerInput)
    # end_date_time_field = forms.DateTimeField(widget=DateTimePickerInput)

    start_date_time_field = forms.DateField(widget=DatePickerInput)
    end_date_time_field = forms.DateTimeField(widget=DatePickerInput)

    class Meta:
        fields = ['start_date_time_field', 'end_date_time_field']

        widgets = {
            'start_date_time_field': DatePickerInput(),
            'end_date_time_field': DatePickerInput()
        }
        

    # start_date_time_field = forms.CharField()
    # end_date_time_field = forms.CharField()