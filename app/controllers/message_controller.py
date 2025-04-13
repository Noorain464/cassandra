from typing import Optional
from datetime import datetime
from fastapi import HTTPException, status
import uuid
from app.models.cassandra_models import ConversationModel, MessageModel
from app.schemas.message import MessageCreate, MessageResponse, PaginatedMessageResponse

class MessageController:
    """
    Controller for handling message operations
    This is a stub that students will implement
    """
    
    async def send_message(self, message_data: MessageCreate) -> MessageResponse:
        """
        Send a message from one user to another
        
        Args:
            message_data: The message data including content, sender_id, and receiver_id
            
        Returns:
            The created message with metadata
        
        Raises:
            HTTPException: If message sending fails
        """
        # This is a stub - students will implement the actual logic
        try:
            conversation_id = await ConversationModel.create_or_get_conversation(
                user1_id=message_data.sender_id,
                user2_id=message_data.receiver_id
            )
            
            print("{con}")
            created_at = datetime.utcnow()

            # Insert into messages table
            message_id = await MessageModel.create_message(
                content=message_data.content,
                sender_id=message_data.sender_id,
                receiver_id=message_data.receiver_id,
                conversation_id=conversation_id
            )
            return MessageResponse(
                id=str(message_id),
                conversation_id=str(conversation_id),
                sender_id=message_data.sender_id,
                receiver_id=message_data.receiver_id,
                content=message_data.content,
                created_at=created_at
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")
    
    async def get_conversation_messages(
        self, 
        conversation_id: uuid.UUID, 
        page: int = 1, 
        limit: int = 20
    ) -> PaginatedMessageResponse:
        """
        Get all messages in a conversation with pagination
        
        Args:
            conversation_id: ID of the conversation
            page: Page number
            limit: Number of messages per page
            
        Returns:
            Paginated list of messages
            
        Raises:
            HTTPException: If conversation not found or access denied
        """
        # This is a stub - students will implement the actual logic
        try:
            messages = await MessageModel.get_conversation_messages(conversation_id, page, limit)
            return PaginatedMessageResponse(
                total=len(messages),
                page=page,
                limit=limit,
                data=[MessageResponse(**msg) for msg in messages]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")
    
    async def get_messages_before_timestamp(
        self, 
        conversation_id: uuid.UUID, 
        before_timestamp: datetime,
        page: int = 1, 
        limit: int = 20
    ) -> PaginatedMessageResponse:
        """
        Get messages in a conversation before a specific timestamp with pagination
        
        Args:
            conversation_id: ID of the conversation
            before_timestamp: Get messages before this timestamp
            page: Page number
            limit: Number of messages per page
            
        Returns:
            Paginated list of messages
            
        Raises:
            HTTPException: If conversation not found or access denied
        """
        # This is a stub - students will implement the actual logic
        try:
            messages = await MessageModel.get_messages_before_timestamp(
                conversation_id=conversation_id,
                before_timestamp=before_timestamp,
                limit=limit
            )
            return PaginatedMessageResponse(
                total=len(messages),
                page=page,
                limit=limit,
                data=[MessageResponse(**msg) for msg in messages]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error fetching messages: {str(e)}")