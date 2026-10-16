import sqlite3


DATABASE = "meals.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():

    conn = get_db()
    cursor = conn.cursor()

    # -------------------------
    # MEALS TABLE
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS meals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            image TEXT NOT NULL,
            instructions TEXT NOT NULL
        )
    """)

    # FAVORITES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
             FOREIGN KEY (meal_id) REFERENCES meals(id)
        )
    """)

    # -------------------------
    # INGREDIENTS TABLE
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ingredients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            meal_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            quantity TEXT,
            image TEXT NOT NULL,
            FOREIGN KEY (meal_id) REFERENCES meals(id)
        )
    """)

   
    # -------------------------
    # CONTACT TABLE
    # -------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    """)

    # -------------------------
    # CHECK DATA
    # -------------------------

    count = cursor.execute(
        "SELECT COUNT(*) FROM meals"
    ).fetchone()[0]

    if count == 0:

        meals = [

            (
                "Chicken Burger",
                "Burger",
                "images/meals/burger.jpg",
                """1. Prepare all the ingredients.
2. Cook the chicken patty.
3. Toast the burger bun.
4. Add lettuce, tomato and cheese.
5. Place the chicken patty inside the bun.
6. Serve hot."""
            ),

            (
                "Cheese Pizza",
                "Pizza",
                "images/meals/pizza.jpg",
                """1. Prepare the pizza dough.
2. Spread pizza sauce over the dough.
3. Add mozzarella cheese.
4. Add tomato and other toppings.
5. Bake until golden brown.
6. Serve hot."""
            ),

            (
                "Creamy Pasta",
                "Pasta",
                "images/meals/pasta.jpg",
                """1. Boil the pasta.
2. Prepare the creamy sauce.
3. Add the cooked pasta.
4. Mix everything together.
5. Add cheese and herbs.
6. Serve warm."""
            ),

            (
                "Fresh Vegetable Salad",
                "Salad",
                "images/meals/salad.jpg",
                """1. Wash all vegetables.
2. Cut vegetables into small pieces.
3. Add vegetables to a bowl.
4. Add salt and dressing.
5. Mix everything well.
6. Serve fresh."""
            ),

            (
                "Gingerbread Waffles",
                "Dessert",
                "images/meals/waffle.jpg",
                """1. Mix flour and other dry ingredients.
2. Add egg and milk.
3. Prepare the waffle batter.
4. Heat the waffle maker.
5. Cook until golden brown.
6. Serve with your favorite topping."""
            ),

            (
                "Chocolate Cake",
                "Dessert",
                "images/meals/cake.jpg",
                """1. Mix flour, sugar and cocoa.
2. Add eggs and milk.
3. Prepare the cake batter.
4. Pour into a baking pan.
5. Bake until fully cooked.
6. Decorate and serve."""
            )
        ]

        cursor.executemany("""
            INSERT INTO meals
            (name, category, image, instructions)
            VALUES (?, ?, ?, ?)
        """, meals)

        # -------------------------
        # INGREDIENTS
        # -------------------------

        ingredients = [

            # Burger
            (1, "Burger Bun", "1", "images/ingredients/bun.jpg"),
            (1, "Chicken Patty", "1", "images/ingredients/chicken.jpg"),
            (1, "Cheese", "2 slices", "images/ingredients/cheese.jpg"),
            (1, "Tomato", "2 slices", "images/ingredients/tomato.jpg"),
            (1, "Lettuce", "2 leaves", "images/ingredients/lettuce.jpg"),

            # Pizza
            (2, "Flour", "200 g", "images/ingredients/flour.jpg"),
            (2, "Cheese", "100 g", "images/ingredients/cheese.jpg"),
            (2, "Tomato", "1", "images/ingredients/tomato.jpg"),

            # Pasta
            (3, "Pasta", "200 g", "images/ingredients/flour.jpg"),
            (3, "Milk", "100 ml", "images/ingredients/milk.jpg"),
            (3, "Cheese", "50 g", "images/ingredients/cheese.jpg"),

            # Salad
            (4, "Tomato", "1", "images/ingredients/tomato.jpg"),
            (4, "Lettuce", "3 leaves", "images/ingredients/lettuce.jpg"),

            # Waffle
            (5, "Flour", "100 g", "images/ingredients/flour.jpg"),
            (5, "Egg", "1", "images/ingredients/egg.jpg"),
            (5, "Milk", "100 ml", "images/ingredients/milk.jpg"),

            # Cake
            (6, "Flour", "200 g", "images/ingredients/flour.jpg"),
            (6, "Egg", "2", "images/ingredients/egg.jpg"),
            (6, "Milk", "100 ml", "images/ingredients/milk.jpg")
        ]

        cursor.executemany("""
            INSERT INTO ingredients
            (meal_id, name, quantity, image)
            VALUES (?, ?, ?, ?)
        """, ingredients)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database created successfully!")

