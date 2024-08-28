from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from users.views import (CustomResetCompleteView, CustomResetConfirmView,
                         CustomResetDoneView, CustomResetView)

from .sitemaps import (CategoryProductSitemap, HeadSitemap, PageSitemap,
                       PostSitemap, ProductSitemap)

sitemaps = {
    'staticpages': PageSitemap,
    'staticposts': PostSitemap,
    'staticcategory': HeadSitemap,
    'staticcategoryproduct': CategoryProductSitemap,
    'staticproduct': ProductSitemap,
}


urlpatterns = [
    path('reset_password/', 
         CustomResetView.as_view(), 
         name="reset_password"),
    path('reset_password_sent/', 
         CustomResetDoneView.as_view(),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         CustomResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         CustomResetCompleteView.as_view(),
         name="password_reset_complete"),
    path('admin/', admin.site.urls),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('', include('basket.urls', namespace='basket')),
    path('', include('main.urls', namespace='main_url')),
    path('', include('catalog.urls', namespace='catalog_url')),
    path('', include('articles.urls', namespace='articles')),


    path('mail/', include('mail_post.urls', namespace='mail_post')),
#     path('ckeditor/', include('ckeditor_uploader.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    path('users/', include('users.urls', namespace='users')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    # path('upload/', upload, name='ckeditor_upload'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    import debug_toolbar

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
