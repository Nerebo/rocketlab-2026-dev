import hashlib
import random

def generate_id():
    palavras = [
        "casa", "carro", "janela", "porta", "livro", "mesa", "cadeira", "computador", "teclado", "mouse",
        "monitor", "celular", "internet", "rede", "servidor", "cliente", "banco", "dados", "arquivo", "pasta",
        "código", "programa", "função", "classe", "objeto", "variável", "lista", "dicionario", "tupla", "string",
        "inteiro", "float", "booleano", "verdadeiro", "falso", "condicao", "loop", "while", "for", "if",
        "else", "elif", "import", "modulo", "pacote", "sistema", "usuario", "senha", "login", "seguranca"
    ]

    tres_palavras = random.sample(palavras, 3)
    id_string = ''.join(tres_palavras)

    # Randomiza maiúsculo/minúsculo por caractere
    id_random = ''.join(
        ch.upper() if random.choice([True, False]) else ch.lower()
        for ch in id_string
    )

    return(hashlib.md5(id_random.encode()).hexdigest())