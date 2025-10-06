def print_calendar(days, start):
    days_list = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    print(" ".join(days_list))
    print("    " * start, end="")

    for d in range(1, days + 1):
        print(f"{d:>3}", end=" ")
        if (start + d) % 7 == 0:
            print()
    print()

if __name__ == "__main__":
    days = int(input("Days in month: "))
    start = int(input("Start day (0=Sun, 1=Mon, ... 6=Sat): "))
    print_calendar(days, start)