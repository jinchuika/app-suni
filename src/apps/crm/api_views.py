import django_filters
from datetime import datetime
from django.db.models import Count

from rest_framework import viewsets, filters
from braces.views import LoginRequiredMixin

from apps.crm import (
    serializers as crm_s,
    models as crm_m)
