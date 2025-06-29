from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from book.models import Livro, ClienteFavoritos
from .models import Cliente

class FavoritoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, book_id):
        try:
            livro = Livro.objects.get(id=book_id)
        except Livro.DoesNotExist:
            return Response({"detail": "Livro não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        cliente = Cliente.objects.get(user=request.user)

        favorito, created = ClienteFavoritos.objects.get_or_create(cliente=cliente, livro=livro)
        if created:
            return Response({"detail": "Livro adicionado aos favoritos."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "Livro já está nos favoritos."}, status=status.HTTP_200_OK)

    def delete(self, request, book_id):
        try:
            livro = Livro.objects.get(id=book_id)
        except Livro.DoesNotExist:
            return Response({"detail": "Livro não encontrado."}, status=status.HTTP_404_NOT_FOUND)

        cliente = Cliente.objects.get(user=request.user)

        try:
            favorito = ClienteFavoritos.objects.get(cliente=cliente, livro=livro)
            favorito.delete()
            return Response({"detail": "Livro removido dos favoritos."}, status=status.HTTP_204_NO_CONTENT)
        except ClienteFavoritos.DoesNotExist:
            return Response({"detail": "Livro não está nos favoritos."}, status=status.HTTP_404_NOT_FOUND)
