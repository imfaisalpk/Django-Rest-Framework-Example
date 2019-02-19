from rest_framework import generics, mixins
from postings.models import *
from .serializers import *
from .permissions import *

from django.db.models import Q



class BlogPostAPIView(mixins.CreateModelMixin,generics.ListAPIView):
    
    lookup_field = 'pk' # (?P<pk>\d+)
    serializer_class = BlogPostSerializer
    # permission_classes = [IsOwnerOrReadOnly]


    def get_queryset(self):
        queryset = BlogPost.objects.all()

        query = self.request.GET.get("q")
        if query is not None:
            queryset =  queryset.filter( Q(title__icontains=query) | Q(content__icontains=query)).distinct()

        return queryset

    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

    def post(self,request, *args, **kwargs):
        return self.create(request,*args, **kwargs)

    
    def get_serializer_context(self,*args, **kwargs ):
        return {"request":self.request}


class BlogPostRUDView(generics.RetrieveUpdateDestroyAPIView):
    
    lookup_field = 'pk' # (?P<pk>\d+)
    serializer_class = BlogPostSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = BlogPost.objects.all()
        return queryset
    
    def get_serializer_context(self,*args, **kwargs ):
        return {"request":self.request}