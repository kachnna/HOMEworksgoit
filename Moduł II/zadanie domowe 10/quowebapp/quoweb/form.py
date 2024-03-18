from django.forms import ModelForm, CharField, TextInput, Textarea, ModelChoiceField, DateField, DateInput, SelectDateWidget, Select, ChoiceField
from .models import Tag, Author, Quote


class TagForm(ModelForm):

    name = CharField(min_length=3, max_length=50,
                     required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):

    fullname = CharField(max_length=100, required=True, widget=TextInput())

    born_date = DateField(
        label="Date of Birth",
        required=True,
        widget=DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        input_formats=["%Y-%m-%d"]
    )

    born_location = CharField(
        max_length=100, widget=TextInput(), required=False)
    description = CharField(widget=Textarea(), required=False)

    class Meta:
        model = Author
        fields = ["fullname", "born_date", "born_location", "description"]


class QuoteForm(ModelForm):

    quote = CharField(required=True, widget=Textarea())

    class Meta:
        model = Quote
        fields = ["quote"]
        exclude = ["tags", "author"]
