from django.urls import path, include

# from django.views.generic.base import RedirectView
from rest_framework.routers import DefaultRouter

from . import views as mv_views

router = DefaultRouter()

router.register(r"media", mv_views.NodeViewSet)
router.register(r"permission", mv_views.NodePermissionViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "images/<str:slug>/file.<str:ext>",
        mv_views.MediaStorageImageView.as_view(),
        name="mb-image",
    ),
    path(
        "images/<str:slug>/versions/<str:version>/file.<str:ext>",
        mv_views.MediaStorageImageVersionView.as_view(),
        name="mb-version",
    ),
    path(
        "images/<str:slug>/thumbnail.<str:ext>",
        mv_views.MediaStorageImageThumbnailView.as_view(),
        name="mb-thumbnail",
    ),
    path(
        "files/<str:slug>/file.<str:ext>",
        mv_views.MediaStorageFileView.as_view(),
        name="mb-file",
    ),
]
