from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

import os

from database import (
    get_db,
    init_db
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)


# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

app.secret_key = "mealnest-secret-key"


# =========================================
# IMAGE UPLOAD SETTINGS
# =========================================

UPLOAD_FOLDER = "static/images/meals"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)


# =========================================
# INITIALIZE DATABASE
# =========================================

init_db()


# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    conn = get_db()

    # -----------------------------
    # Total meals
    # -----------------------------

    total_meals = conn.execute("""
        SELECT COUNT(*)
        FROM meals
    """).fetchone()[0]


    # -----------------------------
    # Total ingredients
    # -----------------------------

    total_ingredients = conn.execute("""
        SELECT COUNT(*)
        FROM ingredients
    """).fetchone()[0]


    # -----------------------------
    # Total images
    # -----------------------------

    total_images = conn.execute("""
        SELECT COUNT(*)
        FROM meals
        WHERE image IS NOT NULL
        AND image != ''
    """).fetchone()[0]


    # -----------------------------
    # Latest meals
    # -----------------------------

    meals = conn.execute("""
        SELECT *
        FROM meals
        ORDER BY id DESC
        LIMIT 6
    """).fetchall()


    # -----------------------------
    # Categories
    # -----------------------------

    categories = conn.execute("""
        SELECT DISTINCT category
        FROM meals
        WHERE category IS NOT NULL
        AND category != ''
        ORDER BY category
    """).fetchall()


    conn.close()


    return render_template(
        "index.html",
        total_meals=total_meals,
        total_ingredients=total_ingredients,
        total_images=total_images,
        meals=meals,
        categories=categories
    )


# =========================================
# EXPLORE
# =========================================

@app.route("/explore")
def explore():

    conn = get_db()

    meals = conn.execute("""
        SELECT *
        FROM meals
        ORDER BY id DESC
    """).fetchall()

    conn.close()


    return render_template(
        "explore.html",
        meals=meals
    )


# =========================================
# CATEGORIES
# =========================================

@app.route("/categories")
def categories():

    conn = get_db()

    categories = conn.execute("""
        SELECT
            category,
            COUNT(*) AS meal_count
        FROM meals
        GROUP BY category
        ORDER BY category
    """).fetchall()

    conn.close()


    return render_template(
        "categories.html",
        categories=categories
    )


# =========================================
# CATEGORY MEALS
# =========================================

@app.route("/category/<category>")
def category(category):

    conn = get_db()

    meals = conn.execute("""
        SELECT *
        FROM meals
        WHERE category = ?
        ORDER BY id DESC
    """, (category,)).fetchall()

    conn.close()


    return render_template(
        "category.html",
        category=category,
        meals=meals
    )


# =========================================
# SEARCH
# =========================================

@app.route("/search")
def search():

    query = request.args.get(
        "q",
        ""
    ).strip()


    conn = get_db()


    if query:

        meals = conn.execute("""
            SELECT *
            FROM meals
            WHERE
                name LIKE ?
                OR category LIKE ?
            ORDER BY id DESC
        """, (
            f"%{query}%",
            f"%{query}%"
        )).fetchall()

    else:

        meals = []


    conn.close()


    return render_template(
        "search.html",
        meals=meals,
        query=query
    )


# =========================================
# RECIPE DETAILS
# =========================================

@app.route("/recipe/<int:meal_id>")
def recipe(meal_id):

    conn = get_db()


    # -----------------------------
    # Get meal
    # -----------------------------

    meal = conn.execute("""
        SELECT *
        FROM meals
        WHERE id = ?
    """, (meal_id,)).fetchone()


    # -----------------------------
    # Meal not found
    # -----------------------------

    if meal is None:

        conn.close()

        flash(
            "Recipe not found."
        )

        return redirect(
            url_for("explore")
        )


    # -----------------------------
    # Get ingredients
    # -----------------------------

    ingredients = conn.execute("""
        SELECT *
        FROM ingredients
        WHERE meal_id = ?
        ORDER BY id
    """, (meal_id,)).fetchall()


    conn.close()


    return render_template(
        "recipe.html",
        meal=meal,
        ingredients=ingredients
    )


