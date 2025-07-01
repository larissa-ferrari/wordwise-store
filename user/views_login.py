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
from utils.cart import get_carrinho_anonimo_por_sessao


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

        token, _ = Token.objects.get_or_create(user=user)

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

        carrinho_anonimo = get_carrinho_anonimo_por_sessao(request)

        if carrinho_anonimo:
            carrinho_cliente, _ = Carrinho.objects.get_or_create(
                cliente=cliente, status="ativo"
            )

            for item in carrinho_anonimo.itemcarrinho_set.all():
                item_existente = ItemCarrinho.objects.filter(
                    carrinho=carrinho_cliente, livro=item.livro
                ).first()

                if item_existente:
                    item_existente.quantidade += item.quantidade
                    item_existente.save()
                else:
                    item.carrinho = carrinho_cliente
                    item.save()

            carrinho_anonimo.delete()

            request.session.pop("carrinho_id", None)

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
