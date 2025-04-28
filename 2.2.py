"""
Задание 2. Дан целочисленный массив (candidates) и цель (target), найдите все уникальные
комбинации чисел, сумма которых равна цели. Каждое число может быть использовано
только один раз в комбинации. Набор решений не должен содержать повторяющихся
комбинаций.
"""
def fun(lis, n):
    def backtrack(ind, sol, n):
        if n == 0:
            res.append(sol)
            return
        for i in range(ind, len(lis)):
            if i > ind and lis[i] == lis[i-1]:
                continue
            if lis[i] > n:
                break
            backtrack(i + 1, sol+[lis[i]], n-lis[i])
    lis.sort()
    res = []
    backtrack(0, [], n)
    return res
lis1 = [2,5,2,1,2]
n1 = 5
print(fun(lis1, n1))
list2 = [10, 1, 2, 7, 6, 1, 5]
n2 = 8
print(fun(list2, n2))