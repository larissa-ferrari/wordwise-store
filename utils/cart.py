from cart.models import Carrinho


def get_carrinho_anonimo_por_sessao(request):
    if not request.session.session_key:
        request.session.create()

    carrinho_id = request.session.get("carrinho_id")
    if not carrinho_id:
        return None

    try:
        return Carrinho.objects.get(identificador=carrinho_id, status="ativo")
    except Carrinho.DoesNotExist:
        return None
