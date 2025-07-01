
# MAC 

A Django-based e-commerce web application with Stripe integration for payments, Cloudinary for media storage, and deployment-ready configurations for Render.

## Features

- Product listing and detail pages
- Shopping cart
- Stripe-based checkout
- Django admin for managing products (with Cloudinary image hosting for HTTPS)
- Cloudinary storage for images (secure, HTTPS-ready)
- Deployed on Render
- User-friendly storefront
- Product Quick View modal
- Add to Cart functionality
- Order Tracking with Gmail Email notifications
- Product Search feature
- Responsive design

## Tech Stack

- Django 4.2
- SQLite (default) / Render Postgres (prod-ready)
- Stripe
- Cloudinary for media storage
- Gmail SMTP for email notifications
- Render for deployment
---

## Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/rijo7/MAC.git
cd MAC
```

### 2️⃣ Install Dependencies

It’s recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

---

### 3️⃣ Configure Environment Variables

Create a `.env` file in the project root:

```
SECRET_KEY=your-secret-key
STRIPE_SECRET_KEY=your-stripe-secret
STRIPE_PUBLISHABLE_KEY=your-stripe-publishable
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

---

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

---

### 5️⃣ Create a Superuser

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run the Server Locally

```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)  
Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Deployment on Render

This project includes:

- `render.yaml` (for Render Blueprint deploy)
- `Procfile` (for Gunicorn WSGI)

Typical Render environment variables:

```
RENDER=true
SECRET_KEY=your-secret
...
```

Render will use:

```
gunicorn mac.wsgi:application
```

---

## Media & Static Files

- Static files collected to `staticfiles/`
- Media files uploaded to Cloudinary
- Cloudinary integration via `DEFAULT_FILE_STORAGE`

---

## Admin Interface

- Fully HTTPS-ready for production
- Upload products & images via Django Admin

---

## Deployment

- Uses **Render** for hosting
- Includes `render.yaml` and `Procfile`
- Cloudinary for HTTPS-ready media hosting

---

## Live Site

👉 [https://mac-1.onrender.com](https://mac-1.onrender.com)

---

## License

MIT
