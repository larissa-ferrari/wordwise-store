from django.core.management.base import BaseCommand
from faker import Faker
from random import randint, choice, shuffle
from datetime import datetime
from book.models import Livro, Categoria


class Command(BaseCommand):
    help = "Popula o banco de dados com livros fictícios"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num", type=int, default=50, help="Número de livros a criar"
        )

    def handle(self, *args, **options):
        fake = Faker("pt_BR")
        num = options["num"]
        categorias = Categoria.objects.all()

        if not categorias.exists():
            self.stdout.write(self.style.ERROR("Crie categorias primeiro!"))
            return

        tipos_livro = ["Capa dura", "Capa mole", "E-book", "Audiobook"]
        idiomas = ["Português", "Inglês", "Espanhol", "Francês"]
        real_isbns = [
            "9780743273565",
            "9780316769488",
            "9780451524935",
            "9780060934347",
            "9780544003415",
            "9780061120084",
            "9780060883287",
            "9780375842207",
            "9782070612758",
            "9780141439518",
            "9780140449136",
            "9780553296983",
            "9780061122415",
            "9780307474278",
            "9788532511010",
            "9780451526342",
            "9780060850524",
            "9780141439556",
            "9780141442464",
        ]

        isbn_pool = real_isbns.copy()
        shuffle(isbn_pool)
        isbn_index = 0

        for i in range(num):
            if isbn_index >= len(isbn_pool):
                isbn_pool = real_isbns.copy()
                shuffle(isbn_pool)
                isbn_index = 0

            selected_isbn = isbn_pool[isbn_index]
            isbn_index += 1

            try:
                Livro.objects.create(
                    titulo=f"{fake.sentence(nb_words=3)} {choice(['Edição', 'Volume', 'Coleção'])}",
                    autor=fake.name(),
                    editora=fake.company(),
                    ano_publicacao=randint(1900, datetime.now().year),
                    preco=round(fake.random.uniform(10.0, 200.0), 2),
                    estoque=randint(0, 100),
                    descricao=fake.paragraph(nb_sentences=3),
                    imagem_url=f"https://covers.openlibrary.org/b/isbn/{selected_isbn}-M.jpg",
                    isbn=selected_isbn,
                    tipo=choice(tipos_livro),
                    numero_paginas=randint(100, 600),
                    idioma=choice(idiomas),
                    categoria=choice(categorias),
                    status=choice([True, False]),
                )
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Erro ao criar livro {i + 1}: {e}"))

        self.stdout.write(self.style.SUCCESS(f"{num} livros criados com sucesso."))
