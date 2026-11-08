# K – Design doc

> Status: draft

## Context

- K is a social network (microblogging) for scientists and science enthusiasts
- In a general-purpose social network it's difficult to find content related to a scientific or technical topic. Furthermore, a scientific discussion is more stimulating and appropriate in a dedicated space
- The first version of K offers a feed to discover new content and a feed to read the content of chosen users. The topics of a post are visible at a glance through its tags.
- In a future version, K will offer a way to reply to a post, dedicated areas where one can discuss specific topics and a way to share knowledge through mathematical formulas and scientific papers.

## Goals

- Users can navigate the explore feed to discover new content and make new connections
- Users can publish text posts and keep up with the people they connect with in the home feed
- Users can tag posts in order to help other users associate them with a topic
- Users can connect with each other to build a network and stay up to date
- Users can access their profile to easily manage their connections and posts

## Non-goals

- Topic feed and comments on a post (deferred): important but not core, easy to implement in the next version without changes to the core. Postponed to avoid initial scope creep
- LaTeX, paper card (deferred): optional features to implement in a future version without changes to the core of the posts
- Likes (out of scope for now): none of K's goals involves reacting to posts, so likes would add work without serving what K wants to be
- Recommended posts in explore feed (out of scope for now): a global timeline is enough to discover scientific content, as long as the number of posts stays small enough to be readable (roughly below 10^6 DAU, see Estimates)
- Image and video attachments (out of scope for now): K is about text-based discussion. Media would make storage and bandwidth costs orders of magnitude higher than text, without serving any of the goals

## Requirements

### Functional requirements

- A user can sign up and log in
- A user can publish a text post of up to 500 characters
- A user can see all users' posts in the explore feed
- A user can see their own posts and their connections' posts in the home feed
- A user can tag a post with 0 to a maximum of 3 topics from a predefined list
- A user can delete their own posts
- A user can see the topics of every post
- A user can see feeds in reverse chronological order
- A user can connect with other users
- A user can break a connection with another user
- A user can see their posts in their profile
- A user can see their connections in their profile

### Non-functional requirements

- Readers may see a feed that is stale by at most 4 seconds (eventual consistency): a short delay is barely noticeable, while an error is immediately visible to everyone
- An author always sees their own post immediately after publishing it (read-your-writes)
- Post publishing must be available 99% of the time; when it fails, the user gets an error and can retry. It's a reasonable choice as it does not damage the reputation of the service
- Reading the feed is more frequent than post publishing, so reading the feed must have high availability (99.9%). In this case, an extended outage could cause the loss of a large number of users
- No post is lost once the author has received a confirmation (durability)
- Both feeds load in under 200 ms for 99% of requests (p99)
- Within 2 seconds of deletion, a post is no longer readable by other users

## Estimates

### Assumptions

| Assumption | Value | Rationale |
|---|---|---|
| Feed opens per user per day | 10 | A few times a day (morning, breaks, evening): K is a niche social network, not a general-purpose one |
| Posts published per user per day | 0.5 | Most users read and rarely post; on average one post every two days |
| Average post text size | ~100 bytes | Based on typical posts on other social networks, well below the 500-character limit |
| Metadata per post | ~100 bytes | id, author, timestamp, topics |
| Peak factor | ~×2 | 30% of the traffic during time window; 3 hours time window |
| Storage horizon | 5 years | Typical planning horizon for capacity estimates |

**Derived read/write ratio:** 20:1

NB: the ratio does not depend on the DAU as it originates from the behavior of each user.

### Estimates at three scales

| DAU | 10^4 | 10^6 | 10^8 |
|---|---|---|---|
| Posts per day | 5 × 10^3  | 5 × 10^5 | 5 × 10^7 |
| Feed reads per day | 10^5 | 10^7 | 10^9 |
| Write QPS (avg / peak) | 0.05 / 0.1 | 5 / 10 | 500 / 1,000 |
| Feed read QPS (avg / peak) | 1 / 2 | 100 / 200 | 10,000 / 20,000 |
| Storage per day | 1 MB | 100 MB | 10 GB |
| Storage over 5 years | 2 GB | 200 GB | 20 TB |
| New posts per second in the explore feed (avg) | 0.05 | 5 | 500 |

### Impact on design

For each scale, the estimates are compared with what the simplest possible system (one application server and one database) can handle. The goal is to find where the bottlenecks are before designing the architecture, not to solve them.

#### 10^4 DAU

Peak read QPS is ~2 and storage is ~2 GB in 5 years: far below what a single server and database can handle. The explore feed gets a new post every ~20 seconds, so it is still readable.

#### 10^6 DAU

Peak read QPS is ~200 and storage is ~200 GB in 5 years: in general, one single server and database can still handle this load without much effort. However, each home feed varies from user to user and can potentially reach the upper limit of the QPS due to the queries for the ids of each user connection and their posts. The explore feed starts to be unreadable for a human as it receives 5 new posts per second: a different approach is needed to show the posts on that feed (e.g. recommended posts).

#### 10^8 DAU

In this scenario peak read QPS (~20k) is far above the capacity of one single server: it is required to distribute the load on multiple servers. Required storage is ~10 GB per day and ~20 TB in 5 years: older posts (rarely read) should be moved to secondary storage. As at 10^6 DAU, the update rate of the explore feed is too high (~500/s): a different approach is needed than showing all posts.

### Target scale

- The design of the first version is for 10^4 scale as it is a new social network, therefore over-engineering must be avoided
- When the number of requests is more than a certain threshold (a few thousand) it's time to scale. In particular, when the availability of the feed read starts to be below 99.9% or p99 feeds load above 200ms it's time to scale.
