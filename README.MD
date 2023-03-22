First create a python virtual environment. Then install the packages with requirement.txt.
Use the Primary database for the user management. For admin 
username:cdcju
password:cdcju@112358



-------------------------------------------
How to use the logger ?
- Step 1: Import the logger from the utils folder
```
from logmanager.manager import ApplicationLogger
```
- Step 2. Call logger and pass a message.

Now, There is total 5 level of logging.
You can call them by using the following code.
```
ApplicationLogger.info("This is info message")
ApplicationLogger.debug("This is debug message")
ApplicationLogger.warn("This is warning message")
ApplicationLogger.error("This is error message")
ApplicationLogger.trace("This is trace message")
```

--------------------------------------------------
Docker related command

Start docker instance
```bash
docker-compose up
```

> Acccess Service at `172.0.0.2:8000`
