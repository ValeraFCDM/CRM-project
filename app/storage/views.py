from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import Storage
from .serializers import StorageSerializer
from drf_spectacular.utils import extend_schema, OpenApiRequest


@extend_schema(
    tags=['Storage'],
    description='Создание склада. Доступно только владельцам компании.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'address': {
                    'type': 'string',
                    'example': 'Москва, ул.Рябиновая, д.25, пом.Г'
                }
            }
        }
    )
)
class CreateStorageView(CreateAPIView):
    serializer_class = StorageSerializer

    def post(self, request):
        user = request.user
        if not user.is_company_owner:
            return Response({'message': 'Вы не являетесь владельцем компании!'}, status=400)
        company = user.company
        storage = Storage.objects.filter(company=company).first()
        if storage:
            return Response({'message': f'За Вашей компанией уже числится склад (id: {storage.id})!'}, status=400)
        serializer = StorageSerializer(data=request.data, context={'company': company})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        storage = Storage.objects.filter(company=company).first()
        return Response ({'message': 'Склад успешно добавлен!',
                          'id' : f'{storage.id}',
                          'address': f'{storage.address}',
                          'company_id': f'{storage.company.id}'}, status=201)


@extend_schema(
    tags=['Storage'],
    description='Получение данных о складе, привязанном к компании пользователя.'
                'Доступно всем пользователям, связанным с этой компанией'
)
class GetStorageView(RetrieveAPIView):
    def get(self,request, pk):
        user = request.user
        storage = Storage.objects.filter(id=pk).first()
        if not storage:
            return Response({'message': 'Склад не найден!'}, status=404)
        if user.company != storage.company:
            return Response({'message': 'Вы не являетесь сотрудником компании, к которой относится склад!'}, status=403)

        return Response({'id': f'{storage.id}',
                         'address': f'{storage.address}',
                         'company_id': f'{storage.company.id}'}, status=200)


@extend_schema(
    tags=['Storage'],
    description='Редактирование склада. Доступно только владельцам компании, связанной со складом.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'address': {
                    'type': 'string',
                    'example': 'Москва, ул.Рябиновая, д.25, пом.Г'
                }
            }
        }
    )
)
class UpdateStorageView(UpdateAPIView):
    http_method_names = ['put']
    serializer_class = StorageSerializer

    def update(self,request, pk):
        user = request.user
        storage = Storage.objects.filter(id=pk).first()
        if not storage:
            return Response({'message': 'Склад не найден!'}, status=404)
        if user.is_company_owner and user.company == storage.company:
            serializer = StorageSerializer(instance=storage, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'id': 'Склад обновлен'}, status=201)
        return Response({'message': 'Вы не являетесь владельцем компании, к которой относится склад!'}, status=403)


@extend_schema(
    tags=['Storage'],
    description='Удаление склада. Доступно только владельцам компании, связанной со складом.'
)
class DeleteStorageView(DestroyAPIView):
    def delete(self, request, pk):
        user = request.user
        storage = Storage.objects.filter(id=pk).first()
        if not storage:
            return Response({'message': 'Склад не найден!'}, status=404)
        if user.is_company_owner and user.company == storage.company:
            storage.delete()
            return Response(status=204)
        return Response({'message': 'Вы не являетесь владельцем компании, к которой относится склад!'}, status=403)