from django.shortcuts import render, get_object_or_404
from rest_framework import generics, mixins
from . models import Products
from . serializers import ProductSerializer
from rest_framework. decorators import api_view
from rest_framework.response import Response
 

# Create your views here.
class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        print(serializer.validated_data)
        title = serializer.validated_data.get('title') 
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = title
        serializer.save(content=content)

# product_create_view = ProductCreateAPIView.as_view

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        super().perform_destroy(instance)


# class ProductListAPIView(generics.RetrieveAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer


class ProductMixinView(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    def get(self, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(self.request, *args, **kwargs)
        return self.list(self.request, *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.create(self.request, *args, **kwargs)
    def get(self, *args, **kwargs):
        return self.destroy(self.request, *args, **kwargs)

@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            obj = get_object_or_404(Products, pk=pk)
            data = ProductSerializer(obj).data
            return Response(data)
        queryset = Products.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        serializer = ProductSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title') 
            content = serializer.validated_data.get('content') or None
            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return response({"invalid": "not good data"},
        status=400)




# product_detail_view = ProductDetailAPIView.as_view()

