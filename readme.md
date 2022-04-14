# Real Estate Head Office


These are the recommended commands for macOS:
```bash
python -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
python3 create.py
python3 add_data.py
python3 query_data.py
```
Recommended commands for Windows:
```cmd
python -m venv venv
venv\Scripts\activate.bat
pip3 install -r requirements.txt
python3 create.py
python3 add_data.py
python3 query_data.py
```

### Important design decisions

I used Codeacademy as a resource; I alsoconsulted Thiago Silva to ask some questions to him.

I try to catch errors if someone tries to sell a house in the listing; or a house already sold.

Random number generators in conjunction with for loops to populate the databases.

Seperation of concerns to enable - files that have different functionalities to be seperated.