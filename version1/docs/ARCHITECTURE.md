# System Architecture
## Food Recommendation System

---

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (HTML/CSS/JS + Bootstrap)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DJANGO WEB FRAMEWORK                       │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
│  │   Views      │  │  Templates   │  │   URL Routing      │   │
│  │  (Controllers)│  │  (Rendering) │  │   (Navigation)     │   │
│  └──────────────┘  └──────────────┘  └────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                   ┌─────────┴─────────┐
                   │                   │
                   ↓                   ↓
    ┌──────────────────────┐  ┌──────────────────────┐
    │   Business Logic     │  │   ML Engine          │
    │   - Cart Management  │  │   - Collaborative    │
    │   - Order Processing │  │   - Content-Based    │
    │   - User Auth        │  │   - Hybrid System    │
    └──────────┬───────────┘  └──────────┬───────────┘
               │                          │
               │         ┌────────────────┘
               │         │
               ↓         ↓
    ┌───────────────────────────────────┐
    │      Django ORM (Data Layer)      │
    └───────────────┬───────────────────┘
                    │
                    ↓
    ┌───────────────────────────────────┐
    │      SQLite Database              │
    │  - User Data                      │
    │  - Product Catalog                │
    │  - Orders & Cart                  │
    │  - Interactions & Logs            │
    └───────────────────────────────────┘
```

---

## 🗂️ Application Structure

### **Directory Organization**

```
version1/
│
├── FoodRecommendationSystem/          # Django Project Configuration
│   ├── __init__.py
│   ├── settings.py                    # Project settings
│   ├── urls.py                        # Root URL configuration
│   ├── wsgi.py                        # WSGI server entry point
│   └── asgi.py                        # ASGI server entry point
│
├── app/                               # Main Application
│   ├── __init__.py
│   ├── apps.py                        # App configuration
│   │
│   ├── models.py                      # Database Models (7 models)
│   ├── views.py                       # View Controllers
│   ├── urls.py                        # App URL patterns
│   ├── forms.py                       # Django Forms
│   ├── admin.py                       # Admin interface config
│   │
│   ├── recommendation_engine.py       # ML Recommendation System
│   ├── utils.py                       # Helper utilities
│   ├── analytics.py                   # Analytics & metrics
│   │
│   ├── templates/                     # HTML Templates
│   │   └── app/
│   │       ├── base.html
│   │       ├── home.html
│   │       ├── product_detail.html
│   │       ├── cart.html
│   │       ├── orders.html
│   │       ├── login.html
│   │       └── ... (other templates)
│   │
│   ├── static/                        # Static Files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── migrations/                    # Database migrations
│
├── media/                             # User-uploaded files
│   ├── productimg/
│   └── chefproductimg/
│
├── docs/                              # Documentation
│   ├── ML_APPROACH.md
│   ├── ARCHITECTURE.md
│   └── INTERVIEW_GUIDE.md
│
├── manage.py                          # Django management script
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation
```

---

## 📦 Component Architecture

### **1. Models Layer (Database)**

```python
Customer  ──────────┐
    ↓               ↓
OrderPlaced ←── ChefProduct ──→ Cart
    ↓               ↓              ↓
    └───────────→ User ←──────────┘
                    ↓
            UserInteraction
                    ↓
          RecommendationLog

Product ←── ChefProduct
```

**Model Relationships:**
- `Customer` ↔ `User` (OneToOne)
- `ChefProduct` ↔ `Product` (ManyToOne)
- `Cart` ↔ `User` (ManyToOne)
- `OrderPlaced` ↔ `User` (ManyToOne)
- `UserInteraction` ↔ `User` (ManyToOne)
- `RecommendationLog` ↔ `User` (ManyToOne)

---

### **2. Recommendation Engine Architecture**

```
┌─────────────────────────────────────────────────────┐
│            HybridRecommender (Main Entry)           │
└────────────┬────────────────────────────────────────┘
             │
             ├──→ CollaborativeFiltering
             │    ├── calculate_user_similarity()
             │    ├── find_similar_users()
             │    └── get_recommendations()
             │
             ├──→ ContentBasedFiltering
             │    ├── calculate_item_similarity()
             │    ├── get_similar_items()
             │    └── get_recommendations_from_history()
             │
             ├──→ get_popularity_based()
             │
             ├──→ get_profile_based()
             │
             └──→ get_hybrid_recommendations()
                  └── Weighted Combination
