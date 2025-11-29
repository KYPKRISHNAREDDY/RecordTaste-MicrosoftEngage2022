# Food Recommendation System

**Microsoft Engage 2022 Project**
*ML-Based Food Ordering Platform with Intelligent Recommendations*

---

## 📋 Project Overview

A full-stack e-commerce food ordering platform built with Django that implements **machine learning-based recommendation algorithms** to provide personalized food suggestions to users. The system uses a hybrid approach combining collaborative filtering and content-based filtering to deliver accurate recommendations.

**Project Duration:** May 2022 (1 month)
**Methodology:** Agile Scrum (4 sprints)

---

## 🎯 Key Features

### 1. **ML-Based Recommendation Engine**
- **Collaborative Filtering**: Finds similar users based on purchase history using Jaccard similarity
- **Content-Based Filtering**: Recommends similar items using weighted feature matching (cuisine, category, price, ratings)
- **Hybrid Approach**: Combines multiple recommendation strategies with configurable weights
- **Cold Start Handling**: Profile-based and popularity-based fallback for new users

### 2. **User Management**
- User registration and authentication
- Profile creation with food preferences (used for recommendations)
- Order history tracking
- Shopping cart management

### 3. **Product Features**
- Multi-category food items (Indian, Chinese, Italian, Continental)
- Chef-specific product variants
- Advanced filtering (price, ratings, preparation time, meal type)
- Search functionality

### 4. **Analytics & Tracking**
- User interaction logging (views, clicks, cart additions, purchases)
- Recommendation performance tracking
- Product popularity metrics
- User behavior analytics

---

## 🏗️ Architecture

### **Technology Stack**

**Backend:**
- Python 3.8+
- Django 4.0.4
- SQLite Database

**ML Libraries:**
- scikit-learn 1.0.2 (for similarity calculations)
- pandas 1.4.2 (data manipulation)
- numpy 1.22.3 (numerical operations)

**Frontend:**
- HTML5, CSS3, JavaScript
- Bootstrap 5

---

## 📊 Database Models

### Core Models:
1. **Customer**: User profiles with preferences
2. **Product**: Base food items with attributes
3. **ChefProduct**: Chef-specific variants with pricing and ratings
4. **Cart**: Shopping cart items
5. **OrderPlaced**: Order history (crucial for collaborative filtering)

### ML-Supporting Models:
6. **UserInteraction**: Tracks user behavior for ML improvements
7. **RecommendationLog**: Logs recommendations for A/B testing and accuracy measurement

---

## 🤖 Recommendation System Details

### **1. Collaborative Filtering (User-Based)**

**How it works:**
- Calculates user similarity using **Jaccard Similarity Coefficient**
- Formula: `|A ∩ B| / |A ∪ B|` where A and B are sets of purchased items
- Finds top 5 similar users
- Recommends items purchased by similar users
- **Weight in hybrid system: 40%**

**Interview Explanation:**
> "I implemented user-based collaborative filtering by comparing users' purchase histories. When User A and User B have purchased similar items, the system calculates their similarity score using Jaccard coefficient. Items that User B purchased but User A hasn't are then recommended to User A."

### **2. Content-Based Filtering**

**How it works:**
- Calculates item similarity based on features:
  - Cuisine type (weight: 0.3)
  - Category - Veg/Non-veg (weight: 0.25)
  - Meal type (weight: 0.2)
  - Price range similarity (weight: 0.15)
  - Rating similarity (weight: 0.1)
- Uses **weighted feature matching** algorithm
- Recommends items similar to user's purchase history
- **Weight in hybrid system: 30%**

**Interview Explanation:**
> "Content-based filtering analyzes food item attributes like cuisine, category, price range, and ratings. When a user orders Biryani (Indian, Non-Veg, ₹150), the system finds items with similar characteristics by calculating feature-based similarity scores."

### **3. Hybrid Recommendation System**

**How it works:**
- Combines multiple recommendation strategies:
  - Collaborative Filtering: 40%
  - Content-Based Filtering: 30%
  - Popularity-Based: 20%
  - Profile-Based: 10%
- Weighted scoring algorithm
- Handles cold-start problem for new users
- Adapts based on user history (< 3 orders = profile-based, >= 3 = full hybrid)

