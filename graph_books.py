import os
import pandas as pd
import kagglehub
from neo4j import GraphDatabase

# 1. Download Amazon Books dataset using kagglehub
print("Downloading Amazon Books dataset from Kaggle...")
path = kagglehub.dataset_download("chhavidhankhar11/amazon-books-dataset")
print(f"Dataset downloaded to path: {path}")

# Search recursively for 'Books_df.csv' in all subfolders
csv_file_path = None
for root, dirs, files in os.walk(path):
    for f in files:
        if f == 'Books_df.csv':
            csv_file_path = os.path.join(root, f)
            break
    if csv_file_path:
        break

if csv_file_path:
    print(f"CSV file found at: {csv_file_path}")
    df = pd.read_csv(csv_file_path)
else:
    raise FileNotFoundError("Books_df.csv not found in the dataset!")

print(f"Columns in Books_df: {df.columns.tolist()}")

# Take a small sample of the first 10 rows for a quick and clean POC test
df = df.head(10)
print(f"Successfully loaded the first {len(df)} books for testing!")

# 2. Connect to local Neo4j instance running via Docker
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "password")
driver = GraphDatabase.driver(URI, auth=AUTH)

# 3. Function to create nodes and relationships in Neo4j
def create_book_graph(tx, title, author, price):
    query = """
    MERGE (a:Author {name: $author})
    MERGE (b:Book {title: $title})
    ON CREATE SET b.price = $price
    MERGE (a)-[:WROTE]->(b)
    """
    tx.run(query, title=title, author=author, price=price)

print("\nBuilding the book and author graph in Neo4j...")
with driver.session() as session:
    for index, row in df.iterrows():
        title = str(row.get('Title', 'Unknown Title'))
        author = str(row.get('Author', 'Unknown Author'))
        
        # Clean price field (remove currency symbol '₹', remove commas, convert to float safely)
        raw_price = row.get('Price', 0.0)
        if pd.notna(raw_price):
            price_str = str(raw_price).replace('₹', '').replace(',', '').strip()
            try:
                price = float(price_str)
            except ValueError:
                price = 0.0
        else:
            price = 0.0
        
        session.execute_write(create_book_graph, title, author, price)

print("✅ Successfully built the graph and imported books into Neo4j!")

# 4. Query the graph to retrieve authors and their books
def get_author_books(tx, author_name):
    query = """
    MATCH (a:Author {name: $author_name})-[:WROTE]->(b:Book)
    RETURN a.name AS Author, b.title AS Book
    """
    result = tx.run(query, author_name=author_name)
    return [(record["Author"], record["Book"]) for record in result]

# Test the query with the first author in our sample
with driver.session() as session:
    sample_author = df.iloc[0].get('Author', 'Unknown Author')
    books = session.execute_read(get_author_books, sample_author)
    print(f"\n📚 Books by '{sample_author}' retrieved from the Graph:")
    for author, book in books:
        print(f"- {author} wrote: {book}")

driver.close()
