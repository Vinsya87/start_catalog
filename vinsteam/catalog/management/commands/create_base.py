import random

from articles.models import Head, MenuItem, Page, Post
from banner.models import Slider
from catalog.models import (Category, Portfolio, PortfolioImage, Product,
                            ProductImage)
from config_site.models import City, Config, Config_seo
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from dotenv import load_dotenv
from reviews.models import Review, ReviewProduct
from users.models import User

load_dotenv()
import os


class Command(BaseCommand):
    help = 'Create sample categories, products, reviews, and pages'

    def handle(self, *args, **options):
        # Создаем две категории
        category1, created1 = Category.objects.get_or_create(
            title="Категория продукта 1", 
            slug="category-1"
        )
        category2, created2 = Category.objects.get_or_create(
            title="Категория продукта 2", 
            slug="category-2"
        )

        # Создаем 6 продуктов для каждой категории
        # Перемешиваем изображения
        image_paths = [f"images/{i}.png" for i in range(1, 7)]
        shuffled_images = image_paths.copy()

        # Создаем продукты и добавляем изображения
        for category in [category1, category2]:
            for i in range(1, 7):
                post_slug = f"product-{i}-{category.slug}"
                product = Product.objects.create(
                    title=f"Продукт {i} ({category.title})",
                    description=f"Описание продукта {i}",
                    slug=post_slug,
                    price=f'100{i}',
                    category=category
                )
                self.stdout.write(self.style.SUCCESS(f"Создан продукт: {product.title}"))

                # Добавление двух изображений к каждому продукту
                for j in range(2):
                    image_path = shuffled_images.pop(0)  # Берем изображение из списка
                    ProductImage.objects.create(
                        product=product,
                        image=image_path,
                        order=j
                    )
                    self.stdout.write(self.style.SUCCESS(f"Добавлено изображение {image_path} к продукту {product.title}"))

                # Восстанавливаем список изображений, если он опустел
                if not shuffled_images:
                    shuffled_images = image_paths.copy()
                self.stdout.write(self.style.SUCCESS(f"Создан продукт: {product.title}"))

        # Создаем 6 отзывов
        for i in range(1, 7):
            review = Review.objects.create(
                name=f"Пользователь {i}",
                email=f"user{i}@example.com",
                phone=f"+7123456789{i}",
                text=f"Это отзыв пользователя {i} о продуктах.",
                is_enabled=True
            )
            self.stdout.write(self.style.SUCCESS(f"Создан отзыв: {review.name}"))
        products = Product.objects.all()  # Получаем все продукты из базы данных

        for product in products:
            for i in range(1, 7):  # Создаем 6 отзывов для каждого продукта
                review = ReviewProduct.objects.create(
                    product=product,
                    name=f"Пользователь {i} для {product.title}",
                    email=f"user{i}@example.com",
                    phone=f"+7123456789{i}",
                    text=f"Это отзыв пользователя {i} о продукте {product.title}.",
                    is_enabled=True
                )
                self.stdout.write(self.style.SUCCESS(f"Создан отзыв для {product.title}: {review.name}"))

        # Создаем страницу "Главная"
        homepage_content = "<h1>Добро пожаловать на наш сайт!</h1><p>Это главная страница.</p>"
        homepage = Page.objects.create(
            title="Главная",
            slug="home",
            is_homepage=True,
            content_ckeditor=homepage_content
        )
        self.stdout.write(self.style.SUCCESS(f"Создана страница: {homepage.title}"))

        # Создаем страницу "Контакты"
        contacts_content = (
            "<p>Наш адрес: 123456, г. Москва, ул. Примерная, д. 1.</p>"
            "<p>Телефон: +7 (495) 123-45-67</p>"
            "<p>Email: info@example.com</p>"
        )
        contacts_page = Page.objects.create(
            title="Контакты",
            slug="contacts",
            is_homepage=False,
            content_ckeditor=contacts_content
        )
        self.stdout.write(self.style.SUCCESS(f"Создана страница: {contacts_page.title}"))

        # Создаем страницу "О нас"
        contacts_content = (
            "<p>Мы крутые ребята :)</p>"
        )
        contacts_page = Page.objects.create(
            title="О нас",
            slug="about",
            is_homepage=False,
            content_ckeditor=contacts_content
        )
        self.stdout.write(self.style.SUCCESS(f"Создана страница: {contacts_page.title}"))

        # Создаем объект Config
        config, created = Config.objects.get_or_create(
            site_name="Название сайта",
            phone_number="+123456789",
            logo="favicon.png",
            telegram="https://t.me/example",
            whatsapp="https://wa.me/123456789",
            vk="https://vk.com/example",
            placeholder="favicon.png",
        )
        self.stdout.write(self.style.SUCCESS("Создан объект Config"))

        # Создаем объект Config_seo
        config_seo, created = Config_seo.objects.get_or_create(
            title="Название компании",
            meta_description="Короткое описание компании",
            reviews_meta_title="Отзывы о компании",
            reviews_meta_description="Описание отзывов о компании",
            og_img="favicon.png",
            favicon="favicons/favicon.png",
        )
        self.stdout.write(self.style.SUCCESS("Создан объект Config_seo"))

        superuser_name = os.getenv('SUPERUSER_NAME')
        superuser_password = os.getenv('SUPERUSER_PASSWORD')
        superuser_email = os.getenv('SUPERUSER_EMAIL')

        if superuser_name and superuser_password:
            if not User.objects.filter(username=superuser_name).exists():
                User.objects.create_superuser(
                    username=superuser_name,
                    password=superuser_password,
                    email=superuser_email,
                )
                self.stdout.write(self.style.SUCCESS(f"Суперпользователь '{superuser_name}' успешно создан"))
            else:
                self.stdout.write(self.style.WARNING(f"Суперпользователь с именем '{superuser_name}' уже существует"))
        else:
            self.stdout.write(self.style.ERROR("Не удалось создать суперпользователя: переменные окружения 'NAME' и 'PASSWORD' не заданы"))

        # Создаем 3 баннера
        Slider.objects.create(
            title="Баннер 1",
            text="Описание баннера 1",
            link="/some-link-1/",
            is_active=True,
            order=1,
            class_css="slider-class-1",
            title_btn="Подробнее",
            slug="slider-1",
            image="sliders/slider-1.jpg",
            header_type="h1",
        )
        
        Slider.objects.create(
            title="Баннер 2",
            text="Описание баннера 2",
            link="/some-link-2/",
            is_active=True,
            order=2,
            class_css="slider-class-2",
            title_btn="Подробнее",
            slug="slider-2",
            image="sliders/slider-2.jpg",
            header_type="h2",
        )

        Slider.objects.create(
            title="Баннер 3",
            text="Описание баннера 3",
            link="/some-link-3/",
            is_active=True,
            order=3,
            class_css="slider-class-3",
            title_btn="Подробнее",
            slug="slider-3",
            image="sliders/slider-3.jpg",
            header_type="h2",
        )

        self.stdout.write(self.style.SUCCESS("Созданы три баннера"))

        MenuItem.objects.create(
            title="Контакты",
            url="contacts/",
            order=1,
            is_active=True,
            is_main_menu=True
        )

        MenuItem.objects.create(
            title="О нас",
            url="about/",
            order=2,
            is_active=True,
            is_main_menu=True
        )
        
        MenuItem.objects.create(
            title="Портфолио",
            url="portfolio/",
            order=2,
            is_active=True,
            is_main_menu=True
        )

        self.stdout.write(self.style.SUCCESS("Созданы пункты меню: Контакты и О нас"))

        # Создание новой рубрики
        category_title = "Новая рубрика"
        new_head, created = Head.objects.get_or_create(
            title=category_title,
            slug='category_slug'
        )

        if created:
            self.stdout.write(self.style.SUCCESS(f"Создана рубрика: {new_head.title}"))
        else:
            self.stdout.write(self.style.WARNING(f"Рубрика уже существует: {new_head.title}"))

        # Создание 6 произвольных статей в этой рубрике
        for i in range(1, 7):
            post_title = f"Произвольная статья {i}"
            post_slug = f"post-{i}-{new_head.slug}"
            content = f"<p>Это контент для статьи {i} в рубрике {new_head.title}. Это пример текста.</p>"

            Post.objects.create(
                title=post_title,
                slug=post_slug,
                category=new_head,
                content_ckeditor=content,
                short_description=f"Короткое описание для статьи {i}",
                description=f"Полное описание для статьи {i}"
            )
            self.stdout.write(self.style.SUCCESS(f"Создана статья: {post_title}"))

        self.stdout.write(self.style.SUCCESS("Завершено создание рубрики и статей"))

        # Города
        cities = ['Moscow', 'Saint Petersburg', 'Novosibirsk']
        for city_name in cities:
            city, created = City.objects.get_or_create(name=city_name)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Город "{city_name}" успешно создан.'))
            else:
                self.stdout.write(self.style.WARNING(
                    f'Город "{city_name}" уже существует.'))

        # Портфолио
        categories = Category.objects.all()
        products = Product.objects.all()

        image_files = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png']
        image_dir = 'images/'

        for i in range(1, 11):  # Создаем 10 портфолио
            category = random.choice(categories) if categories.exists() else None
            product = random.choice(products) if products.exists() else None
            portfolio_title = f"Портфолио {i} - {category.title if category else 'Без категории'}"
            portfolio_slug = f"portfolio-{i}-{category.slug if category else 'no-category'}"
            image_catalog_path = f"{image_dir}{random.choice(image_files)}"

            portfolio = Portfolio.objects.create(
                category=category,
                product=product,
                title=portfolio_title,
                slug=portfolio_slug,
                image_catalog=image_catalog_path,
                description=f"Описание портфолио {i}",
                content_ckeditor=f"<p>Контент для портфолио {i}</p>",
                order=i
            )

            # Добавляем 2 изображения к каждому портфолио
            selected_images = random.sample(image_files, 2)
            for image in selected_images:
                PortfolioImage.objects.create(
                    portfolio=portfolio,
                    image=f"{image_dir}{image}"
                )

            self.stdout.write(self.style.SUCCESS(f"Создано портфолио: {portfolio.title} с изображениями: {', '.join(selected_images)}"))
