from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed
from rest_framework.viewsets import ModelViewSet
from authentication.models import User
from authentication.serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['POST'], detail=False, url_path='register')
    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User(
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data['first_name'],
            phone_number=serializer.validated_data['phone_number'],
            is_active=True
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({'message': 'success'})

    @action(methods=['POST'], detail=False, url_path='login')
    def login(self, request):
        if 'email' not in request.data:
            raise ValidationError({'error': 'E-mail не может быть пустым'})
        if 'password' not in request.data:
            raise ValidationError({'error': 'Пароль не может быть пустым'})

        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            raise NotFound({'error': 'Пользователь не найден'})

        if not user.check_password(request.data['password']):
            raise AuthenticationFailed({'error': 'Неверный пароль'})

        if not user.is_active:
            raise AuthenticationFailed({'error': 'Пользователь не активен'})

        refresh = RefreshToken.for_user(user)
        response = Response()
        response.set_cookie('refresh', str(refresh))
        response.data = {'accessToken': str(refresh.access_token)}

        return response

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated], url_path='me')
    def get_user(self, request):
        user = request.user
        data = self.serializer_class(user).data
        return Response(data)

    @action(methods=['POST'], detail=False, url_path='logout', permission_classes=[IsAuthenticated])
    def logout(self, request):
        response = Response()
        response.delete_cookie('refresh')
        return response

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            raise PermissionDenied('У вас нет прав на просмотр этих данных.')
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            raise PermissionDenied('У вас нет прав на изменение этих данных.')
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance != request.user:
            raise PermissionDenied('У вас нет прав на удаление этих данных.')
        return super().destroy(request, *args, **kwargs)