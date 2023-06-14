from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'diet'
db_path = os.path.join(os.path.dirname(__file__), 'diet.db')
db_uri = 'sqlite:///{}'.format(db_path)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    calorie = db.Column(db.Integer, nullable=False)
    date_of_reception = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"Food('{self.name}', '{self.category}', {self.calorie}, '{self.date_of_reception}')"


@app.route('/')
def home():
    foods = Food.query.all()
    return render_template('home.html', foods=foods)


@app.route('/add_food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        name = request.form['name']
        category = request.form['category']
        calorie = int(request.form['calorie'])

        new_food = Food(name=name, category=category, calorie=calorie)
        db.session.add(new_food)
        db.session.commit()
        flash('საკვები ინფორმაცია წარმატებით დაემატა!', 'success')
        return redirect(url_for('home'))

    return render_template('add_food.html')


@app.route('/edit_food/<int:food_id>', methods=['GET', 'POST'])
def edit_food(food_id):
    food = Food.query.get_or_404(food_id)

    if request.method == 'POST':
        food.name = request.form['name']
        food.category = request.form['category']
        food.calorie = int(request.form['calorie'])
        db.session.commit()
        flash('საკვების ინფორმაცია წარმატებით განახლდა!', 'success')
        return redirect(url_for('home'))

    return render_template('edit_food.html', food=food)


@app.route('/delete_food/<int:food_id>')
def delete_food(food_id):
    food = Food.query.get_or_404(food_id)
    db.session.delete(food)
    db.session.commit()
    flash('საკვების ინფორმაცია წარმატებით ამოიშალა!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
