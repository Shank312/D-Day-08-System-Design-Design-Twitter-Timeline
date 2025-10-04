

USE timeline;

CREATE TABLE IF NOT EXISTS home_timeline (
  user_id text,
  created_at timeuuid,
  tweet_id text,
  celeb boolean,
  PRIMARY KEY (user_id, created_at)
) WITH CLUSTERING ORDER BY (created_at DESC);
