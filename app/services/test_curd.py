# test_crud.py
import sys
import os
import uuid
from datetime import datetime
from sqlalchemy import text

# Import database connection
from app.db.database import get_db, engine, Base

# Import models and crud operations
from app.models.models import (
    UserInfo, MasterChat, MasterMessage, ForumBoard,
    ForumArticle, ForumComment, UserMessage
)
import app.CRUD.crud as crud


def test_database_connection():
    """Test the database connection."""
    try:
        # Try executing a simple query
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            for row in result:
                print(f"Database connection successful. Test query result: {row[0]}")
            return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False


def test_user_operations():
    """Test user CRUD operations."""
    print("\n=== Testing User Operations ===")

    # Generate a unique user ID and email
    test_user_id = f"test_{uuid.uuid4().hex[:8]}"
    test_email = f"{test_user_id}@example.com"

    # Create a new user
    with get_db() as db:
        print(f"Creating test user with ID: {test_user_id}")
        user_data = {
            "user_id": test_user_id,
            "nick_name": "def",
            "email": test_email,
            "password": "test_password",
            "sex": 1,
            "person_description": "This is a test user",
            "join_time": datetime.now(),
            "status": 1
        }

        user = crud.create_user(db, user_data)
        print(f"User created: {user.nick_name} (ID: {user.user_id})")

        # Get the user by ID
        retrieved_user = crud.get_user(db, test_user_id)
        if retrieved_user:
            print(f"Retrieved user: {retrieved_user.nick_name} (Email: {retrieved_user.email})")
        else:
            print("Failed to retrieve user by ID")

        # Update the user
        update_data = {
            "person_description": "Updated description",
            "last_login_time": datetime.now()
        }
        updated_user = crud.update_user(db, test_user_id, update_data)
        if updated_user:
            print(f"Updated user description: {updated_user.person_description}")
        else:
            print("Failed to update user")

        # Clean up - delete the test user
        deleted = crud.delete_user(db, test_user_id)
        print(f"Test user deleted: {deleted}")


def test_board_operations():
    """Test forum board operations."""
    print("\n=== Testing Board Operations ===")

    with get_db() as db:
        # Create a parent board
        parent_board_data = {
            "board_name": "Test Parent Board",
            "board_desc": "This is a test parent board",
            "sort": 1,
            "post_type": True,
            "p_board_id": 0,  # No parent
            "cover": "test_cover.jpg"
        }

        parent_board = crud.create_board(db, parent_board_data)
        print(f"Created parent board: {parent_board.board_name} (ID: {parent_board.board_id})")

        # Create a child board
        child_board_data = {
            "board_name": "Test Child Board",
            "board_desc": "This is a test child board",
            "sort": 1,
            "post_type": True,
            "p_board_id": parent_board.board_id,  # Set parent ID
            "cover": "test_child_cover.jpg"
        }

        child_board = crud.create_board(db, child_board_data)
        print(f"Created child board: {child_board.board_name} (ID: {child_board.board_id})")

        # Get all boards
        boards = crud.get_boards(db)
        print(f"Total boards: {len(boards)}")

        # Get child boards
        child_boards = crud.get_boards(db, p_board_id=parent_board.board_id)
        print(f"Child boards of parent {parent_board.board_id}: {len(child_boards)}")

        # Clean up - delete the boards
        deleted_child = crud.delete_board(db, child_board.board_id)
        deleted_parent = crud.delete_board(db, parent_board.board_id)
        print(f"Boards deleted: child={deleted_child}, parent={deleted_parent}")


