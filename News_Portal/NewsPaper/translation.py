from .models import *
from modeltranslation.translator import register, TranslationOptions

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
    
@register(Post)
class PostTranslatioOptions(TranslationOptions):
    fields = ('title',)
    