def read_csv(path: str = 'Corp_summary.csv',
             delimiter: str = ','
             ) -> tuple[list, list[list[str, str, str, str, str, str]]]:
    """
    Функция для чтения из .csv-файла в удобный для работы с данными вид.

    Parameters
    ----------
    path: str
        Путь к файлу, по дефолту - файл лежит в директории скрипта
    delimiter: str
        Разделитель внутри .csv файла, запятая по умолчанию

    Returns
    -------
    list
        Названия атрибутов в .csv файле в виде списка
    list[list[str, str, str, str, str, str]]
        Список из списков, где каждый отдельный элемент - строка атрибутов.
        Все элементы - типа string, для работы с числами необходимо дальнейшее
        преобразование.
    """
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        # Убираем \n в конце
        result = [line[:-1].split(delimiter) for line in lines]
    return result[0], result[1:]


def team_hierarchy_print(columns_csv: list,
                         result_csv: list[list[str, str, str, str, str, str]]
                         ) -> None:
    """
    Функция для печати иерархии команд в департаментах.

    Parameters
    ----------
    columns_csv: list
        Названия атрибутов в .csv файле в виде списка
    result_csv: list[list[str, str, str, str, str, str]]
        Список из списков, где каждый отдельный элемент - строка атрибутов
    """
    # Ищем индекс значений в списках, что при изменении порядка в .csv
    # позволит сохранить логику
    dep_index_in_list = columns_csv.index('Департамент')
    team_index_in_list = columns_csv.index('Отдел')
    dep_to_teams = {}   # Словарь вида департамент:[команды]
    for line in result_csv:
        # Если департамент ранее не появлялся в словаре,
        # необходимо инициализировать его пустым списком,
        # в который будут добавляться команды
        if line[dep_index_in_list] not in dep_to_teams:
            dep_to_teams[line[dep_index_in_list]] = []
        # Если команда из новой 'строки' данных не присутствует в
        # списке из команд департамента, то необходимо ее добавить
        if line[team_index_in_list] not in \
                dep_to_teams[line[dep_index_in_list]]:
            dep_to_teams[line[dep_index_in_list]].append(
                line[team_index_in_list]
            )

    for dep, teams in dep_to_teams.items():
        print(f'Департамент \'{dep}\' включает команды - ' + ', '.join(teams))


def dep_report_print(columns_csv: list,
                     result_csv: list[list[str, str, str, str, str, str]],
                     saving: bool = False,
                     save_path: str = 'result_pivot.csv',
                     separator: str = ';'
                     ) -> None:
    """
    Функция для печати или сохранения сводной таблицы для департаментов.

    Parameters
    ----------
    columns_csv: list
        Названия атрибутов в .csv файле в виде списка
    result_csv: list[list[str, str, str, str, str, str]]
        Список из списков, где каждый отдельный элемент - строка атрибутов
    saving: bool
        Опция сохранения, по умолчанию - отключена. При отключенной опции
        сохранения сводная таблица выводится на печать, при включенной опции
        сохранения сводная таблица выводится в файл
    save_path: str
        Путь для сохранения результирующей сводной таблицы при включенной
        опции сохранения
    separator: str
        Разделитель для вывода сводной таблицы в .csv-файл, по умолчанию
        установлен на точку с запятой
    """
    dep_index_in_list = columns_csv.index('Департамент')
    salary_index_in_list = columns_csv.index('Оклад')
    dep_salaries = {}   # Словарь вида департамент:[зарплаты]
    for line in result_csv:
        if line[dep_index_in_list] not in dep_salaries:
            dep_salaries[line[dep_index_in_list]] = []
        dep_salaries[line[dep_index_in_list]].append(
            float(line[salary_index_in_list])
        )

    result_pivot = []
    pivot_columns = ['Департамент', 'К-во сотрудников',
                     'Вилка зарплат', 'Средняя зарплата']
    result_pivot.append(pivot_columns)
    for dep, salaries in dep_salaries.items():
        # Количество сотрудников можно посчитать по количеству зарплат
        # сотрудников в списке зарплат департамента
        number_of_workers = len(salaries)
        min_salary = min(salaries)
        max_salary = max(salaries)
        avg_salary = round(sum(salaries) / len(salaries), 2)
        result_pivot.append([dep, number_of_workers,
                             str(min_salary) + '-' + str(max_salary),
                             avg_salary])
    if saving:
        with open(save_path, 'w', encoding='utf-8') as file:
            for line in result_pivot:
                file.write(separator.join([str(x) for x in line]) + '\n')
    else:
        for row in result_pivot:
            print('{:<25} {:<25} {:<25} {:<25}'.format(*[str(x) for x in row]))


if __name__ == '__main__':
    columns_csv, result_csv = read_csv(delimiter=';')
    options = {'1': 'Вывести иерархию команд',
               '2': 'Вывести сводный отчет по департаментам',
               '3': 'Сохранить сводный отчет по департаментам в .csv',
               '4': 'Выход'}
    option = ''
    while option not in options:
        print('Выберите опцию: \n' +
              ';\n'.join('{}) {}'.format(k, v) for k, v in options.items()))
        option = input()

    if option == '1':
        team_hierarchy_print(columns_csv, result_csv)
    elif option == '2':
        dep_report_print(columns_csv, result_csv)
    elif option == '3':
        dep_report_print(columns_csv, result_csv, saving=True)
    elif option == '4':
        print('Завершение...')
