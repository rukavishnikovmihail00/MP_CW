import json
import logging
import os


def validate_data(data):
    res_data = {}
    res_data["n"] = data.get("n")
    res_data["p"] = data.get("p")
    res_data["m"] = data.get("m")
    res_data["C"] = data.get("C")
    res_data["A"] = data.get("A")
    res_data["D"] = data.get("D")

    if not (res_data["n"] or res_data["p"] or res_data["m"] or
            res_data["C"] or res_data["A"] or res_data["D"]):
            raise Exception("Одна или несколько переменных не определены")

    if res_data["p"] != len(res_data["A"]):
        raise Exception("Размерность А должна быть равной p")

    if sum(res_data["A"]) > sum(res_data["D"]):
        raise Exception("Нельзя погрузить больше, чем общая грузоподъемность")
    
    if res_data["n"]*res_data["m"] != len(res_data["D"]):
        raise Exception("Размерность D должна быть равной n*m")

    if len(res_data["C"]) != res_data["n"]:
        raise Exception("Размерность массива затрат должна быть равна количеству кораблей")

    if res_data["n"] <= 1 or res_data["m"] <=1:
        raise Exception("Условие задачи не предусматривает таких входных данных")

    logging.info("\n======== Валилация прошла успешно ========\n")
    
    return res_data


def init_logger(debug : False):
    logger = logging.getLogger()

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s', datefmt='%H:%M:%S')
    sh = logging.StreamHandler()

    logger.addHandler(sh)


def calculate_loads_weight(load_unit_weight, A): # сколько можем загрузить полностью
    logging.debug(f"\nГрузы = {A}\n")
    checkLen = len(load_unit_weight)
    total_weight_start = sum(load_unit_weight)
    arr = []
    remain = []
    start = 0
    for i, el in enumerate(A):
        weight_el = el
        for j in range(len(load_unit_weight)):
            if load_unit_weight[j] != -1:
                if checkLen != 1:
                    #if load_unit_weight[j+1]: # change back if fails
                    if len(load_unit_weight) >= j+2:
                        if weight_el >= load_unit_weight[j]:
                            weight_el -= load_unit_weight[j]
                            logging.debug(f"Остаток груза для вида {i+1} = {weight_el}")
                            arr.append([i+1, load_unit_weight[j]])
                            logging.debug(f"Погружено (вид, количество) = {arr}")

                        if weight_el < load_unit_weight[j+1]:
                            remain.append([i+1, weight_el])
                            logging.debug(f"Грузы для заполнения во втором этапе (вид, количество) = {remain}")
                            load_unit_weight[j] = -1
                            break 
                    
                    load_unit_weight[j] = -1
                    logging.debug(f"Грузы для заполнения во втором этапе (вид, количество) = {remain}")
                    logging.debug(f"Еще не погружено (распределение)  = {load_unit_weight}")
                    logging.debug(f"Погружено (вид, количество) = {arr}")
                
    if checkLen != 1:           
        logging.debug("-----------------------")
        logging.debug(f"Грузы для заполнения во втором этапе (итог) = {remain}")
        logging.debug(f"Еще не погружено (итог) = {load_unit_weight}")
        logging.debug(f"Погружено (итог) = {arr}")
        logging.debug("-----------------------")

    shipment = []

    new_arr = arr.copy()

    new_remain = []
    new_remain_to_load = []

    for el in remain:
        if el[1] != 0:
            new_remain_to_load.append(el)
    for i, item in enumerate(load_unit_weight):
        if item != -1:
            new_remain.append(item)


    logging.info("\n================ Первый этап погрузки ================\n")

    ship_num = 0
    cont_num = 0
    for i in range(n):
        for j in range(m):
            if new_arr:
                shipment.append([f"Судно {str(i+1)}, контейнер {str(j+1)}: груз вида {str(new_arr[0][0])} = {str(new_arr[0][1])} единиц"])
                new_arr.pop(0)
                cont_num = j + 1
                ship_num = i + 1
    for el in shipment:
        logging.info(el[0])

    logging.info("\n======================================================\n")

    logging.info("\n================ Второй этап погрузки ================\n")
    logging.info("Остается для погрузки во втором этапе:\n")
    for item in new_remain_to_load:
        logging.info(f"{item[-1]} единиц товара из {item[0]} вида грузов")
        #logging.debug(f"{item[-1]} единиц товара из {item[0]} вида грузов разложены по {len(load_unit_weight) - len(arr)} оставшимся контейнерам")
    
    logging.debug("\nРаспределяем:\n")
    for i, el in enumerate(new_remain_to_load):
        weight_remain = el[1]
        while weight_remain != 0:
            for i, item in enumerate(new_remain):
                if weight_remain >= item:
                    if item != -1:
                        weight_remain = weight_remain - item
                        el[1] = weight_remain
                        logging.debug(f"Груз вида {el[0]} весом {item}")
                        logging.debug(f"Осталось погрузить (вид, количество) = {new_remain_to_load}")
                        new_remain[i] = -1
                        logging.debug(f"Оставшееся распределение = {new_remain}")
                else:
                    if item != -1:
                        new_remain[i] -= weight_remain
                        logging.debug(f"Груз вида {el[0]} весом {item}")
                        weight_remain = 0
                        el[1] = weight_remain
                        logging.debug(f"Осталось погрузить (вид, количество) = {new_remain_to_load}")
                        logging.debug(f"Оставшееся распределение = {new_remain}")
                        break
                         
    logging.info("\n======================================================\n")


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
            logging.debug(f"Вес контейнера {i+1} на корабле {j+1} = {x}")
                
        
        ship_weight = get_ship_weight(containers_weight)
        logging.debug(f"\nВес корабля {j+1} = {ship_weight}\n")
        logging.debug("------------------------------------")

        if ship_weight != 0:
            result.append(C[j]*1)
            Y.append([j+1, 1]) # используем корабль
        else:
            Y.append([j+1, 0]) # не используем корабль
    
    return Y, result


if __name__=="__main__":

    choice = 3
    print("Решить задачу:\n")
    print("[1] - подробно")
    print("[2] - только результаты\n")

    try:
        while (choice != 1 or choice !=2):
            os.system("cls")
            print("Решить задачу:\n")
            print("[1] - подробно")
            print("[2] - только результаты\n")
            choice = int(input())
            if choice == 1:
                debug = True
                os.system("cls")
                break
            if choice == 2:
                debug = False
                os.system("cls")
                break
    except: 
        os.system("cls")
        print("Нужно ввести число")
        exit(0)


    try:
        init_logger(debug)
        

        ENV_FILE = "env.json"

        with open(ENV_FILE, 'r') as r_file:
            data = json.load(r_file)

        res_data = validate_data(data)

        n = res_data["n"]
        p = res_data["p"]
        m = res_data["m"]
        C = res_data["C"]
        A = res_data["A"]
        D = res_data["D"]


        load_unit_weight, A = A_to_X(A, D) # считаем вес каждой единицы груза на основе А


        Y, result = calculate(n, p, m, C, A, D, load_unit_weight)
        
        logging.info(f"\n=============== Использование кораблей ===============\n")
        for el in Y:
            if el[1] != 0:
                logging.info(f"                Судно {el[0]} используется")
            else:
                logging.info(f"               Судно {el[0]} не используется")
        logging.info(f"\n======================================================\n")

        logging.info(f"====================== Затраты =======================\n")
        for i, el in enumerate(result):
            logging.info(f"Затраты на использование судна {i+1} = {el}")
        logging.info(f"\n======================================================\n")
    except:
        raise Exception("Что-то пошло не так в процессе вычисления")