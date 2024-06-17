# School Bell Ringer App

The School Bell Ringer App is a Python application that uses the `tkinter` library to create a graphical user interface (GUI) for scheduling and ringing school bells. The app allows users to set schedules for different days and times and upload custom sound files to be played as the bell sound.

## Features

- Add schedules for different days and times.
- Upload custom sound files to be used as the bell sound.
- Edit and delete existing schedules.
- Save and load schedules to/from a JSON file.
- Automatic bell ringing based on the schedule.

## Requirements

- Python 3.x
- `tkinter`
- `pygame`
- `schedule`

## Installation

1. **Clone the repository:**
    ```sh
    git clone <repository_url>
    cd <repository_name>
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    On Windows:
    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    ```

    On macOS and Linux:
    ```sh
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**
    ```sh
    python main.py
    ```

## Usage

1. **Add Schedule:**
   - Select the day from the dropdown.
   - Select the time from the dropdown.
   - Click "Upload Sound" to choose a custom sound file.
   - Click "Save" to add the schedule.

2. **Edit Schedule:**
   - Select an existing schedule from the list.
   - Click "Edit" and modify the schedule details.
   - Click "Save" in the edit window to save the changes.

3. **Delete Schedule:**
   - Select an existing schedule from the list.
   - Click "Delete" to remove the schedule.

4. **Automatic Bell Ringing:**
   - The app will automatically ring the bell at the scheduled times using the uploaded sound files.

## Dependencies

- `tkinter`: Standard Python interface to the Tk GUI toolkit.
- `pygame`: Library for making multimedia applications.



