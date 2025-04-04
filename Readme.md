# Devops CI Task

Within this repo contains the frontend and backend application for the simple application requested built with React Typescript and FastAPI from Python.

The application is a image color extractor. A user simply uploads and image and the dominant color gets extracted from such image. 

Below are the instructions to set up and run the project locally, as well as how to trigger GitHub Actions for Continuous Integration (CI).

---

## Prerequisites

Ensure you have the following installed on your system:
- Node.js (v14 or later)
- Python (v3.8 or later)
- Git

---

## Running the Frontend (React)

1. Navigate to the frontend directory:
    ```
    cd img-color-gen-fe
    ```

2. Install dependencies:

on your terminal run: 
    ```
    npm install
    ```

3. Start the development server:
    ```
    npm run dev
    ```

4. Open your browser and navigate or, perform ctrl + click on the link to open to:
    ```
    http://localhost:5173
    ```

---

## Running the Backend (FastAPI)
Open a new terminal and navigate to the backend directory

1. Navigate to the backend directory:
    ```
    cd color-generator-be
    ```

2. Create and activate a virtual environment:
    ```
    python -m venv venv
    venv\Scripts\activate.bat #For windows system
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Start the FastAPI server:
    ```
    uvicorn main:app --reload
    ```

5. Access the API documentation at:
    ```
    http://127.0.0.1:8000/docs
    ```
You should be able to use the frontend application provided this backend api is running
---

## Triggering GitHub Actions for CI

GitHub Actions are configured to run automatically on the following events:
- **Pull Request**: Any pull request to the `main` branch.
- On each pull request, a two CI workflows are trigerred which are: creation of the docker images for the frontend and backend application. Subsequently pushed to dockerhub
- The second CI creates a multi-node cluster. Installs the necessary tools, performs tests and generates the report expected. The tools include

    ```
    KinD
    kubectl
    helm
    NGINX Ingress Controller
    Testing tool 
    ```
After wards, a performance result is generated and uploaded to github actions.

---

## Notes

- Ensure both the frontend and backend are running simultaneously for full functionality.


## Time accountability

Creating the whole application took a total of 4h:42mins

- Fullstack development using React Typescript and Python: 1h:14m
- Configuring CI for deploying the images: 46mins
- Writing scripts for multi-node kubernetes cluster 2hh: 42m

## Challenges encountered

Various challenges are errors were discovered.

- Execution the fullstack application
- Rewriting the application from imperative to declarative programming style using React framework
- Correcting the multinode clusters deployment
