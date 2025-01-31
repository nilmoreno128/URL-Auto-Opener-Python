import csv
import webbrowser
import time
import threading
import keyboard

# Function to read URLs from a CSV file
def get_urls(file_path):
    urls = []
    try:
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row:  # Ensure the row is not empty
                    urls.append(row[0])  # Take the first column as the URL
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error reading the file: {e}")
    return urls

# Function to open URLs with a timer, skip key, and stop key
def open_urls(urls, seconds_per_url=None, skip_key="enter", stop_key="esc"):
    stop_script = threading.Event()  # Persistent event to stop the script

    # Function to detect Esc key globally
    def listen_for_stop():
        keyboard.wait(stop_key)
        stop_script.set()

    # Start the stop listener in a separate thread
    stop_thread = threading.Thread(target=listen_for_stop, daemon=True)
    stop_thread.start()

    for url in urls:
        if stop_script.is_set():
            print("\nThe script has been stopped.")
            break  # Exit the loop immediately if Esc was pressed

        print(f"Opening URL: {url}")
        webbrowser.open(url)

        stop_waiting = threading.Event()  # Controls waiting time

        # Function to detect the skip key (Enter) while waiting
        def wait_for_key():
            while not keyboard.is_pressed(skip_key) and not stop_script.is_set():
                time.sleep(0.1)
            stop_waiting.set()

        if seconds_per_url:
            key_thread = threading.Thread(target=wait_for_key, daemon=True)
            key_thread.start()
            stop_waiting.wait(timeout=seconds_per_url)
            key_thread.join(timeout=0.1)
        else:
            keyboard.wait(skip_key)  # Wait until Enter is pressed

        if stop_script.is_set():
            print("\nThe script has been stopped.")
            break

        # Close the current tab
        keyboard.press_and_release('ctrl+w')

        time.sleep(0.5)  # Ensure tab closes before next URL

# Explain the controls and options
def explain_controls():
    print("\nWelcome to the URL Opener!")
    print("This script will open URLs from a CSV file and allow you to navigate between them.")
    print("\nControls:")
    print("- Press 'Enter' to skip to the next URL manually.")
    print("- The script can automatically move to the next URL after a set time, or you can skip manually.")
    print("- If you choose to wait between URLs, the script will pause for a specified time before moving to the next one.")
    print("- Press 'Esc' at any time to stop the script.")

# Wait for the user to press 'Enter' to start the script
def wait_for_start():
    input("\nPress 'Enter' to start the process...")

# Ask the user if they want a delay
def ask_for_delay():
    delay_choice = input("Do you want a delay between URLs? (yes/no): ").strip().lower()
    if delay_choice == "yes":
        seconds = int(input("How many seconds do you want to wait between URLs? "))
        return seconds
    return None

# Default values for keys
skip_key = "enter"
stop_key = "esc"

# Main execution


file_path = input("Enter the name of the CSV file (with .csv extension): ")

explain_controls()

seconds_per_url = ask_for_delay()


wait_for_start()

urls = get_urls(file_path)

if urls:
    open_urls(urls, seconds_per_url, skip_key, stop_key)
else:
    print("No valid URLs found in the file.")
