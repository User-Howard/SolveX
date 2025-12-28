#set document(
  title: "SolveX - Database Systems Final Project",
  author: ("沈俊佑", "吳浩瑋", "林嘉盛", "蔡雨翰"),
)

#set page(
  paper: "a4",
  margin: (x: 2.5cm, y: 3cm),
  numbering: "1",
)

#set text(
  font: ("New Computer Modern", "Noto Sans TC"),
  size: 11pt,
  lang: "en",
)

#show raw: set text(font: "JetBrains Mono")

#set par(justify: true)
#set heading(numbering: "1.1")

// Title page
#align(center)[
  #text(size: 24pt, weight: "bold")[Final Project]

  #v(0.5em)
  #text(size: 18pt)[Introduction to Database Systems]

  #v(2em)
  #text(size: 20pt, weight: "bold")[Title:SolveX]

  #v(3em)
  #text(size: 14pt)[Team Number:33]

  #v(4em)
]

// Team members table
#align(center)[
  #text(size: 14pt, weight: "bold")[Team Members]

  #v(1em)
  #table(
    columns: (1fr, 1.5fr, 1.5fr),
    align: (center, center, center),
    stroke: 0.5pt,
    fill: (x, y) => if y == 0 { rgb("#e8e8e8") },
    [*ID*], [*Name*], [*Department/Year*],
    [113550150], [沈俊佑], [CS/year 2],
    [113550171], [吳浩瑋], [CS/year 2],
    [113550174], [林嘉盛], [CS/year 2],
    [113550190], [蔡雨翰], [CS/year 2],
  )
]

#pagebreak()

// Table of Contents
#outline(
  title: [Table of Contents],
  indent: auto,
  depth: 2,
)

#pagebreak()

= Introduction

As programming learners, we often experience inefficiency and frustration caused by fragmented knowledge sources. In addition, when students are writing code or exploring new technical domains, solving a problem typically requires multiple trials and iterative refinements before reaching a successful solution.

SolveX is a database-driven web application designed to support problem-solving by organizing users' programming questions, corresponding solutions, and relevant reference materials in a unified system. Furthermore, by incorporating a scoring and evaluation mechanism for different solution attempts, the platform enables a more systematic debugging process, allowing learners to compare approaches, identify effective strategies, and learn from unsuccessful attempts.

= Design Motivation

== What is the problem your system is trying to address?

Learners often have difficulty organizing programming problems, solutions, and learning resources in one place. Therefore, we want to create a platform that allows users to store and manage these materials efficiently.

== Why is your system suitable in addressing the problem?

Our system provides a platform for programming learners that can save the problems, solutions, and learning resources. Users of our platform can create their own problems and then someone or themselves can create the solutions for the problems with resources below. This enables the programming learners to manage their learning resources more efficiently.

== Why does this application need a database?

Because we have to  store and manage diverse data such as users, programming problems, solutions, and learning resources in our system. A database enables structured data organization and supports efficient data retrieval. This makes it suitable for handling growing data volumes and multiple users in a reliable way i.e more scalable.

#pagebreak()

= Database Design

(Describe the schema of all your tables in the database, including keys and index, if applicable.)

== Overview of the Database Schema

The SolveX database consists of 10 tables organized into three categories:

*Core Entity Tables (5)*
- users - User accounts
- problems - Problems/issues being tracked
- solutions - Solutions to problems
- resources - External resources (URLs, documentation)
- tags - Categorization tags

*Relationship Tables (5)*
- problem_resources - Links problems to resources
- solution_resources - Links solutions to resources
- problem_relations - Links problems to other problems
- problem_tags - Links problems to tags
- resource_tags - Links resources to tags

#figure(
  image("assets/er-diagram.svg", width: 100%),
  caption: [SolveX Database Entity-Relationship Diagram]
)

== Detailed Table Descriptions

=== Users Table

Purpose: Store user account information

