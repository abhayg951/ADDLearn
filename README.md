# ADDLearn
This is the Learning Management System developed by team ADD

The backend of this project is available on this repo and the front end can be seen on the following git repo -> 
https://github.com/DevanshSK/add-learn

### How to Run 

- Go to the `server` folder, and create the `.env` file with following values-
    - DATABASE_NAME
    - DATABASE_HOST
    - DATABASE_PORT
    - DATABASE_USER
    - DATABASE_PASSWORD
    - SECRET_KEY
    - ALGORITHM
    - ACCESS_KEY_EXPIRE_MINUTES
    - CLOUD_NAME
    - API_KEY
    - API_SECRET 
- Create the virtual environment.
- Install all the dependencies from the `requirements.txt` file.
          - `For windows` -> `pip install -r requirements.txt`
          - `for Linux/mac` -> `pip3 install -r requirements.txt`
  - Now, run the `uvicorn` using the following command `uvicorn app.main:app --reload`.
    
