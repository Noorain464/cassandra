"""
Script to generate test data for the Messenger application.
This script is a skeleton for students to implement.
"""
import os
import uuid
import logging
import random
from datetime import datetime, timedelta
from cassandra.cluster import Cluster

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cassandra connection settings
CASSANDRA_HOST = os.getenv("CASSANDRA_HOST", "localhost")
CASSANDRA_PORT = int(os.getenv("CASSANDRA_PORT", "9042"))
CASSANDRA_KEYSPACE = os.getenv("CASSANDRA_KEYSPACE", "messenger")

# Test data configuration
NUM_USERS = 10  # Number of users to create
NUM_CONVERSATIONS = 15  # Number of conversations to create
MAX_MESSAGES_PER_CONVERSATION = 50  # Maximum number of messages per conversation

def connect_to_cassandra():
    """Connect to Cassandra cluster."""
    logger.info("Connecting to Cassandra...")
    try:
        cluster = Cluster([CASSANDRA_HOST])
        session = cluster.connect(CASSANDRA_KEYSPACE)
        logger.info("Connected to Cassandra!")
        return cluster, session
    except Exception as e:
        logger.error(f"Failed to connect to Cassandra: {str(e)}")
        raise

def generate_test_data(session):
    """
    Generate test data in Cassandra.
    
    Students should implement this function to generate test data based on their schema design.
    The function should create:
    - Users (with IDs 1-NUM_USERS)
    - Conversations between random pairs of users
    - Messages in each conversation with realistic timestamps
    """
    logger.info("Generating test data...")
    
    # TODO: Students should implement the test data generation logic
    # Hint:
    # 1. Create a set of user IDs
    # 2. Create conversations between random pairs of users
    # 3. For each conversation, generate a random number of messages
    # 4. Update relevant tables to maintain data consistency
      # Step 1: Create user UUIDs
    user_ids = [uuid.uuid4() for _ in range(NUM_USERS)]

    # Step 2: Create conversations between random pairs
    conversation_ids = []
    for _ in range(NUM_CONVERSATIONS):
        user1, user2 = random.sample(user_ids, 2)
        conversation_id = uuid.uuid4()
        conversation_ids.append((conversation_id, user1, user2))

        last_message_at = datetime.utcnow()
        last_message_content = "Initial message"

        session.execute("""
            INSERT INTO conversations (id, user1_id, user2_id, last_message_at, last_message_content)
            VALUES (%s, %s, %s, %s, %s)
        """, (conversation_id, user1, user2, last_message_at, last_message_content))

        # Step 3: Generate messages
        num_messages = random.randint(1, MAX_MESSAGES_PER_CONVERSATION)
        for i in range(num_messages):
            message_id = uuid.uuid4()
            sender_id, receiver_id = random.sample([user1, user2], 2)
            content = f"Test message {i + 1}"
            created_at = datetime.utcnow() - timedelta(minutes=random.randint(0, 10000))

            session.execute("""
                INSERT INTO messages (id, conversation_id, sender_id, receiver_id, content, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (message_id, conversation_id, sender_id, receiver_id, content, created_at))

    
    logger.info(f"Generated {NUM_CONVERSATIONS} conversations with messages")
    logger.info(f"User IDs range from 1 to {NUM_USERS}")
    logger.info("Use these IDs for testing the API endpoints")

def main():
    """Main function to generate test data."""
    cluster = None
    
    try:
        # Connect to Cassandra
        cluster, session = connect_to_cassandra()
        
        # Generate test data
        generate_test_data(session)
        
        logger.info("Test data generation completed successfully!")
    except Exception as e:
        logger.error(f"Error generating test data: {str(e)}")
    finally:
        if cluster:
            cluster.shutdown()
            logger.info("Cassandra connection closed")

if __name__ == "__main__":
    main() 