**Interview Explanation:**
> "The hybrid approach combines the strengths of different algorithms. For new users with fewer than 3 orders, we rely more on profile preferences and popular items. For returning users, we use collaborative and content-based filtering weighted by their proven effectiveness."

---

## 🚀 Installation & Setup

### Prerequisites:
- Python 3.8 or higher
- pip package manager

### Steps:

```bash
# 1. Clone the repository
cd version1

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Create superuser (for admin panel)
python manage.py createsuperuser

# 6. Run development server
python manage.py runserver

# 7. Access the application
# Open browser: http://127.0.0.1:8000/
# Admin panel: http://127.0.0.1:8000/admin/
```

---

## 📁 Project Structure

```
version1/
├── FoodRecommendationSystem/     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── app/                          # Main application
│   ├── models.py                 # Database models
│   ├── views.py                  # View controllers
│   ├── recommendation_engine.py  # ML recommendation algorithms
│   ├── utils.py                  # Helper functions
│   ├── analytics.py              # Analytics and metrics
│   ├── forms.py                  # Django forms
│   ├── admin.py                  # Admin configurations
│   └── urls.py                   # URL routing
├── docs/                         # Documentation
│   ├── ML_APPROACH.md           # ML methodology
│   ├── ARCHITECTURE.md          # System design
│   └── INTERVIEW_GUIDE.md       # Interview Q&A
├── media/                        # User-uploaded images
├── requirements.txt              # Python dependencies
└── manage.py                     # Django management script
```

---

## 🎓 Learning Outcomes

### Technical Skills:
- ✅ Implemented ML algorithms (Collaborative Filtering, Content-Based Filtering)
- ✅ Built scalable Django backend architecture
- ✅ Designed normalized database schema
- ✅ Developed RESTful patterns
- ✅ User authentication and authorization
- ✅ Data analysis and recommendation systems

### Soft Skills:
- ✅ Agile Scrum methodology
- ✅ Sprint planning and execution
- ✅ Incorporating feedback iteratively
- ✅ Documentation and code organization

---

## 📈 Agile Methodology (4 Sprints)

### **Sprint 1 (Week 1):** Foundation
- Project selection and planning
- Technology stack research
- Basic Django setup
- Database schema design
- User authentication implementation

### **Sprint 2 (Week 2):** Core Features
- Product catalog implementation
- Shopping cart functionality
- Order management
- Basic filtering and search
- Mentor feedback integration

### **Sprint 3 (Week 3):** ML Implementation
- Collaborative filtering algorithm
- Content-based filtering algorithm
- Hybrid recommendation system
- User interaction tracking
- Cold start problem handling

### **Sprint 4 (Week 4):** Polish & Documentation
- UI/UX improvements
- Analytics implementation
- Performance optimization
- Testing and bug fixes
- Comprehensive documentation

---

## 🎤 For Interviews

**Key Points to Emphasize:**

1. **ML Implementation**: Real machine learning algorithms, not just simple filters
2. **Hybrid Approach**: Combining multiple strategies for better accuracy
3. **Cold Start Handling**: Thoughtful approach to new user recommendations
4. **Scalability**: Database design supports growth
5. **Agile Methodology**: Iterative development with feedback incorporation

**See `docs/INTERVIEW_GUIDE.md` for detailed Q&A preparation**

---

## 📊 System Metrics

- **Recommendation Accuracy Tracking**: Built-in analytics to measure recommendation performance
- **User Interaction Logging**: Comprehensive tracking of user behavior
- **A/B Testing Support**: Recommendation log for comparing algorithm effectiveness

---

## 🔒 Security Features

- Django's built-in authentication system
- CSRF protection
- Password hashing
- SQL injection prevention (ORM)
- XSS protection

---

## 🚧 Future Enhancements

- Real-time recommendation updates
- Deep learning models for improved accuracy
- Multi-language support
- Payment gateway integration
- Mobile app version
- Social features (reviews, ratings by users)

---

## 👨‍💻 Developer

**KYP Krishna Reddy**
Microsoft Engage 2022 Participant

---

## 📄 License

This project was developed as part of the Microsoft Engage 2022 mentorship program.

---

## 📚 Additional Resources

- [ML Approach Documentation](docs/ML_APPROACH.md)
- [System Architecture](docs/ARCHITECTURE.md)
- [Interview Guide](docs/INTERVIEW_GUIDE.md)
