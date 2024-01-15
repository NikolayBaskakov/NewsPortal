from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from NewsPaper.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет посты по выбранным категориям'
    missing_args_message = 'Недостаточно аргументов'
    requires_migrations_checks = True
    
    def add_arguments(self, parser):
        parser.add_argument('category', type=str)
    
    def handle(self, *args: Any, **options: Any):
        answer = input(f'Действительно хотите удалить все посты по категории {options["category"]} y/n')
        
        if answer == "y":
            try:
                category = Category.objects.get(name=options['category'])
                Post.objects.filter(category=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category {category.name}'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Could not find category {options["category"]}'))
        else:
            pass