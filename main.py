from sympy import *
import string


def check_int(text):
    var = input(text)
    while True:
        try:
            int(var)
            break
        except ValueError:
            var = input("Некоректні дані. Уведіть ціле число")
    return int(var)


def check_float(text):
    var = input(text)
    while True:
        try:
            float(var)
            break
        except ValueError:
            var = input("Некоректні дані. Уведіть число")
    return float(var)


def enter_params():
    n = check_int("Уведіть кількість видів товарів:")
    while n < 1:
        n = check_int("Некоректні дані. Спробуйте ще раз")
    a = []
    b = []
    B = check_float("Уведіть бюджет закупки товарів (грн):")
    while B < 0:
        B = check_float("Некоректні дані. Спробуйте ще раз")
    for i in range(n):
        a_i = check_float(f"Уведіть прогнозоване значення середнього попиту на товар {i + 1} (кг):")
        while a_i < 0:
            a_i = check_float("Некоректні дані. Спробуйте ще раз")
        a.append(a_i)
        b_i = check_float(f"Уведіть ціну закупки {i + 1}го товару (грн/кг):")
        while b_i < 0:
            b_i = check_float("Некоректні дані. Спробуйте ще раз")
        b.append(b_i)
    return n, B, a, b


def solve_problem(n, B, a, b):
    if b == [0 for i in range(n)]:
        print("Задача не має розв'язку")
        solution = -1
    else:
        vars = []
        for i in range(n):
            vars.append(string.ascii_lowercase[len(string.ascii_lowercase) - 1 - i])
        for i in range(n):
            vars[i] = symbols(f'{vars[i]}')
        lmbd = symbols('lmbd')

        limitation = lambda variables, price, budget, quantity, lmbd: sum(
            price[i] * variables[i] for i in range(quantity)) - budget
        lagrange = lambda variables, demand, price, budget, quantity, lmbd: sum(
            (variables[i] - demand[i]) ** 2 for i in range(quantity)) + lmbd * (limitation(variables, price, budget,
                                                                                           quantity, lmbd))

        system_diff = []
        find_lmbd = []
        for i in range(n):
            system_diff.append(diff(lagrange(vars, a, b, B, n, lmbd), vars[i]))
            find_lmbd.append(solve(system_diff[i], vars[i])[0])

        lambd = solve(limitation(find_lmbd, b, B, n, lmbd), lmbd)[0]
        solution = []
        for i in range(n):
            solution.append(find_lmbd[i].subs({lmbd: lambd}))
    return solution


def answer(n, B, a, b):
    print("\nВідповідь:")
    if solve_problem(n, B, a, b) != -1:
        for i in range(len(solve_problem(n, B, a, b))):
            print(f"необхідно закупити {round(solve_problem(n, B, a, b)[i], 3)} кг виробів {i + 1}-го виду")


n, B, a, b = enter_params()
answer(n, B, a, b)

