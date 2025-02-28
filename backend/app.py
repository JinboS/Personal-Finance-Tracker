from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)

# 配置 SQLite 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义财务记录模型
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    category = db.Column(db.String(10), nullable=False)  # income 或 expense
    description = db.Column(db.String(200))
    amount = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.strftime("%Y-%m-%d"),
            "category": self.category,
            "description": self.description,
            "amount": self.amount
        }

# 获取所有记录
@app.route('/api/records', methods=['GET'])
def get_records():
    records = Record.query.all()
    return jsonify([r.to_dict() for r in records])

# 添加记录
@app.route('/api/records', methods=['POST'])
def add_record():
    data = request.get_json()
    date_str = data.get('date')
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else datetime.utcnow().date()
    except Exception:
        date_obj = datetime.utcnow().date()
    record = Record(
        date = date_obj,
        category = data.get('category', 'expense'),
        description = data.get('description', ''),
        amount = data.get('amount', 0)
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

# 更新记录
@app.route('/api/records/<int:id>', methods=['PUT'])
def update_record(id):
    data = request.get_json()
    record = Record.query.get_or_404(id)
    date_str = data.get('date')
    try:
        record.date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else record.date
    except Exception:
        pass
    record.category = data.get('category', record.category)
    record.description = data.get('description', record.description)
    record.amount = data.get('amount', record.amount)
    db.session.commit()
    return jsonify(record.to_dict())

# 删除记录
@app.route('/api/records/<int:id>', methods=['DELETE'])
def delete_record(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted"})

# 示例：获取指定年月的报表（扩展功能）
@app.route('/api/reports/monthly', methods=['GET'])
def monthly_report():
    year = request.args.get('year', type=int)
    month = request.args.get('month', type=int)
    if not year or not month:
        return jsonify({"error": "Please provide year and month parameters"}), 400

    from sqlalchemy import extract
    records = Record.query.filter(
        extract('year', Record.date) == year,
        extract('month', Record.date) == month
    ).all()

    total_income = sum(r.amount for r in records if r.category == "income")
    total_expense = sum(r.amount for r in records if r.category == "expense")
    
    return jsonify({
        "year": year,
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "net": total_income - total_expense
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 如果数据库不存在则创建
    app.run(debug=True)
