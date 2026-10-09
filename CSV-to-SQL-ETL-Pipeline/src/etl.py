"""Reproducible CSV-to-SQLite ETL for retail transactions."""
import argparse
import sqlite3
from pathlib import Path
import pandas as pd

COLUMNS = ['order_id', 'order_date', 'customer_id', 'product', 'quantity', 'unit_price']

def transform(df):
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    clean = df[COLUMNS].copy()
    for col in ['order_id', 'customer_id', 'product']:
        clean[col] = clean[col].astype('string').str.strip()
    clean['order_date'] = pd.to_datetime(clean['order_date'], errors='coerce').dt.strftime('%Y-%m-%d')
    clean['quantity'] = pd.to_numeric(clean['quantity'], errors='coerce')
    clean['unit_price'] = pd.to_numeric(clean['unit_price'], errors='coerce')
    invalid = clean.isna().any(axis=1) | (clean['quantity'] <= 0) | (clean['unit_price'] < 0)
    invalid |= clean['order_id'].eq('') | clean['customer_id'].eq('') | clean['product'].eq('')
    rejected = clean.loc[invalid].copy()
    valid = clean.loc[~invalid].copy()
    duplicates = valid.duplicated('order_id', keep='first')
    rejected = pd.concat([rejected, valid.loc[duplicates]], ignore_index=True)
    valid = valid.loc[~duplicates].copy()
    if (valid['quantity'] % 1 != 0).any():
        fractional = valid['quantity'] % 1 != 0
        rejected = pd.concat([rejected, valid.loc[fractional]], ignore_index=True)
        valid = valid.loc[~fractional].copy()
    valid['quantity'] = valid['quantity'].astype(int)
    valid['line_total'] = (valid['quantity'] * valid['unit_price']).round(2)
    return valid, rejected

def load(valid, db_path):
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS sales (
            order_id TEXT PRIMARY KEY, order_date TEXT NOT NULL,
            customer_id TEXT NOT NULL, product TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL CHECK(unit_price >= 0),
            line_total REAL NOT NULL)''')
        rows = valid[COLUMNS + ['line_total']].itertuples(index=False, name=None)
        conn.executemany('''INSERT INTO sales VALUES (?,?,?,?,?,?,?)
            ON CONFLICT(order_id) DO UPDATE SET
            order_date=excluded.order_date, customer_id=excluded.customer_id,
            product=excluded.product, quantity=excluded.quantity,
            unit_price=excluded.unit_price, line_total=excluded.line_total''', rows)
        return conn.execute('SELECT COUNT(*) FROM sales').fetchone()[0]

def main():
    parser = argparse.ArgumentParser(description='Extract, clean and load retail CSV to SQLite')
    parser.add_argument('--input', default='data/sample_sales.csv')
    parser.add_argument('--db', default='data/sales.db')
    parser.add_argument('--rejects', default='data/rejected_rows.csv')
    args = parser.parse_args()
    valid, rejected = transform(pd.read_csv(args.input, dtype={'order_id': str, 'customer_id': str}))
    count = load(valid, args.db)
    Path(args.rejects).parent.mkdir(parents=True, exist_ok=True)
    rejected.to_csv(args.rejects, index=False)
    print(f'Valid input rows: {len(valid)} | Rejected: {len(rejected)} | Database rows: {count}')

if __name__ == '__main__':
    main()
