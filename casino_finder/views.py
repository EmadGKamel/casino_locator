import geocoder
from django.contrib.gis.db.models.functions import Distance
from rest_framework import generics
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from casino_finder.models import Casino
from casino_finder.serializers import CasinoSerializer


class ListCreateCasino(generics.ListCreateAPIView):
    queryset = Casino.objects.all()
    serializer_class = CasinoSerializer

    def perform_create(self, serializer):
        address = serializer.initial_data['address']
        g = geocoder.mapbox(address, key='pk.eyJ1IjoiZW1hZC1rYW1lbCIsImEiOiJjam40NTF6YWQybW1pM3FxdjNmZmgzNWJwIn0.BBl23kGQ_WApeC64Id07rQ')
        lat = g.latlng[0]
        lng = g.latlng[1]
        pnt = 'POINT(' + str(lng) + ' ' + str(lat) + ')'
        serializer.save(location=pnt)

    def get_queryset(self):
        qs = super(ListCreateCasino, self).get_queryset()
        lat = self.request.query_params.get('lat', None)
        lng = self.request.query_params.get('lng', None)

        if lat and lng:
            pnt = GEOSGeometry('POINT(' + str(lng) + ' ' + str(lat) + ')', srid=4326)
            qs = qs.annotate(distance=Distance('location', pnt)).order_by('distance')
        return qs