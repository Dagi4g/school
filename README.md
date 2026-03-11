# High School Website

A Django-based website for **chencha secondary school** featuring dynamic home pages and an announcements system. This project provides a modern, responsive web presence for schools to share information with students, parents, and staff.

## Features

- **Dynamic Home Pages**: Multiple customizable home pages with flexible content management
- **Announcements System**: Post and manage school announcements, events, and news
- **Responsive Design**: Mobile-friendly interface that works on all devices
- **Admin Dashboard**: Easy content management through Django's admin interface
- **Clean, Professional Design**: School-appropriate aesthetic with customizable branding

## Prerequisites

Before you begin, ensure you have the following installed:

- Python (3.8 or higher)
- pip (Python package manager)
- virtualenv (recommended)

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/school.git
cd school
```

2. **Create and activate a virtual environment**

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run database migrations**

```bash
python manage.py migrate
```

5. **Create a superuser (admin account)**

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

6. **Collect static files**

```bash
python manage.py collectstatic
```

## Running the Development Server

1. **Start the Django development server**

```bash
python manage.py runserver
```

2. **Access the website**

- Main site: http://127.0.0.1:8000/
- Admin interface: http://127.0.0.1:8000/admin/

## Usage

### Managing Announcements

1. Log in to the admin interface at `/admin`
2. Navigate to **Announcements**
3. Click **Add Announcement**
4. Fill in title, content, and optional image/attachment
5. Set publication date and expiration if needed
6. Save to publish

### Managing Home Pages

1. In the admin interface, go to **Home Pages**
2. Add or edit page sections (hero banner, featured content, etc.)
3. Customize layout and content for different pages
4. Set active/inactive status and display order

## Customization

### Styling

- Modify CSS files in `static/css/` to change the appearance
- Update colors, fonts, and layout in the main stylesheet
- Replace the school logo in `static/images/`

### Templates

- Base template: `templates/base.html`
- Home page templates: `home/templates/home/`
- Announcement templates: `announcements/templates/announcements/`

## Deployment

For production deployment:

1. Set `DEBUG = False` in `settings.py`
2. Configure a production database (PostgreSQL recommended)
3. Set up proper static file serving (WhiteNoise or CDN)
4. Configure email settings for password resets
5. Use Gunicorn as the WSGI server
6. Set up an SSL certificate for HTTPS

Example production requirements:

```bash
pip install gunicorn psycopg2-binary whitenoise
```

## Troubleshooting

### Database migration fails

- Ensure the database is properly configured
- Try resetting migrations:

```bash
python manage.py migrate --fake-initial
```

### Static files not loading

- Run:

```bash
python manage.py collectstatic
```

- Check `STATIC_URL` and `STATIC_ROOT` settings

### Admin interface inaccessible

- Verify a superuser exists:

```bash
python manage.py createsuperuser
```

- Check that the admin URL is included in `urls.py`

## Contributing

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/AmazingFeature
```

3. Commit your changes

```bash
git commit -m "Add AmazingFeature"
```

4. Push to the branch

```bash
git push origin feature/AmazingFeature
```

5. Open a Pull Request

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Support

For support, email **[your-email@example.com]** or open an issue in the GitHub repository.

## Acknowledgments

- Django Framework
- Bootstrap for responsive design
- All contributors and testers

---


## Quick Start Commands

```bash
# Clone and setup
git clone [your-repo-url]
cd highschool-website
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Database and admin
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

# Visit: http://localhost:8000
# Admin: http://localhost:8000/admin
```
