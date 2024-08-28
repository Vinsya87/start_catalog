from catalog.views import (AddToFavoriteView, CategoryAllView,
                           CategoryDetailView, FavoriteView,
                           PortfolioDetailView, PortfolioListView,
                           ProductDetailView, SearchView)
from django.urls import path

app_name = 'catalog_url'

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('favorite/', FavoriteView.as_view(), name='favorite'),
    path(
        'category/',
        CategoryAllView.as_view(),
        name='category_all'),
    path(
        'category/<slug:slug>/',
        CategoryDetailView.as_view(),
        name='category_detail'),
    path(
        'add-to-favorite/<int:pk>/',
        AddToFavoriteView.as_view(),
        name='add_to_favorite'),
    path(
        'product/<slug:slug>/',
        ProductDetailView.as_view(),
        name='product_detail'),
    path(
        'portfolio/',
        PortfolioListView.as_view(),
        name='portfolio_list'),
    path(
        'portfolio/<slug:slug>/',
        PortfolioDetailView.as_view(),
        name='portfolio_detail'),
    ]