# =========================================
# FAVORITES
# =========================================

@app.route("/favorites")
def favorites():

    conn = get_db()


    meals = conn.execute("""
        SELECT meals.*
        FROM meals
        INNER JOIN favorites
        ON meals.id = favorites.meal_id
        ORDER BY favorites.id DESC
    """).fetchall()


    conn.close()


    return render_template(
        "favorites.html",
        meals=meals
    )


# =========================================
# ADD FAVORITE
# =========================================

@app.route(
    "/favorite/<int:meal_id>",
    methods=["POST", "GET"]
)
def add_favorite(meal_id):

    conn = get_db()


    # Check if already favorite

    existing = conn.execute("""
        SELECT *
        FROM favorites
        WHERE meal_id = ?
    """, (meal_id,)).fetchone()


    if existing is None:

        conn.execute("""
            INSERT INTO favorites
            (meal_id)
            VALUES (?)
        """, (meal_id,))

        conn.commit()

        flash(
            "Recipe added to favorites ❤️"
        )

    else:

        flash(
            "Recipe is already in favorites."
        )


    conn.close()


    return redirect(
        request.referrer
        or url_for("explore")
    )

# =========================================
# REMOVE FAVORITE
# =========================================

@app.route(
    "/remove_favorite/<int:meal_id>",
    methods=["POST", "GET"]
)
def remove_favorite(meal_id):

    conn = get_db()

    conn.execute("""
        DELETE FROM favorites
        WHERE meal_id = ?
    """, (meal_id,))

    conn.commit()

    conn.close()

    flash(
        "Recipe removed from favorites."
    )

    return redirect(
        url_for("favorites")
    )

# =========================================
# ADD NEW RECIPE
# =========================================

@app.route(
    "/add_recipe",
    methods=["GET", "POST"]
)
def add_recipe():

    # =====================================
    # SHOW ADD RECIPE PAGE
    # =====================================

    if request.method == "GET":

        return render_template(
            "add_recipe.html"
        )


    # =====================================
    # GET FORM DATA
    # =====================================

    name = request.form.get(
        "name",
        ""
    ).strip()


    category = request.form.get(
        "category",
        ""
    ).strip()


    instructions = request.form.get(
        "instructions",
        ""
    ).strip()


    # =====================================
    # GET INGREDIENTS
    # =====================================

    ingredient_names = request.form.getlist(
        "ingredient_name"
    )


    ingredient_quantities = request.form.getlist(
        "ingredient_quantity"
    )


    # =====================================
    # VALIDATION
    # =====================================

    if not name:

        flash(
            "Please enter a recipe name."
        )

        return redirect(
            url_for("add_recipe")
        )


    if not category:

        flash(
            "Please enter a category."
        )

        return redirect(
            url_for("add_recipe")
        )


    if not instructions:

        flash(
            "Please enter recipe instructions."
        )

        return redirect(
            url_for("add_recipe")
        )


    # =====================================
    # IMAGE UPLOAD
    # =====================================

    image_file = request.files.get(
        "image"
    )


    image_path = ""


    if image_file and image_file.filename:

        # Get safe filename

        filename = os.path.basename(
            image_file.filename
        )


        # Save image

        image_file.save(
            os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )
        )


        # Path stored in database

        image_path = (
            "images/meals/"
            + filename
        )


    # =====================================
    # INSERT MEAL
    # =====================================

    conn = get_db()

    cursor = conn.cursor()


    cursor.execute("""
        INSERT INTO meals
        (
            name,
            category,
            image,
            instructions
        )
        VALUES (?, ?, ?, ?)
    """, (
        name,
        category,
        image_path,
        instructions
    ))


    meal_id = cursor.lastrowid


    # =====================================
    # INSERT INGREDIENTS
    # =====================================

    for i in range(
        len(ingredient_names)
    ):

        ingredient_name = (
            ingredient_names[i].strip()
        )


        # Get quantity

        if i < len(
            ingredient_quantities
        ):

            quantity = (
                ingredient_quantities[i].strip()
            )

        else:

            quantity = ""


        # Only save non-empty ingredients

        if ingredient_name:

            cursor.execute("""
                INSERT INTO ingredients
                (
                    meal_id,
                    name,
                    quantity,
                    image
                )
                VALUES (?, ?, ?, ?)
            """, (
                meal_id,
                ingredient_name,
                quantity,
                ""
            ))


    # =====================================
    # SAVE DATABASE
    # =====================================

    conn.commit()

    conn.close()


    flash(
        "Recipe added successfully! 🍴"
    )


    # =====================================
    # OPEN NEW RECIPE
    # =====================================

    return redirect(
        url_for(
            "recipe",
            meal_id=meal_id
        )
    )


