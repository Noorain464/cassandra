from fastapi import HTTPException, status
import uuid
from app.models.cassandra_models import ConversationModel
from app.schemas.conversation import ConversationResponse, PaginatedConversationResponse

class ConversationController:
    """
    Controller for handling conversation operations
    This is a stub that students will implement
    """
    
    async def get_user_conversations(
        self, 
        user_id: int, 
        page: int = 1, 
        limit: int = 20
    ) -> PaginatedConversationResponse:
        """
        Get all conversations for a user with pagination
        
        Args:
            user_id: ID of the user
            page: Page number
            limit: Number of conversations per page
            
        Returns:
            Paginated list of conversations
            
        Raises:
            HTTPException: If user not found or access denied
        """
        # This is a stub - students will implement the actual logic
        try:
            conversations = await ConversationModel.get_user_conversations(user_id, limit)
            return PaginatedConversationResponse(
                total=len(conversations),
                page=page,
                limit=limit,
                data=[ConversationResponse(**c) for c in conversations]
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get conversations: {str(e)}")
    
    async def get_conversation(self, conversation_id: uuid.UUID) -> ConversationResponse:
        """
        Get a specific conversation by ID
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            Conversation details
            
        Raises:
            HTTPException: If conversation not found or access denied
        """
        # This is a stub - students will implement the actual logic
        try:
            conversation = await ConversationModel.get_conversation(conversation_id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
            print(conversation)
            return ConversationResponse(**conversation)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get conversation: {str(e)}")