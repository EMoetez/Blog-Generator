# YouTube to Blog Generator

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Technologies used](#technologyies-used)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Database Schema](#database-schema)
7. [Troubleshooting](#troubleshooting)
8. [Contribution](#contribution)
9. [License](#license)


## Project Overview

The YouTube to Blog Generator is a web application that allows users to convert YouTube videos into blog posts. By simply providing a YouTube URL, the application extracts the transcript from the video, processes it using the LLaMA 2 model via the Ollama API, and generates a well-structured blog post. The generated blogs are stored in a PostgreSQL database, allowing users to consult and manage their blogs through an intuitive interface.

## Features

- **YouTube to Blog Conversion**: Automatically generates a blog post from a YouTube video.
- **User Authentication**: Secure login and registration system.
- **Blog Management**: View and delete generated blogs.
- **Responsive Design**: Frontend built with Tailwind CSS for a seamless experience across devices.
- **Multi-Page Application**: Includes dedicated pages for login, blog management, and user dashboard.
- **Persistent Storage**: Blogs are stored in a PostgreSQL database, allowing users to access their content anytime.

## Technologies used

- **Backend**: Django
- **Frontend**: HTML, Tailwind CSS, js
- **Database**: PostgreSQL
- **AI Model**: LLaMA 2 (via Ollama API)
- **APIs**: Assembly AI for transcription, Ollama for blog generation

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL
- Git
- Virtualenv
- Django
- Assembly AI API Key
- Ollama API (for LLaMA 2 or any model of your choice)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/EMoetez/Blog-Generator.git
   cd Blog-Generator

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
3. **Install Dependencies:**
  
   ```bash
   pip install -r requirements.txt

4. **Configure Environment Variables:**

    - **Create a .env file in the root directory.**
    - **Add your API keys and database configuration:**
      
         - ASSEMBLY_AI_API_KEY=your_assembly_ai_api_key
         - DATABASE_Password=YourDBPassword

5. **Run Migrations:**
   ```python
   python manage.py migrate
   ```

6. **Start the Development Server:**
   ```python
   python manage.py runserver
   ```


7. **Access the Application:**
   
  -**Open your browser and go to http://127.0.0.1:8000/.** 


## Usage

1. **Register or Log In:** Create an account or log in using your credentials.
2. **Input YouTube URL:** Enter the YouTube video URL you want to convert into a blog.
3. **Generate Blog:** Click the "Generate Blog" button to start the process.
4. **View Your Blogs:** Access all your generated blogs from the dashboard.
5. **Manage Blogs:** Edit or delete blogs as needed.

## Database Schema
The project uses a PostgreSQL database with the following schema:

 - **Users:**

    - id: Integer (Primary Key)
    - username: String
    - email: String
    - password: String (Hashed)
      
 - **Blogs:**

    - user: string (Primary Key)
    - youtube_title: String
    - youtube_link: String
    - generated_content: Text
    - created_at: DateTime
    

## Troubleshooting

- Database Connection Errors: Ensure PostgreSQL is running and the DATABASE_URL is correctly configured in your .env file.
- API Errors: Check if your API keys for Assembly AI and Ollama are correctly set up and have sufficient quota.
- Static Files Not Loading: Ensure you’ve run collectstatic in production.
  
## Contribution

Contributions are welcome! If you have suggestions or improvements, please fork the repository, create a feature branch, and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.



