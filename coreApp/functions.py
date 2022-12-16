import math



def intervale(number):
    return [round(number, 1), round(number, 1)+0.1]
    # return [number - 0.02, number + 0.0]



def intervale2(number):
    if number > 2.5:
        return [2.51, 3]
    elif 2. < number <= 2.5 :
        return [2.1, 2.5]
    elif 1.5 < number <= 2. :
        return [1.51, 2.]
    elif 1. < number <= 1.5 :
        return [1.1, 1.5]
    elif 0.5 < number <= 1. :
        return [0.51, 1.]
    elif 0 <= number <= 0.5 :
        return [0, 0.5]



def factorial(n):
    if n == 1 or n == 0:
        return 1
    return n * factorial(n-1)


def moyenne_harmonique(a, b):
    return math.sqrt((math.pow(a, 2) + math.pow(b, 2)) / 2)


def moyenne_geometrique(a, b):
    return math.sqrt(a * b)



def fish_law(avg, number):
    return round(((math.pow(avg, number) * math.exp(-avg)) / factorial(number)) * 100, 2)


def fish_law_moins(avg, but):
    x = total = 0
    while x < but:
        total += fish_law(avg, x)
        x += 1
    return total


def fish_law_plus(avg, but):
    return 100 - fish_law_moins(avg, but)


def fish_law_favoris_vn(avg, but):
    return (fish_law_moins(avg, but) + (avg * 100) )/ 2