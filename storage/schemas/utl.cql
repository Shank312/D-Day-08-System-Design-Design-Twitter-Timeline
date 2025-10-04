

USE timeline;

CREATE TABLE IF NOT EXISTS user_timeline (
  user_id text,
  created_at timeuuid,
  tweet_id text,
  PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);
