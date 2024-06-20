from flask import Blueprint, request, jsonify
from models import db, User, Transaction
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

main = Blueprint('main', __name__)

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "User already exists"}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token), 200

@main.route('/user-info', methods=['PUT'])
@jwt_required()
def add_user_info():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    data = request.get_json()
    user.name = data.get('name')
    user.phone = data.get('phone')
    db.session.commit()
    return jsonify({"message": "User information updated"}), 200

@main.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    transactions = Transaction.query.filter_by(user_id=user.id).all()

    income = sum([txn.amount for txn in transactions if txn.type == 'income'])
    expense = sum([txn.amount for txn in transactions if txn.type == 'expense'])
    balance = income - expense

    return jsonify({
        "name": user.name,
        "phone": user.phone,
        "balance": balance,
        "income": income,
        "expense": expense
    }), 200

@main.route('/transaction', methods=['POST'])
@jwt_required()
def add_transaction():
    user_id = get_jwt_identity()
    data = request.get_json()
    category = data.get('category')
    amount = data.get('amount')
    txn_type = data.get('type')  # 'income' or 'expense'

    transaction = Transaction(user_id=user_id, category=category, amount=amount, type=txn_type)
    db.session.add(transaction)
    db.session.commit()

    return jsonify({"message": "Transaction added successfully"}), 201

@main.route('/report', methods=['GET'])
@jwt_required()
def report():
    user_id = get_jwt_identity()
    report_type = request.args.get('type')  # 'income' or 'expense'
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    query = Transaction.query.filter_by(user_id=user_id, type=report_type)

    if start_date and end_date:
        query = query.filter(Transaction.timestamp.between(start_date, end_date))

    transactions = query.all()

    report = [
        {"category": txn.category, "amount": txn.amount, "timestamp": txn.timestamp}
        for txn in transactions
    ]

    return jsonify(report), 200

@main.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Simply revoke the token on client side to handle logout
    return jsonify({"message": "Logged out successfully"}), 200
