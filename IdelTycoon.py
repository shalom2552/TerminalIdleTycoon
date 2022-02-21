"""
Constants
"""
MAX_WORKERS = 5
BASE_PRICE = 10
FACTOR = 2.5
GAIN = 2


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main():
    """
    """
    print(bcolors.HEADER + "Hello and welcome to Idle Game!" + bcolors.ENDC)
    cash, income, workers = 10, 0, [0 for _ in range(MAX_WORKERS)]
    while True:
        printStatus(cash, income, workers)
        cash, income, workers = operate(cash, income, workers)
        income = calculateIncome(workers)
    pass


def getNextRuns():
    """
    :return:
    :rtype:
    """
    next_round = 25
    res = input(bcolors.BOLD +
                bcolors.OKCYAN + "(1) " + bcolors.HEADER + "One round\n" +
                bcolors.OKCYAN + "(2) " + bcolors.HEADER + "10 rounds\n" +
                bcolors.OKCYAN + "(3) " + bcolors.HEADER + "25 rounds\n" +
                bcolors.OKCYAN + "(4) " + bcolors.HEADER + "50 rounds\n" +
                bcolors.OKCYAN + "(5) " + bcolors.HEADER + "100 rounds\n" + bcolors.ENDC)
    if res == '1':
        next_round = 1
    elif res == '2':
        next_round = 10
    elif res == '3':
        next_round = 25
    elif res == "4":
        next_round = 50
    elif res == '5':
        next_round = 100
    return next_round


def Round(cash, income):
    next_runs = getNextRuns()
    round_income = 0
    while next_runs > 0:
        round_income = round_income + income
        next_runs -= 1
    cash = cash + round_income
    print(bcolors.BOLD + bcolors.OKBLUE + "Cash = " + str(cash) + " + " + str(round_income))
    return cash, income


def printStatus(cash, income, workers):
    """
    :param cash:
    :type cash:
    :param income:
    :type income:
    :param workers:
    :type workers:
    """
    print(bcolors.OKGREEN + "┌───────────────────────────────┐")
    print("│ \t\t " + bcolors.BOLD + bcolors.HEADER + "Farm Stats" + bcolors.OKGREEN + " \t\t\t│")
    print("│ Cash: \t" + bcolors.OKBLUE + "{:^20}".format(str(cash)) + bcolors.OKGREEN + "│")
    print("│ Income: \t" + bcolors.OKBLUE + "{:^20}".format(str(income)) + bcolors.OKGREEN + "│")
    print("│ Workers: \t" + bcolors.OKBLUE + "{:^20}".format(str(countWorkers(workers))) + bcolors.OKGREEN + "│")
    print("└───────────────────────────────┘" + bcolors.ENDC)
    pass


def calculateIncome(workers):
    """
    :param workers:
    :type workers:
    :return:
    :rtype:
    """
    income = 0
    for worker in workers:
        income = income + worker * GAIN + worker * FACTOR
    return income


def operate(cash, income, workers):
    """
    :param cash:
    :type cash:
    :param income:
    :type income:
    :param workers:
    :type workers:
    :return:
    :rtype:
    """
    res = input(bcolors.BOLD +
                bcolors.OKCYAN + "(1) " + bcolors.HEADER + "Buy New Worker\n" +
                bcolors.OKCYAN + "(2) " + bcolors.HEADER + "Upgrade Worker\n" +
                bcolors.OKCYAN + "(3) " + bcolors.HEADER + "See workers table\n" +
                bcolors.OKCYAN + "(4) " + bcolors.HEADER + "See stats\n" +
                bcolors.OKCYAN + "(5) " + bcolors.HEADER + "Run\n" + bcolors.ENDC)
    if res == '1':
        cash, workers = addWorker(cash, workers)
    elif res == '2':
        cash, workers = upgradeWorker(cash, workers)
    elif res == '3':
        printWorkers(workers, cash)
    elif res == "4":
        printStatus(cash, income, workers)
    elif res == '5':
        cash, income = Run(cash, income)
    else:
        pass
    return cash, income, workers


def Run(cash, income):
    cash, income = Round(cash, income)
    return cash, income


def addWorker(cash, workers):
    """
    :param cash:
    :type cash:
    :param workers:
    :type workers:
    :return:
    :rtype:
    """
    if countWorkers(workers) >= MAX_WORKERS:
        print(bcolors.FAIL + "You have maximum of " + str(MAX_WORKERS) + " workers!" + bcolors.ENDC)
        return
    worker_price = BASE_PRICE
    if worker_price <= cash:
        index = get_index(workers, True)
        workers[index] = 1
        cash -= worker_price
        print(bcolors.HEADER + "Added New Worker, for the price: " + str(worker_price) + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "You dont have enough cash!" + bcolors.ENDC)
    # printWorkers(workers, cash)
    return cash, workers


