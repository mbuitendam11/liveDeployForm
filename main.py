import os
# Flask imports
from flask import Flask, abort, render_template, redirect, url_for, flash, request, jsonify
from flask_bootstrap import Bootstrap5
# sqlalchemy imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
# form imports
from forms import testForm


app = Flask(__name__)
app.config['SECRET_KEY'] = "os.environ.get('FLASH_KEY')"
Bootstrap5(app)

# Create Database
class Base(DeclarativeBase):
    pass
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sqlite3.db"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

class FormInfo(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    firstName: Mapped[str] = mapped_column(String(250), nullable=False)
    lastName: Mapped[str] = mapped_column(String(250), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False) 

with app.app_context():
    db.create_all()

## Routes ##

# Landing Page
@app.route("/", methods=["GET", "POST"])
def index():
    form = testForm()
    if form.validate_on_submit():
        new_record = FormInfo(
            firstName = form.firstName.data,
            lastName = form.lastName.data,
            text = form.content.data
        )

        db.session.add(new_record)
        db.session.commit()
        return redirect(url_for("this_worked"))
    return render_template("new_record.html", form=form)

# Complete List
@app.route("/congrats", methods=["GET", "POST"])
def this_worked():
    result = db.session.execute(
        db.select(FormInfo)
    )
    all_results = result.scalars().all()
    return render_template("this_worked.html", queries = all_results)

# Update
@app.route("/update/<int:id>", methods=["GET", "POST"])
def patch(id):
    form = testForm()
    item_to_update = FormInfo.query.get_or_404(id)

    if request.method == "POST":
        item_to_update.firstName = request.form['firstName']
        item_to_update.lastName = request.form['lastName']
        item_to_update.text = request.form['content']
        
        try:
            db.session.commit()
            return redirect(url_for("this_worked"))
        except:
            return render_template("update-form.html", form=form, item_to_update=item_to_update, id=id)
    else:
        return render_template("update-form.html", form=form, item_to_update=item_to_update, id=id)



# ARCHIVE

# DELETE


## Debugger ##

if __name__ == "__main__":
    app.run(debug=True)