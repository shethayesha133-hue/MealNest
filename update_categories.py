import sqlite3

conn = sqlite3.connect("meals.db")
cursor = conn.cursor()

# Breakfast
cursor.execute("""
    UPDATE meals
    SET category = 'Breakfast'
    WHERE name IN (
        'Poha',
        'Aloo Paratha'
    )
""")

# Lunch
cursor.execute("""
    UPDATE meals
    SET category = 'Lunch'
    WHERE name IN (
        'Rajma Chawal',
        'Chole Bhature',
        'Fresh Vegetable Salad'
    )
""")

# Dinner
cursor.execute("""
    UPDATE meals
    SET category = 'Dinner'
    WHERE name IN (
        'Classic Chicken Burger',
        'Chicken Burger',
        'Cheese Pizza',
        'Creamy Pasta'
    )
""")

# Dessert
cursor.execute("""
    UPDATE meals
    SET category = 'Dessert'
    WHERE name IN (
        'Rasgulla',
        'Kaju Katli',
        'Jalebi',
        'Kheer',
        'Gulab Jamun'
    )
""")

# Snacks
cursor.execute("""
    UPDATE meals
    SET category = 'Snacks'
    WHERE name = 'Maggi'
""")

# Beverages
cursor.execute("""
    UPDATE meals
    SET category = 'Beverages'
    WHERE name = 'Tea'
""")

conn.commit()

# Show updated categories
cursor.execute("""
    SELECT id, name, category
    FROM meals
    ORDER BY category, name
""")

print("\nUpdated Recipes:")
print("------------------------------")

for recipe in cursor.fetchall():
    print(f"{recipe[0]}. {recipe[1]} → {recipe[2]}")

conn.close()

print("\nCategories updated successfully! ✅")