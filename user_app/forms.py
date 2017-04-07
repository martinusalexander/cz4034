from django import forms
from models.models import *

from django.utils.safestring import mark_safe

SEARCH_TYPE = [
    ('basic', 'Basic Search'),
    ('advanced', 'Advanced Search'),
]

HOTEL_STAR = [
    ('0.5', '0.5'),
    ('1.0', '1'),
    ('1.5', '1.5'),
    ('2.0', '2'),
    ('2.5', '2.5'),
    ('3.0', '3'),
    ('3.5', '3.5'),
    ('4.0', '4'),
    ('4.5', '4.5'),
    ('5.0', '5'),
]


# Create radio button to be aligned horizontally
# Reference: http://stackoverflow.com/a/5936347
class HorizontalRadioRenderer(forms.RadioSelect.renderer):
    def render(self):
        return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))


class SearchDocumentsForm(forms.Form):
    search_keyword = forms.CharField(label='Keyword',
                                     max_length=500,
                                     widget=forms.TextInput(
                                         attrs={
                                             'placeholder': 'Enter the search keyword', 'style': 'display:table-cell; width:100%',
                                         }
                                     ),
                                     required=True)
    advanced_search = forms.ChoiceField(label="Search Type",
                                        choices=SEARCH_TYPE,
                                        initial='basic',
                                        widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
                                        required=True)
    hotel_name = forms.ModelMultipleChoiceField(label="Hotel Name",
                                                queryset=Hotel.objects.all().order_by('name'),
                                                to_field_name='name',
                                                required=False,
                                                widget=forms.SelectMultiple(
                                                    attrs={
                                                        'class': 'selectpicker',
                                                        'multiple': '',
                                                        'data-live-search':
                                                            'true',
                                                        'data-selected-text-format':
                                                            "count > 1"}))
    hotel_star = forms.ChoiceField(label="Hotel Star",
                                   choices=HOTEL_STAR,
                                   widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
                                   required=False)
    hotel_rating = forms.FloatField(min_value=0.0, max_value=10.0,
                                    initial=0.0,
                                    widget=forms.TextInput(
                                        attrs={'onfocus': 'this.blur()',
                                               'size':'5',
                                               }
                                    ),
                                    required=False,
                                    )
    review_type = forms.MultipleChoiceField(label="Review Type",
                                            choices=REVIEW_TYPE[1:],
                                            required=False,
                                            widget=forms.CheckboxSelectMultiple(),
                                            )
    review_rating = forms.FloatField(min_value=0.0, max_value=10.0,
                                     initial=0.0,
                                     widget=forms.TextInput(
                                         attrs={'onfocus': 'this.blur()',
                                                'size': '5',
                                                }
                                     ),
                                     required=False,
                                     )
