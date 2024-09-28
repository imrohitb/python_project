from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import icmplib if hasattr(icmplib, 'ping') else ping3  # Handle different Python versions
import xlsxwriter
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/network_monitoring'
db = SQLAlchemy(app)

class NetworkStatus(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.now())
    status = db.Column(db.Boolean)  # 1 for up, 0 for down
    duration = db.Column(db.Integer)  # Duration in seconds

@app.route('/ping')
def ping():
    result = icmplib.ping('example.com', count=1, timeout=1)
    status = result.is_success
    duration = None  # Calculate duration based on previous status

    network_status = NetworkStatus(timestamp=datetime.datetime.now(), status=status, duration=duration)
    db.session.add(network_status)
    db.session.commit()

    return jsonify({'status': status})

@app.route('/report', methods=['GET'])
def report():
    results = NetworkStatus.query.filter_by().all()

    # Process results and generate Excel report
    workbook = xlsxwriter.Workbook('network_report.xlsx')
    worksheet = workbook.add_worksheet()

    # Write header row
    worksheet.write(0, 0, 'Timestamp')
    worksheet.write(0, 1, 'Status')
    worksheet.write(0, 2, 'Duration')

    # Write data rows
    row = 1
    for result in results:
        worksheet.write(row, 0, result.timestamp)
        worksheet.write(row, 1, 'Up' if result.status else 'Down')
        worksheet.write(row, 2, str(result.duration))
        row += 1

    workbook.close()
    return send_file('network_report.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)