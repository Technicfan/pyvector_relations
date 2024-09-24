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

from sys import exit, platform, argv

def custom_round(number):
    part = number - int(number)
    if part != 0:
        return round(number, 2)
    else:
        return int(number)

def check_zero_vector(r1, r2):
    zero1, zero2 = 0, 0
    for one, two in zip(r1, r2):
        zero1 += abs(one)
        zero2 += abs(two)
    return zero1 == 0 or zero2 == 0

def check_crossing(s1, r1, s2, r2, numpy):
    first_part = []
    second_part = []
    for x, y, a1, a2 in zip(r1, r2, s1, s2):
        first_part.append([x, -y])
        second_part.append([a2 - a1])

    try:
        if not numpy:
            raise ImportError
        import numpy as np
        try:
            results = np.linalg.solve(first_part[:2], second_part[:2])
            if len(first_part) == 3 and not np.allclose(np.dot(first_part[-1], results), second_part[-1]):
                return False
        except:
            return False
    except ImportError:
        if numpy:
            print("Um numpy zu verwenden, muss es installiert sein (pip)")
        try:
            x = ( first_part[1][1] * second_part[0][0] - first_part[0][1] * second_part[1][0] ) /\
                 ( first_part[0][0] * first_part[1][1] - first_part[0][1] * first_part[1][0] )
            y = ( second_part[0][0] - first_part[0][0] * x ) / first_part[0][1]
        except ZeroDivisionError:
            return False
        if len(first_part) == 3 and first_part[-1][0] * x + first_part[-1][1] * y != second_part[-1][0]:
            return False
        else:
            results = [[x, y]]

    point = []
    for one, two in zip(s1, r1):
        point.append(one + results[0][0] * two)
    return point

def check_parallel(r1, r2):
    i = 0
    while i < len(r1) - 1 and r1[i] == r2[i] == 0:
        i += 1
    try:
        first = r1[i] / r2[i]
        for one, two in zip(r1[i+1:], r2[i+1:]):
            if not (one == two == 0) and one / two != first:
                return False
    except ZeroDivisionError:
        return False
    return True

def check_same(s1, s2, r2):
    i = 0
    while i < len(r2) - 1 and r2[i] == (s1[i] - s2[i]) == 0:
        i += 1
    try:
        first = (s1[i] - s2[i]) / r2[i]
        for one, two, three in zip(s1[i+1:], s2[i+1:], r2[i+1:]):
            if not ((one - two) == three == 0) and (one - two) / three != first:
                return False
    except ZeroDivisionError:
        return False
    return True

def help(status):
    print(
        "\nHilfe:\n"
        "\nEingabe der Vektoren:\n" +
        "   x, y, z oder x, y\n" +
        "   - Leerzeichen nicht notwending\n" +
        "   - '.' als Dezimaltrennzeichen\n" +
        "   - alle vier Vektoren müssen entweder zwei- oder dreidimensional sein (alle gleich)\n" +
        "\nErweitert:\n" +
        "   Argumente:\n" +
        "   - \"help\" für diesen Text\n"
        "   - \"numpy\" um numpy für die Bestimmung des Schnittpunkts verwenden\n"
    )
    exit(status)

def main(args):
    if "help" in args:
        help(0)

    try:
        print("\n1. Gerade:")
        s1 = list(map(float, input("    Stützvektor: ").split(",")))
        r1 = list(map(float, input("    Richtungsvektor: ").split(",")))
        print("2. Gerade:")
        s2 = list(map(float, input("    Stützvektor: ").split(",")))
        r2 = list(map(float, input("    Richtungsvektor: ").split(",")))
        if not (len(s1) == len(r1) == len(s2) == len(r2) in [2, 3]):
            raise ValueError
    except ValueError:
        help(1)

    print()
    if check_zero_vector(r1, r2):
        print("Mit einem Nullvektor als Richtungsvektor entsteht keine Gerade.")
    else:
        if check_parallel(r1, r2):
            if check_same(s1, s2, r2):
                print("Die Geraden sind identisch.")
            else:
                print("Die Geraden sind parallel.")
        else:
            relation = check_crossing(s1, r1, s2, r2, "numpy" in args)
            if relation:
                print("Die Geraden schneiden sich im Punkt S(" + "|".join(str(custom_round(i)) for i in relation) + ").")
            else:
                print("Die Geraden sind windschief.")
    print()

if __name__ == "__main__":
    try:
        main(argv)
        if platform == "win32":
            # no better solution for keeping it open
            input("ENTER zum Beenden ")
    except KeyboardInterrupt:
        exit(1)