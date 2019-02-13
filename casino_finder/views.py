# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import generics
from django.shortcuts import render

from casino_finder.models import Casino
from casino_finder.serializers import CasinoSerializer


class ListCreateCasino(generics.ListCreateAPIView):
    queryset = Casino.objects.all()
    serializer_class = CasinoSerializer