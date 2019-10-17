import time

if __name__ == '__main__':
    user_input = input("Please input a date (yyyy/mm/dd): ").replace(" ", "")
    try:
        time_obj = time.strptime(user_input, "%Y/%m/%d")
    except ValueError:
        print("Invalid input. (Need yyyy/mm/dd)")
    else:
        print("Result:", int(time.strftime("%j", time_obj)))
