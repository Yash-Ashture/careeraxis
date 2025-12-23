# CareerAxis – Job Portal Web Application

CareerAxis is a full-stack Job Portal web application designed to connect job seekers and recruiters through a clean, role-based system.

## 🚀 Features

### 👤 User (Candidate)
- User registration & login
- Create and update profile
- Browse available jobs
- Apply for jobs
- Track application status (Pending / Approved / Rejected)

### 🛠 Admin (Recruiter)
- Admin authentication
- Post new jobs
- View only jobs posted by the logged-in admin
- View applicants for specific jobs
- Approve or reject applications
- Dashboard with job & application statistics

### 🔐 Security & Logic
- Role-based access control
- Admins can manage **only their own jobs**
- Users can apply only once per job
- Session-based authentication

---

## 🧰 Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Deployment:** Render
- **Version Control:** Git & GitHub

## 📂 Project Structure
# CareerAxis – Job Portal Web Application

CareerAxis is a full-stack Job Portal web application designed to connect job seekers and recruiters through a clean, role-based system.

## 🚀 Features

### 👤 User (Candidate)
- User registration & login
- Create and update profile
- Browse available jobs
- Apply for jobs
- Track application status (Pending / Approved / Rejected)

### 🛠 Admin (Recruiter)
- Admin authentication
- Post new jobs
- View only jobs posted by the logged-in admin
- View applicants for specific jobs
- Approve or reject applications
- Dashboard with job & application statistics

### 🔐 Security & Logic
- Role-based access control
- Admins can manage **only their own jobs**
- Users can apply only once per job
- Session-based authentication

---

## 🧰 Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **Deployment:** Render
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

job_portal/
│
├── app.py
├── database.db
├── templates/
│ ├── login.html
│ ├── register.html
│ ├── dashboard.html
│ ├── jobs.html
│ ├── view_profile.html
│ └── ...
│
├── static/
│ ├── css/
│ │ └── main.css
│ └── js/
│ └── main.js
│
└── README.md


---

## ⚙️ Installation & Run Locally

```bash
git clone https://github.com/your-username/careeraxis.git
cd careeraxis
pip install flask
python app.py

