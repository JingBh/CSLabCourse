import time


def is_leap_year(year: int):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def which_day(time_tuple: time.struct_time):
    months = {
        1: 31, 2: 28, 3: 31, 4: 30,
        5: 31, 6: 30, 7: 31, 8: 31,
        9: 30, 10: 31, 11: 30, 12: 31
    }
    if is_leap_year(time_tuple.tm_year):
        months[2] += 1
    result = time_tuple.tm_mday
    for month in range(1, time_tuple.tm_mon):
        result += months[month]
    return result


if __name__ == '__main__':
    user_input = input("Please input a date (yyyy/mm/dd): ").replace(" ", "")
    try:
        time_obj = time.strptime(user_input, "%Y/%m/%d")
        print("Self-made algorithm result:", which_day(time_obj))
        print("Built-in algorithm result:", int(time_obj.tm_yday))
    except ValueError:
        print("Invalid input. (Need yyyy/mm/dd)")
