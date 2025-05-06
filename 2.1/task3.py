"""
Задание 3. Дан целочисленный массив nums, верните true, если какое-либо значение
встречается в массиве по крайней мере дважды, иначе верните false.
"""
def repeated_num(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
print(repeated_num([1,2,3,4]))
print(repeated_num([1,1,1,3,3,4,3,2,4,2]))
print(repeated_num([1,2,3,1]))