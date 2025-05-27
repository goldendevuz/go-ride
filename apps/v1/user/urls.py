from django.urls import path

from .views import CreateUserView, VerifyAPIView, GetNewVerification, \
    UpdateUserInformationView, ChangeUserPhotoView, LoginView, LoginRefreshView, \
    LogOutView, ResetPasswordView, PasswordGeneratorView, test_login, ForgetPasswordAPIView

urlpatterns = [
    path('signup/', CreateUserView.as_view(), name='signup'), #1
    path('login/', LoginView.as_view(), name='login'), #6
    path('login/refresh/', LoginRefreshView.as_view(), name='refresh'), #8
    path('logout/', LogOutView.as_view(), name='logout'), #9
    path('verify/', VerifyAPIView.as_view(), name='verify'), #2
    path('new-verify/', GetNewVerification.as_view(), name='new-verify'), #3
    path('', UpdateUserInformationView.as_view(), name='update'), #7
    path('photo/', ChangeUserPhotoView.as_view()), #10
    path('reset-password/', ResetPasswordView.as_view()), #4
    path('forget-password/', ForgetPasswordAPIView.as_view(), name='forget-password'), #5
    path('test-login/', test_login, name='test-login'),
    path('generate-password/', PasswordGeneratorView.as_view(), name='generate-password'),
]