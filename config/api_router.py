from django.urls import path
from django.urls.conf import include
from rest_framework.routers import SimpleRouter

from bot.job.api.viewset import JobViewset

router = SimpleRouter()
router.register("", JobViewset, basename="job")

app_name = "api"
urlpatterns = [
    path("", include(router.urls)),
]
