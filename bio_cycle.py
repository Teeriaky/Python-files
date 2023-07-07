import datetime
import argparse

cycles_description = {
"phys_cycle_description" : "    Физический цикл определяет в основном индивидуальную изменчивость проявления двигательных способностей человека в течение 23 дней. \
В положительную фазу наблюдается повышенная физическая работоспособность. Меньше проявляется усталость. В отрицательную фазу, напротив, наблюдается снижение физической работоспособности.\
В эту фазу нужно следить за своим здоровьем. Здесь повышенная болевая чувствительность, дольше длится выздоровление.\n",
"intel_cycle_description" : "    Интеллектуальный цикл контролирует индивидуальную изменчивость умственных способностей человека.\
В первую, положительную, интеллектуальную фазу творческие процессы протекают эффективнее, внимание повышено, математические расчеты делаются быстро, а задачи решаются легко. \
Это хорошее время для выполнения интеллектуальных тестов и сдачи экзаменов.\
В негативной фазе умственная деятельность ухудшается, снижается внимание, решение простых задач требует значительных усилий.\n",
"emote_cycle_description" : "    Эмоциональный цикл определяет эмоциональную сферу человека: чувствительность, настроение, поведение в обществе, психологическую устойчивость. \
Первая половина цикла относится к положительной фазе, в которую человек оптимистичен, весел, отзывчив.\
Во второй, отрицательной, фазе становится раздражительным, унылым."}

def main():
    received_data = get_args()
    #temporal solution
    if received_data.description:
        [print(x) for x in cycles_description.values()]
    received_date = received_data.birth_date[0].split(".")
    birth_date = datetime.date(*list(map(int, received_date[::-1])))
    current_date = datetime.date.today()
    lived = (current_date - birth_date)
    days_between_dates = lived.days + 1
    
    physical_cycle = days_between_dates % 23
    emotional_cycle = days_between_dates % 28
    intellectual_cycle = days_between_dates % 33

    output = (
"День физического цикла: {0} {3}\n\
День эмоционального цикла: {1} {4}\n\
День интеллектуального цикла: {2} {5}".format(physical_cycle, emotional_cycle, intellectual_cycle, "критический" if physical_cycle in [7, 18] else "",                                               
                                                                                                   "критический" if emotional_cycle in [8, 22] else "",
                                                                                                   "критический" if intellectual_cycle in [9, 26] else ""))
    print(output, days_between_dates)

def get_args():
    parser = argparse.ArgumentParser(description="Usage: bio_cycle.py birth_date [birth_date1 [... birth_dateN]]")
    parser.add_argument(action="store", default="", dest="birth_date", metavar="birth_date", type=str, nargs="+", 
                        help="date has to match the following format: date.month.year")
    parser.add_argument("-d", "--description", action="store_true", dest="description",
                        help="show a description of each cycle.")
    args = parser.parse_args()
    if not args:
        parser.error("At least one of a file's name is required.")
    return args

main()