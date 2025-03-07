from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app1.views import (Owner_list_view, OwnerViewSet, PropertyViewSet,
                        aboutus, Property_list, home, property_create, property_form, property_form_view)

router = DefaultRouter()

router.register('property', PropertyViewSet)
router.register('owner', OwnerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("create-property/", property_form, name="create_property"),
    path("ownerlist/", Owner_list_view, name="owner-list-view"),
    path("property-create/", property_create, name="property-create"),
    path("home/", home, name="home"),
    path("aboutus/", aboutus, name="aboutus"),
    path("buying/", Property_list, name="buying"),
    path("create-property-form/", property_form_view, name="property_form"),
    ]
