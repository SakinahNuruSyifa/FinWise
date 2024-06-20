from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/db_finwise'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-screet'
db = SQLAlchemy(app)
CORS(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Pengeluaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.Date, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    kategori = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('pengeluaran', lazy=True))

class Pemasukan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sumber = db.Column(db.String(100), nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('pemasukan', lazy=True))

class Anggaran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal_mulai = db.Column(db.Date, nullable=False)
    tanggal_akhir = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('anggaran', lazy=True))

class Laporan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_pengeluaran = db.Column(db.DECIMAL(10, 2), nullable=False)
    total_pemasukan = db.Column(db.DECIMAL(10, 2), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('laporan', lazy=True))





@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    app.logger.info('email: %s', email)
    app.logger.info('password: %s', password)

    user = User.query.filter_by(email=email, password=password).first()
    if user:
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401



# CRUD for User
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    new_user = User(nama=data['nama'], email=data['email'], password=data['password'], telepon=data['telepon'])
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Email already exists'}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'email': user.email}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.json
        user.email = data.get('email', user.email)
        user.password = data.get('password', user.password)
        db.session.commit()
        return jsonify({'message': 'User updated successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

# CRUD for Pengeluaran
@app.route('/pengeluaran', methods=['POST'])
def create_pengeluaran():
    data = request.json
    new_pengeluaran = Pengeluaran(tanggal=data['tanggal'], jumlah=data['jumlah'], kategori=data['kategori'], user_id=data['user_id'])
    db.session.add(new_pengeluaran)
    db.session.commit()
    return jsonify({'message': 'Pengeluaran created successfully'}), 201

@app.route('/pengeluaran/<int:pengeluaran_id>', methods=['GET'])
def get_pengeluaran(pengeluaran_id):
    pengeluaran = Pengeluaran.query.get(pengeluaran_id)
    if pengeluaran:
        return jsonify({'id': pengeluaran.id, 'tanggal': str(pengeluaran.tanggal), 'jumlah': pengeluaran.jumlah, 'kategori': pengeluaran.kategori, 'user_id': pengeluaran.user_id}), 200
    else:
        return jsonify({'error': 'Pengeluaran not found'}), 404

@app.route('/pengeluaran/<int:pengeluaran_id>', methods=['PUT'])
def update_pengeluaran(pengeluaran_id):
    pengeluaran = Pengeluaran.query.get(pengeluaran_id)
    if pengeluaran:
        data = request.json
        pengeluaran.tanggal = data.get('tanggal', pengeluaran.tanggal)
        pengeluaran.jumlah = data.get('jumlah', pengeluaran.jumlah)
        pengeluaran.kategori = data.get('kategori', pengeluaran.kategori)
        pengeluaran.user_id = data.get('user_id', pengeluaran.user_id)
        db.session.commit()
        return jsonify({'message': 'Pengeluaran updated successfully'}), 200
    else:
        return jsonify({'error': 'Pengeluaran not found'}), 404

@app.route('/pengeluaran/<int:pengeluaran_id>', methods=['DELETE'])
def delete_pengeluaran(pengeluaran_id):
    pengeluaran = Pengeluaran.query.get(pengeluaran_id)
    if pengeluaran:
        db.session.delete(pengeluaran)
        db.session.commit()
        return jsonify({'message': 'Pengeluaran deleted successfully'}), 200
    else:
        return jsonify({'error': 'Pengeluaran not found'}), 404

# Similar CRUD routes for Pemasukan, Anggaran, and Laporan

# CRUD for Pemasukan
@app.route('/pemasukan', methods=['POST'])
def create_pemasukan():
    data = request.json
    new_pemasukan = Pemasukan(sumber=data['sumber'], tanggal=data['tanggal'], jumlah=data['jumlah'], user_id=data['user_id'])
    db.session.add(new_pemasukan)
    db.session.commit()
    return jsonify({'message': 'Pemasukan created successfully'}), 201

@app.route('/pemasukan/<int:pemasukan_id>', methods=['GET'])
def get_pemasukan(pemasukan_id):
    pemasukan = Pemasukan.query.get(pemasukan_id)
    if pemasukan:
        return jsonify({'id': pemasukan.id, 'sumber': pemasukan.sumber, 'tanggal': str(pemasukan.tanggal), 'jumlah': pemasukan.jumlah, 'user_id': pemasukan.user_id}), 200
    else:
        return jsonify({'error': 'Pemasukan not found'}), 404

@app.route('/pemasukan/<int:pemasukan_id>', methods=['PUT'])
def update_pemasukan(pemasukan_id):
    pemasukan = Pemasukan.query.get(pemasukan_id)
    if pemasukan:
        data = request.json
        pemasukan.sumber = data.get('sumber', pemasukan.sumber)
        pemasukan.tanggal = data.get('tanggal', pemasukan.tanggal)
        pemasukan.jumlah = data.get('jumlah', pemasukan.jumlah)
        pemasukan.user_id = data.get('user_id', pemasukan.user_id)
        db.session.commit()
        return jsonify({'message': 'Pemasukan updated successfully'}), 200
    else:
        return jsonify({'error': 'Pemasukan not found'}), 404

@app.route('/pemasukan/<int:pemasukan_id>', methods=['DELETE'])
def delete_pemasukan(pemasukan_id):
    pemasukan = Pemasukan.query.get(pemasukan_id)
    if pemasukan:
        db.session.delete(pemasukan)
        db.session.commit()
        return jsonify({'message': 'Pemasukan deleted successfully'}), 200
    else:
        return jsonify({'error': 'Pemasukan not found'}), 404

# CRUD for Anggaran
@app.route('/anggaran', methods=['POST'])
def create_anggaran():
    data = request.json
    new_anggaran = Anggaran(tanggal_mulai=data['tanggal_mulai'], tanggal_akhir=data['tanggal_akhir'], total=data['total'], user_id=data['user_id'])
    db.session.add(new_anggaran)
    db.session.commit()
    return jsonify({'message': 'Anggaran created successfully'}), 201

@app.route('/anggaran/<int:anggaran_id>', methods=['GET'])
def get_anggaran(anggaran_id):
    anggaran = Anggaran.query.get(anggaran_id)
    if anggaran:
        return jsonify({'id': anggaran.id, 'tanggal_mulai': str(anggaran.tanggal_mulai), 'tanggal_akhir': str(anggaran.tanggal_akhir), 'total': anggaran.total, 'user_id': anggaran.user_id}), 200
    else:
        return jsonify({'error': 'Anggaran not found'}), 404

@app.route('/anggaran/<int:anggaran_id>', methods=['PUT'])
def update_anggaran(anggaran_id):
    anggaran = Anggaran.query.get(anggaran_id)
    if anggaran:
        data = request.json
        anggaran.tanggal_mulai = data.get('tanggal_mulai', anggaran.tanggal_mulai)
        anggaran.tanggal_akhir = data.get('tanggal_akhir', anggaran.tanggal_akhir)
        anggaran.total = data.get('total', anggaran.total)
        anggaran.user_id = data.get('user_id', anggaran.user_id)
        db.session.commit()
        return jsonify({'message': 'Anggaran updated successfully'}), 200
    else:
        return jsonify({'error': 'Anggaran not found'}), 404

@app.route('/anggaran/<int:anggaran_id>', methods=['DELETE'])
def delete_anggaran(anggaran_id):
    anggaran = Anggaran.query.get(anggaran_id)
    if anggaran:
        db.session.delete(anggaran)
        db.session.commit()
        return jsonify({'message': 'Anggaran deleted successfully'}), 200
    else:
        return jsonify({'error': 'Anggaran not found'}), 404

# CRUD for Laporan
@app.route('/laporan', methods=['POST'])
def create_laporan():
    data = request.json
    new_laporan = Laporan(total_pengeluaran=data['total_pengeluaran'], total_pemasukan=data['total_pemasukan'], user_id=data['user_id'])
    db.session.add(new_laporan)
    db.session.commit()
    return jsonify({'message': 'Laporan created successfully'}), 201

@app.route('/laporan/<int:laporan_id>', methods=['GET'])
def get_laporan(laporan_id):
    laporan = Laporan.query.get(laporan_id)
    if laporan:
        return jsonify({'id': laporan.id, 'total_pengeluaran': laporan.total_pengeluaran, 'total_pemasukan': laporan.total_pemasukan, 'user_id': laporan.user_id}), 200
    else:
        return jsonify({'error': 'Laporan not found'}), 404

@app.route('/laporan/<int:laporan_id>', methods=['PUT'])
def update_laporan(laporan_id):
    laporan = Laporan.query.get(laporan_id)
    if laporan:
        data = request.json
        laporan.total_pengeluaran = data.get('total_pengeluaran', laporan.total_pengeluaran)
        laporan.total_pemasukan = data.get('total_pemasukan', laporan.total_pemasukan)
        laporan.user_id = data.get('user_id', laporan.user_id)
        db.session.commit()
        return jsonify({'message': 'Laporan updated successfully'}), 200
    else:
        return jsonify({'error': 'Laporan not found'}), 404

@app.route('/laporan/<int:laporan_id>', methods=['DELETE'])
def delete_laporan(laporan_id):
    laporan = Laporan.query.get(laporan_id)
    if laporan:
        db.session.delete(laporan)
        db.session.commit()
        return jsonify({'message': 'Laporan deleted successfully'}), 200
    else:
        return jsonify({'error': 'Laporan not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
    
