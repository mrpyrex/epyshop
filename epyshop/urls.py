from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(
        template_name='accounts/logout.html'), name='logout'),
    path('accounts/register/', accounts_views.register, name='register'),
    path('accounts/password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name='password_reset'),
    path('accounts/password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('accounts/password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/password-reset-complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),

    path('address/', include('address.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payment/', include('payment.urls')),
    path('admin/', admin.site.urls),
    path('', include('shop.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
