# coding: utf-8


def username_to_dni(username):
    username = username[1:len(username)+1]
    return username+letra_de_numeros(username)


def letra_de_numeros(numeros):
        seq = 'TRWAGMYFPDXBNJZSQVHLCKE'
        aux = int(numeros) % len(seq)
        return seq[aux]