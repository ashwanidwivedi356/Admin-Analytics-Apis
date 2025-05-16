# 🛒 E-Commerce API Backend with Admin Analytics

A robust and scalable **E-Commerce API** developed with **Django** and **Django REST Framework**. This backend system facilitates the creation, management, and delivery of online products, supporting features akin to platforms like Shopify or WooCommerce.

---

## 🚀 Features

- **User Management**: JWT-based authentication with roles for Customers and Admins.
- **Product Management**: Admins can create, update, and delete products with detailed metadata.
- **Cart & Order Management**: Customers can add products to their cart, place orders, and track order status.
- **Payment Integration**: Simulate a payment gateway or integrate with Razorpay/Stripe for real transactions.
- **Admin Analytics Dashboard**: Admins can view daily/monthly revenue, most sold products, top customers, and order trends over time.
- **Discounts & Coupons**: Apply discount codes to orders for promotions.
- **Password Reset**: Secure password reset functionality via email.

---

## 🧱 Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (with djangorestframework-simplejwt)
- **Asynchronous Tasks**: Celery with Redis
- **Payments**: Razorpay or Stripe
- **API Documentation**: Swagger or ReDoc
- **Optional**: Docker for containerization, GitHub Actions for CI/CD

- **Clone the repository**:

  
   git clone https://github.com/yourusername/ecommerce-api-backend.git
   cd ecommerce-api-backend