def test_article_operations():
    """Test forum article operations."""
    print("\n=== Testing Article Operations ===")

    # First create a test user and board
    test_user_id = f"test_{uuid.uuid4().hex[:8]}"

    with get_db() as db:
        # Create test user
        user_data = {
            "user_id": test_user_id,
            "nick_name": f"abcd",
            "email": f"{test_user_id}@example.com",
            "password": "test_password",
            "status": 1
        }
        user = crud.create_user(db, user_data)

        # Create test board
        board_data = {
            "board_name": "Test Board",
            "board_desc": "Test board for articles",
            "sort": 1,
            "post_type": True,
            "p_board_id": 0
        }
        board = crud.create_board(db, board_data)

        # Create an article
        article_id = f"{uuid.uuid4().hex[:8]}"
        article_data = {
            "article_id": article_id,
            "board_id": board.board_id,
            "board_name": board.board_name,
            "p_board_id": board.p_board_id,
            "p_board_name": "Parent Board",
            "user_id": user.user_id,
            "nick_name": user.nick_name,
            "user_ip_address": "127.0.0.1",
            "title": "Test Article",
            "content": "This is a test article content",
            "markdown_content": "# Test Article\n\nThis is a test article content",
            "editor_type": 1,
            "summary": "Test article summary",
            "status": 1
        }

        article = crud.create_article(db, article_data)
        print(f"Created article: {article.title} (ID: {article.article_id})")

        # Increment view count
        crud.increment_article_view(db, article_id)

        # Get the article
        retrieved_article = crud.get_article(db, article_id)
        print(f"Retrieved article: {retrieved_article.title} (Views: {retrieved_article.read_count})")

        # Create a comment
        comment_data = {
            "article_id": article_id,
            "content": "This is a test comment",
            "user_id": user.user_id,
            "nick_name": user.nick_name,
            "user_ip_address": "127.0.0.1",
            "p_comment_id": 0,
            "status": 1
        }

        comment = crud.create_comment(db, comment_data)
        print(f"Created comment ID: {comment.comment_id}")

        # Get article comments
        comments = crud.get_comments_by_article(db, article_id)
        print(f"Article has {len(comments)} comments")

        # Check article comment count was incremented
        article_updated = crud.get_article(db, article_id)
        print(f"Article comment count: {article_updated.comment_count}")

        # Clean up - delete the comment, article, board, and user
        crud.delete_comment(db, comment.comment_id)
        crud.hard_delete_article(db, article_id)
        crud.delete_board(db, board.board_id)
        crud.delete_user(db, test_user_id)
        print("Test data cleaned up")


def test_chat_operations():
    """Test chat and message operations."""
    print("\n=== Testing Chat Operations ===")

    # Create a test user
    test_user_id = f"test_{uuid.uuid4().hex[:8]}"

    with get_db() as db:
        # Create test user
        user_data = {
            "user_id": test_user_id,
            "nick_name": f"abce",
            "email": f"{test_user_id}@example.com",
            "password": "test_password",
            "status": 1
        }
        user = crud.create_user(db, user_data)

        # Create a chat
        chat_id = f"chat_{uuid.uuid4().hex[:12]}"
        chat_data = {
            "chat_id": chat_id,
            "title": "Test Chat",
            "user_id": user.user_id
        }

        chat = crud.create_chat(db, chat_data)
        print(f"Created chat: {chat.title} (ID: {chat.chat_id})")

        # Add messages to the chat
        message1_data = {
            "role": "user",
            "content": "Hello, this is a test message",
            "user_id": user.user_id,
            "chat_id": chat_id
        }

        message2_data = {
            "role": "assistant",
            "content": "This is a test response",
            "user_id": user.user_id,
            "chat_id": chat_id
        }

        message1 = crud.create_message(db, message1_data)
        message2 = crud.create_message(db, message2_data)

        print(f"Created messages: {message1.id}, {message2.id}")

        # Get chat messages
        messages = crud.get_messages_by_chat(db, chat_id)
        print(f"Chat has {len(messages)} messages")

        # Clean up
        for message in messages:
            crud.delete_message(db, message.id)

        crud.delete_chat(db, chat_id)
        crud.delete_user(db, test_user_id)
        print("Test data cleaned up")


def main():
    """Main function to run tests."""
    print("Testing database connection and CRUD operations...")

    if not test_database_connection():
        print("Database connection failed. Exiting.")
        sys.exit(1)

    # Run tests
    try:
        test_user_operations()
        test_board_operations()
        test_article_operations()
        test_chat_operations()

        print("\nAll tests completed successfully!")
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()