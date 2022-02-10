from django import forms


class SearchForm(forms.Form):
    origin = forms.CharField(max_length=100, label='Miejsce wylotu', help_text='Wpisz co najmniej 3 znaki', min_length=3)
    destination = forms.CharField(max_length=100, label='Miejsce przylotu', help_text='Wpisz co najmniej 3 znaki', min_length=3)

    departure_date = forms.DateField(label='Data wylotu', widget=forms.DateInput(attrs={'type': 'date'}))
    return_date = forms.DateField(label='Data powrotu', widget=forms.DateInput(attrs={'type': 'date'}))
