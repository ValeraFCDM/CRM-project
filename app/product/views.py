from rest_framework.response import Response
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import Product
from storage.models import Storage
from .serializers import ProductSerializer
from drf_spectacular.utils import extend_schema, OpenApiRequest

@extend_schema(
    tags=['Product'],
    description='Создание товара. Доступно всем пользователям, связанным с компанией.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'storage': {
                    'type': 'integer',
                    'example': 1
                },
                'title': {
                    'type': 'string',
                    'example': 'Игровая приставка PS5'
                },
                'description': {
                    'type': 'string',
                    'example': 'Описание характеристик приставки'
                },
                'purchase_price': {
                    'type': 'string',
                    'example': '50000.00'
                },
                'sale_price': {
                    'type': 'string',
                    'example': '79990.90'
                },
            }
        }
    )
)
class CreateProductView(CreateAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        user = request.user
        storage = Storage.objects.filter(id=request.data['storage']).first()
        if not storage:
            return Response({'message': 'Склад не найден!'}, status=404)
        if user.company != storage.company:
            return Response({'message': 'У Вас нет доступа к этому складу!'}, status=403)
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Товар успешно добавлен!', 'detail': serializer.data}, status=201)


@extend_schema(
    tags=['Product'],
    description='Получение списка товаров на складе. Доступно всем пользователям, связанным с компанией.',
)
class ListProductView(ListAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        user = request.user
        company = user.company
        if not company:
            return Response({'message': 'Вы не прикреплены к компании!'}, status=403)
        storage = Storage.objects.filter(company=company).first()
        if not storage:
            return Response({'message': 'Склад не найден!'}, status=404)
        queryset = Product.objects.filter(storage=storage).all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=['Product'],
    description='Получение данных о продукте по ID. Доступно всем пользователям, связанным с компанией.'
)
class GetProductView(RetrieveAPIView):
    serializer_class = ProductSerializer

    def get(self,request, pk):
        user = request.user
        company = user.company
        if not company:
            return Response({'message': 'Вы не прикреплены к компании!'}, status=403)
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response({'message': 'Товар не найден!'}, status=404)
        if product.storage.company != company:
            return Response({'message': 'У Вас нет доступа к этому товару!'}, status=403)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=200)


@extend_schema(
    tags=['Product'],
    description='Изменение товара. Доступно всем пользователям, связанным с компанией.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'storage': {
                    'type': 'integer',
                    'example': 1
                },
                'title': {
                    'type': 'string',
                    'example': 'Игровая приставка PS5'
                },
                'description': {
                    'type': 'string',
                    'example': 'Описание характеристик приставки'
                },
                'purchase_price': {
                    'type': 'string',
                    'example': '50000.00'
                },
                'sale_price': {
                    'type': 'string',
                    'example': '79990.90'
                },
            }
        }
    )
)
class UpdateProductView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = ProductSerializer

    def update(self,request, pk):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response({'message': 'Товар не найден!'}, status=404)
        if product.storage.company != request.user.company:
            return Response({'message': 'У Вас нет доступа к этому товару!'}, status=403)

        new_storage = Storage.objects.filter(id=request.data['storage']).first()
        if not new_storage:
            return Response({'message': 'Новый склад не найден!'}, status=404)
        if request.user.company != new_storage.company:
            return Response({'message': 'У Вас нет доступа к указанному складу!'}, status=403)

        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Поставщик обновлен', 'detail': serializer.data})


@extend_schema(
    tags=['Product'],
    description='Удаление товара по ID. Доступно всем пользователям, связанным с компанией.',
)
class DeleteProductView(DestroyAPIView):
    serializer_class = ProductSerializer

    def delete(self, request, pk):
        product = Product.objects.filter(id=pk).first()
        if not product:
            return Response({'message': 'Товар не найден!'}, status=404)
        user = request.user
        if product.storage.company != user.company:
            return Response({'message': 'У Вас нет доступа к этому товару!'}, status=403)
        product.delete()
        return Response(status=204)