# =========================================
# CONTACT
# =========================================

@app.route(
    "/contact",
    methods=["GET", "POST"]
)
def contact():

    # -----------------------------
    # Form submitted
    # -----------------------------

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()


        email = request.form.get(
            "email",
            ""
        ).strip()


        subject = request.form.get(
            "subject",
            ""
        ).strip()


        message = request.form.get(
            "message",
            ""
        ).strip()


        # -----------------------------
        # Validation
        # -----------------------------

        if not name or not email or not message:

            flash(
                "Please fill in all required fields."
            )

            return redirect(
                url_for("contact")
            )


        # -----------------------------
        # Save message
        # -----------------------------

        conn = get_db()


        conn.execute("""
            INSERT INTO contacts
            (
                name,
                email,
                subject,
                message
            )
            VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            subject,
            message
        ))


        conn.commit()

        conn.close()


        flash(
            "Thank you! Your message has been sent. ❤️"
        )


        return redirect(
            url_for("contact")
        )


    # -----------------------------
    # Show contact page
    # -----------------------------

    return render_template(
        "contact.html"
    )


# =========================================
# REGISTER
# =========================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # -----------------------------
    # Show register page
    # -----------------------------

    if request.method == "GET":

        return render_template(
            "register.html"
        )


    # -----------------------------
    # Get form data
    # -----------------------------

    name = request.form.get(
        "name",
        ""
    ).strip()


    email = request.form.get(
        "email",
        ""
    ).strip()


    password = request.form.get(
        "password",
        ""
    )


    # -----------------------------
    # Validation
    # -----------------------------

    if not name or not email or not password:

        flash(
            "Please fill in all fields."
        )

        return redirect(
            url_for("register")
        )


    if len(password) < 6:

        flash(
            "Password must be at least 6 characters."
        )

        return redirect(
            url_for("register")
        )


    # -----------------------------
    # Hash password
    # -----------------------------

    hashed_password = (
        generate_password_hash(password)
    )


    conn = get_db()


    # -----------------------------
    # Check existing email
    # -----------------------------

    existing_user = conn.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,)).fetchone()


    if existing_user:

        conn.close()

        flash(
            "Email is already registered."
        )

        return redirect(
            url_for("register")
        )


    # -----------------------------
    # Create user
    # -----------------------------

    conn.execute("""
        INSERT INTO users
        (
            name,
            email,
            password
        )
        VALUES (?, ?, ?)
    """, (
        name,
        email,
        hashed_password
    ))


    conn.commit()

    conn.close()


    flash(
        "Registration successful! Please login."
    )


    return redirect(
        url_for("login")
    )


# =========================================
# LOGIN
# =========================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # -----------------------------
    # Show login page
    # -----------------------------

    if request.method == "GET":

        return render_template(
            "login.html"
        )


    # -----------------------------
    # Get form data
    # -----------------------------

    email = request.form.get(
        "email",
        ""
    ).strip()


    password = request.form.get(
        "password",
        ""
    )


    # -----------------------------
    # Find user
    # -----------------------------

    conn = get_db()


    user = conn.execute("""
        SELECT *
        FROM users
        WHERE email = ?
    """, (email,)).fetchone()


    conn.close()


    # -----------------------------
    # Check login
    # -----------------------------

    if user and check_password_hash(
        user["password"],
        password
    ):

        session["user_id"] = user["id"]

        session["user_name"] = user["name"]

        session["user_email"] = user["email"]


        flash(
            "Login successful! Welcome back."
        )


        return redirect(
            url_for("home")
        )


    # -----------------------------
    # Wrong login
    # -----------------------------

    flash(
        "Invalid email or password."
    )


    return redirect(
        url_for("login")
    )


# =========================================
# LOGOUT
# =========================================

@app.route("/logout")
def logout():

    session.clear()


    flash(
        "You have been logged out."
    )


    return redirect(
        url_for("home")
    )


# =========================================
# RUN APPLICATION
# =========================================

# =====================================================
# EDIT RECIPE
# =====================================================

@app.route("/edit-recipe/<int:meal_id>", methods=["GET", "POST"])
def edit_recipe(meal_id):

    conn = get_db()

    # Get existing recipe
    meal = conn.execute("""
        SELECT *
        FROM meals
        WHERE id = ?
    """, (meal_id,)).fetchone()

    # Recipe not found
    if meal is None:
        conn.close()
        flash("Recipe not found.")
        return redirect(url_for("explore"))

    # Get existing ingredients
    ingredients = conn.execute("""
        SELECT *
        FROM ingredients
        WHERE meal_id = ?
        ORDER BY id
    """, (meal_id,)).fetchall()

    # =============================================
    # UPDATE RECIPE
    # =============================================

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        category_name = request.form.get("category", "").strip()
        instructions = request.form.get("instructions", "").strip()

        if not name or not category_name or not instructions:

            conn.close()

            flash("Please fill all required fields.")

            return redirect(
                url_for("edit_recipe", meal_id=meal_id)
            )

        # =========================================
        # IMAGE
        # =========================================

        image_file = request.files.get("image")

        image_path = meal["image"]

        if image_file and image_file.filename:

            filename = image_file.filename

            image_file.save(
                os.path.join(
                    app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            image_path = "images/meals/" + filename

        # =========================================
        # UPDATE MEAL
        # =========================================

        conn.execute("""
            UPDATE meals
            SET
                name = ?,
                category = ?,
                image = ?,
                instructions = ?
            WHERE id = ?
        """, (
            name,
            category_name,
            image_path,
            instructions,
            meal_id
        ))

        # =========================================
        # UPDATE INGREDIENTS
        # =========================================

        # Delete old ingredients
        conn.execute("""
            DELETE FROM ingredients
            WHERE meal_id = ?
        """, (meal_id,))

        ingredient_names = request.form.getlist(
            "ingredient_name"
        )

        ingredient_quantities = request.form.getlist(
            "quantity"
        )

        ingredient_images = request.form.getlist(
            "ingredient_image"
        )

        for i in range(len(ingredient_names)):

            ingredient_name = ingredient_names[i].strip()

            if not ingredient_name:
                continue

            if i < len(ingredient_quantities):
                quantity = ingredient_quantities[i].strip()
            else:
                quantity = ""

            if i < len(ingredient_images):
                ingredient_image = ingredient_images[i].strip()
            else:
                ingredient_image = ""

            conn.execute("""
                INSERT INTO ingredients
                (
                    meal_id,
                    name,
                    quantity,
                    image
                )
                VALUES (?, ?, ?, ?)
            """, (
                meal_id,
                ingredient_name,
                quantity,
                ingredient_image
            ))

        conn.commit()
        conn.close()

        flash("Recipe updated successfully! ✨")

        return redirect(
            url_for(
                "recipe",
                meal_id=meal_id
            )
        )

    conn.close()

    return render_template(
        "edit_recipe.html",
        meal=meal,
        ingredients=ingredients
    )

if __name__ == "__main__":

    init_db()

    app.run(
        debug=True
    )