from neo4j import GraphDatabase

# ==========================================
# 1. Database Connection Settings
# ==========================================
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")
driver = GraphDatabase.driver(URI, auth=AUTH)

# ==========================================
# 2. CRUD Functions Definition
# ==========================================

# --- [CREATE] ---
def create_book(tx, author_name, title, price):
    query = """
    MERGE (a:Author {name: $author_name})
    MERGE (b:Book {title: $title})
    ON CREATE SET b.price = $price
    MERGE (a)-[:WROTE]->(b)
    """
    tx.run(query, author_name=author_name, title=title, price=price)

# --- [READ] ---
def get_book_details(tx, title):
    query = """
    MATCH (a:Author)-[:WROTE]->(b:Book {title: $title})
    RETURN a.name AS Author, b.title AS Book, b.price AS Price
    """
    result = tx.run(query, title=title)
    record = result.single()
    if record:
        print(f"📖 Read -> Author: '{record['Author']}' | Book: '{record['Book']}' | Price: ₹{record['Price']}")
    else:
        print(f"❌ Read -> Book '{title}' not found in the graph.")

# --- [UPDATE] ---
def update_book_price(tx, title, new_price):
    query = """
    MATCH (b:Book {title: $title})
    SET b.price = $new_price
    RETURN b.title AS Book, b.price AS NewPrice
    """
    result = tx.run(query, title=title, new_price=new_price)
    record = result.single()
    if record:
        print(f"🔄 Update -> Price for '{record['Book']}' updated to ₹{record['NewPrice']}")
    else:
        print(f"❌ Update -> Book '{title}' not found!")

# --- [DELETE] ---
def delete_book(tx, title):
    query = """
    MATCH (b:Book {title: $title})
    DETACH DELETE b
    """
    tx.run(query, title=title)
    print(f"🗑️ Delete -> Book '{title}' was removed from the graph.")


# ==========================================
# 3. Testing CRUD Operations
# ==========================================
test_author = "Agatha Christie"
test_title = "The Mysterious Affair at Styles"
test_price = 299.0

print("--- 1. [CREATE] ---")
with driver.session() as session:
    session.execute_write(create_book, test_author, test_title, test_price)
    print(f"✅ Added new book: '{test_title}' by '{test_author}'")

print("\n--- 2. [READ] ---")
with driver.session() as session:
    session.execute_read(get_book_details, test_title)

print("\n--- 3. [UPDATE] ---")
with driver.session() as session:
    session.execute_write(update_book_price, test_title, 349.0)
    session.execute_read(get_book_details, test_title)

print("\n--- 4. [DELETE] ---")
with driver.session() as session:
    session.execute_write(delete_book, test_title)
    session.execute_read(get_book_details, test_title)

driver.close()
print("\n🎉 CRUD testing script executed successfully!")
