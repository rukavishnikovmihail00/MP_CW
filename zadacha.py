import json
import logging


def init_logger(debug : False):
    logger = logging.getLogger()
    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] : %(message)s', datefmt='%H:%M:%S')
    sh = logging.StreamHandler()

    logger.addHandler(sh)


def calculate_loads_weight(load_unit_weight, A):
    print(f"\nГрузы = {A}\n")
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
                        logging.debug(f"Остаток для {el} = {weight_el}")
                        arr.append([i+1, load_unit_weight[j]])
                        logging.debug(arr)

                
                    if weight_el < load_unit_weight[j+1]:
                        remain.append([i+1, weight_el])
                        logging.debug(f"remain = {remain}")
                        load_unit_weight[j] = -1
                        break 
                load_unit_weight[j] = -1
                logging.debug(f"remain = {remain}")
                logging.debug(load_unit_weight)
                logging.debug(f"arr = {arr}")
                
    logging.debug("-----------------------")
    logging.debug(f"remain = {remain}")
    logging.debug(f"load_unit_weight = {load_unit_weight}")
    logging.debug(f"arr = {arr}")
    logging.debug("-----------------------")
    logging.info(f"Единиц груза для погрузки всего: {total_weight_start}\n")


    for item in remain:
        if item[-1] != 0:
            logging.debug(f"{item[-1]} единиц товара из {item[0]} вида грузов разложены по {len(load_unit_weight) - len(arr)} оставшимся контейнерам")
           
    
    total_weight = 0

    for item in arr:
        total_weight += item[-1]

    logging.debug(f"{total_weight} единиц груза полностью заполнили первые {len(arr)} контейнеров")


    logging.info("\n======= Оптимальное распределение грузов =======\n")
    shipment = []

    new_arr = arr.copy()

    for i in range(n):
        for j in range(m):
            if new_arr:
                shipment.append([f"Корабль {str(i+1)}, контейнер {str(j+1)}: груз вида {str(new_arr[0][0])} = {str(new_arr[0][1])} единиц"])
                new_arr.pop(0)
    for el in shipment:
        logging.info(el[0])
    # ДОДЕЛАТЬ С ПОСЛЕДНИМИ КОНТЕЙНЕРАМИ
    logging.info("=================================================\n")


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

        if ship_weight != 0:
            result.append(C[j]*1)
            Y.append([j+1, 1]) # the ship is in use
        else:
            Y.append([j+1, 0]) # the ship is not in use
    
    return Y, result


if __name__=="__main__":

    debug = True
    init_logger(debug)
    

    ENV_FILE = "env1.json"

    with open(ENV_FILE, 'r') as r_file:
        data = json.load(r_file)

    n = data["n"]
    p = data["p"]
    m = data["m"]
    C = data["C"]
    A = data["A"]
    D = data["D"]


    load_unit_weight, A = A_to_X(A, D) # считаем вес каждой единицы груза на основе А

    logging.debug(f"Итоговая загрузка контейнеров = {load_unit_weight}\n")

    Y, result = calculate(n, p, m, C, A, D, load_unit_weight)
    
    logging.info(f"==== Использование кораблей ====\n")
    for el in Y:
        if el[1] != 0:
            logging.info(f"     Судно {el[0]} используется")
        else:
            logging.info(f"    Судно {el[0]} не используется")
    logging.info(f"================================\n")

    logging.info(f"=============== Затраты ===============\n")
    for i, el in enumerate(result):
        logging.info(f"Затраты на использование судна {i+1} = {el}")
    logging.info(f"=======================================\n")