def get_index(workers, free):
    """
    :param workers:
    :type workers:
    :param free:
    :type free:
    :return:
    :rtype:
    """
    if free:
        workers_list = [i + 1 for i in range(MAX_WORKERS) if workers[i] == 0]
    else:
        workers_list = [i + 1 for i in range(MAX_WORKERS) if workers[i] != 0]
    index = int(input(bcolors.OKBLUE + bcolors.BOLD + "Select a worker number -> "
                      + str(workers_list) + " : " + bcolors.ENDC) or 0)
    while index < 1 or index > MAX_WORKERS:
        print(bcolors.FAIL + "Enter a valid worker number please!" + bcolors.ENDC)
        index = int(input(bcolors.OKBLUE + bcolors.BOLD + "Select a worker number -> "
                          + str(workers_list) + " : " + bcolors.ENDC))
    return index - 1


def upgradeWorker(cash, workers):
    """
    :param cash:
    :type cash:
    :param workers:
    :type workers:
    :return:
    :rtype:
    """
    if countWorkers(workers) == 0:
        print(bcolors.FAIL + "You dont have any workers!" + bcolors.ENDC)
        return cash, workers
    printWorkers(workers, cash)
    index = get_index(workers, False)
    upgrade_price = getUpgradePrice(workers[index])
    if cash >= upgrade_price:
        workers[index] += 1
        cash -= upgrade_price
        print(bcolors.OKCYAN + "Worker " + str(index + 1) + " as upgraded, for the price: " +
              str(upgrade_price) + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "You dont have enough cash!" + bcolors.ENDC)
    return round(cash), workers


def printWorkers(workers, cash):
    """
    :param workers:
    :type workers:
    :param cash:
    :type cash:
    """
    print(bcolors.OKGREEN + "You have " + str(countWorkers(workers)) + " workers." + bcolors.ENDC)
    printWorkingWorkers(workers, cash)
    pass


def printWorkingWorkers(workers, cash):
    """
    :param workers:
    :type workers:
    :param cash:
    :type cash:
    """
    workers_table = []
    working_index = 1
    for worker in workers:
        if worker > 0:
            workers_table.append([working_index, worker, workerIncome(worker), getUpgradePrice(worker)])
            working_index += 1
    print(bcolors.OKGREEN + bcolors.BOLD + "Total cash:" + str(cash) + bcolors.ENDC)
    print(bcolors.OKGREEN + bcolors.BOLD, end="")
    for worker in workers_table:
        print("┌───────────────┐ \t", end="")
    print()
    for worker in workers_table:
        print("│ " + bcolors.HEADER + " Worker:\t" + bcolors.OKCYAN +
              str(worker[0]) + bcolors.OKGREEN + "\t│\t", end="")
    print()
    for worker in workers_table:
        print("│ " + bcolors.HEADER + " Level:\t" + bcolors.OKCYAN +
              str(worker[1]) + bcolors.OKGREEN + "\t│\t", end="")
    print()
    for worker in workers_table:
        print("│ " + bcolors.HEADER + " Income:\t" + bcolors.OKCYAN +
              str(worker[2]) + bcolors.OKGREEN + "\t│\t", end="")
    print()
    for worker in workers_table:
        if cash < getUpgradePrice(worker[1]):
            color = bcolors.FAIL
        else:
            color = bcolors.OKGREEN
        print("│ " + bcolors.HEADER + " Cost:\t" + color + str(worker[3]) +
              bcolors.OKGREEN + "\t│\t", end="")
    print()
    for worker in workers_table:
        print("└───────────────┘ \t", end="")
    print(bcolors.ENDC)
    pass


def workerIncome(worker):
    """
    :param worker:
    :type worker:
    :return:
    :rtype:
    """
    return worker ** GAIN


def getUpgradePrice(worker):
    """
    :param worker:
    :type worker:
    :return:
    :rtype:
    """
    level_cost = worker ** FACTOR
    return round(BASE_PRICE + level_cost)


def countWorkers(workers):
    """
    :param workers:
    :type workers:
    :return:
    :rtype:
    """
    working = 0
    for i in range(MAX_WORKERS):
        if workers[i] > 0:
            working += 1
    return working


if __name__ == '__main__':
    main()