```

**Algorithm Flow:**

1. **Check User History**
   - If orders < 3: Use profile + popularity
   - If orders >= 3: Use full hybrid

2. **Generate Component Scores**
   - Collaborative: Find similar users → Recommend their items
   - Content-Based: Find similar items → Based on user history
   - Popularity: Get trending/popular items
   - Profile: Match cuisine & category preferences

3. **Combine Scores**
   ```
   Final_Score = 0.4×Collab + 0.3×Content + 0.2×Pop + 0.1×Profile
   ```

4. **Rank and Return**
   - Sort by final score
   - Remove duplicates
   - Return top N items

---

### **3. Views Architecture (MVC Pattern)**

```
User Request
     ↓
URL Router (urls.py)
     ↓
View Function/Class (views.py)
     ↓
┌────────────────┐
│  View Logic    │
├────────────────┤
│ 1. Authenticate│
│ 2. Get Data    │ ←──── Models (models.py)
│ 3. ML Process  │ ←──── Recommendation Engine
│ 4. Analytics   │ ←──── Analytics Module
│ 5. Prepare     │
│    Context     │
└───────┬────────┘
        ↓
    Template (HTML)
        ↓
    Render Response
        ↓
    User Browser
```

**Key Views:**
- `HomeView`: Main page with personalized recommendations
- `ProductDetailView`: Product details + similar items
- `show_cart()`: Cart with complementary recommendations
- `checkout()`: Process orders + update ML data
- `orders()`: Order history + reorder recommendations

---

### **4. Data Flow for Recommendations**

```
User Action (View Product)
        ↓
    Log Interaction (UserInteraction model)
        ↓
Update Product Popularity
        ↓
User Adds to Cart
        ↓
    Log Interaction (add_to_cart)
        ↓
User Checks Out
        ↓
Create Order (OrderPlaced model)
        ↓
Update ChefProduct statistics
        ↓
Background: Recommendation Engine Uses This Data
        ↓
Next Visit: Personalized Recommendations
        ↓
    Log Recommendations (RecommendationLog)
        ↓
User Clicks Recommendation
        ↓
Update RecommendationLog (clicked=True)
        ↓
Measure Recommendation Accuracy
```

---

## 🔄 Request-Response Cycle

### **Example: Homepage with Recommendations**

```
1. User visits homepage
   ↓
2. HomeView.get() triggered
   ↓
3. Check authentication
   │
   ├─ Authenticated:
   │  ├─ Get Customer profile
   │  ├─ Call HybridRecommender(user)
   │  ├─ Get hybrid recommendations (12 items)
   │  ├─ Get profile-based recommendations (6 items)
   │  └─ Get order history recommendations (6 items)
   │
   └─ Anonymous:
      └─ Get popular items (12 items)
   ↓
4. Get category-wise products (browsing)
   ↓
5. Prepare context dictionary
   ↓
6. Render 'home.html' with context
   ↓
7. Display to user
   ↓
8. User interactions logged for next time
```

---

## 📊 Database Schema

### **Entity-Relationship Diagram**

```
┌──────────────┐
│     User     │ (Django built-in)
│──────────────│
│ id           │
│ username     │
│ email        │
│ password     │
└──────┬───────┘
       │ 1:1
       ↓
┌──────────────────────┐
│      Customer        │
│──────────────────────│
│ id                   │
│ user_id (FK)         │
│ name                 │
│ category_preference  │ → For profile-based recommendations
│ cuisine_preference   │ → For profile-based recommendations
│ mobile               │
│ created_at           │
└──────────────────────┘

