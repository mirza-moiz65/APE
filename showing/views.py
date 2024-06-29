from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.db.models.functions import Cast
from django.db.models import CharField
from .models import Coin
from .serializers import CoinSerializer

def index(request):
    return render(request, 'index.html')

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.page_size,
            'current_page': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'results': data,
        })

class CoinListView(generics.ListAPIView):
    serializer_class = CoinSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        queryset = Coin.objects.all().order_by('symbol')
        cap = self.request.query_params.get('cap', None)
        
        if cap:
            # Convert market_cap to a numerical value for comparison
            queryset = queryset.annotate(market_cap_num=Cast('market_cap', CharField()))
            
            if cap == 'mega':
                queryset = queryset.filter(market_cap_num__gt=200e9)
            elif cap == 'large':
                queryset = queryset.filter(market_cap_num__gt=10e9, market_cap_num__lte=200e9)
            elif cap == 'mid-market':
                queryset = queryset.filter(market_cap_num__gt=1e9, market_cap_num__lte=10e9)
            elif cap == 'small-market':
                queryset = queryset.filter(market_cap_num__gt=100e6, market_cap_num__lte=1e9)
            elif cap == 'micro-market':
                queryset = queryset.filter(market_cap_num__gt=10e6, market_cap_num__lte=100e6)
            elif cap == 'nano-market':
                queryset = queryset.filter(market_cap_num__gt=1e6, market_cap_num__lte=10e6)
            elif cap == 'pico-market':
                queryset = queryset.filter(market_cap_num__gt=100e3, market_cap_num__lte=1e6)
            elif cap == 'femto-market':
                queryset = queryset.filter(market_cap_num__lt=100e3)
        
        return queryset
