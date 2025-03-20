from datetime import datetime

# Get the current date and time
current_datetime = datetime.now()

# Extract the date
current_date = current_datetime.date()

# Extract the time
current_time = current_datetime.time()

# Print the results
print("Date:", current_date)
print("Time:", current_time)
