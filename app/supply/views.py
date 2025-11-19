from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Supply, SupplyProduct
from .serializers import SupplySerializer
from drf_spectacular.utils import extend_schema, OpenApiRequest


@extend_schema(
    tags=['Supply'],
    description='Создание поставки. Доступно всем пользователям, связанным с компанией.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'supplier_id': {
                    'type': 'integer',
                    'example': '1'
                },
                'delivery_date': {
                    'type': 'string',
                    'example': '1999-12-31'
                },
                'products': {
                    'type':'array',
                    'items': {
                        'type':'object',
                        'properties': {
                            'id': {
                                'type': 'integer',
                                'example': '1'
                            },
                            'quantity': {
                                'type': 'integer',
                                'example': '10'
                            },
                        }
                    }
                }
            }
        }
    )
)
class CreateSupplyView(CreateAPIView):
    serializer_class = SupplySerializer

    def post(self, request):
        user = request.user
        if not user.company:
            return Response({'message': 'Вы не прикреплены к компании!'}, status=403)
        company = user.company
        if not company.storage:
            return Response({'message': 'У Вашей компании не зарегистрирован склад!'}, status=404)

        serializer = SupplySerializer(data=request.data, context={'company': company})
        serializer.is_valid(raise_exception=True)
        data_for_save = serializer.validated_data

        supply = Supply.objects.create(
            supplier=data_for_save['supplier'],
            delivery_date=data_for_save['delivery_date']
        )
        for supply_item in data_for_save['products']:
            product_supply_item = SupplyProduct.objects.create(
                supply=supply,
                product=supply_item['product'],
                quantity=supply_item['quantity']
            )
            product = product_supply_item.product
            product.quantity += product_supply_item.quantity
            product.save()
        return Response({'message': 'Поставка успешно создана!', 'supply_id': supply.id}, status=201)


@extend_schema(
    tags=['Supply'],
    description='Получение списка поставок. Доступно всем пользователям, связанным с компанией.',
)
class ListSupplyView(ListAPIView):
    serializer_class = SupplySerializer

    def get(self, request):
        user = request.user
        company = user.company
        if not company:
            return Response({'message': 'Вы не прикреплены к компании!'}, status=403)

        queryset = Supply.objects.filter(supplier__company=company)
        supply_data_list = []
        for supply_item in queryset:
            serializer = SupplySerializer(supply_item)
            supply_data = serializer.data
            supply_data['supply_products'] = []
            supply_products_set = supply_item.supply_products.all()

            for supply_products_item in supply_products_set:
                supply_data_detail = {'product': supply_products_item.product.id,
                                      'quantity': supply_products_item.quantity}
                supply_data['supply_products'].append(supply_data_detail)

            supply_data_list.append(supply_data)

        return Response(supply_data_list)