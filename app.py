from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


# silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb/db.sqlite'

db = SQLAlchemy(app)

# Models


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    name = db.Column(db.Text, nullable=False)


@app.route('/')
@app.route('/home')
def Home():
    return render_template('index.html')


# Getting Data => Posted
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        new = BlogPost(name=name, age=age)
        print(new)
        db.session.add(new)
        db.session.commit()
        return redirect('/posts')
    else:
        data = BlogPost.query.all()
        return render_template('blogs.html', posts=data)

# Delete Post


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
# Edit Post
def edit(id):
    post = BlogPost.query.get_or_404(id)
    if request.method == 'POST':
        post.name = request.form['name']
        post.age = request.form['age']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
