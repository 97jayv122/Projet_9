# LitReview

A Django-powered web application for requesting and publishing book or article reviews.

---

## 🚀 Overview

CritiqueHub lets users:

- **Request** reviews of books or literary articles by creating a **ticket**.  
- **Read** reviews submitted in response to tickets.  
- **Publish** their own reviews of books or articles.  
- **Follow** other users to see their tickets and reviews in a personalized feed.

---

## ⚙️ Key Features

1. ### Authentication  
   - User registration and login pages.  
   - Unauthenticated visitors can only access signup and login.

2. ### Tickets  
   - Create a ticket to request a review for a book or article.  
   - Optionally create a ticket and its review in one step (“from scratch” review).

3. ### Reviews  
   - Post reviews in response to existing tickets.  
   - Create both a ticket **and** its review in a single operation.

4. ### Feed  
   - Displays, in reverse chronological order (newest first):  
     - All tickets and reviews by users you follow.  
     - Your own tickets and reviews.  
     - Reviews on **your** tickets, even if the reviewer isn’t someone you follow.  
   - “Ticket + Review” shortcut for starting a review from scratch directly in the feed.

5. ### Following  
   - Follow other users by entering their username.  
   - Error message if the username doesn’t exist.  
   - View and manage your following list with options to unfollow or block.

6. ### Content Management  
   - Edit or delete your own tickets and reviews.

---

## 🛠️ Technical Specifications

- **Framework:** Django  
- **Image handling:** Pillow (>=9.0)
- **Database:** SQLite (`db.sqlite3` included in the repo)  
- **Code Style:** PEP 8 compliance  
- **Templates:** Django template engine, utilisation de Bootstrap 5


---

## 📥 Installation & Local Setup

1. **Clone the repository**

   `git clone https://github.com/97jayv122/Projet_9.git`
   `cd Projet_9`

2. **Create and activate a virtual environment**
    
    `python3 -m venv .venv`

    macOS/Linux
    `source .venv/bin/activate`

    Windows
    `.\venv\Scripts\activate`    

3. **Install depandancies**
    `pip install --upgrade pip`
    `pip install -r requirements.txt`

4. **Run the development server**
    `python manage.py runserver`

Visit http://127.0.0.1:8000/ in your browser.
### Log in with one of the following accounts:
   - dev / testpassword
   - sandrine / testpassword
   - éric / testpassword

🎯 Usage

    Sign Up & Log In
    Create an account or log in to access your feed.

    Feed
    Automatically shows tickets and reviews based on your follows and your own posts.

    Create a Ticket
    Click “Ask a review” to request a review.

    Post a Review
    From any ticket, click “Create a review” to submit your review.

    Ticket + Review
    Click “Create a review” at the top of your feed to start a review from scratch.

    Follow / Unfollow
    Enter a username to follow in the “Follow Users” field, or manage your following list on the dedicated page.

    Edit / Delete
    On the My Posts page, use the “Modify” buttons to edit your own tickets and reviews