```sql
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

Keys:
- Primary Key: user_id (SERIAL) - Auto-incrementing unique identifier
- Unique Constraint: email - Ensures each email address is used only once

// #pagebreak()

=== Problems Table

Purpose: Store problems/issues that users want to solve

```sql
CREATE TABLE problems (
    problem_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    description TEXT,
    problem_type VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    resolved BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_problems_user_id ON problems(user_id);
CREATE INDEX idx_problems_created_at ON problems(created_at DESC);
```

Keys:
- Primary Key: problem_id - Unique identifier for each problem
- Foreign Key: user_id → users(user_id)

Indexes:
- idx_problems_user_id - Frequently used in queries like "get all problems by user"
- idx_problems_created_at DESC - Used for sorting by recency in dashboard and list views

#pagebreak()

=== Solutions Table

Purpose: Store solutions to problems with support for solution hierarchies

```sql
CREATE TABLE solutions (
    solution_id SERIAL PRIMARY KEY,
    problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    parent_solution_id INTEGER REFERENCES solutions(solution_id) ON DELETE CASCADE,
    code_snippet TEXT NOT NULL,
    explanation TEXT,
    approach_type VARCHAR(100),
    version_number INTEGER DEFAULT 1,
    branch_type VARCHAR(50),
    improvement_description TEXT,
    success_rate FLOAT,
    created_at TIMESTAMP DEFAULT NOW(),
    CONSTRAINT no_self_loop CHECK (solution_id != parent_solution_id),
    CONSTRAINT solution_success_rate_range CHECK (success_rate >= 0 AND success_rate <= 100)
);

CREATE INDEX idx_solutions_problem_id ON solutions(problem_id);
CREATE INDEX idx_solutions_parent_id ON solutions(parent_solution_id);
CREATE INDEX idx_solutions_created_at ON solutions(created_at DESC);
```

Keys:
- Primary Key: solution_id
- Foreign Keys:
  - problem_id → problems(problem_id)
  - parent_solution_id → solutions(solution_id) (self-referencing for solution versions/improvements)

Constraints:
- no_self_loop - Prevents a solution from being its own parent
- solution_success_rate_range - Ensures success rate is between 0-100

Indexes:
- idx_solutions_problem_id - Critical for "get all solutions for a problem" queries
- idx_solutions_parent_id - Used for finding child solutions (solution evolution tree)
- idx_solutions_created_at DESC - For recent solutions in dashboard

#pagebreak()

=== Resources Table

Purpose: Store external resources (articles, documentation, Stack Overflow posts, etc.)

```sql
CREATE TABLE resources (
    resource_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    title VARCHAR(500),
    source_platform VARCHAR(50),
    content_summary TEXT,
    visit_count INTEGER DEFAULT 1,
    first_visited_at TIMESTAMP,
    last_visited_at TIMESTAMP,
    usefulness_score FLOAT,
    CONSTRAINT resource_usefulness_range CHECK (usefulness_score >= 0 AND usefulness_score <= 5)
);

CREATE INDEX idx_resources_user_id ON resources(user_id);
CREATE INDEX idx_resources_last_visited ON resources(last_visited_at DESC);
```

Keys:
- Primary Key: resource_id
- Foreign Key: user_id → users(user_id)

Constraints:
- resource_usefulness_range - Usefulness score must be 0-5 (star rating system)

Indexes:
- idx_resources_user_id - For "get all resources saved by user"
- idx_resources_last_visited DESC - For showing recently accessed resources

=== Tags Table

Purpose: Categorization system for problems and resources

```sql
CREATE TABLE tags (
    tag_id SERIAL PRIMARY KEY,
    tag_name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50),
    description TEXT
);
```

Keys:
- Primary Key: tag_id
- Unique Constraint: tag_name - Prevents duplicate tag names

#pagebreak()

=== Problem-Resource Junction Table

Purpose: Many-to-many relationship between problems and resources

```sql
CREATE TABLE problem_resources (
    problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    resource_id INTEGER NOT NULL REFERENCES resources(resource_id) ON DELETE CASCADE,
    relevance_score FLOAT,
    contribution_type VARCHAR(50),
    added_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (problem_id, resource_id),
    CONSTRAINT problem_resource_relevance_range CHECK (relevance_score >= 0 AND relevance_score <= 1)
);

