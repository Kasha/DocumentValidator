Example of DDD Python software for Parsing and Validating documents - IO bound and CPU bound (loading files, parsing files, CRUD DB operations) using AsyncIO,  Multi-Processing, and Coroutine.
MongoDB - Async Database using AsyncIOMotorClient + Beanie (ODM)
Files IO - Async  aiofiles
Pydantic and Beanie Document Model for DB CRUD
MyPy and Pydantinc for type errors and validation
Poetry - dependency management and packaging

Summary:
Parser for parsing documents (default - html files) according to docs\-config.yaml rules for valid document
Parsing using lxml.xpath and regular expression for finding discrepancies and their location (-1 for missing data structure and position for invalid content)
Document expected data and discovered discrepancies are inserted into MongoDB docs and discrepancy collection.
Parser.parse() for Parsing 1…N documents
DocumentValidator.validate() for validating document with 4 optional results(`VALID`, `INVALID`, `ERROR`,
`NOT_PROCESSED`,
)
 or validate_all() for finding all discrepancies 


A.Technology:
DDD (Domain Driven Design) and structure (Interfaces for extending and future different behavior implementation)
1. Domains - Parser, DocumentValidator - Main Classes 
2. Clients - ParserClient , DocumentValidatorClient orchestrating and executing the desired behavior services and repositories
3. Services - Parsing uploaded HTML files using lxml and RegularExpression. Parsing Documents into DocdDB and DiscrepancyDB models. Basic implementation of Parsers for future parsing of more file types.
4. Repositories and Models - db_base, db_discrepancy, and db_document implementing MongoDB CRUD based on DocsDB, Doc, DiscrepancyDB, and Discrepancy models designed for HTML parsing as defined. db_base is an abstract class (interface) also using generic dyntamic.factory model for other document types' future support.
5. Resources - utility functions, dependencies (Injection for chosen implemented Domain+Client+Reposetiry+Services), config class parsing and using docs_config.yaml documents parsing rules (implemented and used), test_config.yaml (for future use) 
6. I’m using upsert for updating documents if not exist and inserting them otherwise. I’ve also added a layer of scheme version so the document is a combination of document_id+scheme_version+file_name 
B.Structure:
7. DB name beancure, MongoDB (Atlas - Remote), docs collection, discrepancy collection
8. .env +.resources/settings setup and configuration
9. Poetry for resource dependencies management
10. Command line application with external arguments,  --docs (absolute path and file name or path) and --tests (not implemented)  or --help
11. --docs argument example: --docs=C:\Dev\BeancureDocumentValidator\storage\
12. main.py - main execution file
C. How to install: 
13. git clone https://github.com/Kasha/BeancureDocumentValidator.git
14. From root folder: (command line, bash, terminal)
15.  Run:
install poetry if you don't have: pip install poetry
poetry init
poetry shell
Poetry install

D.MongoDB
16. Async+Process Pooling for loading files and keeping them in DB
17. Async Database AsyncIOMotorClient + Beanie (ODM)
18. Pydantic and Beanie Document for DB CRUD
E. Multi Processing and Coroutine:
Asyncio for coroutine (Async methods) + aiofiles (for files ) + concurrent.futures.ProcessPoolExecuto (Real Parallel) + AsyncIOMotorClient (Async) MongoDB 
F. Design Patterns and Data Structure:
19. Injection like of behavior implementation: get_validator_domain, get_parser_domain
20. Class_factory and Strategic like for creating supported files parsing and extracting according to docs_config.yaml (Any definition of other types besides HTML will raise ParserServiceNotImplementedError. Implemented Service for parsing HTML ParserDataServiceHTML
21. Polymorphism 
22. DB Design Patterns: scheme versioning
23. The Extended Reference Pattern
G.Guide Lines:
24. DDD, Abstraction, Small functions, Popper Error handling, and log data, declaring data types for every variable and forcing function parameters names.
25. Acync+Processes for best io/cpu bound performance.
26. Empty tests/scripts (PyTests, Linter and Coverage) E2E, Integration, UnitTests
H. Structure:

I.Restrictions:
Emphasizing Type Checking:
Using MyPy and Pydantic
Setting the data type for each argument, with limitation of time and 3’rd party documentation issues and complexability forced me to use also ”Any” as the type, so I could increase development time and still keep the data type syntax

Implementation of:
await domain_document_validator.validate_all()

Empty skeleton for one document validation:
await domain_document_validator.validate())


