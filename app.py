from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import date

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/beerdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = SQLAlchemy(app)

### Init DB ###
class Pictures(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)
    date = db.Column(db.Date, nullable=True, default=None)
    link = db.Column(db.Text, nullable=False)
    by = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<Pictures "{}">'.format(self.name)

### pages url ###
@app.route('/', defaults={'page_num': 1})
@app.route('/page/<int:page_num>')
def home(page_num):
    pics = Pictures.query.filter_by(active=1).order_by(Pictures.date.desc()).paginate(max_per_page=1, page=page_num)
    return render_template('pages/home.html', pics=pics)

@app.route('/new')
def new():
    return render_template('pages/newpics.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.errorhandler(404)
def page_not_found(error):
    flash(u'La page que vous demandez n\'existe pas.', 'danger')
    return redirect("/", code=302)

### CRUD ###
@app.route('/post/create', methods=['post'])
def create():
    if request.form['name'] and request.form['link'] and request.form['by']:
        picName = request.form['name']
        picLink = request.form['link']
        picBy = request.form['by']
        newPic = Pictures(name=picName,link=picLink,by=picBy)
        db.session.add(newPic)
        db.session.commit()
        flash(u'Votre proposition a bien été transmise.', 'success')
        return redirect("/", code=302)
    else:
        flash(u'Vous n\'avez pas rempli le formulaire correctement.', 'danger')
        return redirect("/", code=302)

@app.route('/post/update')
def update():
    if request.form['name'] and request.form['link'] and request.form['by'] and request.form['date' and request.form['valid'] and request.form['active']]:
        picName = request.form['name']
        picLink = request.form['link']
        picBy = request.form['by']
        newPic = Pictures(name=picName,link=picLink,by=picBy)
        db.session.add(newPic)
        db.session.commit()
        flash(u'La photo a bien été mise à jour.', 'success')
        return redirect("/", code=302)
    else:
        flash(u'Il y a eu une erreur lors de la mise a jour de la photo.', 'danger')
        return redirect("/", code=302)

@app.route('/post/delete/<int:id>')
def delete(id):
    picToDelete = Pictures.query.get(id)
    db.session.delete(picToDelete)
    db.session.commit()
    flash(u'La photo a bien été supprimé.', 'success')
    return redirect("/", code=302)
    

@app.route('/get/all')
def getAll():
    allPics = Pictures.query.all()
    print(allPics)
    return redirect("/", code=302)

@app.route('/get/<int:id>')
def get(id):
    picture = Pictures.query.get(id)
    print(picture)
    return redirect("/", code=302)

if  __name__ == '__main__':
    db.create_all()
    app.run(debug=True)