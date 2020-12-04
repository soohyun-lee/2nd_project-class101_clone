from django.urls import path, include

urlpatterns = [
    path('products', include('product.urls')),
    path('user', include('user.urls')),
    path('s3direct/', include('s3direct.urls')),
    # path('user', include('user.urls')),
]
