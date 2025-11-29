# Machine Learning Approach
## Food Recommendation System

---

## 📖 Overview

This document explains the machine learning approach used in the Food Recommendation System. The implementation focuses on **simplicity, explainability, and effectiveness** - perfect for interview discussions.

---

## 🎯 Business Problem

**Challenge**: Recommend relevant food items to users in a food ordering platform to improve:
- User engagement
- Order conversion rates
- Customer satisfaction
- Average order value

**Solution**: Hybrid recommendation system combining multiple ML techniques

---

## 🤖 Recommendation Algorithms

### 1. Collaborative Filtering (User-Based)

#### **Concept**
"Users who ordered similar items in the past will likely order similar items in the future"

#### **Algorithm Details**

**Step 1: Build User-Item Matrix**
```
         Biryani  Pizza  Pasta  Dosa
User A      1      1      0      0
User B      1      1      1      0
User C      0      0      1      1
User D      1      0      0      1
```

**Step 2: Calculate User Similarity**

Using **Jaccard Similarity Coefficient**:

```
Jaccard(A, B) = |Items_A ∩ Items_B| / |Items_A ∪ Items_B|
```

Example:
- User A ordered: {Biryani, Pizza}
- User B ordered: {Biryani, Pizza, Pasta}
- Intersection: {Biryani, Pizza} = 2 items
- Union: {Biryani, Pizza, Pasta} = 3 items
- Similarity: 2/3 = 0.67 (67%)

**Step 3: Find Similar Users**
- Calculate similarity between target user and all other users
- Rank by similarity score
- Select top 5 most similar users

**Step 4: Generate Recommendations**
- Aggregate items ordered by similar users
- Weight by similarity score
- Filter out items already ordered by target user
- Return top N items

#### **Code Location**
`app/recommendation_engine.py` → `CollaborativeFiltering` class

#### **Advantages**
- ✅ Discovers unexpected item connections
- ✅ No need for item features
- ✅ Improves over time with more data

#### **Limitations**
- ❌ Cold start problem (new users)
- ❌ Requires sufficient order history
- ❌ Scalability concerns with many users

---

### 2. Content-Based Filtering

#### **Concept**
"Recommend items similar to what the user has liked before"

#### **Algorithm Details**

**Step 1: Define Item Features**

Each food item has attributes:
```python
Item Features:
- Cuisine: {Indian, Chinese, Italian, Continental}
- Category: {Vegetarian, Non-Vegetarian}
- Meal Type: {Breakfast, Lunch, Dinner, Snacks}
- Price Range: Numerical value
- Ratings: 1-5 stars
```

**Step 2: Calculate Item Similarity**

**Weighted Feature Matching Algorithm:**

```
Similarity(Item_A, Item_B) =
    0.30 × cuisine_match +
    0.25 × category_match +
    0.20 × meal_type_match +
    0.15 × price_similarity +
    0.10 × rating_similarity
```

**Feature Matching Logic:**

1. **Categorical Features** (Cuisine, Category, Meal Type):
   - Match = 1, No Match = 0

2. **Price Similarity**:
   ```
   price_similarity = max(0, 1 - |price_A - price_B| / avg_price)
   ```

3. **Rating Similarity**:
   ```
   rating_similarity = 1 - |rating_A - rating_B| / 4
   ```

**Example Calculation:**

```
Item A: Chicken Biryani (Indian, Non-Veg, Lunch, ₹200, 5★)
Item B: Mutton Curry (Indian, Non-Veg, Lunch, ₹220, 4★)

Similarity calculation:
- Cuisine match: 1 × 0.30 = 0.30
- Category match: 1 × 0.25 = 0.25
- Meal type match: 1 × 0.20 = 0.20
- Price similarity: 0.9 × 0.15 = 0.135
- Rating similarity: 0.75 × 0.10 = 0.075

Total Similarity: 0.96 (96%)
```

