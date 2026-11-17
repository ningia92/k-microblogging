# 0002 - Use PostgreSQL as the database

Status: accepted

## Context
K will have three entities: users, posts and follows. The relationships between them are:
- A user can publish one or more posts and a post can be published by one user (one-to-many)
- A user can follow one or more users (many-to-many)

The following queries are required to retrieve the home feed (personal feed):
- Fetch the IDs of all followed users (from follows)
- For each of those users: fetch their posts (from posts)

The queries to retrieve the feeds are more frequent than the one that retrieves the user profile (see Estimates in the design doc).

The persistence of published posts must be guaranteed until they are removed.

## Options considered
- SQLite
    - Pros: relational, with the same constraints and JOINs as PostgreSQL; integrated into Django; simple to use; handles 10^4 DAU
    - Cons: since the DB is a file on a single machine, it cannot be shared by multiple Django instances on different machines, which are needed as DAU grows (10^6 DAU); migrating to a different database when it becomes necessary is costly

- PostgreSQL
    - Pros: constraints to ensure data integrity and consistency; easy to represent the many-to-many relationship (follows); a single query to retrieve the home feed; the Django ORM is designed for relational databases
    - Cons: requires installing and configuring a separate server

- MongoDB (document based)
    - Pros: the profile can be read from a single document with the embedding model (user data and posts in the same document). However, this operation is less frequent than reading feeds
    - Cons: follows, posts and users as separate flat collections linked by ID imitate the relational model, but without its guarantees (no constraints, no single query for the home feed); with the embedding model (user data and posts in the same User document), reading the feeds is expensive (retrieving posts from each User document, merging and sorting them in code); requires installing and configuring a separate server

## Decision
We will use PostgreSQL as the database.

## Consequences
\+ The unique constraint ensures that a follower/followee pair cannot be saved twice; the foreign key constraint ensures that a post cannot exist with a non-existent author; the check constraint "follower_id <> followee_id" ensures that self-follow is blocked by the DB too, not only by the API with a 400 response.

\+ Fetching the home feed posts can be done with a single JOIN on the tables "users", "follows" and "posts".

\+ PostgreSQL is easy to configure and use in Django.

\- To develop K locally it is necessary to run two containers: one for the Django app and one for the PostgreSQL DB (the DB configuration goes into .env). Furthermore, testing requires a running PostgreSQL server since Django creates a test DB on the same server.

\- The DB does not solve the home feed cost as the number of followees grows. This cost depends on the follow relationship (see ADR 0001).
