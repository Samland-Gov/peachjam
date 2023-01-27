from django.urls import include, path

from namiblii import views

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home_page"),
    path("", include("liiweb.urls")),
]
