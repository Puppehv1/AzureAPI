from dotenv import load_dotenv
import os
import pyodbc
from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.INFO, filename="status.log", filemode="w",
                    format="[%(asctime)s] - %(filename)s - %(levelname)s | %(message)s")

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")

def get_db_connection():
    conn = pyodbc.connect(
        f"Driver=ODBC Driver 18 for SQL Server;"
        f"Server=tcp:khsqlserver9745.database.windows.net,1433;"
        f"Database=khdatabase;"
        f"Uid=SqlAdmin;"
        f"Pwd=Password234#;"
        f"Encrypt=yes;"
        f"TrustServerCertificate=no;"
        f"Connection Timeout=30;"
    )
    return conn

def send_logs(data):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO dbo.Metrics (
                    Timestamp,
                    DiskFreeGB,
                    MemoryFreeMB,
                    MemoryTotalMB,
                    RamUsagePercent,
                    RamUsedGB,
                    CpuPercent,
                    TcpEstablished,
                    SshOpen,
                    Samba139,
                    Samba445
                )
                VALUES (
                    {data[Timestamp]},
                    {data[DiskFreeGB]},
                    {data[MemoryFreeMB]},
                    {data[MemoryTotalMB]},
                    {data[RamUsagePercent]},
                    {data[RamUsedGB]},
                    {data[CpuPercent]},
                    {data[TcpEstablished]},
                    {data[SshOpen]},
                    {data[Samba139]},
                    {data[Samba445]}
                );""")

    conn.commit()
    logging.info("Data pushed to DB")
    cursor.close()
    conn.close()


@app.route('/', methods=['POST'])
def receive_data():
    auth_header = request.headers.get("Authorization")

    if auth_header != API_KEY:
        logging.warning(f"Unauthorized API connection detected using header {auth_header} while ours is {API_KEY}")
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    logging.info(data)

    send_logs(data)

    return ({"status": "success"}), 200

if __name__ == '__main__':
    app.run(debug=True, port="5000", host="0.0.0.0")

