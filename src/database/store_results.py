import sqlite3


def save_results_to_db(df, db_path="anomaly_results.db"):

    conn = sqlite3.connect(db_path)

    df.to_sql(
        "anomaly_results",
        conn,
        if_exists="replace",
        index=False
    )

    conn.commit()
    conn.close()

    print(f"Results saved to {db_path}")