from datetime import datetime
from salary import calculate_salary
from people import get_employess
if __name__ == '__main__':
    print(f"текущая дата: {datetime.now().strftime('%Y-%m-%d')}")

    calculate_salary()
    get_employess()

    