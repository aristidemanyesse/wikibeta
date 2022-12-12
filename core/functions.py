import math



def intervale(number):
    # if number > 2.6:
    #     return [2.61, 3]
    # elif 2.3 < number <= 2.6 :
    #     return [2.31, 2.6]
    # elif 1.9 < number <= 2.3 :
    #     return [1.91, 2.3]
    # elif 1.3 < number <= 1.9 :
    #     return [1.31, 1.9]
    # elif 0.7 < number <= 1.3 :
    #     return [0.71, 1.3]
    # elif 0 <= number <= 0.7 :
    #     return [0, 0.7]
    return [round(number, 1), round(number, 1)+0.1]
    # return [number - 0.02, number + 0.0]




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