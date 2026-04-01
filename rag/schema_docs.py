documents = [
    """
    Table: customers
    Description: Stores customer details

    Columns:
    - id (INT, Primary Key)
    - name (VARCHAR)
    - city (VARCHAR)
    """,


    """
    Table: orders
    Description: Stores customer orders

    Columns:
    - id (INT, Primary Key)
    - customer_id (INT, Foreign Key -> customers.id)
    - amount (FLOAT)
    - date (DATE)
    """,

    """
    Table: products
    Description: Product catalog

    Columns:
    - id (INT)
    - name (VARCHAR)
    - category (VARCHAR)
    - price (FLOAT)
    """,

    """
    Table: payments
    Description: Payment transactions

    Columns:
    - id (INT)
    - order_id (INT, FK -> orders.id)
    - status (VARCHAR)
    - payment_method (VARCHAR)
    """
]