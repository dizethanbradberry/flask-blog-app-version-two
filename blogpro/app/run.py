from flask import *
import psycopg2
from time import *
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
	return render_template('home.html')
@app.route('/post')
def post():
	return render_template('post.html')
@app.route('/log', methods=['GET', 'POST'])
def log():
	error = None
        if request.method == 'POST':
        	if request.form['username'] != 'admin' or request.form['password'] != '1234':
      			error = 'Invalid Entry. Please try again'
    		else:
 #     			session['logged_in'] = True
			return redirect(url_for('post'))
        return render_template('log.html', error=error)
@app.route('/post',methods=['POST'])
def post_store():
	conn=psycopg2.connect(database='datadb')
	c=conn.cursor()
	c.execute("INSERT INTO blogspot (author,post,day,time) VALUES (%s,%s,%s,%s)",[request.form['name'],request.form['blogpost'],strftime("%d %b %Y ", gmtime()),strftime("%H:%M:%S ", gmtime())])
	conn.commit()
	conn.close()
	return render_template('post.html')
@app.route('/main')
def main():
	conn=psycopg2.connect(database='datadb')
	c=conn.cursor()
	c.execute("SELECT * FROM blogspot ORDER BY id desc")
	posts=[dict(id=i[0],author=i[1],post=i[2],day=i[3],time=i[4],comment=i[5]) for i in c.fetchall()]	
	conn.commit()
	conn.close()
	if not posts:
		return render_template('main.html')
	else:
		return render_template('main.html',posts=posts)
	
		
@app.route('/main',methods=['POST'])
def comment_store():
	p=int(request.form['postid'])
	print p
	conn=psycopg2.connect(database='datadb')
	c=conn.cursor()
	c.execute("SELECT comment FROM blogspot WHERE id=(%s)",[p])
	comments=[c.fetchall()]	
	if comments[0][0][0]==None:
		c.execute("UPDATE blogspot SET comment=(%s) WHERE id=(%s)",['\n@'+request.form['guest']+ '  says: \n'+request.form['comments']+'\n',p])
	else:
		c.execute("UPDATE blogspot SET comment=(%s) WHERE id=(%s)",['\n@'+request.form['guest']+ '  says: \n'+request.form['comments']+'\n'+comments[0][0][0]+'\n',p])
	c.execute("SELECT * FROM blogspot ORDER BY id desc")
	posts=[dict(id=i[0],author=i[1],post=i[2],day=i[3],time=i[4],comment=i[5]) for i in c.fetchall()]	
	conn.commit()
	conn.close()
	if not posts:
		return render_template('main.html')
	else:
		return render_template('main.html',posts=posts)
 	
app.run(debug = True)
