from django.urls import path, include
from profiles.api import views as api_views
from profiles.api.views import ProfileViewSet
from rest_framework.routers import DefaultRouter

profile_list = ProfileViewSet.as_view({"get": "list"})
profile_detail = ProfileViewSet.as_view({"get": "retrieve"})
router = DefaultRouter()
router.register(r"user-profiles-router", ProfileViewSet)
urlpatterns = [
    path("profiles/", api_views.ProfileView.as_view(), name="profiles"),
    path(
        "profiles/<int:pk>",
        api_views.ProfileDetailView.as_view(),
        name="profiles-detail",
    ),
    path("auth/", api_views.AuthView.as_view(), name="auths"),
    path("user-profiles/", profile_list, name="user-profiles"),
    path("user-profiles/<int:pk>", profile_detail, name="user-profiles-detail"),
    path("", include(router.urls)),
]
