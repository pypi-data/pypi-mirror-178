from getpass import getpass


def pegasenha(prompt='Senha: ', stream=None):
    return getpass(prompt=prompt, stream=stream)
