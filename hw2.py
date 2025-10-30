def load_data(file_path: str) -> list[dict[str, str]]:
    """
    читает CSV и возвращает список словарей с данными сотрудников

    Args:
        file_path (str): путь к файлу с данными

    Returns:
        list[dict[str, str]]: список сотрудников, каждый — словарь
    """
    employees = []
    with open(file_path, encoding='utf-8') as f:
        lines = f.readlines()

    headers = lines[0].strip().split(';')

    for i in range(1, len(lines)):
        parts = lines[i].strip().split(';')
        if len(parts) == len(headers):
            emp = {}
            for j in range(len(headers)):
                emp[headers[j]] = parts[j]
            employees.append(emp)

    return employees


def show_hierarchy(employees: list[dict[str, str]]) -> None:
    """
    показывает какие отделы входят в каждый департамент

    Args:
        employees: список сотрудников
    """
    dept_teams = {}

    for emp in employees:
        dept = emp['Департамент']
        team = emp['Отдел']

        if dept not in dept_teams:
            dept_teams[dept] = set()
        dept_teams[dept].add(team)

    print("\nИерархия команд:")
    for dept in sorted(dept_teams.keys()):
        print(f"{dept}:")
        for team in sorted(dept_teams[dept]):
            print(f"  {team}")#тут пробелы для красоты чтоб читаемо было
    print()


def calculate_department_stats(employees: list[dict[str, str]]) -> list[dict[str, float | int | str]]:
    """
    считает по каждому департаменту сколько людей работает и мин/макс/сред зарплату

    Args:
        employees: список сотрудников

    Returns:
        list[dict]: данные по департаментам
    """
    stats = {}

    for emp in employees:
        dept = emp['Департамент']
        salary = int(emp['Оклад'])

        if dept not in stats:
            stats[dept] = {
                'count': 0,
                'min': salary,
                'max': salary,
                'total': 0
            }

        stats[dept]['count'] += 1
        if salary < stats[dept]['min']:
            stats[dept]['min'] = salary
        if salary > stats[dept]['max']:
            stats[dept]['max'] = salary
        stats[dept]['total'] += salary

    result = []
    for dept, data in stats.items():
        avg = round(data['total'] / data['count'], 2)
        result.append({
            'Департамент': dept,
            'Численность': data['count'],
            'Мин. зарплата': data['min'],
            'Макс. зарплата': data['max'],
            'Средняя зарплата': avg
        })

    return result


def show_department_report(employees: list[dict[str, str]]) -> None:
    """
    выводит сводный отчёт

    Args:
        employees: список сотрудников
    """
    report = calculate_department_stats(employees)

    print("\nСводный отчёт:")
    print(f"{'Департамент':<20} {'Численность':<12} {'Мин':<10} {'Макс':<10} {'Средняя':<10}")

    for r in report:
        print(f"{r['Департамент']:<20} {r['Численность']:<12} "
              f"{r['Мин. зарплата']:<10} {r['Макс. зарплата']:<10} {r['Средняя зарплата']:<10}")
    print()


def save_department_report_to_csv(employees: list[dict[str, str]], output_file: str = 'department_report.csv') -> None:
    """
    сохраняет отчёт в CSV

    Args:
        employees: список сотрудников
        output_file: имя файла для сохранения
    """
    report = calculate_department_stats(employees)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Департамент;Численность;Мин. зарплата;Макс. зарплата;Средняя зарплата\n")
        for r in report:
            f.write(f"{r['Департамент']};{r['Численность']};"
                    f"{r['Мин. зарплата']};{r['Макс. зарплата']};{r['Средняя зарплата']}\n")

    print(f"\nОтчёт в файле: {output_file}\n")


def main_menu() -> None:
    """
    меню
    """
    file_path = 'Corp_Summary.csv'
    employees = load_data(file_path)

    while True:
        print("\nменю:")
        print("1. показать иерархию команд")
        print("2. показать сводный отчёт по департаментам")
        print("3. сохранить отчёт в CSV")
        print("0. выйти")

        choice = input("что хотите? (0-3): ").strip()

        if choice == '1':
            show_hierarchy(employees)
        elif choice == '2':
            show_department_report(employees)
        elif choice == '3':
            save_department_report_to_csv(employees)
        elif choice == '0':
            print("пока!")
            break
        else:
            print("ты наверное ошибся:( надо выбрать цифру от 0 до 3")


if __name__ == '__main__':
    main_menu()