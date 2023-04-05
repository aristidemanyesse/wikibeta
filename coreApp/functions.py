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


def moyenne_but(atk, defe):
    atk = round(atk, 1)
    defe = round(defe, 1)
    
    if atk == defe:
        avg = atk + (defe / 2)
        
    elif atk - defe >= 2:
        avg = defe + (defe / (atk - defe))
        
    elif atk - defe > 0:
        avg = defe + ((atk - defe) / 2)
        
    elif defe - atk >= 2 :
        avg =  atk + ((2 * atk ) / defe)
        
    elif defe - atk > 0 :
        avg =  atk / defe
        
    return avg



def calcul_p(a , b):
    if a >= b:
        t = (a-b)/(a+b)
        return 0.5 + (t / 2)
    else:
        t = a / (a +b)
        return t



def bimodal_poisson(lambda_1, lambda_2, p, k):
    prob = p*math.exp(-lambda_1)*(lambda_1**k)/math.factorial(k) + (1-p)*math.exp(-lambda_2)*(lambda_2**k)/math.factorial(k)
    return round(prob, 2)





def fish_law(avg, number):
    return round(((math.pow(avg, number) * math.exp(-avg)) / factorial(number)) * 100, 2)

# def fish_law(avg, number):
#     return round(((avg / number) / factorial(number)) * math.exp(-avg) * 100 , 2)


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