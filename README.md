# 🌐 Social Media App with Django

A social media web application built with **Python and Django**, designed to provide a foundation for an interactive online community.

## 📌 Overview

This project demonstrates web application development using the Django framework, with separate application modules, templates, static assets, and frontend tooling.

🔗 **Repository:** [Social Media App With Django](https://github.com/Mohammed-Elkhamlichi/Social-Media-App-With-Django)

## 🛠️ Tech Stack

- **Backend:** Python, Django
- **API:** Django REST Framework
- **Frontend:** HTML, CSS, JavaScript
- **Styling:** Tailwind CSS
- **Build Tools:** Node.js, npm, Webpack
- **Database Support:** MySQL and PostgreSQL dependencies

## ✨ Features

- Modular Django application structure
- Server-rendered pages using Django templates
- Static asset and frontend styling integration
- REST API development support
- Media file handling support

*Note: Confirm that each feature is implemented and working in the current version before presenting it as a completed feature.*

## 📂 Project Structure

```text
Social-Media-App-With-Django/
├── accounts/        # Account-related functionality
├── core/            # Core application functionality
├── social_media/    # Social media application module
├── website/         # Website-related functionality
├── templates/       # HTML templates
├── static/          # Static assets
├── media/           # Uploaded media files
├── theme/           # Frontend theme configuration
├── manage.py        # Django management utility
├── requirements.txt # Python dependencies
├── package.json     # Frontend dependencies and scripts
└── webpack.config.js
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Mohammed-Elkhamlichi/Social-Media-App-With-Django.git
```

### 2. Navigate to the project directory

```bash
cd Social-Media-App-With-Django
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 4. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configure the database

Review the Django database configuration in `social_media/settings.py` or the relevant settings module. Configure the database credentials and ensure the required database server is running.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Start the development server

```bash
python manage.py runserver
```

Open the application in your browser:

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)

**Important:** This project uses older dependency versions. Installation may require compatibility adjustments depending on your Python version and operating system. Additional frontend setup may also be necessary.

## 🖼️ Screenshots

Add screenshots of the application's main pages here to demonstrate its interface and functionality.

```markdown
![Application Homepage](screenshots/homepage.png)
```

## 🎯 Project Goals

- Practice full-stack web development with Django.
- Organize application code into reusable modules.
- Work with templates, static assets, and database integration.
- Explore REST API development.

## 👨‍💻 Author

**Mohammed El Khamlichi**

- GitHub: [@Mohammed-Elkhamlichi](https://github.com/Mohammed-Elkhamlichi)
- LinkedIn: [Connect with me](https://www.linkedin.com/)

## 📄 License

No license has been specified in this README. Add a license if you intend to permit reuse or distribution of the project.
