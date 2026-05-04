# 🍽️ FlavorMap

FlavorMap is a web application where users can explore restaurants, leave reviews, and manage their own content.  
The project focuses on building a dynamic, database-driven platform using Django.

---

## 🚀 Features

### 👤 Authentication
- User registration & login system
- Profile page showing user reviews and favorites

### 🍴 Restaurants
- Create, edit, and delete restaurants
- Upload images and add opening hours
- Filter by category, location, and price range
- Search functionality

### ⭐ Reviews
- Users can leave **one review per restaurant**
- Edit and delete their own reviews
- Reply to other users’ reviews (nested replies)

### ❤️ Favorites
- Add / remove restaurants from favorites
- Dynamic UI (filled / empty heart)

### 📋 Menu System
- Restaurant owners can:
  - Add menu items
  - Edit menu items
  - Delete menu items
- Menu items include:
  - Name, description, category, and price

### 🔐 Authorization
- Only restaurant owners can edit/delete their restaurants
- Only review owners can edit/delete reviews
- Only owners can manage menu items

### ⚙️ Advanced Features
- Atomic transactions used for critical operations
- Database consistency ensured
- Basic error handling implemented

---

## 🛠️ Technologies Used

- Python
- Django
- SQLite
- HTML / CSS (Bootstrap)
- Django ORM

---

## 📂 Project Structure
main/
├── models.py
├── views.py
├── forms.py
├── urls.py
├── templates/
---

## ▶️ How to Run

```bash
git clone https://github.com/ipekerturk/FlavorMap.git
cd FlavorMap

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
---
🎯 Project Goal

The goal of this project is to practice:

* Django MVC structure
* Database relationships
* CRUD operations
* Authentication & authorization
* Real-world web application logic
---
👨‍💻 Team Project

This project was developed as a team project.
Each member contributed to different parts of the system including backend logic, UI, and database design.
---
📌 Notes

* This project is built for educational purposes
* Focus is on functionality rather than production-level design
---