CREATE INDEX idx_problem_resources_resource_id ON problem_resources(resource_id);
```

Keys:
- Composite Primary Key: (problem_id, resource_id) - Ensures unique pairing
- Foreign Keys: Both with CASCADE delete (delete link if either entity is deleted)

Indexes:
- idx_problem_resources_resource_id - For reverse lookups ("which problems use this resource")

=== Solution-Resource Junction Table

Purpose: Many-to-many relationship between solutions and resources

```sql
CREATE TABLE solution_resources (
    solution_id INTEGER NOT NULL REFERENCES solutions(solution_id) ON DELETE CASCADE,
    resource_id INTEGER NOT NULL REFERENCES resources(resource_id) ON DELETE CASCADE,
    PRIMARY KEY (solution_id, resource_id)
);

CREATE INDEX idx_solution_resources_resource_id ON solution_resources(resource_id);
```

Keys:
- Composite Primary Key: (solution_id, resource_id)
- Foreign Keys: Both CASCADE

Indexes:
- For reverse lookups ("which solutions reference this resource")

#pagebreak()

=== Problem Relations Table

Purpose: Directed graph of problem relationships (e.g., "prerequisite", "similar", "related")

```sql
CREATE TABLE problem_relations (
    from_problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    to_problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    relation_type VARCHAR(50),
    strength FLOAT,
    PRIMARY KEY (from_problem_id, to_problem_id),
    CONSTRAINT problem_relation_strength_range CHECK (strength >= 0 AND strength <= 1),
    CONSTRAINT no_self_relation CHECK (from_problem_id != to_problem_id)
);

