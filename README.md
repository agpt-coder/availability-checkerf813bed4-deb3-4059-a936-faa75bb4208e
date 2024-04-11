---
date: 2024-04-11T11:18:39.843928
author: AutoGPT <info@agpt.co>
---

# Availability Checker

To develop a function that returns the real-time availability of professionals, updating based on current activity or schedule, we'll utilize the following tech stack: Python as the programming language, FastAPI for the API framework, PostgreSQL for the database, and Prisma as the ORM. The system will focus on professionals in sectors where immediate response is crucial, such as healthcare, IT support, and customer service. Updates to a professional's availability status will be triggered by various activities including new appointments, meeting completions, and schedule changes.

The implementation will leverage WebSockets in FastAPI for real-time updates, ensuring a persistent, two-way communication channel. For storing and tracking dynamic schedules and availability, PostgreSQL's robust features like triggers and stored procedures will be utilized. Prisma ORM will facilitate efficient database interactions. The solution will enable manual updates by professionals for flexibility, complemented by automation for predictable or recurring changes. Best practices such as using a publish-subscribe pattern, ensuring secure data transmission, and implementing throttling will be followed to optimize performance and user experience. This will enable a seamless integration of real-time functionality, enhancing workflow coordination and reducing downtime in critical operations.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Availability Checker'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
