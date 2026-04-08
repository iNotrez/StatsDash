# StatsDash 📊
 
Local web dashboard showing live CPU, RAM, disk, and network stats.
Auto-refreshes every 2 seconds. Dark themed.
 
## Install & run
```bash
git clone https://github.com/iNotrez/StatsDash.git
cd StatsDash
pip install -r requirements.txt
python app.py
```
 
Open http://localhost:5000 in your browser.
 
## API
`GET /stats` — returns live stats as JSON.
 
## Run on a server
Set `host='0.0.0.0'` in `app.py` (already set).
Access from any device: `http://<server-ip>:5000`
 
## Stack
![Python](https://img.shields.io/badge/Python-000?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000?style=flat&logo=flask&logoColor=white)
![psutil](https://img.shields.io/badge/psutil-000?style=flat&logo=python&logoColor=white)
