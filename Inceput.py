import datetime
import hashlib
import json
import sqlite3
import MySQLdb
import MySQLdb.cursors
import re

from flask import Flask, jsonify, render_template, flash, request, redirect, url_for, session, logging, url_for
from flask_mysqldb import MySQL

nr=0


# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 3 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 3 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True




# Creating a Web App
app = Flask(__name__)
mysql = MySQL(app)
# Creating a Blockchain
blockchain = Blockchain()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nss'



def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("https://localhost/phpmyadmin/index.php?route=/database/structure&db=nss/nss.sqlite")
    except sqlite3.Error as e:
        print(e)
    return conn


#!!!Site!!!

@app.route('/', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def upload_log():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['ID'] = account['ID']
            session['username'] = account['username']
            session['cnp'] = account['cnp']
            kok=session['cnp']
            msg = 'Logged in successfully !'
            return redirect(url_for("home", ID=kok))
        else:
            msg = 'Incorrect username / password !'
    return render_template('upload_login.html', msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def upload_reg():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'Password' in request.form and 'verif' in request.form and 'cnp'in request.form:
        username = request.form['username']
        Password = request.form['Password']
        Verif = request.form['verif']
        cnp = request.form['cnp'] #cnp este primele 6 sunt data de nastere dd/mm/yy si dupa random
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curr.execute('SELECT * FROM cnps WHERE cnp = % s', (cnp, ))
        cnps = curr.fetchone()
        currs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        currs.execute('SELECT * FROM cooldown WHERE id = %s', (cnp, ))
        passat = curr.fetchone()
        curs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curs.execute('SELECT * FROM accounts WHERE cnp = % s', (cnp, ))
        checkitycheck = curs.fetchone()
        if account:
            msg = 'Account already exists !'
        elif checkitycheck:
            msg= 'This Personal code is already in use!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not Password:
            msg = 'Please fill out the form !'
        elif Verif != 'a1b2c3':
            msg = 'Wrong verification code!'
        else:
            if cnps:
                cursor.execute('INSERT INTO accounts VALUES (NULL,% s, % s, %s, DEFAULT)', (username, Password,cnp, ))
                currs.execute(
                    'INSERT INTO cooldown VALUES (%s, NULL)', (cnp, ))
                mysql.connection.commit()
                msg = 'You have successfully registered !'
                return redirect('/', code=302)
            else:
                msg= "The Personal Code doesn't exist!"
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('upload_register.html', msg=msg)

@app.route('/<ID>', methods=['POST', 'GET'])
def home(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE cnp = % s', (ID, ))
    account = cursor.fetchone()
    if account:
        return render_template('main_page.html', account=account)

@app.route('/<ID>/wallet', methods=['GET', 'POST'])
def wallet(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE cnp = % s', (ID, ))
    account = cursor.fetchone()
    if account:
        return render_template('wallet.html', account=account)

@app.route('/info')
def info():
    return render_template('info.html')


@app.route('/<ID>/proof-of-work', methods=['GET', 'POST'])
def proof_of_work(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE cnp = % s', (ID, ))
    account = cursor.fetchone()
    curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute('SELECT * FROM cooldown WHERE id = %s', (ID, ))
    passat = curr.fetchone()
    now = datetime.datetime.now()
    data_time = now.strftime("%Y%m%d")
    date_time = int(data_time)

    if request.method == 'POST':
        if passat['data'] != None:
            if account['cnp'] == passat['id'] and passat['data'] != date_time:
                curr.execute(
                    'UPDATE cooldown SET data = %s WHERE id = %s', (None, ID))
                return render_template('work.html', account=account, cool="True")
            else:
                return render_template('work.html', account=account, cool="True")
        else:
            curr.execute(
                'UPDATE cooldown SET data = %s  WHERE id = %s', (date_time, ID))
            cursor.execute(
                'UPDATE accounts SET wallet = %s WHERE cnp = %s', (account['wallet']+0.76, ID))
            return render_template('work.html', account=account, cool="True")
    return render_template('work.html', account=account, cool="True")


@app.route('/<ID>/friends', methods=['GET', 'POST'])
def friends(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE cnp = % s', (ID, ))
    account = cursor.fetchone()
    dar = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    dar.execute(
        'SELECT * FROM frequests JOIN accounts ON accounts.cnp = frequests.id WHERE frequests.send = %s', (account['username'], ))
    dap = dar.fetchall()
    curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute(
        'SELECT friend.friend2, accounts.wallet FROM friend JOIN accounts ON friend.friend2 = accounts.username WHERE friend1 = % s', (ID, ))
    entries = curr.fetchall()
    msg = ''
    if request.method == 'POST' and 'addFr' in request.form:
        username = request.form['addFr']

        curs = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curs.execute(
            'SELECT * FROM accounts WHERE username = %s', (username, ))
        user = curs.fetchone()

        passat = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        passat.execute(
            'SELECT * FROM friend WHERE friend2 = %s AND friend1 = %s', (username, account['cnp']))
        sex = passat.fetchone()

        curier = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        curier.execute(
            'SELECT * FROM frequests WHERE send = %s AND id = %s', (username, account['cnp']))
        plan = curier.fetchone()

        if not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif plan:
            msg = 'Friend request already sent!'
        elif sex:
            msg = 'Already friends'
        else:
            if account and user:
                curier.execute(
                    'INSERT INTO frequests VALUES (%s, %s)', (username, account['cnp']))
                mysql.connection.commit()
                msg = 'You have sent a friend request!'

    if request.method == 'POST':
        usere = request.form['nume']
        hihihi = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        hihihi.execute('SELECT * FROM accounts WHERE cnp = % s', (usere, ))
        cont = cursor.fetchone()
        if ('poz(%s)', (cont['cnp'])) in request.form:
            hihihi.execute('INSERT INTO friend VALUES (%s, %s)',
                           (cont['cnp'], account['username']))
            hihihi.execute('INSERT INTO friend VALUES (%s, %s)',
                           (account['cnp'], cont['username']))
            hihihi.execute(
                'DELETE FROM frequests WHERE send = %s AnD id=%s', (account['username'], cont['cnp']))
            mysql.connection.commit()
        else:
            hihihi.execute(
                'DELETE FROM frequests WHERE send = %s AnD id=%s', (account['username'], cont['cnp']))
            mysql.connection.commit()

    if account:
        return render_template('friends.php', account=account, entries=entries, dap=dap, msg=msg)


@app.route('/<ID>/transactions')
def trans(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE cnp = % s', (ID, ))
    account = cursor.fetchone()
    curr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    curr.execute('SELECT * FROM tranzactii WHERE din OR pentru = % s', (ID, ))
    tranz = curr.fetchall()
    if account:
        return render_template('trans.html', account=account, tranz=tranz)


@app.route('/<ID>/shop')
def shop(ID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts WHERE cnp = % s', (ID, ))
    account = cursor.fetchone()
    if account:
        return render_template('shop.html', account=account)


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'We have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

if __name__ == "__main__":
    app.secret_key = 'super secret key'

app.run(debug=True,host="192.168.100.3", port=5000)
