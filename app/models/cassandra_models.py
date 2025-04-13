"""
Sample models for interacting with Cassandra tables.
Students should implement these models based on their database schema design.
"""
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

from app.db.cassandra_client import cassandra_client

class MessageModel:
    """
    Message model for interacting with the messages table.
    Students will implement this as part of the assignment.
    
    They should consider:
    - How to efficiently store and retrieve messages
    - How to handle pagination of results
    - How to filter messages by timestamp
    """
    
    # TODO: Implement the following methods
    
    @staticmethod
    async def create_message(content: str, sender_id: int, receiver_id: int, conversation_id: uuid.UUID) -> uuid.UUID:
        """
        Create a new message.
        
        Students should decide what parameters are needed based on their schema design.
        """
        # This is a stub - students will implement the actual logic
        created_at = datetime.utcnow()
        message_id = uuid.uuid4()

        query = """
        INSERT INTO messages (conversation_id, created_at, message_id, sender_id, receiver_id, content)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        await cassandra_client.execute(
            query, (conversation_id, created_at, message_id, sender_id, receiver_id, content)
        )
        return message_id
    
    @staticmethod
    async def get_conversation_messages(conversation_id: uuid.UUID, page: int = 1, limit: int = 20) -> List[dict]:
        """
        Get messages for a conversation with pagination.
        
        Students should decide what parameters are needed and how to implement pagination.
        """
        # This is a stub - students will implement the actual logic
        query = """
        SELECT * FROM messages WHERE conversation_id = %s
        LIMIT %s
        """
        result = await cassandra_client.execute(query, (conversation_id, limit))
        return [row._asdict() for row in result.current_rows]
    
    @staticmethod
    async def get_messages_before_timestamp(conversation_id: uuid.UUID, before_timestamp: datetime, limit: int = 20) -> List[dict]:
        """
        Get messages before a timestamp with pagination.
        
        Students should decide how to implement filtering by timestamp with pagination.
        """
        # This is a stub - students will implement the actual logic
        query = """
        SELECT * FROM messages
        WHERE conversation_id = %s AND created_at < %s
        LIMIT %s
        """
        result = await cassandra_client.execute(query, (conversation_id, before_timestamp, limit))
        return [row._asdict() for row in result.current_rows]


class ConversationModel:
    """
    Conversation model for interacting with the conversations-related tables.
    Students will implement this as part of the assignment.
    
    They should consider:
    - How to efficiently store and retrieve conversations for a user
    - How to handle pagination of results
    - How to optimize for the most recent conversations
    """
    
    # TODO: Implement the following methods
    
    @staticmethod
    async def get_user_conversations(user_id: int, limit: int = 20) -> List[dict]:
        """
        Get conversations for a user with pagination.
        
        Students should decide what parameters are needed and how to implement pagination.
        """
        # This is a stub - students will implement the actual logic
        query = """
        SELECT * FROM conversations
        WHERE user1_id = %s OR user2_id = %s
        ALLOW FILTERING
        """
        result = await cassandra_client.execute(query, (user_id, user_id))
        rows = result.current_rows[:limit]
        return [row._asdict() for row in rows]
    
    @staticmethod
    async def get_conversation(conversation_id: uuid.UUID) -> Optional[dict]:
        """
        Get a conversation by ID.
        
        Students should decide what parameters are needed and what data to return.
        """
        # This is a stub - students will implement the actual logic
        query = """
        SELECT * FROM conversations WHERE conversation_id = %s
        """
        result = await cassandra_client.execute(query, (conversation_id,))
        row = result.one()
        return row._asdict() if row else None
    
    @staticmethod
    async def create_or_get_conversation(user1_id: int, user2_id: int) -> uuid.UUID:
        """
        Get an existing conversation between two users or create a new one.
        
        Students should decide how to handle this operation efficiently.
        """
        # This is a stub - students will implement the actual logic
        u1, u2 = sorted((user1_id, user2_id))

        # Try to find conversation
        query = """
        SELECT conversation_id FROM conversations
        WHERE user1_id = %s AND user2_id = %s
        ALLOW FILTERING
        """
        result = await cassandra_client.execute(query, (u1, u2))

        if result.one():
            return result.one().conversation_id

        # Otherwise create new
        conversation_id = uuid.uuid4()
        insert_query = """
        INSERT INTO conversations (conversation_id, user1_id, user2_id, last_message_at)
        VALUES (%s, %s, %s, %s)
        """
        await cassandra_client.execute(insert_query, (conversation_id, u1, u2, datetime.utcnow()))
        return conversation_id 