**Step 3: Generate Recommendations**
- Get user's order history (last 5 orders)
- For each historical item, find top 5 similar items
- Aggregate similarity scores
- Remove duplicates and already-ordered items
- Return top N items

#### **Code Location**
`app/recommendation_engine.py` → `ContentBasedFiltering` class

#### **Advantages**
- ✅ No cold start problem for items
- ✅ Explainable recommendations
- ✅ Works for users with limited history
- ✅ Domain knowledge integration

#### **Limitations**
- ❌ Limited serendipity
- ❌ Requires good feature engineering
- ❌ May create "filter bubble"

---

### 3. Hybrid Recommendation System

#### **Concept**
"Combine multiple recommendation strategies to leverage their strengths and mitigate weaknesses"

#### **Algorithm Details**

**Adaptive Weighting Strategy:**

```python
if user_order_count < 3:
    # New users: Cold start handling
    weights = {
        'profile_based': 0.60,
        'popularity_based': 0.40
    }
else:
    # Returning users: Full hybrid
    weights = {
        'collaborative_filtering': 0.40,
        'content_based': 0.30,
        'popularity_based': 0.20,
        'profile_based': 0.10
    }
```

**Scoring Algorithm:**

```python
final_score(item) =
    w1 × collaborative_score(item) +
    w2 × content_based_score(item) +
    w3 × popularity_score(item) +
    w4 × profile_match_score(item)
```

**Normalization:**
- Each component score is normalized to [0, 1] range
- Position-based decay: score = base_score × (N - position) / N
- Items are ranked by final weighted score

#### **Cold Start Handling**

**Problem**: New users have no order history

**Solution Hierarchy**:
1. **Profile-Based**: Use preferences from registration
   - Cuisine preference
   - Veg/Non-veg preference

2. **Popularity-Based**: Recommend trending items
   - Based on total orders
   - Recent activity
   - High ratings

3. **Transition**: As user orders increase
   - Orders 1-2: 80% profile, 20% popularity
   - Orders 3-5: 50% profile, 30% content-based, 20% popularity
   - Orders 6+: Full hybrid with collaborative filtering

#### **Code Location**
`app/recommendation_engine.py` → `HybridRecommender` class

---

## 📊 ML Performance Metrics

### 1. **Click-Through Rate (CTR)**
```
CTR = (Clicked Recommendations / Total Recommendations Shown) × 100
```

**Implementation**: `RecommendationLog` model tracks what was shown and what was clicked

### 2. **Conversion Rate**
```
Conversion = (Purchased Recommended Items / Total Recommendations Shown) × 100
```

**Implementation**: Compare `RecommendationLog` with `OrderPlaced`

### 3. **Coverage**
```
Coverage = (Unique Items Recommended / Total Available Items) × 100
```

**Purpose**: Ensure long-tail items are also recommended

### 4. **Diversity**
```
Diversity = Average dissimilarity between recommended items
```

**Purpose**: Avoid showing only similar items

---

## 🔧 Implementation Decisions

### Why Jaccard Similarity for Collaborative Filtering?

**Decision**: Use Jaccard instead of Cosine or Pearson

**Reasoning**:
1. ✅ **Binary data**: Users either ordered or didn't (no ratings)
2. ✅ **Simplicity**: Easy to explain in interviews
3. ✅ **Efficiency**: Fast to calculate
4. ✅ **Interpretability**: Similarity score has clear meaning

### Why Weighted Features for Content-Based?

**Decision**: Manual feature weighting instead of TF-IDF or embeddings

**Reasoning**:
1. ✅ **Explainability**: Can justify why items are similar
2. ✅ **Control**: Can adjust weights based on business logic
3. ✅ **Simplicity**: No need for complex vectorization
4. ✅ **Performance**: Fast computation

### Why Hybrid Approach?

**Decision**: Combine multiple methods instead of using one

**Reasoning**:
1. ✅ **Robustness**: Different methods work in different scenarios
2. ✅ **Cold start**: Graceful degradation for new users
3. ✅ **Accuracy**: Leverages strengths of each method
4. ✅ **Industry standard**: Real systems use hybrid approaches

