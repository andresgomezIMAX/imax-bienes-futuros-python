import pandas as pd
import math

def nLetras(numeros, n, con):
    if n != 0:
        mT = f'{con}{numeros[n]} '
    else:
        mT = ''
    
    return mT

def menorTreinta(intt, uni):
    if intt < 30 and intt > 10:
        decimos = intt
        un = 0
    else:
        un = uni
        decimos = intt - un
    
    return decimos, un

def numaLetras(num):
    numeros ={
            0: '', 1: 'UNO', 2: 'DOS', 3: 'TRES', 4: 'CUATRO', 5: 'CINCO', 6: 'SEIS', 7: 'SIETE', 8: 'OCHO', 9: 'NUEVE', 10: 'DIEZ',
            11: 'ONCE', 12: 'DOCE', 13: 'TRECE', 14: 'CATORCE', 15: 'QUINCE', 16: 'DIECISÉIS', 17: 'DIECISIETE', 18: 'DIECIOCHO', 19: 'DIECINUEVE', 20: 'VEINTE',
            21: 'VEINTIUNO', 22: 'VEINTIDÓS', 23: 'VEINTITRÉS', 24: 'VEINTICUATRO', 25: 'VEINTICINCO', 26: 'VEINTISÉIS', 27: 'VEINTISIETE', 28: 'VEINTIOCHO', 29: 'VEINTINUEVE', 30: 'TREINTA',
            40: 'CUARENTA', 50: 'CINCUENTA', 60: 'SESENTA', 70: 'SETENTA', 80: 'OCHENTA', 90: 'NOVENTA', 100: 'CIENTO',
            200: 'DOSCIENTOS', 300: 'TRESCIENTOS', 400: 'CUATROCIENTOS', 500: 'QUINIENTOS', 600: 'SEISCIENTOS', 700: 'SETECIENTOS', 800: 'OCHOCIENTOS', 900: 'NOVECIENTOS', 
            }

    decimales = (num - math.floor(num))*100
    letras = f"CON {'{:.0f}'.format(round(decimales, 0))}/100"

    entero = num - decimales/100
    
    decimos, uni = menorTreinta(entero - math.floor(entero/100)*100, entero - math.floor(entero/10)*10)

    cientos = entero - math.floor(entero/1000)*1000 - uni - decimos 
    if cientos + decimos != 0:
        y = 'Y '
    else:
        y = ''

    letras = f"{nLetras(numeros, cientos, '')}{nLetras(numeros, decimos, '')}{nLetras(numeros, uni, y)}{letras}"

    miles = (entero - math.floor(entero/10000)*10000 - uni - decimos - cientos)/1000
    decimosmiles = (entero - math.floor(entero/100000)*100000 - uni - decimos - cientos - miles*1000)/1000
    cientosmiles = (entero - math.floor(entero/1000000)*1000000 - uni - decimos - cientos - miles*1000 - decimosmiles*1000)/1000
    if decimosmiles + cientosmiles + miles != 0:
        if decimosmiles + cientosmiles != 0:
            y = 'Y '
        else:
            y = ''
        letras = f"{nLetras(numeros, cientosmiles, '')}{nLetras(numeros, decimosmiles, '')}{nLetras(numeros, miles, y)}MIL {letras}"

    millones = (entero - math.floor(entero/10000000)*10000000 - uni - decimos - cientos - miles*1000 - decimosmiles*1000 - cientosmiles*1000)/1000000
    decimosmillones = (entero - math.floor(entero/100000000)*100000000 - uni - decimos - cientos - miles*1000 - decimosmiles*1000 - cientosmiles*1000 - millones*1000000)/1000000
    cientosmillones = (entero - math.floor(entero/1000000000)*1000000000 - uni - decimos - cientos - miles*1000 - decimosmiles*1000 - cientosmiles*1000 - millones*1000000 - decimosmillones*1000000)/1000000
    if cientosmillones + decimosmillones + millones !=0:
        if cientosmillones + decimosmillones != 0:
            y = 'Y '
        else:
            y = ''
        letras = f"{nLetras(numeros, cientosmillones, '')}{nLetras(numeros, decimosmillones, '')}{nLetras(numeros, millones, y)}MILLONES {letras}"

    return letras

if __name__ == '__main__':

    letras = numaLetras(float(input('Digite un numero: ')))
    print(letras)