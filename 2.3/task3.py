"""
Задание 3. Создайте класс Calculation, в котором будет одно свойство calculationLine.
методы: SetCalculationLine, который будет изменять значение свойства,
SetLastSymbolCalculationLine, который будет в конец строки прибавлять символ,
GetCalculationLine который будет выводить значение свойства, GetLastSymbol получение
последнего символа, DeleteLastSymbol удаление последнего символа из строки
"""
class Calculation(object):
    def __init__(self):
        self.calculationLine = ""
    def SetCalculationLine(self, value):
        self.calculationLine = value
    def SetLastSymbolCalculationLine(self, symbol):
        self.calculationLine += symbol
    def GetCalculationLine(self):
        print(f"Значение свойства: {self.calculationLine}")
    def GetLastSymbol(self):
        if self.calculationLine:
            return self.calculationLine[-1]
        return ""
    def DeleteLastSymbol(self):
        if self.calculationLine:
            self.calculationLine = self.calculationLine[:-1]


cl = Calculation() # определение объекта cl
cl.SetCalculationLine("пока") # изменение значения
cl.SetLastSymbolCalculationLine("*") # добавление символа в конец строки
cl.GetCalculationLine() # вывод значения
print(cl.GetLastSymbol()) # получение последнего символа
cl.DeleteLastSymbol() # удаление последнего символа
cl.GetCalculationLine() # вывод





