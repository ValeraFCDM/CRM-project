from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from .models import Supplier
from .serializers import SupplierSerializer
from drf_spectacular.utils import extend_schema, OpenApiRequest

@extend_schema(
    tags=['Supplier'],
    description='Создание поставщика. Доступно всем пользователям, связанным с компанией.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'title': {
                    'type': 'string',
                    'example': 'ИП Иванов И.И.'
                },
                'inn': {
                    'type': 'string',
                    'example': '0123456789'
                }
            }
        }
    )
)
class CreateSupplierView(CreateAPIView):
    serializer_class = SupplierSerializer

    def post(self, request):
        user = request.user
        if not user.company:
            return Response({'message': 'Вы не прикреплены к компании!'}, status=403)
        serializer = SupplierSerializer(data=request.data, context={'company': user.company})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Поставщик успешно добавлен!', 'detail': serializer.data}, status=201)


@extend_schema(
    tags=['Supplier'],
    description='Получение списка поставщиков компании. Доступно всем пользователям, связанным с компанией.',
)
class ListSupplierView(ListAPIView):
    serializer_class = SupplierSerializer

    def get(self, request):
        user = request.user
        company = user.company
        if not company:
            return Response({'message': 'Вы не прикреплены к компании!'}, status=403)
        queryset = Supplier.objects.filter(company=company).all()
        serializer = SupplierSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=['Supplier'],
    description='Изменение поставщика по ID. Доступно всем пользователям, связанным с компанией, закрепленной за поставщиком.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'title': {
                    'type': 'string',
                    'example': 'ИП Иванов И.И.'
                },
                'inn': {
                    'type': 'string',
                    'example': '0123456789'
                }
            }
        }
    )
)
class UpdateSupplierView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = SupplierSerializer


    def update(self,request, pk):
        user = request.user
        supplier = Supplier.objects.filter(id=pk).first()
        if not supplier:
            return Response({'message': 'Поставщик не найден!'}, status=404)
        if user.company != supplier.company:
            return Response({'message': 'Вы не относитесь к данной компании!'}, status=403)
        serializer = SupplierSerializer(instance=supplier, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Поставщик обновлен', 'detail': serializer.data})


@extend_schema(
    tags=['Supplier'],
    description='Удаление поставщика по ID. Доступно всем пользователям, связанным с компанией.',
)
class DeleteSupplierView(DestroyAPIView):
    serializer_class = SupplierSerializer

    def delete(self, request, pk):
        user = request.user
        supplier = Supplier.objects.filter(id=pk).first()
        if not supplier:
            return Response({'message': 'Поставщик не найден!'}, status=404)
        if user.company != supplier.company:
            return Response({'message': 'Вы не относитесь к данной компании!'}, status=403)
        supplier.delete()
        return Response(status=204)