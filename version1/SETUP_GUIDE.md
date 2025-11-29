# Setup Guide - Food Recommendation System

## 🚀 Quick Start (5 minutes)

Follow these steps to get the project running on your local machine.

---

## Prerequisites

- **Python 3.8 or higher** ([Download Python](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** (optional, for cloning)

---

## Step-by-Step Installation

### **Step 1: Navigate to Project Directory**

```bash
cd version1
```

### **Step 2: Create Virtual Environment**

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### **Step 3: Install Dependencies**

```bash
pip install -r requirements.txt
```

This will install:
- Django 4.0.4
- scikit-learn 1.0.2
- pandas 1.4.2
- numpy 1.22.3
- Pillow 9.1.1

### **Step 4: Initialize Database**

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates the SQLite database with all necessary tables.

### **Step 5: Create Admin User (Optional)**

```bash
python manage.py createsuperuser
```

Enter:
- Username: `admin`
- Email: `admin@example.com`
- Password: (choose a password)

### **Step 6: Load Sample Data (Optional)**

If you have sample data fixtures:
```bash
python manage.py loaddata sample_data.json
```

### **Step 7: Run Development Server**

```bash
python manage.py runserver
```

You should see:
```
Starting development server at http://127.0.0.1:8000/
```

### **Step 8: Access the Application**

Open your browser and visit:
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 🎨 Adding Sample Data

To test the recommendation system, you need some data:

### **Option 1: Through Admin Panel**

1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. Add:
   - **Products** (base food items like "Biryani", "Pizza", etc.)
   - **ChefProducts** (variants by different chefs)
   - **Customers** (user profiles)

### **Option 2: Using Django Shell**

```bash
python manage.py shell
```

```python
from app.models import Product, ChefProduct

# Create a product
product = Product.objects.create(
    title="Chicken Biryani",
    description="Aromatic rice with spiced chicken",
    meal_type="Lunch",
    category="NonVegetarian",
    cuisine="Indian",
    product_image="productimg/biryani.jpg"
)

# Create chef variants
ChefProduct.objects.create(
    titleid=product,
    chef_name="Chef Ramesh",
    selling_price=250,
    discounted_price=200,
    preparation_time=45,
    description="Hyderabadi style biryani",
    ratings=5,
    category="NonVegetarian",
    meal_type="Lunch",
    product_image="chefproductimg/ramesh_biryani.jpg"
)
```

---

## 🧪 Testing the Recommendation System

### **1. Create a User Account**
- Go to http://127.0.0.1:8000/register/
- Create an account
- Fill profile with preferences

### **2. Browse and Order**
- Browse products
- Add items to cart
- Place orders

### **3. See Recommendations**
- After 3+ orders, you'll see personalized ML recommendations
- Recommendations adapt based on your order history

---

## 🐛 Troubleshooting

### **Issue: "No module named 'app'"**

**Solution:**
Make sure you're in the `version1` directory and virtual environment is activated.

### **Issue: "Port already in use"**

**Solution:**
```bash
python manage.py runserver 8001
```
(Use different port)

### **Issue: "ModuleNotFoundError: No module named 'sklearn'"**

**Solution:**
```bash
pip install scikit-learn
```

### **Issue: "OperationalError: no such table"**

**Solution:**
```bash
python manage.py migrate
```

### **Issue: Images not showing**

**Solution:**
Make sure `MEDIA_URL` and `MEDIA_ROOT` are configured in `settings.py`:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## 📊 Verifying ML Components

### **Check if Recommendation Engine Works:**

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from app.recommendation_engine import HybridRecommender

# Get a user
user = User.objects.first()

# Get recommendations
recommender = HybridRecommender(user)
recommendations = recommender.get_hybrid_recommendations(top_n=5)

print(f"Recommended {len(recommendations)} items:")
for item in recommendations:
    print(f"- {item.product_name} by {item.chef_name}")
```

---

## 🔧 Configuration

### **Important Settings (FoodRecommendationSystem/settings.py)**

```python
# Debug mode (set to False in production)
DEBUG = True

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Authentication
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'
```

---

## 📝 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test app

# Run with verbose output
python manage.py test --verbosity=2
```

---

## 🔐 Security Checklist for Production

Before deploying to production:

- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY` to a random value
- [ ] Set `ALLOWED_HOSTS` to your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure HTTPS
- [ ] Set up proper static file serving
- [ ] Enable CSRF protection
- [ ] Configure secure cookies
- [ ] Set up backup system

---

## 📚 Next Steps

1. **Add More Data**: More products and orders = better recommendations
2. **Test Recommendations**: Try different user scenarios
3. **Review Documentation**:
   - [README.md](README.md) - Project overview
   - [docs/ML_APPROACH.md](docs/ML_APPROACH.md) - ML algorithms explained
   - [docs/INTERVIEW_GUIDE.md](docs/INTERVIEW_GUIDE.md) - Interview preparation
   - [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System architecture

---

## 💡 Development Tips

### **Check Database Schema**
```bash
python manage.py dbshell
.tables
.schema app_product
```

### **Create Database Backup**
```bash
cp db.sqlite3 db_backup.sqlite3
```

### **Reset Database**
```bash
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### **View SQL Queries**
```python
# In views.py
from django.db import connection
print(connection.queries)
```

---

## 🎓 Learning the Codebase

**Start Here:**

1. **Models** (`app/models.py`) - Understand data structure
2. **Recommendation Engine** (`app/recommendation_engine.py`) - ML logic
3. **Views** (`app/views.py`) - Request handling
4. **URLs** (`app/urls.py`) - Routing

**ML Components:**

1. `CollaborativeFiltering` - User-based recommendations
2. `ContentBasedFiltering` - Item similarity
3. `HybridRecommender` - Combined approach

---

## 🆘 Getting Help

**If you encounter issues:**

1. Check error message in terminal
2. Search error in documentation
3. Check Django logs
4. Review settings.py configuration

**Common Commands:**

```bash
# Check Django version
python -m django --version

# Check installed packages
pip list

# Run migrations status
python manage.py showmigrations

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Run server
python manage.py runserver

# Access shell
python manage.py shell
```

---

## ✅ Verification Checklist

After setup, verify:

- [ ] Virtual environment activated
- [ ] All packages installed (`pip list`)
- [ ] Database migrated (tables created)
- [ ] Server runs without errors
- [ ] Can access homepage
- [ ] Can register new user
- [ ] Can login
- [ ] Can view products
- [ ] Admin panel accessible

---

**Setup complete! You're ready to explore the Food Recommendation System. 🎉**
