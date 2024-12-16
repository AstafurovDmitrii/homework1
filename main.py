from application.salary import calculate_salary
from application.people import get_employess
from utils.datetime_utils import get_current_date

if __name__ == '__main__':
    print(f"Текущая дата: {get_current_date()}")
    calculate_salary()
    get_employess()

    