import sqlite3

DATABASE = "meals.db"


def add_recipe(
    cursor,
    name,
    category,
    image,
    instructions,
    ingredients
):
    # Check if recipe already exists
    cursor.execute(
        "SELECT id FROM meals WHERE name = ?",
        (name,)
    )

    existing = cursor.fetchone()

    if existing:
        print(f"Already exists: {name}")
        return

    # Add meal
    cursor.execute("""
        INSERT INTO meals
        (name, category, image, instructions)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        category,
        image,
        instructions
    ))

    meal_id = cursor.lastrowid

    # Add ingredients
    for ingredient_name, quantity, ingredient_image in ingredients:

        cursor.execute("""
            INSERT INTO ingredients
            (meal_id, name, quantity, image)
            VALUES (?, ?, ?, ?)
        """, (
            meal_id,
            ingredient_name,
            quantity,
            ingredient_image
        ))

    print(f"Added: {name}")


conn = sqlite3.connect(DATABASE)
cursor = conn.cursor()


# =========================================================
# 1. RAJMA CHAWAL
# =========================================================

add_recipe(
    cursor,

    "Rajma Chawal",

    "North Indian",

    "images/meals/rajma-chawal.jpg",

    """1. Soak rajma overnight in water.

2. Pressure cook the rajma until soft.

3. Heat oil and prepare the onion and tomato masala.

4. Add ginger, garlic and spices.

5. Add the cooked rajma and simmer for 10 minutes.

6. Serve hot with steamed rice.""",

    [
        ("Rajma", "1 cup", "images/ingredients/rajma.jpg"),
        ("Rice", "1 cup", "images/ingredients/rice.jpg"),
        ("Onion", "1", "images/ingredients/onion.jpg"),
        ("Tomato", "2", "images/ingredients/tomato.jpg"),
        ("Ginger Garlic", "1 tbsp", "images/ingredients/ginger-garlic.jpg"),
        ("Garam Masala", "1 tsp", "images/ingredients/garam-masala.jpg")
    ]
)


# =========================================================
# 2. CHOLE BHATURE
# =========================================================

add_recipe(
    cursor,

    "Chole Bhature",

    "North Indian",

    "images/meals/chole-bhature.jpg",

    """1. Soak chickpeas overnight.

2. Pressure cook the chickpeas until soft.

3. Prepare onion and tomato masala with spices.

4. Add the cooked chickpeas and simmer well.

5. Prepare a soft dough for bhature.

6. Roll the dough into round shapes.

7. Deep fry the bhature until golden and fluffy.

8. Serve hot chole with bhature.""",

    [
        ("Chickpeas", "1 cup", "images/ingredients/chickpeas.jpg"),
        ("Flour", "2 cups", "images/ingredients/flour.jpg"),
        ("Onion", "1", "images/ingredients/onion.jpg"),
        ("Tomato", "2", "images/ingredients/tomato.jpg"),
        ("Yogurt", "2 tbsp", "images/ingredients/yogurt.jpg"),
        ("Spices", "1 tsp", "images/ingredients/spices.jpg")
    ]
)


# =========================================================
# 3. MAGGI
# =========================================================

add_recipe(
    cursor,

    "Maggi",

    "Street Food",

    "images/meals/maggi.jpg",

    """1. Boil water in a pan.

2. Add the Maggi noodles.

3. Add the tastemaker and mix well.

4. Add chopped vegetables if desired.

5. Cook for 2 to 3 minutes.

6. Serve hot.""",

    [
        ("Maggi Noodles", "1 packet", "images/ingredients/maggi.jpg"),
        ("Water", "1.5 cups", "images/ingredients/water.jpg"),
        ("Onion", "1/2", "images/ingredients/onion.jpg"),
        ("Capsicum", "1/2", "images/ingredients/capsicum.jpg"),
        ("Maggi Masala", "1 packet", "images/ingredients/maggi-masala.jpg")
    ]
)


# =========================================================
# 4. TEA
# =========================================================

add_recipe(
    cursor,

    "Tea",

    "Beverages",

    "images/meals/tea.jpg",

    """1. Boil water in a saucepan.

2. Add tea leaves and ginger.

3. Add milk and sugar.

4. Let the tea simmer for a few minutes.

5. Strain the tea into a cup.

6. Serve hot.""",

    [
        ("Water", "1 cup", "images/ingredients/water.jpg"),
        ("Milk", "1 cup", "images/ingredients/milk.jpg"),
        ("Tea Leaves", "1 tsp", "images/ingredients/tea-leaves.jpg"),
        ("Sugar", "2 tsp", "images/ingredients/sugar.jpg"),
        ("Ginger", "Small piece", "images/ingredients/ginger.jpg")
    ]
)


# =========================================================
# 5. RASGULLA
# =========================================================

add_recipe(
    cursor,

    "Rasgulla",

    "Sweets",

    "images/meals/rasgulla.jpg",

    """1. Prepare fresh chenna using milk.

2. Knead the chenna until smooth.

3. Make small round balls.

4. Prepare sugar syrup with water.

5. Add the chenna balls to the boiling syrup.

6. Cook until the rasgullas become soft and spongy.

7. Serve chilled or at room temperature.""",

    [
        ("Milk", "1 litre", "images/ingredients/milk.jpg"),
        ("Lemon Juice", "2 tbsp", "images/ingredients/lemon.jpg"),
        ("Sugar", "1 cup", "images/ingredients/sugar.jpg"),
        ("Water", "4 cups", "images/ingredients/water.jpg")
    ]
)


# =========================================================
# 6. KAJU KATLI
# =========================================================

add_recipe(
    cursor,

    "Kaju Katli",

    "Sweets",

    "images/meals/kaju-katli.jpg",

    """1. Grind cashews into a fine powder.

2. Prepare sugar syrup in a pan.

3. Add cashew powder to the syrup.

4. Cook on low heat while continuously mixing.

5. Knead the mixture into a smooth dough.

6. Roll it into a thin sheet.

7. Cut into diamond-shaped pieces.

8. Serve once cooled.""",

    [
        ("Cashews", "2 cups", "images/ingredients/cashews.jpg"),
        ("Sugar", "1 cup", "images/ingredients/sugar.jpg"),
        ("Water", "1/2 cup", "images/ingredients/water.jpg"),
        ("Cardamom", "1/2 tsp", "images/ingredients/cardamom.jpg")
    ]
)


# =========================================================
# 7. JALEBI
# =========================================================

add_recipe(
    cursor,

    "Jalebi",

    "Sweets",

    "images/meals/jalebi.jpg",

    """1. Prepare a smooth jalebi batter.

2. Let the batter rest for a few hours.

3. Prepare sugar syrup in a pan.

4. Heat oil or ghee for frying.

5. Pour the batter into spiral shapes.

6. Fry until golden and crispy.

7. Dip the jalebi into warm sugar syrup.

8. Serve hot.""",

    [
        ("All Purpose Flour", "1 cup", "images/ingredients/flour.jpg"),
        ("Yogurt", "2 tbsp", "images/ingredients/yogurt.jpg"),
        ("Sugar", "1 cup", "images/ingredients/sugar.jpg"),
        ("Water", "1 cup", "images/ingredients/water.jpg"),
        ("Oil", "For frying", "images/ingredients/oil.jpg")
    ]
)


# =========================================================
# 8. KHEER
# =========================================================

add_recipe(
    cursor,

    "Kheer",

    "Sweets",

    "images/meals/kheer.jpg",

    """1. Wash and soak the rice.

2. Boil milk in a heavy-bottomed pan.

3. Add rice to the milk.

4. Cook on low heat until the rice becomes soft.

5. Add sugar and cardamom.

6. Add chopped nuts.

7. Cook for a few more minutes.

8. Serve warm or chilled.""",

    [
        ("Rice", "1/4 cup", "images/ingredients/rice.jpg"),
        ("Milk", "1 litre", "images/ingredients/milk.jpg"),
        ("Sugar", "1/2 cup", "images/ingredients/sugar.jpg"),
        ("Cardamom", "1/2 tsp", "images/ingredients/cardamom.jpg"),
        ("Cashews", "2 tbsp", "images/ingredients/cashews.jpg"),
        ("Almonds", "2 tbsp", "images/ingredients/almonds.jpg")
    ]
)


# =========================================================
# 9. GULAB JAMUN
# =========================================================

add_recipe(
    cursor,

    "Gulab Jamun",

    "Sweets",

    "images/meals/gulab-jamun.jpg",

    """1. Prepare a soft dough using khoya and flour.

2. Make small smooth balls.

3. Prepare sugar syrup with cardamom.

4. Heat oil or ghee.

5. Fry the balls on low heat until golden brown.

6. Soak them in warm sugar syrup.

7. Let them absorb the syrup.

8. Serve warm.""",

    [
        ("Khoya", "1 cup", "images/ingredients/khoya.jpg"),
        ("All Purpose Flour", "2 tbsp", "images/ingredients/flour.jpg"),
        ("Sugar", "1.5 cups", "images/ingredients/sugar.jpg"),
        ("Water", "2 cups", "images/ingredients/water.jpg"),
        ("Cardamom", "1/2 tsp", "images/ingredients/cardamom.jpg"),
        ("Oil", "For frying", "images/ingredients/oil.jpg")
    ]
)


# =========================================================
# 10. POHA
# =========================================================

add_recipe(
    cursor,

    "Poha",

    "Breakfast",

    "images/meals/poha.jpg",

    """1. Wash poha gently and drain the water.

2. Heat oil in a pan.

3. Add mustard seeds and let them crackle.

4. Add onion, green chilli and peanuts.

5. Add turmeric and salt.

6. Add the soaked poha and mix gently.

7. Cook for a few minutes.

8. Add lemon juice and coriander.

9. Serve hot.""",

    [
        ("Poha", "2 cups", "images/ingredients/poha.jpg"),
        ("Onion", "1", "images/ingredients/onion.jpg"),
        ("Peanuts", "2 tbsp", "images/ingredients/peanuts.jpg"),
        ("Green Chilli", "1", "images/ingredients/green-chilli.jpg"),
        ("Turmeric", "1/2 tsp", "images/ingredients/turmeric.jpg"),
        ("Lemon", "1/2", "images/ingredients/lemon.jpg")
    ]
)


# =========================================================
# 11. ALOO PARATHA
# =========================================================

add_recipe(
    cursor,

    "Aloo Paratha",

    "Breakfast",

    "images/meals/aloo-paratha.jpg",

    """1. Boil and mash the potatoes.

2. Add spices, green chilli and coriander.

3. Prepare a soft wheat flour dough.

4. Fill the dough with the potato mixture.

5. Roll into a round paratha.

6. Heat a tawa.

7. Cook the paratha with ghee until golden brown.

8. Serve hot with yogurt or pickle.""",

    [
        ("Potatoes", "3", "images/ingredients/potato.jpg"),
        ("Wheat Flour", "2 cups", "images/ingredients/wheat-flour.jpg"),
        ("Green Chilli", "1", "images/ingredients/green-chilli.jpg"),
        ("Coriander", "2 tbsp", "images/ingredients/coriander.jpg"),
        ("Garam Masala", "1/2 tsp", "images/ingredients/garam-masala.jpg"),
        ("Ghee", "2 tbsp", "images/ingredients/ghee.jpg")
    ]
)


# Save everything
conn.commit()
conn.close()

print("\n===================================")
print(" All recipes added successfully! ")
print("===================================")