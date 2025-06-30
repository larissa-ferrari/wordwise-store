from django.core.management.base import BaseCommand
from faker import Faker
from random import choice
from category.models import Categoria


class Command(BaseCommand):
    help = "Popula o banco de dados com categorias fictícias"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num", type=int, default=15, help="Número de categorias a criar"
        )

    def handle(self, *args, **options):
        fake = Faker("pt_BR")
        num = options["num"]

        categorias_base = [
            "Romance",
            "Ficção Científica",
            "Fantasia",
            "Terror",
            "Suspense",
            "Biografia",
            "História",
            "Autoajuda",
            "Negócios",
            "Tecnologia",
            "Infantil",
            "Juvenil",
            "Poesia",
            "Arte",
            "Culinária",
        ]

        for i in range(num):
            nome = (
                categorias_base[i]
                if i < len(categorias_base)
                else fake.word().capitalize() + " " + fake.word().capitalize()
            )
            Categoria.objects.create(
                nome=nome,
                descricao=f"Livros sobre {nome}. {fake.sentence()}",
                imagem_url=f"https://picsum.photos/200/300?random={i}",
                status=choice([True, True, False]),  # ~67% ativo
            )

        self.stdout.write(self.style.SUCCESS(f"Successfully created {num} categorias"))
