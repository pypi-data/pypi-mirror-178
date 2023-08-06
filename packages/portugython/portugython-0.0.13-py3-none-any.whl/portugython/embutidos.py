# TODO: Improve error messages
# TODO: Improve importing structure: avoid deep nested import -> from example.a.b import


def absoluto(numero):
    """ Retorna o valor absoluto de um número. O argumento pode ser um inteiro, um número de ponto flutuante ou um
    objeto implementando __abs__(). Se o argumento é um número complexo, sua magnitude é retornada. """
    try:
        return abs(numero)
    except TypeError as err:
        print()
        raise


# TODO: aiter not yet implemented


def todos(iteravel):
    """ Retorna True se todos os elementos de iterable são verdadeiros (ou se iterable estiver vazio)."""
    try:
        return all(iteravel)
    except TypeError as e:
        raise TypeError(f'Erro de tipo. Objeto "{type(iteravel).__name__}" não é iterável')


def qualquer(iteravel):
    """
    Retorna True se algum elemento de iterable for verdadeiro. Se iterable estiver vazio, retorna False.
    :return:
    """
    try:
        return any(iteravel)
    except TypeError:
        raise


# TODO: anext not yet implemented

# TODO: ascii not yet implemented


def binario(inteiro):
    """Converte um número inteiro para uma string de binários prefixada com “0b”. O resultado é uma expressão Python
    válida. Se x não é um objeto Python int, ele tem que definir um método __index__() que devolve um inteiro. """

    try:
        return bin(inteiro)
    except TypeError as err:
        raise


# TODO: breakpoint not yet implemented


chamavel = callable
unicode = chr

# TODO: compile not yet implemented
# TODO: copyright not yet implemented
# TODO: credits not yet implemented
# TODO: delattr not yet implemented
# TODO: dir not yet implemented
# TODO: divmod not yet implemented
# TODO: eval not yet implemented
# TODO: exec not yet implemented

sair = exit

# TODO: format not yet implemented
# TODO: getattr not yet implemented
# TODO: globals not yet implemented

tem_atributo = hasattr

# TODO: hash not yet implemented
# TODO: help NEEDS IMPLEMENTATION
# TODO: hex not yet implemented
# TODO: id not yet implemented

entrada = input
isinstancia = isinstance
isumasubclasse = issubclass

# TODO: iter not yet implemented

comprimento = len

# TODO: license not yet implemented
# TODO: locals not yet implemented
# TODO: map not yet implemented


maior = max
menor = min
proximo = next


# TODO: oct not yet implemented

def abra(arquivo, modo=None, buffering=None, encoding=None, errors=None, newline=None, closefd=True):
    modos = {
        'leitura': 'r',
        'escrita': 'w',
        'exclusivo': 'x',
        'anexo': 'a',
        'binario': 'b',
        'text': 't',
    }
    return open(file=arquivo, mode=modos.get(modo, 'r'), encoding=encoding)


valorascii = ord

elevado = potencia = pow
imprima = print
parar = quit

# TODO: repr not yet implemented

invertido = reversed
arredonde = round
definaatributo = setattr
arrumado = sorted
some = sum

# TODO: vars not yet implemented

junte = zip
