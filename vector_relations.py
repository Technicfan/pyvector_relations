#!/bin/python

"""
MIT License

Copyright (c) 2024 Technicfan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
try:
    import numpy as np
except ImportError:
    print("numpy muss installiert sein!")
    exit(1)

def custom_round(number):
    part = number - int(number)
    if part != 0:
        return round(number, 2)
    else:
        return int(number)

def check_crossing(s1, r1, s2, r2):
    first_part = []
    for x, y in zip(r1, r2):
        first_part.append([x, -y])

    second_part = []
    for a1, a2 in zip(s1, s2):
        second_part.append([a2 - a1])

    if len(first_part) == 3:
        results = np.linalg.solve(first_part[:-1], second_part[:-1])
        if not np.allclose(np.dot(first_part[-1], results), second_part[-1]):
            return 0
    else:
        results = np.linalg.solve(first_part, second_part)

    point = []
    for one, two in zip(s1, r1):
        point.append(one + results[0][0] * two)
    return point

def check_parallel(s1, r1, s2, r2):
    i = 0
    while i < len(r1) - 1 and r1[i] == r2[i] == 0:
        i += 1
    if r2[i] != 0:
        first = r1[i] / r2[i]
        for one, two in zip(r1[i:], r2[i:]):
            if not (one == two == 0) and one / two != first:
                return 0
    else:
        return 0
    i = 0
    while i < len(r2) - 1 and r2[i] == (s1[i] - s2[i]) == 0:
        i += 1
    if r2[i] != 0:
        first = (s1[0] - s2[0]) / r2[0]
        for one, two, three in zip(s1[1:], s2[1:], r2[1:]):
            if not ((one - two) == three == 0) and (one - two) / three != first:
                return 1
    else:
        return 2

def help():
    print(
        "\nFehlerhafte Eingabe!\n" +
        "\nEingabe der Vektoren:\n" +
        "   x, y, z oder x, y\n" +
        "   - Leerzeichen nicht notwending\n" +
        "   - '.' als Dezimaltrennzeichen\n" +
        "   - alle vier Vektoren müssen entweder zwei- oder dreidimensional sein (alle gleich)\n"
    )
    exit()

def main():
    try:
        print("\n1. Gerade:")
        s1 = list(map(float, input("    Stützvektor: ").split(",")))
        r1 = list(map(float, input("    Richtungsvektor: ").split(",")))
        print("2. Gerade:")
        s2 = list(map(float, input("    Stützvektor: ").split(",")))
        r2 = list(map(float, input("    Richtungsvektor: ").split(",")))
    except:
        help()
    
    if not (len(s1) == len(r1) == len(s2) == len(r2) in [2, 3]):
        help()

    relation = check_parallel(s1, r1, s2, r2)
    print()
    if relation != 0:
        if relation == 1:
            print("Die Geraden sind parallel.")
        else:
            print("Die Geraden sind Deckungsgleich.")
    else:
        relation = check_crossing(s1, r1, s2, r2)
        if relation != 0:
            print("Die Geraden schneiden sich bei S(" + "|".join(str(custom_round(i)) for i in relation) + ").")
        else:
            print("Die Geraden sind Windschief.")

main()