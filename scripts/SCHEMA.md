CREATE TABLE users(
user_id UUID,
email TEXT,
password TEXT,
time_created TIMESTAMP
PRIMARY KEY(user_id)
)

CREATE TABLE conversations (
user_id UUID,
conversation_id UUID,
last_message_timestamp TIMESTAMP,
PRIMARY KEY (user_id, last_message_timestamp)
) WITH CLUSTERING ORDER BY (last_message_timestamp DESC);

CREATE TABLE messages (
conversation_id UUID,
message_id UUID,
sender_id UUID,
recipient_id UUID,
message_body TEXT,
timestamp TIMESTAMP,
PRIMARY KEY ((conversation_id), timestamp)
) WITH CLUSTERING ORDER BY (timestamp DESC);