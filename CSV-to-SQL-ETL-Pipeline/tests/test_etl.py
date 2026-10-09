import sqlite3
import pandas as pd
from src.etl import transform, load

def test_clean_and_reject():
    df = pd.DataFrame([
        dict(order_id='A', order_date='2026-01-01', customer_id='C', product='Pen', quantity=2, unit_price=5),
        dict(order_id='A', order_date='2026-01-01', customer_id='C', product='Pen', quantity=2, unit_price=5),
        dict(order_id='B', order_date='2026-01-01', customer_id='C', product='Pen', quantity=0, unit_price=5),
    ])
    valid, rejected = transform(df)
    assert len(valid) == 1 and len(rejected) == 2
    assert valid.iloc[0]['line_total'] == 10

def test_load_idempotent(tmp_path):
    df = pd.DataFrame([dict(order_id='A', order_date='2026-01-01', customer_id='C', product='Pen', quantity=2, unit_price=5)])
    valid, _ = transform(df)
    db = tmp_path / 'test.db'
    assert load(valid, db) == 1
    assert load(valid, db) == 1
    with sqlite3.connect(db) as conn:
        assert conn.execute('SELECT line_total FROM sales').fetchone()[0] == 10
