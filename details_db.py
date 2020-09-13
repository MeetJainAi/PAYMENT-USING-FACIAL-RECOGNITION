import sqlite3

# Create sqlite database connection
conn = sqlite3.connect('details.db')
cur = conn.cursor()

# Create database to store customer details

# cur.execute("""
# CREATE TABLE customer_details(
#     email text,
#     clientId text,
#     secret text,
#     ref text
#  )""")

# Delete all customer entries from database
# cur.execute("DELETE from customer_details")

# Delete entire table
# cur.execute("DROP TABLE customer_details")


conn.commit()
conn.close()

# Create a customer record in database


def create_record(email, clientId, secret_number, ref):

    conn = sqlite3.connect('details.db')
    cur = conn.cursor()

    cur.execute('INSERT INTO customer_details VALUES(:email,:clientId,:secret_number,:ref)',
                {
                    'email': email,
                    'clientId': clientId,
                    'secret_number': secret_number,
                    'ref': ref
                })

    conn.commit()
    conn.close()

# Fetch image refernces from database


def fetch_references():
    refernces = []
    conn = sqlite3.connect('details.db')
    cur = conn.cursor()

    cur.execute("SELECT ref FROM customer_details")
    rows = cur.fetchall()

    for row in rows:
        print(row[0])
        refernces.append(row[0])
        print()

    conn.commit()
    conn.close()

    return refernces

# Fetch customer details for a match


def fetch_payment_details(img_ref):
    conn = sqlite3.connect('details.db')
    cur = conn.cursor()

    cur.execute("SELECT * FROM customer_details WHERE ref=?", (img_ref,))
    row = cur.fetchall()
    print('Customer details are --------')
    print(row)

    conn.commit()
    conn.close()
    return row