🍽️ FlavorMap

A Django-based web application where users can explore restaurants, leave reviews, and manage their own content.

⸻

🚀 Features

👤 Authentication

* Register & login system
* User profile page (reviews & favorites)

🍴 Restaurants

* Create, edit, delete restaurants
* Upload images
* Add opening hours
* Filter by category, location, price
* Search functionality

⭐ Reviews

* One review per user per restaurant
* Edit / delete own reviews
* Reply to reviews (nested)

❤️ Favorites

* Add / remove favorites
* Dynamic heart UI

📋 Menu System

* Restaurant owners can:
    * Add menu items
    * Edit menu items
    * Delete menu items

🔐 Authorization

* Only owners can edit/delete restaurants
* Only review owners can edit/delete reviews
* Menu control belongs to restaurant owner

⚙️ Advanced

* Atomic transactions
* Data consistency
* Basic error handling

⸻

🛠️ Tech Stack

* Python
* Django
* SQLite
* Bootstrap
* Django ORM

⸻

📂 Project Structure

main/
├── models.py
├── views.py
├── forms.py
├── urls.py
└── templates/

⸻

▶️ Run Locally

git clone https://github.com/ipekerturk/FlavorMap.git
cd FlavorMap

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver

⸻

🎯 Purpose

This project was built to practice:

* Django MVC structure
* Database relationships
* CRUD operations
* Authentication & authorization
* Real-world web logic

⸻

👨‍💻 Team Project

Developed as a team project.
Different parts were implemented collaboratively.

⸻

📌 Note

Educational project – focus is functionality, not production-level polish.
