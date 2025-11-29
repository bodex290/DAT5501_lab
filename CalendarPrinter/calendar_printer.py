def print_calendar(days, start):
    days_list = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    print(" ".join(days_list))  # Print the days of the week header
    print("    " * start, end="")  # Print leading spaces for the first week

    for d in range(1, days + 1):
        print(f"{d:>3} ", end=" ")  # Print each day, right-aligned
        if (start + d) % 7 == 0:
            print()  # Start a new line at the end of the week
    print()  # Final newline after printing all days

if __name__ == "__main__":
    # Get user input for number of days and starting day
    days = int(input("Days in month: "))
    start = int(input("Start day (0=Sun, 1=Mon, ... 6=Sat): "))
    print_calendar(days, start)