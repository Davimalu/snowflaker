import sys
from datetime import datetime

def main():
    # Check for proper usage
    if not len(sys.argv) == 2:
        print("Usage: python snowflaker.py <log_file.txt>")
        sys.exit(1)

    # Try to open the log file - if not successfull, throw an error
    try:
        # Open log file
        log_file = open(sys.argv[1], "r")
        # Create ReadLine Object
        lines = log_file.readlines()
    except:
        print("Error opening file. Check if the filename was spelled right or if the file is corrupted.")
        sys.exit(2)

    # Keep track of the amount of lines, keep track of the amount of errors, keep track of the amount of startups
    line_count = 0
    error_count = 0
    startup_count = 0
    
    # A dictionary is utilized to store all information from the log file
    # Each line is stored as a separate key in the dicitionary - the timestamp serves as the key
    # The information (No. of connections, Traffic relayed ↓↑) is stored inside a list which is stored as the value for each key
    log = dict()

    # Loop through every line of the log file
    for line in lines:
        line_count += 1

        # Converts the line into a list of words
        line_words = line.split()

        # Check for an empty or too short line
        if len(line_words) < 4:
            print("Error: Couldn't read line | Unknown line format")
            continue

        # Check if line is an error message
        if line_words[1] == "ERROR:":
            error_count += 1
            continue

        # Check if line is a startup message
        if line_words[2] == "Proxy" and line_words[3] == "starting":
            startup_count += 1
            continue
        if line_words[2] == "NAT":
            continue

        # Check if line is a valid log message
        if len(line_words) < 18:
            print("Error: Couldn't read line | Unknown line format")
            continue

        # Get date and time from each line
        try:
            date_time_unformatted = line_words[0] + " " + line_words[1]
            date_time_formatted = datetime.strptime(date_time_unformatted, '%Y/%m/%d %H:%M:%S')
        except:
            print("Error: Couldn't read line | Unknown line format")
            continue

        # Get number of connections in that hour
        connection_count = line_words[8]
        try:
            int(connection_count)
        except:
            print("Error: Couldn't read line | Unknown line format")
            continue

        # Get number of forwarded traffic ↓ and ↑
        down_forward = line_words[13]
        up_forward = line_words[16]
        try:
            int(down_forward)
            int(up_forward)
        except:
            print("Error: Couldn't read line | Unknown line format")
            continue

        # Write data into dictionary
        log[date_time_formatted] = [connection_count, down_forward, up_forward]

    # Calculate quick stats
    total_connection_count = 0 
    total_down_forward = 0
    total_up_forward = 0

    for line in log:
        total_connection_count += int(log[line][0])
        total_down_forward += int(log[line][1])
        total_up_forward += int(log[line][2])

    # Output quick stats
    print("Quick Overview:")
    print(f"• Startups: {startup_count}")    
    print(f"• Snowflake Errors: {error_count}")
    print(f"• Total number of connections: {total_connection_count}")
    print(f"• Total forwarded traffic ↓: {total_down_forward} KB » {round(total_down_forward / 1000, 2)} MB » {round(total_down_forward / 1000000, 2)} GB")
    print(f"• Total forwarded traffic ↑: {total_up_forward} KB » {round(total_up_forward / 1000, 2)} MB » {round(total_up_forward / 1000000, 2)} GB")

    # Ask user if he wants to continue with generating graphical statistics
    print("\nWould you like to generate graphical statistical data from your log file? (y/n)")
    question = input().lower()

    if question == "y":
        pass
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()