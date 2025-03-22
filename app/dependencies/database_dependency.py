from app.db.database import get_db_session

# Re-export for API use
get_db = get_db_session