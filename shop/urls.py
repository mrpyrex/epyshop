from django.urls import path
from . import views


app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name='shop_home'),
    # path('category/', views.category, name='category'),
    # path('category/<slug:c_slug>/', views.category,
    #      name='product_list_by_category'),
    path('<slug:slug>/', views.product_detail, name='product_detail'),
    # path('category/<slug:c_slug>/', views.category_detail, name='category_detail'),
]
