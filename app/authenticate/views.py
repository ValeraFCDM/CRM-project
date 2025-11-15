from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserRegisterSerializer, UserAttachSerializer
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiRequest

@extend_schema(
    tags=['Users'],
    description='Регистрация нового пользователя.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'username': {
                    'type': 'string',
                    'example': 'User_2000'
                },
                'email': {
                    'type': 'string',
                    'example': 'user@example.com'
                },
                'password': {
                    'type': 'string',
                    'example': 'Q12345wertY'
                },
                'password_confirm': {
                    'type': 'string',
                    'example': 'Q12345wertY'
                }
            }
        }
    )
)
class UserRegisterView(CreateAPIView):
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer


@extend_schema(
    tags=['Users'],
    description='Прикрепление пользователя к компании. Доступно только владельцам компании.',
    request=OpenApiRequest(
        request={
            'type':'object',
            'properties': {
                'email': {
                    'type': 'string',
                    'example': 'user@example.com'
                }
            }
        }
    )
)
class UserAttachView(CreateAPIView):
    serializer_class = UserAttachSerializer

    def post(self, request):
        if not request.user.is_company_owner:
            return Response({'message': 'Вы не являетесь владельцем компании!'}, status=403)
        company = request.user.company
        serializer = UserAttachSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        user = serializer.validated_data['user']
        user.company = company
        user.save()

        return Response ({'detail': f'Пользователь {user.username} успешно прикреплен к компании {company}'}, status=201)

