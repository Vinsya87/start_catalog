from articles.models import Category, Post
from django.core.management.base import BaseCommand
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Create sample posts and categories'

    def handle(self, *args, **options):
        # Создаем две категории
        category1, created1 = Category.objects.get_or_create(
            name="Категория 1", 
            slug="cat-1"
        )
        category2, created2 = Category.objects.get_or_create(
            name="Категория 2", 
            slug="cat-2"
        )

        # Создаем 6 записей для каждой категории
        for category in [category1, category2]:
            for i in range(1, 7):
                # Изменяем слаг, добавив часть, зависящую от категории
                post_slug = f"post-{i}-{category.slug}"
                Post.objects.create(
                    title=f"Заголовок поста {i} ({category.name})",
                    short_description=f"Короткое описание {i}",
                    content_ckeditor=f"Контент {i}",
                    slug=post_slug,
                    category=category
                )
                self.stdout.write(self.style.SUCCESS(f"Создан пост: {i} ({category.name})"))
