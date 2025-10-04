

CREATE KEYSPACE IF NOT EXISTS timeline WITH replication = {'class':'SimpleStrategy','replication_factor':1};

USE timeline;

CREATE TABLE IF NOT EXISTS tweets (
  tweet_id text PRIMARY KEY,
  author_id text,
  text text,
  created_at timestamp
);