┌──────────────────────┐
│      Product         │ (Base food items)
│──────────────────────│
│ id                   │
│ title                │
│ description          │
│ meal_type            │ → Content-based feature
│ category             │ → Content-based feature
│ cuisine              │ → Content-based feature
│ product_image        │
│ popularity_score     │ → Popularity-based ranking
│ created_at           │
└──────┬───────────────┘
       │ 1:N
       ↓
┌──────────────────────┐
│    ChefProduct       │ (Chef variants)
│──────────────────────│
│ id                   │
│ titleid (FK)         │
│ chef_name            │
│ selling_price        │
│ discounted_price     │ → Content-based feature
│ preparation_time     │
│ description          │
│ ratings              │ → Content-based feature
│ category             │
│ meal_type            │
│ product_image        │
│ total_orders         │ → Popularity metric
│ created_at           │
└──────┬───────────────┘
       │
       ├───────────┐
       │           │
       ↓           ↓
┌─────────────┐  ┌──────────────────┐
│    Cart     │  │  OrderPlaced     │ ← Critical for Collaborative Filtering
│─────────────│  │──────────────────│
│ id          │  │ id               │
│ user_id (FK)│  │ user_id (FK)     │
│ customer    │  │ customer_id (FK) │
│ product (FK)│  │ product_id (FK)  │
│ quantity    │  │ quantity         │
│ added_at    │  │ ordered_date     │
└─────────────┘  └──────────────────┘

┌────────────────────────┐
│   UserInteraction      │ ← For behavior tracking & ML improvement
│────────────────────────│
│ id                     │
│ user_id (FK)           │
│ product_id (FK)        │
│ chef_product_id (FK)   │
│ interaction_type       │ (view/click/add_to_cart/purchase)
│ timestamp              │
│ session_id             │
└────────────────────────┘

┌────────────────────────┐
│  RecommendationLog     │ ← For A/B testing & accuracy measurement
│────────────────────────│
│ id                     │
│ user_id (FK)           │
│ recommended_products   │ (JSON: list of product IDs)
│ recommendation_type    │ (collaborative/content/hybrid/popularity)
│ shown_at               │
│ clicked                │ (boolean)
│ clicked_product_id     │
└────────────────────────┘
```

---

## 🔐 Security Architecture

### **Authentication & Authorization**

```
┌─────────────────────────────────────────┐
│        Django Authentication            │
│  - Session-based authentication         │
│  - Password hashing (PBKDF2)            │
│  - CSRF protection                      │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│         Middleware Stack                │
│  1. SecurityMiddleware                  │
│  2. SessionMiddleware                   │
│  3. CsrfViewMiddleware                  │
│  4. AuthenticationMiddleware            │
└─────────────────────────────────────────┘
         ↓
┌─────────────────────────────────────────┐
│          View Decorators                │
│  - @login_required                      │
│  - Permission checks                    │
└─────────────────────────────────────────┘
```

**Security Features:**
- ✅ Password hashing with PBKDF2
- ✅ CSRF token validation
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection (template escaping)
- ✅ Session management
- ✅ Secure cookie settings

---

## ⚡ Performance Optimization

### **Database Level**

1. **Indexes**
   ```python
   class UserInteraction:
       class Meta:
           indexes = [
               models.Index(fields=['user', 'interaction_type']),
               models.Index(fields=['product', 'interaction_type']),
           ]
   ```

2. **Query Optimization**
   ```python
   # Avoid N+1 queries
   products = ChefProduct.objects.select_related('titleid').all()

   # Aggregate at database level
   popular = ChefProduct.objects.annotate(
       order_count=Count('orderplaced')
   )
   ```

### **Algorithm Level**

1. **Limit Computations**
   - Only calculate similarity for top K users (K=5)
   - Set similarity threshold (>0.3) to filter weak matches
   - Early stopping when enough recommendations found

2. **Caching Strategy**
   ```python
   # Cache recommendations for active users
   # TTL: 1 hour

   # Cache popular items
   # TTL: 24 hours

   # Cache user similarity matrices
   # TTL: 6 hours
   ```

---

## 📈 Scalability Considerations

### **Current System (Development)**
- **Users**: 1K - 10K
- **Products**: 100 - 1000
- **Orders/day**: 100 - 500
- **Database**: SQLite
- **Server**: Single Django instance

### **Scaled System (Production)**

```
┌─────────────┐
│Load Balancer│
└──────┬──────┘
       │
   ┌───┴────┐
   │        │