CREATE INDEX idx_problem_relations_to ON problem_relations(to_problem_id);
```

Keys:
- Composite Primary Key: (from_problem_id, to_problem_id) - Directed edge
- Foreign Keys: Both self-referencing to problems with CASCADE

Constraints:
- no_self_relation - Problem cannot relate to itself
- strength_range - Relationship strength is 0-1

Indexes:
- idx_problem_relations_to - For finding incoming relations ("what problems lead to this one")

=== Problem-Tags Junction Table

Purpose: Many-to-many relationship between problems and tags

```sql
CREATE TABLE problem_tags (
    problem_id INTEGER NOT NULL REFERENCES problems(problem_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    PRIMARY KEY (problem_id, tag_id)
);

CREATE INDEX idx_problem_tags_tag_id ON problem_tags(tag_id);
```

Keys:
- Composite Primary Key: (problem_id, tag_id)
- Foreign Keys: Both CASCADE

Indexes:
- For finding all problems with a specific tag

#pagebreak()

=== Resource-Tags Junction Table

Purpose: Many-to-many relationship between resources and tags (with confidence scoring)

```sql
CREATE TABLE resource_tags (
    resource_id INTEGER NOT NULL REFERENCES resources(resource_id) ON DELETE CASCADE,
    tag_id INTEGER NOT NULL REFERENCES tags(tag_id) ON DELETE CASCADE,
    confidence FLOAT,
    PRIMARY KEY (resource_id, tag_id),
    CONSTRAINT resource_tag_confidence_range CHECK (confidence >= 0 AND confidence <= 1)
);

CREATE INDEX idx_resource_tags_tag_id ON resource_tags(tag_id);
```

Keys:
- Composite Primary Key: (resource_id, tag_id)
- Foreign Keys: Both CASCADE

Constraints:
- confidence_range - Tag confidence score 0-1 (for auto-tagging ML systems)

Indexes:
- For tag-based resource search

#pagebreak()

== Schema Changes from Milestone 2:

=== Added problem_resources

Table: problem_resources

Change Type: Added

Specific Change: New junction table linking problems and resources (M:N)

Rationale: Milestone 2 only linked resources to solutions. During development, users needed to bookmark resources directly at the problem level before creating solutions. This table enables problem-level resource organization and tracking.

=== Added resource_tags

Table: resource_tags

Change Type: Added

Specific Change: Extended tagging system from problems to resources

Rationale: Resources also require categorization for search and filtering. This change improves discoverability and supports future auto-tagging features.

=== Added User–Resource Relationship

Table: resources

Change Type: Modified

Specific Change: Added user_id foreign key

Rationale: Resources previously had no ownership. Adding user association enables personal resource management, access control, and usage analytics.

#pagebreak()

=== Refined solution_resources

Table: solution_resources

Change Type: Modified

Specific Change: Implemented explicit junction table for solution–resource relationship

Rationale: Replaced abstract "refer" relationship with a normalized junction table, improving query clarity and referential integrity.

=== Enhanced Solution Versioning

Table: solutions

Change Type: Modified

Specific Change: Added parent_solution_id self-referencing foreign key

Rationale: Supports solution evolution and version tracking (v1 → v2 → v3), aligning with planned version control features.

=== Added problem_relations

Table: problem_relations

Change Type: Added

Specific Change: Self-referencing junction table between problems

Rationale: Enables modeling of problem dependencies and similarity relationships.

#pagebreak()

== Bonus:

=== Completeness of our constraints:

*users:*
- PK: user_id
- NOT NULL: username, email
- UNIQUE: email
- DEFAULT: created_at = now()

*problems*
- PK: problem_id
- FK: user_id -> users.user_id
- NOT NULL: user_id, title
- DEFAULT: created_at = now(), resolved = false

*solutions*
- PK: solution_id
- FK: problem_id -> problems.problem_id, parent_solution_id -> solutions.solution_id
- NOT NULL: problem_id, code_snippet
- CHECK: solution_id != parent_solution_id, success_rate between 0 and 100
- DEFAULT: version_number = 1, created_at = now()

*resources*
- PK: resource_id
- FK: user_id -> users.user_id
- NOT NULL: user_id, url
- CHECK: usefulness_score between 0 and 5
- DEFAULT: visit_count = 1

*tags*
- PK: tag_id
- NOT NULL: tag_name
- UNIQUE: tag_name

#pagebreak()

*problem_resources*
- PK: (problem_id, resource_id)
- FK: problem_id -> problems.problem_id, resource_id -> resources.resource_id
- CHECK: relevance_score between 0 and 1
- DEFAULT: added_at = now()

*solution_resources*
- PK: (solution_id, resource_id)
- FK: solution_id -> solutions.solution_id, resource_id -> resources.resource_id

*problem_relations*
- PK: (from_problem_id, to_problem_id)
- FK: from_problem_id -> problems.problem_id, to_problem_id -> problems.problem_id
- CHECK: strength between 0 and 1, from_problem_id != to_problem_id

*problem_tags*
- PK: (problem_id, tag_id)
- FK: problem_id -> problems.problem_id, tag_id -> tags.tag_id

*resource_tags*
- PK: (resource_id, tag_id)
- FK: resource_id -> resources.resource_id, tag_id -> tags.tag_id
- CHECK: confidence between 0 and 1

#pagebreak()

=== BCNF inplementation:

*In User Table:*

Functional dependencies:
- user_id → {username, email, first_name, last_name, created_at}
- email → user_id (due to UNIQUE constraint)

Both user_id and email are candidate keys

All dependencies have superkeys on the left side

Conclusion: BCNF satisfied

*In Problem Table:*

Primary dependency: problem_id → {all other columns}

problem_id is the only candidate key

No partial dependencies exist

Conclusion: BCNF satisfied

*In Solution Table:*

Same structure as problems table

Self-referencing FK doesn't violate BCNF (it's just a regular FK)

Conclusion: BCNF satisfied

#pagebreak()

= Data Sources(4%)

== Describe the data source and the original format.

The data for SolveX is derived from three primary sources: personal programming records, URLs automatically collected through a browser extension, and technical article details retrieved via the StackOverflow API. Furthermore, an LLM API is utilized to analyze content for generating summaries and tags.

These datasets were originally stored in CSV and structured formats before being processed with the pandas library—which handled DateTime conversions and NULL values—for bulk importation into the database.

== Show a screenshot or text output demonstrating at least 100 tuples.

#figure(
  image("assets/screenshot-data.png", width: 100%),
  caption: [Database Sample Data - Demonstrating 100+ Tuples]
)

== Answer the following questions

*Did your team encounter any challenges during data collection?*

Yes. We encountered challenges mainly related to foreign key constraints, including load order dependencies, self-referential relationships, and many-to-many junction tables. We also had to handle DateTime conversion and NULL value issues when importing CSV data using pandas.

*How did you overcome these challenges?*

We overcame these technical challenges by implementing a bulk CSV import process using the pandas library.This method automated the DateTime conversion to ensure compatibility with PostgreSQL and facilitated precise NULL value handling by mapping pandas NaN values directly to SQL NULL.Additionally, they performed a sequence reset after the bulk insertion to maintain the integrity of auto-incrementing primary keys for subsequent operations.

#pagebreak()

= Data sources to database (4%):

== Describe the methods of importing the original data to your database and strategies for updating the data.

The system employs a bulk CSV import method facilitated by the pandas library for initial data population. This process includes automated DateTime conversion and the mapping of NaN values to SQL NULL to ensure data consistency, followed by a sequence reset to synchronize auto-incrementing primary keys. For ongoing data updates, the system utilizes manual user entries, automated URL collection via browser extensions, and API integrations to fetch metadata and generate summaries.

== How does your system "CREATE" the database?

We implemented a dependency-aware loading pipeline with ordered table insertion, foreign key validation using pandas, and transactional bulk loading. DateTime conversion, NULL handling, and PostgreSQL sequence resets were automated to ensure data integrity and prevent key conflicts.

#pagebreak()

= Application with database (18%):

== Who is the target user of your system?

Please list all the users who may use it and how you customized your design to align with their needs (e.g., provide different views for different roles, etc.)

(Clearly list WHO uses the system and HOW the design accommodates them)

*Primary Users: Programming Learners and Students*

SolveX is designed for programming learners and students who need a centralized system to manage technical problems, solutions, and learning resources.

The system accommodates their needs in the following ways:

- *Personalized knowledge management:* All problems, solutions, and resources are associated with a specific user, ensuring that learners manage and access only their own content.

- *Solution progression tracking:* The system supports iterative improvement of solutions, allowing students to record, revisit, and refine their problem-solving approaches over time.

- *Centralized resource organization:* Learners can attach and categorize learning resources to specific problems, making fragmented information easier to revisit and reuse.

- *Efficient personal retrieval:* User-scoped indexing enables fast access to recently created problems and frequently used resources, supporting an efficient personal learning workflow.

By focusing on a single user role, the design remains simple while directly addressing the core challenges faced by programming learners.

#pagebreak()

== What are the functionalities of your application?

The application provides a centralized platform for managing programming knowledge. Users can record and organize programming problems, track solution evolution through versioning, and maintain a personal library of learning resources. The system supports flexible tagging, problem–resource linking, and problem relationships to help users structure their knowledge. Additionally, a personalized dashboard and advanced search functionality enable efficient retrieval and review of learning content.

== What SQL queries are performed by your application?

(Include actual SQL code, must use raw SQL query strings.)

=== User Management

*Q1: Create User*

```sql
INSERT INTO users (username, email, first_name, last_name)
VALUES (%s, %s, %s, %s)
RETURNING *
```

*Q2: Get User's Problems*

```sql
SELECT * FROM problems
WHERE user_id = %s
ORDER BY created_at DESC
```

*Q3: Update User*

```sql
UPDATE users
SET username = %s, email = %s, first_name = %s, last_name = %s
WHERE user_id = %s
RETURNING *
```

// #pagebreak()

=== Problem Management

*Q4: Create Problem with Tags*

```sql
-- Insert problem
INSERT INTO problems (user_id, title, description, problem_type)
VALUES (%s, %s, %s, %s)
RETURNING *

-- Associate tags
INSERT INTO problem_tags (problem_id, tag_id)
VALUES (%s, %s)
```

*Q5: Mark Problem Resolved*

```sql
UPDATE problems
SET resolved = TRUE
WHERE problem_id = %s
RETURNING *
```

*Q6: Delete Problem*

```sql
DELETE FROM problems WHERE problem_id = %s
-- Cascades to problem_tags, problem_resources, solutions, etc.
```

// #pagebreak()

=== Solution Management

*Q7: Create Solution (Version Tree)*

```sql
INSERT INTO solutions (
    problem_id, parent_solution_id, code_snippet, explanation,
    approach_type, improvement_description, success_rate
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING *
```

*Q8: Get Solution Children*

```sql
SELECT * FROM solutions
WHERE parent_solution_id = %s
ORDER BY created_at DESC
```

*Q9: Count Children (Version Tracking)*

```sql
SELECT COUNT(*) as count
FROM solutions
WHERE parent_solution_id = %s
```

// #pagebreak()

=== Resource Management

*Q10: Create Resource*

```sql
INSERT INTO resources (
    user_id, url, title, source_platform,
    usefulness_score, first_visited_at, last_visited_at
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING *
```

*Q11: Track Visit (Analytics)*

```sql
UPDATE resources
SET visit_count = visit_count + 1,
    last_visited_at = %s
WHERE resource_id = %s
RETURNING *
```

*Q12: Search Resources*

```sql
SELECT DISTINCT r.*
FROM resources r
LEFT JOIN resource_tags rt ON r.resource_id = rt.resource_id
LEFT JOIN tags t ON rt.tag_id = t.tag_id
WHERE
  (%s IS NULL OR r.user_id = %s)
  AND (%s IS NULL OR t.tag_name = %s)
  AND (%s IS NULL OR r.source_platform = %s)
ORDER BY r.last_visited_at DESC NULLS LAST
LIMIT %s OFFSET %s
```

// #pagebreak()

=== Relationship Management

*Q13: Create Problem Relation (Knowledge Graph)*

```sql
INSERT INTO problem_relations (from_problem_id, to_problem_id, relation_type, strength)
VALUES (%s, %s, %s, %s)
RETURNING *
```

*Q14: Get Problem Relations*

```sql
-- Outgoing relations
SELECT * FROM problem_relations
WHERE from_problem_id = %s
ORDER BY strength DESC NULLS LAST

-- Incoming relations
SELECT * FROM problem_relations
WHERE to_problem_id = %s
ORDER BY strength DESC NULLS LAST
```

=== Database Maintenance

*Q15: Bulk Insert from CSV*

```sql
INSERT INTO {table_name} VALUES ({placeholders})
-- Executed via cur.executemany() for batch processing
```

*Q16: Reset Auto-Increment Sequences*

```sql
SELECT setval(
    pg_get_serial_sequence('{table_name}', '{id_column}'),
    COALESCE((SELECT MAX({id_column}) FROM {table_name}), 1),
    true
)
```

#pagebreak()

== How does your application perform these queries?

(connections between application and database)

The application uses FastAPI with psycopg3 to execute raw SQL queries directly against PostgreSQL. Each HTTP request receives a managed database connection via dependency injection, which is automatically closed after completion.

Queries are parameterized to prevent SQL injection and validated with Pydantic schemas before execution. JOINs and JSON aggregation are used to efficiently fetch related data in a single query, while indexes and foreign key constraints ensure performance and maintain data integrity.

== Other functions:

(All the other details of your application that you want us to know.)

answer if any.
