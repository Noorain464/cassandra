

CREATE TABLE conversations (
    id UUID PRIMARY KEY,
    user1_id INT,
    user2_id INT,
    last_message_at TIMESTAMP,
    last_message_content TEXT
)

CREATE TABLE messages (
    id UUID,
    conversation_id UUID,
    sender_id INT,
    receiver_id INT,
    content TEXT,
    created_at TIMESTAMP,
    PRIMARY KEY ((conversation_id), created_at)
) WITH CLUSTERING ORDER BY (created_at DESC)