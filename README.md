# Bingo Caller Display

A lightweight Flask site to share the latest bingo call and show every number that has been revealed.

## Running locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:

   ```bash
   python app.py
   ```

3. Open `http://localhost:5000` to update and view calls.

The page uses a high-contrast palette so it can be projected in bright rooms. Enter the newest number (1–75) to update the large call banner and highlight it on the board.

## Running on a Raspberry Pi 5

1. Make sure Python 3.11+ and `pip` are installed:

   ```bash
   sudo apt update
   sudo apt install -y python3 python3-venv python3-pip
   ```

2. Create and activate a virtual environment (optional but recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies and start the server:

   ```bash
   pip install -r requirements.txt
   python app.py
   ```

4. Open `http://<pi-ip-address>:5000` from any device on the same network. Called numbers are stored in `data/called_numbers.json` so the board survives restarts. Use the **Clear Board** button between games to reset the list.
