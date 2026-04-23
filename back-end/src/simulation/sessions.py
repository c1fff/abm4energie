import uuid
from collections import OrderedDict

# Module-level in-memory session storage
# Structure: { session_id: { "graph": graph, "agent_history": {...}, "timestamp": float } }
sessions = OrderedDict()
MAX_SESSIONS = 20


def store_session(graph, agent_history) -> str:
    """
    Store a session in memory.
    
    Returns:
    - session_id: Unique session identifier
    """
    session_id = str(uuid.uuid4())
    
    # If we've reached max sessions, remove the oldest
    if len(sessions) >= MAX_SESSIONS:
        sessions.popitem(last=False)  # Remove oldest item (FIFO with OrderedDict)
    
    sessions[session_id] = {
        "graph": graph,
        "agent_history": agent_history,
        "timestamp": __import__('time').time()
    }
    
    return session_id


def get_session(session_id: str) -> dict:
    """
    Retrieve a session by ID.
    
    Returns:
    - session data or None if not found
    """
    return sessions.get(session_id)


def session_exists(session_id: str) -> bool:
    """Check if session exists."""
    return session_id in sessions
