from .views import LoginView, LogoutView, Verify2FAView, Setup2FAView, Disable2FAView
from django.urls import path, include

urlpatterns = [
    #path('login/', LoginView.as_view(), name='login'),
    path('account/', include(('two_factor.urls', 'two_factor'), namespace='two_factor')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify-2fa/', Verify2FAView.as_view(), name='verify_2fa'),
    path('setup-2fa/', Setup2FAView.as_view(), name='setup_2fa'),
    path('disable-2fa/', Disable2FAView.as_view(), name='disable_2fa'),
]