┌──▼──┐  ┌─▼───┐
│Web  │  │Web  │  (Multiple Django instances)
│App 1│  │App 2│
└──┬──┘  └─┬───┘
   │        │
   └────┬───┘
        ↓
  ┌──────────────┐
  │Redis Cache   │ (Session + Recommendations)
  └──────────────┘
        ↓
  ┌──────────────┐
  │PostgreSQL DB │ (Primary)
  └──────┬───────┘
         │
    ┌────┴─────┐
    │          │
┌───▼──┐  ┌───▼──┐
│Read  │  │Read  │ (Read Replicas)
│DB 1  │  │DB 2  │
└──────┘  └──────┘
```

**Scaling Strategies:**

1. **Horizontal Scaling**: Multiple app servers behind load balancer
2. **Database Replication**: Read replicas for recommendation queries
3. **Caching**: Redis for frequently accessed data
4. **Async Processing**: Celery for expensive ML computations
5. **CDN**: Static and media files served from CDN
6. **Microservices**: Separate recommendation service

---

## 🧪 Testing Architecture

### **Testing Pyramid**

```
         ┌──────────────┐
         │  E2E Tests   │ (Few)
         └──────────────┘
       ┌──────────────────┐
       │ Integration Tests│ (Some)
       └──────────────────┘
    ┌──────────────────────────┐
    │     Unit Tests           │ (Many)
    └──────────────────────────┘
```

**Test Coverage:**
1. **Unit Tests**: Individual functions (recommendation algorithms)
2. **Integration Tests**: Views + models + ML engine
3. **E2E Tests**: Full user flows (browse → cart → checkout)

---

## 🔄 Deployment Architecture

### **Development → Production Flow**

```
Developer
    ↓
Git Commit → GitHub
    ↓
CI/CD Pipeline (GitHub Actions)
    ↓
    ├─ Run Tests
    ├─ Code Quality Checks
    ├─ Build Docker Image
    └─ Deploy to Server
        ↓
    Staging Environment
        ↓
    Manual Approval
        ↓
    Production Environment
```

---

## 📊 Monitoring & Logging

### **Monitoring Stack**

```
Application Logs
    ↓
┌────────────────┐
│  Log Collector │ (Fluentd/Logstash)
└────────┬───────┘
         ↓
┌────────────────┐
│  Log Storage   │ (Elasticsearch)
└────────┬───────┘
         ↓
┌────────────────┐
│  Visualization │ (Kibana)
└────────────────┘
```

**Metrics to Monitor:**
- Request latency
- Recommendation generation time
- Database query performance
- Error rates
- Recommendation CTR
- User engagement metrics

---

## 🎯 Interview Focus Areas

**When discussing architecture, emphasize:**

1. **Separation of Concerns**: Models, Views, Templates, ML Engine
2. **Scalability Thinking**: How current design supports future growth
3. **Database Design**: Normalized schema, proper relationships, ML support tables
4. **Security**: Built-in Django protections
5. **Performance**: Indexes, query optimization, caching strategy
6. **Modularity**: Recommendation engine as separate module
7. **Data Flow**: How user interactions feed ML improvements

---

**Document Version**: 1.0
**Last Updated**: May 2022
**Author**: KYP Krishna Reddy
