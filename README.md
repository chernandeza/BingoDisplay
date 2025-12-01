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

The page uses a high-contrast palette so it can be projected in bright rooms. Enter the newest number (1–75) to update the large call banner and highlight it on the board. Called numbers are stored in `data/called_numbers.json` so the board survives restarts.

## Fresh Raspberry Pi OS setup (Pi 5)

Use these commands on a clean Raspberry Pi OS (64-bit) install. Replace `/home/pi` with your preferred location if you use another user.

1. Update the system and install prerequisites:

   ```bash
   sudo apt update
   sudo apt upgrade -y
   sudo apt install -y git python3 python3-venv python3-pip
   ```

2. Clone the project and enter it:

   ```bash
   cd /home/pi
   git clone https://github.com/your-org/BingoDisplay.git
   cd BingoDisplay
   ```

3. Create and activate a virtual environment, then install dependencies (includes Flask and Gunicorn):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. (Quick start) Run the development server to verify everything works:

   ```bash
   python app.py
   ```

   Open `http://<pi-ip-address>:5000` from another device to view the board. Press `Ctrl+C` to stop the server.

5. (Recommended) Run with Gunicorn as a service so it starts on boot:

   ```bash
   cat <<'SERVICE' | sudo tee /etc/systemd/system/bingo-display.service
   [Unit]
   Description=Bingo Caller Display
   After=network.target

   [Service]
   WorkingDirectory=/home/pi/BingoDisplay
   Environment="PATH=/home/pi/BingoDisplay/.venv/bin"
   ExecStart=/home/pi/BingoDisplay/.venv/bin/gunicorn --workers 2 --bind 0.0.0.0:8000 app:app
   Restart=always
   User=pi

   [Install]
   WantedBy=multi-user.target
   SERVICE

   sudo systemctl daemon-reload
   sudo systemctl enable --now bingo-display
   ```

   * Check status: `sudo systemctl status bingo-display`
   * View logs: `sudo journalctl -u bingo-display -f`

6. Access the site at `http://<pi-ip-address>:8000`. Use the **Clear Board** button between games to reset the list. Persistent call data lives at `/home/pi/BingoDisplay/data/called_numbers.json`.

## Notes

- The app stores called numbers in `data/called_numbers.json`; delete this file or use the **Clear Board** button to start a new game.
- Gunicorn binds to port 8000 in the service example to avoid conflicts. Change the port in the unit file if you prefer another value.
- For an HTTPS or reverse-proxy setup, place Nginx or another proxy in front of Gunicorn and point it to `http://127.0.0.1:8000`.
