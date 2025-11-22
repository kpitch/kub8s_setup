# Mac Automation Guide

This folder contains the scripts to run your Expense Automation System automatically on your MacBook.

## 📂 Files
- **`run_daily.sh`**: The script that runs the Python application.
- **`setup_cron.sh`**: A one-time setup script to schedule the daily job.
- **`automation.log`**: Created automatically to log the output of each run.

## 🚀 Setup Instructions

### 1. Prepare the Application
1.  **Get an App Password**:
    *   Go to your Google Account > Security > 2-Step Verification > App Passwords.
    *   Create one named "Expense Automation".
    *   Copy the 16-character password.
2.  **Configure Environment**:
    *   Create a file named `.env` in this `mac_automation` folder.
    *   Add the following lines:
        ```
        EMAIL_USER=your_email@gmail.com
        EMAIL_PASS=your_16_char_app_password
        ALERT_EMAIL=your_email@gmail.com
        ```

### 2. Schedule the Automation
1.  Open your terminal.
2.  Navigate to this `mac_automation` folder:
    ```bash
    cd path/to/your/kub8s_setup/mac_automation
    ```
3.  Run the setup script:
    ```bash
    ./setup_cron.sh
    ```
    *This will add a "cron job" to run `run_daily.sh` every day at 9:00 AM.*

### 3. Verify
-   **Check the Schedule**: Run `crontab -l` in the terminal. You should see a line ending with `run_daily.sh`.
-   **Check Logs**: After 9:00 AM, check `automation.log` in this folder to see if it ran successfully.

## ⚠️ Important Notes
-   **Computer Status**: Your MacBook must be **turned on and awake** at 9:00 AM for the script to run.
-   **Internet**: You must be connected to the internet.
