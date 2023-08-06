import logging

from django.db import models
from django.utils.module_loading import import_string
from django_filters import CharFilter, ChoiceFilter, FilterSet
from django_filters import rest_framework as filters
from private_storage.views import PrivateStorageDetailView
from rest_framework import filters as drfFilters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_mediabrowser import appconfig
from rest_mediabrowser import models as mb_model
from rest_mediabrowser import serializers as mb_ser
from rest_mediabrowser.permissions import IsNodePermissionOwner, NodePermission

logger = logging.getLogger(__name__)


class MediaStorageImageView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaImage
    content_disposition = "inline"
    model_file_field = "image"
    lookup_field = "slug"


class MediaStorageImageVersionView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaImage
    content_disposition = "inline"
    model_file_field = "image"
    lookup_field = "slug"

    def get_path(self):
        version = self.kwargs["version"]
        # logger.critical(f"in view: {version}")
        if version == "original":
            file = getattr(self.object, self.model_file_field)
            return file.name
        version_image = self.object.get_version(version)
        return version_image


class MediaStorageImageThumbnailView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaImage
    content_disposition = "inline"
    model_file_field = "thumbnail"
    lookup_field = "slug"


class MediaStorageFileView(PrivateStorageDetailView):
    storage = appconfig.MB_STORAGE
    can_access_file = staticmethod(import_string(appconfig.MEDIA_BROWSER_AUTH_FUNCTION))
    model = mb_model.MediaFile
    content_disposition = "inline"
    model_file_field = "file"
    lookup_field = "slug"


class NodePermissionViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, IsNodePermissionOwner)
    queryset = mb_model.NodePermission.objects.all()
    serializer_class = mb_ser.NodePermissionSerializer
    # lookup_field = "slug"

    def get_queryset(self):
        node_list = list(
            mb_model.Node.objects.filter(owner=self.request.user).values_list(
                "id", flat=True
            )
        )
        return mb_model.NodePermission.objects.filter(node__in=node_list)


class NodeFilterChoices(models.TextChoices):
    ALL = "all", "All"
    COLLECTION = "collection", "Collection"
    MEDIA = "media", "Media"
    IMAGE = "image", "Image"
    FILE = "file", "File"


class NodeOwnerChocies(models.TextChoices):
    SELF = "self", "Self"
    SHARED = "shared", "Shared"


CTYPE_DICT = {"collection": "collection", "image": "mediaimage", "file": "mediafile"}


class NodeFilter(FilterSet):

    parent = CharFilter(field_name="parent", label="Parent", method="filter_by_parent")
    tags = CharFilter(field_name="tags", label="Parent", method="filter_by_tags")

    content_type = ChoiceFilter(
        label="Content Type",
        choices=NodeFilterChoices.choices,
        method="filter_by_content_type",
        initial="all",
    )
    owned_by = ChoiceFilter(
        choices=NodeOwnerChocies.choices,
        label="Owner",
        method="filter_by_owner",
        initial="self",
    )

    def filter_by_owner(self, queryset, name, value):
        if value == "self":
            return queryset.filter(owner=self.request.user)
        else:
            return queryset.filter(
                id__in=models.Subquery(
                    self.request.user.shared_nodes.all().values_list("id", flat=True)
                )
            )

    def filter_by_content_type(self, queryset, name, value):
        if value == "all":
            return queryset
        if value == "media":
            return queryset.filter(media_type__in=["mediaimage", "mediafile"])
        else:
            return queryset.filter(media_type=CTYPE_DICT[value])

    def filter_by_tags(self, queryset, name, value):
        tag_list = [data.strip() for data in value.split(",")]
        media_list = list(
            mb_model.Media.objects.filter(tags__name__in=tag_list).values_list(
                "id", flat=True
            )
        )
        return queryset.filter(id__in=media_list).distinct()

    def filter_by_parent(self, queryset, name, value):
        try:
            node_list = []
            if value == "root":
                node_list = list(
                    mb_model.Collection.objects.filter(parent=None).values_list(
                        "id", flat=True
                    )
                )
                node_list += list(
                    mb_model.Media.objects.filter(parent=None).values_list(
                        "id", flat=True
                    )
                )
            else:
                node_list = list(
                    mb_model.Media.objects.filter(parent__slug=value).values_list(
                        "id", flat=True
                    )
                )
                node_list += list(
                    mb_model.Collection.objects.filter(parent__slug=value).values_list(
                        "id", flat=True
                    )
                )
            qs = queryset.filter(id__in=node_list)
            return qs.distinct()
        except Exception:
            return queryset.none()

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            # get a mutable copy of the QueryDict
            data = data.copy()

            for name, f in self.base_filters.items():
                initial = f.extra.get("initial")

                # filter param is either missing or empty, use initial as default
                if not data.get(name) and initial:
                    data[name] = initial

        super().__init__(data, *args, **kwargs)

    class Meta:
        model = mb_model.Node
        fields = [
            "content_type",
            "parent",
            "owned_by",
            "tags",
        ]


class NodeViewSet(viewsets.ModelViewSet):
    queryset = mb_model.Node.objects.all()
    serializer_class = mb_ser.NodeSerializer
    permission_classes = (
        IsAuthenticated,
        NodePermission,
    )
    pagination_class = staticmethod(import_string(appconfig.MB_NODE_PAGINATION))
    lookup_field = "slug"
    filter_backends = (
        filters.DjangoFilterBackend,
        drfFilters.SearchFilter,
    )
    filterset_class = NodeFilter
    search_fields = [
        "name",
    ]

    def get_queryset(self):
        return mb_model.Node.objects.all()
