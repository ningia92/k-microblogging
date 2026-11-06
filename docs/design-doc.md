# K – Design doc

> Status: draft

## Context

- K is a social network (microblogging) for scientists and science enthusiasts
- In a generic social network it's difficult to find content related to a scientific or technical topic. Furthermore, a scientific discussion is more stimulating and appropriate in a dedicated space
- The first version of K offers a feed to discover new content and a feed to read the content of chosen users. The topics of a post are visible at a glance through its tags.
- In a future version, K will offer a way to reply to a post, dedicated areas where one can discuss specific topics and a way to share knowledge through mathematical formulas and scientific papers.

## Goals

- Users can navigate the explore feed to discover new content and make new connections
- Users can publish text posts and keep up with the people they connect with in the home feed
- Users can tag posts in order to help other users to associate them with a topic
- Users can connect with each other to build a network and stay up to date
- Users can access their profile to easily manage their connections and posts

## Non-goals

- Topic feed and comment on a post (deferred): important but not core, easy to implement in the next version without changes to the core. Postponed to avoid initial scope creep
- LaTeX, paper card (deferred): optional features to implement in a future version without changes to the core of the posts
- Likes (out of scope for now): none of K's goals involves reacting to posts, so likes would add work without serving what K wants to be
- Recommended posts in explore feed (out of scope for now): a global timeline is enough to discover scientific content, as long as the numer of posts stays small enough to be readable 
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