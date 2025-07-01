from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from cart.models import Carrinho, ItemCarrinho
from user.models import Cliente


class LoginView(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"detail": "Usuário ou senha inválidos."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token, created = Token.objects.get_or_create(user=user)

        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        try:
            cliente = user.cliente
        except Cliente.DoesNotExist:
            return Response(
                {"detail": "Usuário autenticado não possui cliente associado."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            carrinho_anonimo = Carrinho.objects.get(
                session_key=session_key, status="ativo"
            )
        except Carrinho.DoesNotExist:
            carrinho_anonimo = None

        if carrinho_anonimo:
            carrinho_cliente, created = Carrinho.objects.get_or_create(
                cliente=cliente, status="ativo"
            )

            if created:
                carrinho_anonimo.cliente = cliente
                carrinho_anonimo.session_key = None
                carrinho_anonimo.identificador = None
                carrinho_anonimo.save()
            else:
                for item in carrinho_anonimo.itemcarrinho_set.all():
                    item_existente, criado = ItemCarrinho.objects.get_or_create(
                        carrinho=carrinho_cliente,
                        livro=item.livro,
                        defaults={"quantidade": item.quantidade},
                    )
                    if not criado:
                        item_existente.quantidade += item.quantidade
                        item_existente.save()
                carrinho_anonimo.delete()

        return Response(
            {
                "token": token.key,
                "username": user.username,
                "email": user.email,
                "user_type": user.user_type,
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({"message": "Logout realizado com sucesso."})
