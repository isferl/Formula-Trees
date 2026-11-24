from src import Tree

INFORMATION = """
1 -- Вывести вашу формулу в обычной записи
2 -- Вывести вашу формулу в префиксной записи
 
0 -- Выйти из программы
"""

flag_formula = True
tree = Tree()
while flag_formula:
    try:
        formula = input("Введите вашу формулу\n").strip().replace(" ", "").lower()
        tree.validate_formula(formula)
        flag_formula = False
    except:
        print("Введите корректную формулу")

tree.build_from_formula(formula)
flag_while = True
while flag_while:
    print(INFORMATION)
    q = input("Введите номер операции\n")
    if not (q.isdigit()):
        continue
    if int(q) == 0:
        flag_while = False
    elif int(q) == 1:
        print(tree.simple_notation())
    elif int(q) == 2:
        print(tree.prefix_notation())
