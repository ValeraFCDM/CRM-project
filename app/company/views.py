from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from .models import Company
from .serializers import CompanySerializer
from drf_spectacular.utils import extend_schema, OpenApiRequest


@extend_schema(
    tags=['Company'],
    description='Создание компании. Доступно только авторизованным пользователям.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'inn': {
                    'type': 'string',
                    'example': '0000000000'
                },
                'title': {
                    'type': 'string',
                    'example': 'ООО Пример'
                }
            }
        }
    )
)
class CreateCompanyView(CreateAPIView):
    serializer_class = CompanySerializer

    def post(self, request):
        user = request.user
        if user.company:
            return Response({'message': f'Вы уже относитесь к компании {user.company}!'}, status=400)
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        new_company = Company.objects.filter(inn=serializer.validated_data['inn']).first()
        user.is_company_owner = True
        user.company = new_company
        user.save()
        return Response ({'message': f'Компания успешно добавлена!', 'detail': serializer.data}, status=201)


@extend_schema(
    tags=['Company'],
    description='Получение данных о компании по ее ID. Доступно только авторизованным пользователям.'
)
class GetCompanyView(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


@extend_schema(
    tags=['Company'],
    description='Редактирование компании. Доступно только владельцам компании.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'inn': {
                    'type': 'string',
                    'example': '0000000000'
                },
                'title': {
                    'type': 'string',
                    'example': 'ООО Пример'
                }
            }
        }
    )
)
class UpdateCompanyView(UpdateAPIView):
    http_method_names = ['put']
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def update(self,request):
        user = request.user
        if not user.is_company_owner:
            return Response({'message': 'Вы не являетесь владельцем компании!'}, status=403)
        company = user.company
        serializer = CompanySerializer(instance=company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Данные компании обновлены!'})


@extend_schema(
    tags=['Company'],
    description='Удаление компании. Доступно только владельцам компании.'
)
class DeleteCompanyView(DestroyAPIView):
    serializer_class = CompanySerializer

    def delete(self, request):
        user = request.user
        if not user.is_company_owner:
            return Response({'message': 'Вы не являетесь владельцем компании!'}, status=403)
        company = Company.objects.filter(id=user.company.id)
        user.is_company_owner = False
        user.save()
        company.delete()
        return Response(status=204)