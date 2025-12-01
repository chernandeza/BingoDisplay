# Bingo Caller Display

Sitio Flask en español para cantar números de bingo y compartirlos en un tablero de alto contraste.

## Running locally

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:

   ```bash
   python app.py
   ```

3. Abre `http://localhost:5000/ingresar` para ingresar números desde el celular y `http://localhost:5000/tablero` para proyectar el tablero.

La interfaz está en español y usa colores de alto contraste para proyectarse en salas iluminadas. Ingresa el número recién cantado (1–75) para actualizar la ficha grande y marcarlo en el tablero. Los números se guardan en `data/called_numbers.json` para sobrevivir reinicios.

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

   Abre `http://<ip-del-pi>:5000/ingresar` en tu teléfono para cantar números y `http://<ip-del-pi>:5000/tablero` en la pantalla o proyector. Presiona `Ctrl+C` para detener el servidor.

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

6. Accede al sitio en `http://<ip-del-pi>:8000` (`/ingresar` para cargar números, `/tablero` para mostrar). Usa el botón **Reiniciar juego** entre partidas para limpiar la lista. Los datos persisten en `/home/pi/BingoDisplay/data/called_numbers.json`.

## Notes

- La app guarda los números en `data/called_numbers.json`; borra este archivo o usa el botón **Reiniciar juego** para empezar de cero.
- Gunicorn escucha en el puerto 8000 en el ejemplo de servicio para evitar conflictos. Cambia el puerto en el unit file si prefieres otro valor.
- Para HTTPS o proxy inverso, coloca Nginx u otro proxy delante de Gunicorn y apúntalo a `http://127.0.0.1:8000`.
