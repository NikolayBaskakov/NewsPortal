from django import forms
from django.core.exceptions import ValidationError
from .models import Post

class NewsForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'author', 
                  'category',
                  'title_en_us',
                  'title_ru',
            
        ]
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['type'] = 'NW'
        text = cleaned_data.get('text')
        text_length = 15
        if text is not None and len(text) < text_length:
            raise ValidationError({"text":f"Текст поста не может быть меньше {text_length} символов"
                                       })
        return cleaned_data

class ArticlesForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',
                  'text',
                  'author', 
                  'category',
                  'title_en_us',
                  'title_ru',
        ]
    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['type'] = 'AR'
        text = cleaned_data.get('text')
        text_length = 15
        if text is not None and len(text) < text_length:
            raise ValidationError({"text":f"Текст поста не может быть меньше {text_length} символов"
                                       })
        return cleaned_data
