from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from apps.main.serializers import DynamicFieldsModelSerializer
from dateutil.relativedelta import relativedelta
