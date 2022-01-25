# sigma-salon
The best salon you will ever find.

Sigma Salon is a web app designed to manage a pseudo salon database.

Made By:
- Jason Jeremy Wijadi
- Monique Senjaya
- Christopher Tendi

## Configuration

1. Git clone the project
```PowerShell
git clone https://github.com/moniquesenjaya/sigma-salon.git
```
2. CD into the project
```Powershell
cd sigma-salon
```

3. Create virtual environment (Python version for this project == 3.10.0)
```PowerShell
python -m venv venv
```

4. Activate the virtual environment
```PowerShell
# For Windows
venv/Scripts/activate
# For Mac or Linux
. venv/bin/activate
```

5. Install the required libraries
```PowerShell
pip install -r requirements.txt
```

6. Rename the ```.env.template``` file to ```.env``` and fill it with the appropriate credentials

7. Run the main.py file
```PowerShell
python main.py
```