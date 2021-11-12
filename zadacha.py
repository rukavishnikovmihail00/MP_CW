import random

def raspr(A, el, load_unit_weight, con):
    total = 0
    print("===RASPR===")
    print()
    #print(A)

    for i,item in enumerate(A):
        if item <= el:
            total += item
            print(load_unit_weight)
            print(A)
            exit(0)
        else:
            A[i] -= el
            load_unit_weight.append({con+1: el})
            print(A)
            print(load_unit_weight)
            return
            
        

    """for item in A:
        total += item"""
    print(el)
    print(load_unit_weight)
    


def A_to_X(A, D):
    load_unit_weight = []
    
    for con, el in enumerate(D): # берем макс вес контейнера
        print("Проверка остатков груза на потребность перераспределения")
        """for load in A:
            if load < el//len(A): # нужно перераспределять (дошли до момента, когда поровну уже взять не получается)
                print(A)
                raspr(A, el, load_unit_weight, con)"""

        for i, item in enumerate(A):
            print(f"Контейнер №{con+1}, грузоподъемность = {el}")
            
            if item >= el//len(A): # если остаток груза в А не меньше 
                weight = el//len(A) # вычисляем вес, как D контейнера / количество элементов в А
                print(f"A = {A}")
                A[i] -= weight
                
            else:
                weight = item
                print(f"A = {A}")
                A[i] -= weight
                A.pop(A[i])
                
                print("TEST")
                # не загружается последний груз
            #load_unit_weight.append({con+1:weight})
            load_unit_weight.append(weight)
            if not A:
                return load_unit_weight
                
        print(f"load = {load_unit_weight}")
        print(f"A после загрузки контейнера = {A}")
        print("-----------------------------------")
        


    # считать максимальный весь исходя из грузоподъемности судна
    return load_unit_weight

def get_container_weight(p, load_unit_weight):
    weight = 0
    for k in range(p):
        load_unit_weight # Х в задаче
        weight += load_unit_weight[0] # добавляем вес груза в вес контейнера
        load_unit_weight.pop(0)
    return weight


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
                x = get_container_weight(p, load_unit_weight) # узнаем вес контейнер
                containers_weight.append(x) # добавляем вес контейнера в массив корабля
            print(f"Вес контейнера {i+1} на корабле {j+1} = {x}")

        # -- возвращаемся к кораблю -- #
        
        ship_weight = get_ship_weight(containers_weight)
        print(f"Вес корабля {j+1} = {ship_weight}")

        if ship_weight != 0:
            result.append(C[j]*ship_weight)
            Y.append([j, 1]) # the ship is in use
        else:
            Y.append([j, 0]) # the ship is not in use
    
    return Y, result


if __name__=="__main__":
    n = 5 # судно
    p = 3 # вид груза
    m = 5 # контейнер
    C = [137, 112, 124, 115, 157] # затраты

    A = [10000, 8000, 13000] # груз на погрузочной площадке РАСПРЕДЕЛЯТЬ ЕГО ПО КОНТЕЙНЕРАМ

    D = [4000, 1000, 3000, 4000, 2000, # грузоподъемность
         2000, 2000, 3000, 1000, 2000,
         2000, 3000, 1000, 2000, 3000,
         1000, 5000, 2000, 1000, 2000,
         1000, 2000, 4000, 3000, 3000]



    

    load_unit_weight = A_to_X(A, D) # считаем вес каждой единицы груза на основе А

    print(f"Веса = {load_unit_weight}")
    print(A)

    Y, result = calculate(n, p, m, C, A, D, load_unit_weight)
    
    print(f"Y = {Y}")
    print(f"Result = {result}")