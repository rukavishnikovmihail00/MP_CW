import json


def calculate_loads_weight(load_unit_weight, A): 
    print(f"load_unit_weight = {load_unit_weight}")
    print(f"A = {A}")
    total_weight_start = sum(load_unit_weight)
    arr = []
    remain = []
    start = 0
    for i, el in enumerate(A):
        weight_el = el
        # сколько можем загрузить полностью
        for j in range(len(load_unit_weight)):
            if load_unit_weight[j] != -1:
                if load_unit_weight[j+1]:
                    if weight_el >= load_unit_weight[j]:

                        weight_el -= load_unit_weight[j]
                        print(f"Остаток для {el} = {weight_el}")
                        arr.append([i+1, load_unit_weight[j]])
                        print(arr)



                
                    if weight_el < load_unit_weight[j+1]:
                        remain.append([i+1, weight_el])
                        print(f"remain = {remain}")
                        load_unit_weight[j] = -1
                        break 
                load_unit_weight[j] = -1
                print(f"remain = {remain}")
                print(load_unit_weight)
                print(f"arr = {arr}")
    print("-----------------------")
    print(f"remain = {remain}")
    print(f"load_unit_weight = {load_unit_weight}")
    print(f"arr = {arr}")
    print("-----------------------")
    print(f"Единиц груза для погрузки всего: {total_weight_start}")


    for item in remain:
        if item[-1] != 0:
            print(f"{item[-1]} единиц товара из {item[0]} вида грузов разложены по {len(load_unit_weight) - len(arr)} оставшимся контейнерам")

    
    total_weight = 0

    for item in arr:
        total_weight += item[-1]


    print(f"{total_weight} единиц груза полностью заполнили первые {len(arr)} контейнеров")


def A_to_X(A, D):
    total = sum(A)
    load_unit_weight = []
    for i, el in enumerate(D):
        if total > el:
            load_unit_weight.append(el)
            total -= el
        else:
            load_unit_weight.append(total)
            break
    
    calculate_loads_weight(load_unit_weight.copy(), A)
    A = []        
    return load_unit_weight, A


def get_container_weight(load_unit_weight):
    weigth = load_unit_weight[0]
    load_unit_weight.pop(0)
    return weigth


def get_ship_weight(containers_weight):
    ship_weight = 0
    for weight in containers_weight:
        ship_weight += weight
    return ship_weight


def calculate(n, p, m, C, A, D, load_unit_weight):
    Y = []
    result = []

    for j in range(n): # по кораблям
        containers_weight = []
        for i in range(m): # контейнерам
            if load_unit_weight:
                
                x = get_container_weight(load_unit_weight) # узнаем вес контейнера
                containers_weight.append(x) # добавляем вес контейнера в массив корабля
            else:
                break
            print(f"Вес контейнера {i+1} на корабле {j+1} = {x}")
                
        
        ship_weight = get_ship_weight(containers_weight)
        print(f"Вес корабля {j+1} = {ship_weight}")

        if ship_weight != 0:
            result.append(C[j]*ship_weight)
            Y.append([j, 1]) # the ship is in use
        else:
            Y.append([j, 0]) # the ship is not in use
    
    return Y, result


if __name__=="__main__":
    ENV_FILE = "env.json"
    
    with open(ENV_FILE, 'r') as r_file:
        data = json.load(r_file)

    print(data)
    n = data["n"]
    p = data["p"]
    m = data["m"]
    C = data["C"]
    A = data["A"]
    D = data["D"]


    load_unit_weight, A = A_to_X(A, D) # считаем вес каждой единицы груза на основе А


    print(f"Итоговая загрузка контейнеров = {load_unit_weight}")

    Y, result = calculate(n, p, m, C, A, D, load_unit_weight)
    
    print(f"Y = {Y}")
    print(f"Result = {result}")