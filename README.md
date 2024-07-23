---
date: 2024-07-23T10:36:17.534050
author: AutoGPT <info@agpt.co>
---

# k3

Based on the information gathered, the kiosk management application requirements include a number of diverse and complex features tailored to a municipal environment. The application requires compatibility with various operating systems such as Windows, macOS, and Linux to ensure broad accessibility. It must support a wide range of peripheral hardware including keyboards, mice, monitors, printers, USB storage devices, barcode scanners, and RFID readers, catering to different user and operational needs.

For security, the application will incorporate strong user authentication mechanisms favoring OAuth 2.0 and JWT for API security, coupled with AES for data encryption, to protect sensitive information both at rest and in transit. Additional security measures include robust access control, regular updates and patch management, comprehensive encryption, firewalls, and intrusion detection systems.

The UI must adhere to existing branding guidelines, offering customization options for colors, fonts, and logos. It will also feature multilingual support, potentially leveraging APIs like Google Translate or Microsoft Translator for dynamic translations, ensuring accessibility and usability across different cultures and languages.

The core functionality revolves around a customizable UI for displaying media and information with options for interactivity and accessibility. A local CMS will manage content scheduling and updates, capable of operating in offline modes with efficient data synchronization once connectivity is restored. Real-time device monitoring and remote management within the local network are crucial for operational integrity and responsiveness.

Analyses and reporting capabilities will focus on generating insights into user engagement and app performance. These features, alongside offline support functionalities, will be critical in enabling the application to deliver content and services uninterrupted, even in fluctuated network conditions.

Development will adopt a human-in-the-loop approach to ensure the final product align to real-world usability and requirements, utilizing agile methodologies for continuous iteration. Recursive programming techniques will be employed to handle the inherent complexity of the application's functionality, especially in managing the customizable UI components and the local CMS.

The technology stack will include Python, FastAPI, PostgreSQL, and Prisma to ensure the application is built with modern, efficient technologies that support the ambitious feature set required. The proposed design and development strategies aim to result in an intuitive, secure, and versatile kiosk management system that meets the specific needs of the municipal server environment.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'k3'

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
