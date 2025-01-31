# **URL Auto Opener**  

This script allows you to open multiple URLs from a CSV file in a web browser, with the ability to:

✅ Set a delay between URLs.  
✅ Skip to the next URL by pressing **Enter**.  
✅ Stop the script at any time by pressing **Esc**.  
✅ Automatically close each tab before opening the next URL.  

## **Installation**  
- Download the [`URL_Opener.exe`](URL_Opener.exe) file.  
- Place your CSV file in the same directory.  
- Double-click `URL_Opener.exe` to start.  

## **CSV File Format**  
The CSV file should contain one URL per row, like this:  

```csv
https://example.com
https://github.com
https://openai.com
```

## **Controls**  
🎯 **Enter** → Skip to the next URL.  
🛑 **Esc** → Stop the script.  

## **How the Script Work**
<details>
  <summary>📦 Requirements to Run in Python</summary>

  To run this script using Python, you need the following:

  ### **1️⃣ Install Python and pip**
  - **Python**  
    - Download it from [python.org](https://www.python.org/downloads/)  
    - Or install it directly from the **Microsoft Store** (search for "Python" in the Store)  
  - **pip** (Comes pre-installed with Python, but you can update it with:  
    ```sh
    python -m pip install --upgrade pip
    ```

  ### **2️⃣ Install Required Libraries**
  If you're running the script as a `.py` file instead of the `.exe`, install the following dependencies:

  ```sh
  pip install keyboard
  ```

  - **csv** → Built-in Python module (no installation required).  
  - **webbrowser** → Built-in Python module (no installation required).  
  - **time** → Built-in Python module (no installation required).  
  - **threading** → Built-in Python module (no installation required).  
  - **keyboard** → Requires manual installation (`pip install keyboard`).  

</details>

<details>
  <summary>🔍 How the Script Works (Detailed Explanation)</summary>

  The script is composed of multiple functions that work together to automate the process of opening URLs. Here’s a breakdown of each part:

  ### **1. Reading URLs from the CSV File**
  ```python
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
  ```
  - Reads the CSV file.
  - Extracts URLs from the first column.
  - Handles errors if the file is missing or unreadable.

  ### **2. Opening URLs and Handling User Inputs**
  ```python
  def open_urls(urls, seconds_per_url=None, skip_key="enter", stop_key="esc"):
      stop_script = threading.Event()  # Persistent event to stop the script
  ```
  - `stop_script` is an event that stops the entire script when **Esc** is pressed.

  ### **3. Detecting the Stop Key (Esc) in a Separate Thread**
  ```python
      def listen_for_stop():
          keyboard.wait(stop_key)
          stop_script.set()
      
      stop_thread = threading.Thread(target=listen_for_stop, daemon=True)
      stop_thread.start()
  ```
  - Runs a background thread that listens for the **Esc** key.
  - If **Esc** is pressed, `stop_script.set()` is triggered, stopping the script.

  ### **4. Iterating Through the URLs**
  ```python
      for url in urls:
          if stop_script.is_set():
              print("\nThe script has been stopped.")
              break

          print(f"Opening URL: {url}")
          webbrowser.open(url)
  ```
  - Opens each URL in the browser.
  - Checks if **Esc** was pressed before opening a new URL.

  ### **5. Waiting for Enter or Time Delay**
  ```python
          stop_waiting = threading.Event()  # Controls waiting time

          def wait_for_key():
              while not keyboard.is_pressed(skip_key) and not stop_script.is_set():
                  time.sleep(0.1)
              stop_waiting.set()
  ```
  - Waits until **Enter** is pressed or the set time expires.

  ```python
          if seconds_per_url:
              key_thread = threading.Thread(target=wait_for_key, daemon=True)
              key_thread.start()
              stop_waiting.wait(timeout=seconds_per_url)
              key_thread.join(timeout=0.1)
          else:
              keyboard.wait(skip_key)
  ```
  - If a delay is set, the script waits before moving to the next URL.
  - If no delay is set, the script waits for **Enter** to be pressed.

  ### **6. Closing the Current Tab**
  ```python
          if stop_script.is_set():
              print("\nThe script has been stopped.")
              break

          keyboard.press_and_release('ctrl+w')
          time.sleep(0.5)
  ```
  - Closes the current browser tab (`Ctrl + W`).
  - Waits for **0.5 seconds** before opening the next URL.

  ### **7. User Interface and Setup**
  ```python
  def explain_controls():
      print("\nWelcome to the URL Opener!")
      print("This script will open URLs from a CSV file and allow you to navigate between them.")
      print("\nControls:")
      print("- Press 'Enter' to skip to the next URL manually.")
      print("- The script can automatically move to the next URL after a set time, or you can skip manually.")
      print("- Press 'Esc' at any time to stop the script.")
  ```

  - Displays instructions before starting.

  ```python
  def wait_for_start():
      input("\nPress 'Enter' to start the process...")
  ```
  - Waits for the user to **press Enter** before starting.

  ```python
  def ask_for_delay():
      delay_choice = input("Do you want a delay between URLs? (yes/no): ").strip().lower()
      if delay_choice == "yes":
          seconds = int(input("How many seconds do you want to wait between URLs? "))
          return seconds
      return None
  ```
  - Asks the user if they want a delay between URLs.

  ### **8. Main Execution**
  ```python
  file_path = input("Enter the name of the CSV file (with .csv extension): ")

  explain_controls()

  seconds_per_url = ask_for_delay()

  wait_for_start()

  urls = get_urls(file_path)

  if urls:
      open_urls(urls, seconds_per_url, skip_key, stop_key)
  else:
      print("No valid URLs found in the file.")
  ```
  - Asks for the CSV file name.
  - Displays instructions.
  - Asks for the delay time.
  - Reads the URLs and starts the process.

</details>

## License  
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
