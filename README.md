# EVCompanion - Vue.js + Django MVP

## Local env

Remember to activate the virtual env:

```
source .venv/bin/activate
```

The very first time you run the app, run:

```
pip install -r backend/requirements.txt
make local-migrate
make local-createsuperuser
```

Finally, run the server
```
make local
```
