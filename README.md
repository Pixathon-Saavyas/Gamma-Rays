
## TherapEaseAI

![ENV file](docs/main.png)

### ❖ Overview

This project is is part of the Fetch.ai hackathon submission at NIT Goa. We were given a Hugging Face model - [*t5-base-finetuned-emotion*](https://huggingface.co/mrm8488/t5-base-finetuned-emotion) (text-to-text model) to use the model to detect emotions in conversations.

### 🏆 Our Goal

We aimed to make use of the given model to build a mental health therapy platform. The chatbot detects emotions in user input and provides therapy recommendations accordingly.

### 🔗 Content

* [Overview](#-overview)
* [Content](#-content)
* [Team](#-team)
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Environment Variables](#-environment-variables)
* [Run Locally](#-run-locally)
* [Documentation](#-documentation)
* [Demo](#-demo)
* [Screen-Shots](#-screen-shots)
* [Author](#-author)

### 👨‍👦‍👦 Team

- `Atharva Parkhe` -  *Python* -   [LinkedIn](https://www.linkedin.com/in/atharva-parkhe-3283b2202/), [GitHub](https://github.com/atharvparkhe), [Instagram](https://www.instagram.com/atharvparkhe/) - Backend Developer

- `Madem Greeshma` -  *JavaScript* - [LinkedIn](https://www.linkedin.com/in/m-greeshma/), [GitHub](https://github.com/Greeshma2903), [Instagram](https://www.instagram.com/prathamshankwalker/)  -  Frontend Developer

- `Pratham Shankhwalker` -  *Python* - [LinkedIn](https://www.linkedin.com/in/pratham-shankwalker-ab2899205/), [GitHub](https://github.com/prathamshankwalker), [Instagram](https://www.instagram.com/prathamshankwalker/)  -  Machine Learning (ML) Developer


### 📋 Features

- **USER AUTHENTICATION :** Users can Signup for a new account, Verify thier email id, Login using email and password, make a Forgot request to reset thier password.

- **PRODUCTS AND BLOGS :** Users can view all products and blogs.

- **REVIEWS AND RATING :** User can add blogs comments, product review and rateings.

- **CONTACT US FORM :** User can fill up the Contact Us form. (Auto Corrospondence email sending feature)

- **CART FUNCTIONALITY :** User can add and remove products from cart. Users can also change the quantity of items in thier cart.

- **PAYMENT GATEWAY :** Users can make payment using Net-Banking, UPI, Card Payments, etc. through Razorpay Payment Gateway which is integrated in the system.

- **AUTO INVOICE :** After payment, users would recieve invoice (auto-generated) in thier mailbox.


### 🧰 Tech Stack

- **`BACKEND`** : Django *(Python)*

- **`DATABASE`** : SQLite3

- **`FRONTEND`** : HTML, CSS, Javascript


### 🔐 Environment Variables

To run this project, you will need to add the following environment variables to your **.env** file

- `EMAIL_ID`  -  Email ID (which would be used to send emails)

- `EMAIL_PW`  -  Email Password

- `PUBLIC_KEY` - Razorpay API Public Key

- `PRIVATE_KEY` - Razorpay API Private Key

![ENV file](docs/env.png)


### 💻 Run Locally

***Step#1 : Clone Project Repository***

```bash
git clone https://github.com/atharvparkhe/sweet-mart.git && cd sweet-mart
```

***Step#2 : Create Virtual Environment***

* If *virtualenv* is not istalled :
```bash
pip install virtualenv && virtualenv env
```
* **In Windows :**
```bash
env/Scripts/activate
```
* **In Linux or MacOS :**
```bash
source env/bin/activate
```

***Step#3 : Install Dependencies***

```bash
pip install --upgrade pip -r requirements.txt
```

***Step#4 : Add .env file***

- ENV file contents
    - **In Windows :**
    ```bash
        copy .env.example .env
    ```
    - **In Linux or MacOS :**
    ```bash
        cp .env.example .env
    ```
- Enter Your Credentials in the *".env"* file. Refer [Environment Variables](#-environment-variables)

***Step#5 : Run Server***

```bash
python manage.py runserver
```

- Open `http://127.0.0.1:8000/` or `http://localhost:8000/` on your browser.

*Check the terminal if any error.*


### 📄 Documentation

The docs folder contain all the project documentations and screenshots of the project.

**Local Server Base Link :** http://localhost:8000/

**Ngroc Server Link (Not Permament) :** https://accurately-frank-wombat.ngrok-free.app


### 🧑🏻‍💻 Demo

YouTube Link : 
