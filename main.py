from flask import Flask, render_template, request, session, redirect
import os
from database import database
import datetime
from auth import auth_bp, login_required
from db_utils import get_connection
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__,template_folder='templates')
context = {'now': datetime.datetime.now().year, 'user': None, 'email': None, 'message': None}
app.secret_key = 'b75dc32acae396bb11a953'
app.register_blueprint(auth_bp)

def send_info():
    context['user'] = session['username']
    alarm_list = check_alarms()
    count_alarms = len(alarm_list)
    context['act_alm'] = count_alarms
    alarm_list_view = []
    if count_alarms>0:
        for message in alarm_list:
            alarm_list_view.append(message['message'])
    context['alarm_list'] = alarm_list_view

@app.route("/")
@login_required
def home():
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            cursor.execute("SELECT types.name, sum(quantity) as 'quantity' FROM products INNER JOIN types ON products.type_id = types.id GROUP BY type_id")
            rows = cursor.fetchall()

        return render_template('dashboard.html', **context, rows=rows)
    else:
        return "Brak pliku bazy danych"



@app.route("/input/", methods=['GET', 'POST'])
@login_required
def input():
    send_info()
    if request.method == 'GET':
        if os.path.isfile('fridge.db'):
            conn = get_connection()
            cursor = conn.cursor()

            with conn:
                cursor.execute("SELECT * FROM types")
                rows = cursor.fetchall()

            if 'product_type' not in context.keys():
                context['product_type'] = rows

            default = 'Drinks'

            return render_template('input.html', **context, default=default)
        else:
            return "Brak pliku bazy danych"

    if request.method == 'POST':
        try:
            quantity = int(request.form['quantity'])
            qbool = True
        except:
            context['message'] = "Quantity must be INT"
            qbool = False

        if(qbool):
            conn = get_connection()
            cursor = conn.cursor()

            with conn:
                # cursor.execute("SELECT * FROM products")
                typeName = request.form['type']
                querry = f"SELECT id FROM types WHERE name=='{typeName}'"
                cursor.execute(querry)
                id = cursor.fetchone()
                id = id['id']

            cursor.execute("INSERT INTO products(name, quantity, type_id) VALUES(?, ?, ?)",
                           (request.form['name'], int(request.form['quantity']), id))
            conn.commit()
            conn.rollback()

        return render_template('input.html', **context)

@app.route("/input_alm/", methods=['GET', 'POST'])
@login_required
def input_alm():
    send_info()
    if request.method == 'GET':
        if os.path.isfile('fridge.db'):
            conn = get_connection()
            cursor = conn.cursor()

            with conn:
                cursor.execute("SELECT * FROM products")
                names = cursor.fetchall()
                cursor.execute("SELECT * FROM alm_type")
                types = cursor.fetchall()

            if 'product_names' not in context.keys():
                context['product_names'] = names

            if 'alarm_types' not in context.keys():
                context['alarm_types'] = types

            return render_template('input_alm.html', **context)
        else:
            return "Brak pliku bazy danych"

    if request.method == 'POST':
        try:
            quantity = int(request.form['quantity'])
            qbool = True
        except:
            context['message'] = "Quantity must be INT"
            qbool = False

        if(qbool):
            conn = get_connection()
            cursor = conn.cursor()

            with conn:
                product_name = request.form['prod_name']
                querry = f"SELECT id FROM products WHERE name=='{product_name}'"
                cursor.execute(querry)
                prod_id = cursor.fetchone()
                prod_id = prod_id['id']

                alm_type = request.form['type']
                querry = f"SELECT id FROM alm_type WHERE name=='{alm_type}'"
                cursor.execute(querry)
                alm_type_id = cursor.fetchone()
                alm_type_id = alm_type_id['id']
                quantity = request.form['quantity']
                message = request.form['message']

            querry = f"INSERT INTO alarms(prod_id, val, type_id, message) VALUES({prod_id}, {quantity}, {alm_type_id}, '{message}')"
            cursor.execute(querry)
            conn.commit()
            conn.rollback()

            querry = f"SELECT id FROM alarms WHERE prod_id=={prod_id} and val=={quantity} and type_id=={alm_type_id} and message=='{message}'"
            cursor.execute(querry)
            alm_id = cursor.fetchone()
            alm_id = alm_id['id']
            user_id = session['user_id']
            querry = f"INSERT INTO users_alm(alm_id, user_id) VALUES({alm_id}, {user_id})"
            cursor.execute(querry)
            conn.commit()
            conn.rollback()


        return render_template('input_alm.html', **context)


@app.route("/output/")
@login_required
def output():
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            # cursor.execute("SELECT * FROM products")
            querry = "SELECT products.id, products.name, products.quantity, types.name as 'type' FROM products INNER JOIN types ON products.type_id = types.id;"
            cursor.execute(querry)
            rows = cursor.fetchall()
            return render_template('output.html', rows=rows, **context)

    return "Brak danych"

@app.route('/delete/<int:id>')
@login_required
def delete(id):
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            querry = f"DELETE FROM products WHERE Id={id}"
            cursor.execute(querry)
            conn.commit()
            conn.rollback()

            return redirect("/output/")
    return "Brak danych"


