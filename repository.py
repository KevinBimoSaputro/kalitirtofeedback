import connection as conn

db = conn.load_database()

def insert_data(data):
    db.insert(data).execute()

def get_count_by_prediction(prediction, start_date, end_date):
    data = db.select("*", count="exact") \
        .eq("prediction", prediction) \
        .gte("created_at", start_date) \
        .lte("created_at", end_date) \
        .limit(1) \
        .execute()
    return data.count

def get_feedback_history(start_date, end_date):
    data = db.select("feedback, prediction, created_at") \
        .gte("created_at", start_date) \
        .lte("created_at", end_date) \
        .order("created_at", desc=False) \
        .execute()
    return data.data
