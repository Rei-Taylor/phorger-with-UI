# Project Readme

## How to Run the Application

### **Development Setup and Run**

1.  **Install dependencies** from the `requirements.txt` file using `uv`:
    ```bash
    uv pip install -r requirements.txt
    ```

2.  **Start the application** directly with Python:
    ```bash
    python app.py
    ```
    Or using `uv` if you prefer:
    ```bash
    uv run python app.py
    ```

### **Creating a Windows Executable**

To distribute your application as a single `.exe` file:

```bash
uv run nicegui-pack --onefile --name "Phoger" app.py