@app.route("/output_alm/")
@login_required
def output_alm():
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            # cursor.execute("SELECT * FROM products")
            querry = f"""
            SELECT alarms.id, products.name, alm_type.name as eq, alarms.val, alarms.message, users.name as user
            FROM products
            INNER JOIN alarms
            ON products.id = alarms.prod_id
            INNER JOIN alm_type
            ON alarms.type_id = alm_type.id
            INNER JOIN users_alm
            ON alarms.id = users_alm.alm_id
            INNER JOIN users
            ON users_alm.user_id = users.id
            WHERE users.name == '{session['username']}'
            """
            cursor.execute(querry)
            rows = cursor.fetchall()
            return render_template('output_alm.html', rows=rows, **context)

    return "Brak danych"

@app.route('/delete_alm/<int:id>')
@login_required
def delete_alm(id):
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            querry = f"DELETE FROM alarms WHERE Id={id}"
            cursor.execute(querry)
            conn.commit()
            conn.rollback()

            querry = f"DELETE FROM users_alm WHERE user_id={id} AND alm_id={session['user_id']}"
            cursor.execute(querry)
            conn.commit()
            conn.rollback()
            return redirect("/output_alm/")
    return "Brak danych"

@app.route("/summary/")
@login_required
def summery():
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            cursor.execute("SELECT name, sum(quantity) as quantity FROM products GROUP BY name")
            rows = cursor.fetchall()
            return render_template('summary.html', rows=rows, **context)

    return "Brak danych"

def check_alarms():
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            cursor.execute("SELECT name, sum(quantity) as quantity FROM products GROUP BY name")
            products = cursor.fetchall()
            products_dict = {}
            for product in products:
                products_dict[product['name']] = product['quantity']

            cursor.execute(f"""
                            SELECT products.name, alm_type.name as eq, alarms.val, alarms.message, users.id as user
                            FROM products
                            INNER JOIN alarms
                            ON products.id = alarms.prod_id
                            INNER JOIN alm_type
                            ON alarms.type_id = alm_type.id
                            INNER JOIN users_alm
                            ON alarms.id = users_alm.alm_id
                            INNER JOIN users
                            ON users_alm.user_id = users.id
                            WHERE user={session['user_id']}            
                            """)
            alarms = cursor.fetchall()
            active_alarms = []
            for alarm in alarms:
                if alarm['eq']=='LT' and (products_dict[alarm['name']] < alarm['val']):
                    active_alarms.append(alarm)

                if alarm['eq']=='LE' and (products_dict[alarm['name']] <= alarm['val']):
                    active_alarms.append(alarm)

                if alarm['eq']=='GT' and (products_dict[alarm['name']] > alarm['val']):
                    active_alarms.append(alarm)

                if alarm['eq']=='GE' and (products_dict[alarm['name']] >= alarm['val']):
                    active_alarms.append(alarm)

            return active_alarms

    return []

@app.route("/summary_alm/")
@login_required
def summery_alm():
    send_info()
    if os.path.isfile('fridge.db'):

        return render_template('summary_alm.html', alarms=check_alarms(),**context)

    return "Brak danych"

@app.route("/about/")
@login_required
def about():
    send_info()
    return render_template('about.html', **context)


@app.route("/find_recipie/")
@login_required
def findRecipie():
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            cursor.execute("SELECT * FROM recipies")
            rows = cursor.fetchall()
            return render_template('find_recipie.html', rows=rows, **context)

    return "Brak danych"


@app.route('/details/<int:id>')
@login_required
def details(id):
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            cursor.execute(f"SELECT * FROM recipies WHERE Id={id}")
            rows = cursor.fetchone()
            return render_template('details_recipie.html', rows=rows, **context)


@app.route('/delete_rec/<int:id>')
@login_required
def delete_rec(id):
    send_info()
    if os.path.isfile('fridge.db'):
        conn = get_connection()
        cursor = conn.cursor()

        with conn:
            querry = f"DELETE FROM recipies WHERE Id={id}"
            cursor.execute(querry)
            conn.commit()
            conn.rollback()

            return redirect("/find_recipie/")
    return "Brak danych"

def chc_user(user_name, user_email):
    conn = get_connection()
    cursor = conn.cursor()

    with conn:
        cursor.execute(f"SELECT * FROM users WHERE name='{user_name}' or mail='{user_email}'")
        rows = cursor.fetchall()
        if len(rows)>0:
            return False
    return True


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html', **context)

    if request.method == 'POST':
        if (chc_user(request.form['userName'], request.form['email'])):
            if (request.form['inputPassword'] == request.form['repeatPassword']):
                conn = get_connection()
                cursor = conn.cursor()

                repetitions = 5  # spróbuj wygenerować kilka hash
                password = request.form['inputPassword']

                for _ in range(repetitions):
                    hashed_password = generate_password_hash(password)

                cursor.execute('INSERT INTO users(name, mail, password) VALUES(?, ?, ?)',
                               (request.form['userName'], request.form['email'], hashed_password))
                conn.commit()
                conn.rollback()
                return render_template('login.html', **context)
            else:
                context['message']="Passwords are not the same"
        else:
            context['messagePass'] = "User or email is already in database"
        context['user'] = request.form['userName']
        context['email'] = request.form['email']
        return render_template('register.html', **context)


@app.errorhandler(404)
@login_required

def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', **context), 404

if __name__=="__main__":
    if (not os.path.isfile('fridge.db')):
        conn = get_connection()
        database.execute_sql_script('db_init.sql', conn.cursor())
        conn.commit()
        conn.close()

    app.run(debug=True)

