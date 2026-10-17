# 📚 Amazon Books Knowledge Graph & Interactive CRUD Engine

A graph-based data engineering and visualization project leveraging **Neo4j**, **Python**, **Pandas**, and **Docker**. This application transforms raw tabular data from the Amazon Books Scraping dataset into an interconnected Property Graph Model (`(Author)-[:WROTE]->(Book)`) and provides seamless programmatic and manual CRUD execution.

---

## 📸 Key Features

- **Automated Pipeline**: Downloads and parses dataset files dynamically via Kaggle API (`kagglehub`).
- **Data Cleaning & Normalization**: Cleans price strings, currency symbols (`₹`), and handles missing properties gracefully.
- **Neo4j Graph Integration**: Ingests structured relational data into a high-performance Neo4j graph database.
- **Complete CRUD Operations**: Custom Python interface for `CREATE`, `READ`, `UPDATE`, and `DELETE` queries on graph entities.
- **Dockerized Environment**: Fully containerized setup for easy setup and reproducibility across platforms.

---

## 🏗 Graph Data Model

The core graph structure models author-book relationships using Cypher:

```
(a:Author {name: String}) -[:WROTE]-> (b:Book {title: String, price: Float})
```

---

## 📁 Repository Structure

```text
.
├── Dockerfile          # Container configuration for Python application
├── README.md           # Project documentation
├── requirements.txt    # Python library dependencies
├── graph_books.py      # Main pipeline script (Download, Process, Ingest)
└── crud_books.py       # Standalone CRUD operation execution suite
```

---

## 🛠 Tech Stack

- **Database**: Neo4j (Graph Database)
- **Language**: Python 3.10
- **Libraries**: `neo4j` (Official Driver), `pandas`, `kagglehub`
- **Containerization**: Docker / Docker Compose
- **Query Language**: Cypher

---

## 🚀 Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and Docker Desktop installed.
- [Python 3.10+](https://www.python.org/) installed locally (optional if running via Docker).
- [Git](https://git-scm.com/) for repository cloning.

---

### 1. Start the Neo4j Container

Launch a local Neo4j instance using Docker:

```bash
docker run \
    --name neo4j-books \
    -p 7474:7474 -p 7687:7687 \
    -d \
    --env NEO4J_AUTH=neo4j/password \
    neo4j:latest
```

> **Neo4j Web UI**: Access the browser interface at [`http://localhost:7474`](http://localhost:7474)  
> **Username**: `neo4j` | **Password**: `password`

---

### 2. Local Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jabaliozoof-hub/amazon-books-neo4j.git
   cd amazon-books-neo4j
   ```

2. **Set up a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the graph builder script:**
   ```bash
   python3 graph_books.py
   ```

5. **Run the CRUD test suite:**
   ```bash
   python3 crud_books.py
   ```

---

### 3. Docker Container Execution

You can build and run the entire Python pipeline within a Docker container:

```bash
# Build the Docker image
docker build -t amazon-books-neo4j .

# Run the container attached to the host network (to connect to Neo4j)
docker run --network="host" amazon-books-neo4j
```

---

## 📊 Sample Cypher Queries (Neo4j Browser)

Run these queries directly in the Neo4j Browser UI (`http://localhost:7474`):

### 1. View Complete Graph
```cypher
MATCH (n) RETURN n LIMIT 50;
```

### 2. Create a Custom Book Entry
```cypher
MERGE (a:Author {name: "ozoof jabali"})
MERGE (b:Book {title: "my creepy story"})
ON CREATE SET b.price = 679.0
MERGE (a)-[:WROTE]->(b)
RETURN a, b;
```

### 3. Update Book Price
```cypher
MATCH (b:Book {title: "my creepy story"})
SET b.price = 720.0
RETURN b.title AS Book, b.price AS UpdatedPrice;
```

### 4. Delete Node Safely
```cypher
MATCH (b:Book {title: "my creepy story"})
DETACH DELETE b;
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/jabaliozoof-hub/amazon-books-neo4j/issues).

---

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.