---

## 🎯 Interview Talking Points

### "Why not Deep Learning?"

**Answer**:
> "For a 1-month project with limited data, traditional ML algorithms offer several advantages:
> 1. **Explainability**: I can explain exactly why an item was recommended
> 2. **Data efficiency**: Works well with smaller datasets
> 3. **Training time**: No need for expensive GPU training
> 4. **Interpretability**: Business stakeholders can understand the logic
> 5. **Appropriate complexity**: Solves the problem without over-engineering
>
> However, the system is designed to be extensible - we could add deep learning models later as we collect more data."

### "How do you handle the cold start problem?"

**Answer**:
> "I implemented a multi-level fallback strategy:
> 1. **During registration**: Collect user preferences (cuisine, veg/non-veg)
> 2. **First visit**: Show profile-based recommendations
> 3. **First interactions**: Track views and clicks, use content-based filtering
> 4. **First order**: Start building collaborative filtering data
> 5. **3+ orders**: Full hybrid system kicks in
>
> This ensures every user gets relevant recommendations regardless of their history."

### "How do you measure success?"

**Answer**:
> "I track multiple metrics:
> 1. **Click-through rate**: Are users clicking on recommended items?
> 2. **Conversion rate**: Are they actually ordering recommended items?
> 3. **Diversity**: Are we showing varied items or just popular ones?
> 4. **Coverage**: Are long-tail items getting recommended?
> 5. **User engagement**: Time on platform, items browsed
>
> All these metrics are logged in the `RecommendationLog` and `UserInteraction` models for analysis."

---

## 📈 Future Enhancements

### Short-term (If I had 2 more weeks):
1. **Session-based recommendations**: Recommend based on current browsing session
2. **Time-aware recommendations**: Consider time of day for meal recommendations
3. **Trending items**: Boost recently popular items
4. **Personalized search rankings**: Re-rank search results using ML

### Long-term (Production system):
1. **Matrix Factorization**: SVD for better collaborative filtering
2. **Neural Collaborative Filtering**: Deep learning for user-item interactions
3. **Contextual Bandits**: Online learning with exploration-exploitation
4. **Graph Neural Networks**: Model complex relationships
5. **Transformer models**: Sequential recommendation using attention

---

## 🔍 Code Walkthrough

### Main Entry Point

```python
# app/recommendation_engine.py

def get_recommendations_for_user(user, recommendation_type='hybrid', top_n=12):
    """
    Main function to get recommendations

    Args:
        user: Django User object
        recommendation_type: 'hybrid', 'collaborative', 'content', etc.
        top_n: Number of recommendations

    Returns:
        QuerySet of recommended ChefProduct objects
    """
    if recommendation_type == 'hybrid':
        engine = HybridRecommender(user)
        return engine.get_hybrid_recommendations(top_n)
    # ... other types
```

### Usage in Views

```python
# app/views.py

def home_view(request):
    if request.user.is_authenticated:
        # Get personalized recommendations
        recommendations = get_recommendations_for_user(
            user=request.user,
            recommendation_type='hybrid',
            top_n=12
        )
    else:
        # Anonymous users get popular items
        recommendations = get_recommendations_for_user(
            user=None,
            recommendation_type='popularity',
            top_n=12
        )
```

---

## 📚 References & Learning Resources

1. **Collaborative Filtering**:
   - "Recommender Systems Handbook" - Ricci, Rokach, Shapira

2. **Content-Based Filtering**:
   - "Content-Based Recommender Systems" - Lops, de Gemmis, Semeraro

3. **Hybrid Systems**:
   - "Hybrid Recommender Systems: Survey and Experiments" - Burke (2002)

4. **Implementation**:
   - scikit-learn documentation
   - Django documentation

---

**Document Version**: 1.0
**Last Updated**: May 2022
**Author**: KYP Krishna Reddy
