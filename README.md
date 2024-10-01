# Parsing documents for validation or finding discrepancies according to set of structure and test rules.

# Guide lines: DDD+Performance+Dynamic docs structure and tests for finding discrepancies.

Extendability design for future support of different:

* Types of document structure and test rules  
* Repositories (Different Data Storage options),  
* Parsers   
* Validators

# **Beancure Document Validator**

## **Introduction**

**Beancure Document Validator** is a Python-based application designed for asynchronous, efficient parsing and validation of documents (e.g., HTML files). It follows Domain-Driven Design (DDD) principles and utilizes AsyncIO, multiprocessing, and coroutines for handling I/O-bound and CPU-bound tasks. MongoDB is used as the backend for data persistence, with **AsyncIOMotorClient** and **Beanie** (ODM) for async database operations. The tool parses documents based on rules defined in a `docs-config.yaml` file, identifies discrepancies using XPath and regex, and inserts the findings into MongoDB collections Docs and Discrepancy.

## **Table of Contents**

* Features  
* Installation  
* Usage  
* Technology Stack  
* Project Structure  
* Configuration  
* Contributors  
* License

## **Features**

* **Asynchronous document parsing** using `aiofiles` and `asyncio`, supporting high-performance file I/O. Finding discrepancies and their location (default support for HTML files)  
* **Document validation** with results indicating VALID, INVALID, ERROR, or NOT\_PROCESSED.  
* **MongoDB integration** using `AsyncIOMotorClient` and `Beanie` for CRUD operations, with upsert functionality and schema versioning.  
* **Configurable parsing rules** via `docs-config.yaml` to customize the validation logic and rules.  
* **Multiprocessing support** for CPU-bound tasks like file parsing using `concurrent.futures.ProcessPoolExecutor`.  
* **Type validation** and error checking using Pydantic and MyPy.  
* **Domain-Driven Design (DDD)** with clearly defined domains (Parser, DocumentValidator) and interfaces for future extensibility.  
* **Command-line interface (CLI)** for easy interaction and execution.

## **Installation**

To set up the project locally, follow these steps (CLI, Bash, Terminal, ZSH):

1. Clone the repository:  
   `git clone https://github.com/Kasha/BeancureDocumentValidator.git`

`cd BeancureDocumentValidator`

2. Install [Poetry](https://python-poetry.org/) for managing dependencies:  
   `pip install poetry`

   `poetry install`

3. Activate the virtual environment:  
   `poetry shell`  
4. Set up environment variables and configuration:  
   * Create a free account for MongoDB Atlas:  
   * Configure the MongoDB connection string and other settings in `.env` and `resources/settings`.

## **Usage**

The command-line tool offers the following options for document parsing and validation:

**Help**:  
`python main.py --help`  
**Run the main parser**  (CLI, Bash, Terminal, ZSH):  
`python main.py --docs=<absolute_path_to_docs>`  
**Example:**  
`python main.py --docs=C:\Dev\BeancureDocumentValidator\storage\`

### **Parsing and Validation Workflow:**

* **Parser.parse()**: Parses 1 or more documents.  
* **DocumentValidator.validate\_all()**: Scans input files for discrepancies  
* **DocumentValidator.validate()**: Validates a document and returns one of the following statuses: `VALID`, `INVALID`, `ERROR`, or `NOT_PROCESSED` (Not Implemented, yet)  
* 

## **Technology Stack**

* **Python** 3.9+  
* **MongoDB Atlas** (Remote) with `AsyncIOMotorClient` and `Beanie` (ODM)  
* **AsyncIO** and **aiofiles** for asynchronous I/O operations  
* **lxml** and **regex** for HTML parsing  
* **Pydantic** for data validation and type checking  
* **MyPy** for static type checking  
* **Poetry** for dependency management and packaging

## **Project Structure**

graphql  
Copy code  
`.`  
`├── main.py                 # Main entry point of the application`  
`├── beancure/`  
`│   ├── domains/            # Domain layer with Parser and Validator logic`  
`│   ├── services/           # Services for document parsing and validation`  
`│   ├── clients/            # Clients orchestrating domains and services`  
`│   ├── repositories/       # Repositories for MongoDB CRUD operations`  
`│   ├── models/             # Pydantic and Beanie models for database entities`  
`│   ├── config/             # Configuration files and utilities`  
`│   ├── resources/          # YAML config files, including docs_config.yaml`  
`│   └── utils/              # Helper functions`  
`├── tests/                  # Pytest unit, integration, and E2E tests (empty)`  
`├── pyproject.toml          # Poetry configuration file`  
`└── README.md               # Project documentation`

### **Key Components:**

* **Domains**: Core business logic (Parser, DocumentValidator).  
* **Clients**: High-level orchestrators for executing domain operations.  
* **Services**: Actual parsing and validation logic implementations, designed for future extensibility for different file types, dynamic validation file structure, and tests rules.  
* **Repositories**: Interfaces and implementations for database operations, including support for schema versioning.  
* **Models**: Pydantic models define the document and discrepancy data structures.

## **Configuration**

### **docs-config.yaml**

The `docs-config.yaml` file defines the parsing and validation rules. `docs-config.yaml` contains XPath and regex expressions to detect discrepancies in the document.

### **.env**

Set up MongoDB connection and other environment-specific settings in the `.env` file.

Example .env`for MongoDB configuration:

`MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/test?retryWrites=true&w=majority`  
`DB_NAME=beancure`

## **Contributors**

* **Kasha** \- [GitHub Profile](https://github.com/Kasha)

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.

---
