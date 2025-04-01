import re
from datetime import datetime

# Código criado para que a cada frase escrita pela pessoa no nome do(a) cliente..
# Ela seja formatada com uma letra Maiúscula no começo de cada frase. Ex: Brandon Rodrigues.

def formatar_nome_pet(e):
    e.control.value = e.control.value.title()
    e.control.update()



# Código para deixar o celular formatado na hora de digitar.
def formatar_celular(e):

    # Remove tudo que não for número
    numero = re.sub(r"\D", "", e.control.value)

    if len(numero) > 11:
        numero = numero[:11]  # Garante no máximo 11 dígitos

    # Aplica a máscara corretamente
    if len(numero) >= 2:
        ddd = numero[:2]
        restante = numero[2:]

        if len(restante) > 5:
            celular_formatado = f"({ddd}) {restante[:5]}-{restante[5:]}"
        else:
            celular_formatado = f"({ddd}) {restante}"
    else:
        celular_formatado = numero  # Caso ainda não tenha 2 números para o DDD

    e.control.value = celular_formatado
    e.control.update()


def formatar_horario(e):
    valor = e.control.value
    valor = ''.join(filter(str.isdigit, valor))  # Mantém apenas números
    if len(valor) >= 2:
        valor = valor[:2] + (":" + valor[2:4] if len(valor) > 2 else "")
    e.control.value = valor[:5]  # Mantém no formato "HH:MM"
    e.control.update()


def formatar_data(e):
    valor = e.control.value
    numeros = ''.join(filter(str.isdigit, valor))  # Mantém apenas números

    if len(numeros) > 8:  # Limita a 8 caracteres (DDMMAAAA)
        numeros = numeros[:8]

    # Monta a string formatada conforme o usuário digita
    formatado = ""
    if len(numeros) > 0:
        formatado += numeros[:2]  # Dia
    if len(numeros) > 2:
        formatado += "/" + numeros[2:4]  # Mês
    if len(numeros) > 4:
        formatado += "/" + numeros[4:8]  # Ano

    e.control.value = formatado
    e.control.update()


def formatar_dinheiro(e):
    """ Formata o valor digitado para o padrão R$ XX,XX """
    valor = e.control.value
    # Remove tudo que não for número
    valor = "".join(filter(str.isdigit, valor))
    if valor == "":
        valor = "0"
    valor = int(valor) / 100  # Converte para decimal
    e.control.value = f"R$ {valor:,.2f}".replace(
        ",", "X").replace(".", ",").replace("X", ".")  # Formatação
    e.control.update()
