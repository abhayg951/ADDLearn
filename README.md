# ADDLearn
This is the Learning Management System developed by team ADD

AddLearn is an innovative e-learning platform designed to provide a seamless and interactive educational experience for students and educators. Developed with a modern tech stack, the platform features a user-friendly interface built using React and Next.js, ensuring smooth navigation and responsive design. The backend, powered by FastAPI, handles essential functionalities such as user authentication, course management, and data processing. AddLearn allows instructors to create and manage courses, upload multimedia content, and monitor student engagement. Students can track their progress with a unique system that matches completed chapters with available content, providing real-time updates. The platform also includes a rating system where students can only rate a course upon completion, ensuring that feedback is informed and constructive. With PostgreSQL as the database backbone, AddLearn supports efficient data management and complex queries. While currently designed as a monolithic application, the platform is being actively developed, with future enhancements planned to further improve scalability, feature set, and user experience.

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
 
  Working on V2 - https://github.com/abhayg951/ADDLearnV2
    
