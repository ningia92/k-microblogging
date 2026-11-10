# 0001 - Use follow for user connections

Status: accepted

## Context
As K is a microblogging platform, a user who publishes a post does so with the intent to reach the whole user base.

A connection between two users is a relationship that can be unidirectional (follow) or bidirectional (friendship). The home feed requirement needs a relationship between users. Furthermore, the FR "A user can see all users' posts in the explore feed" is a constraint that makes the follow relationship the right choice.

The decision is costly to reverse: if we start with follow and after a year we decide to switch to friendship, all the one-way follows break. So home feeds empty out and the users are forced to accept/refuse all the friend requests.

## Options considered
- Friendship: symmetric relation (the connection exists only if both users accept it); offers more control over who reads their posts; restrictive (only a user's friends can see their posts); the greater control on privacy isn't worth it since the explore feed shows all the posts

- Follow: asymmetric relation (you can follow a user even without them having to accept); each post is accessible to everyone; no limit on how many users one can follow; no control over the users' followers.

## Decision
We will use the follow relationship between users.

## Consequences
\+ The friendship process (friend request -> waiting request -> request accepted/refused) requires a pending state and more queries. With the follow relationship there is only one action (A follows B).

\- Home feed cost grows with the number of followed users. Not an issue at the target scale (10^4 DAU), but it becomes the main bottleneck around 10^6 DAU (see Estimates).

\- Users cannot choose who follows them: there is no way to deal with abusive users. A way to block them may be needed in the future.
