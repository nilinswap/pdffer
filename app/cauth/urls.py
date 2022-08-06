from django.urls import path

from . import views

urlpatterns = [
    path("api/invite/verify", views.verify_invite, name="verify_invite"),
    path("api/client/create/", views.create_client, name="create_client"),
    path("api/client/delete", views.delete_client, name="delete_client"),
    path("api/verify_email/<slug:link_ekey>", views.verify_email, name="verify_email"),
    path("api/verify_login/", views.verify_login, name="verify_login"),
    path("api/forgot_password/", views.forgot_password, name="forgot_password"),
    path("api/logout/", views.logout, name="logout"),
    path("api/validate_email", views.validate_email, name="validate_email"),

    ## below are page-views
    path("login", views.login_view, name="login"),
    path("signup", views.signup_view, name="signup"),
    path("forgot_password", views.forgot_password_view, name="forgot_password"),
    path(
        "please_verify_your_email",
        views.please_verify_your_email_view,
        name="please_verify_your_email",
    ),
    path(
        "reset_password_success",
        views.reset_password_success_view,
        name="reset_password_success",
    ),
]
