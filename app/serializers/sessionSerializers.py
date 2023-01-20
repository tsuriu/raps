from app.serializers.userSerializers import embeddedUserResponse

def sessionEntity(session) -> dict:
    return {
        "id": str(session["_id"]),
        "user": str(session["user"]),
        "key": session["key"],
        #"active": session["active"],
        "parent": str(session["parent"]),
        "client_host": str(session["client_host"]),
        "client_port": session["client_port"],
        "created_at": session["created_at"],
        "refreshed_at": session["refreshed_at"]
    }

def populateSessionEntity(session) -> dict:
    return {
        "id": str(session["_id"]),
        "user": embeddedUserResponse(session["user"]),
        "key": session["key"],
        #"active": session["active"],
        "parent": str(session["parent"]),
        "client_host": str(session["client_host"]),
        "client_port": session["client_port"],
        "created_at": session["created_at"],
        "refreshed_at": session["refreshed_at"]
    }

def embeddedSessionResponse(session) -> dict:
    return {
        "id": str(session["_id"]),
        "user": embeddedUserResponse(session["user"]),
        "key": session["key"],
        #"active": session["active"],
        "parent": str(session["parent"]),
        "client_host": str(session["client_host"]),
        "client_port": session["client_port"],
        "created_at": session["created_at"],
        "refreshed_at": session["refreshed_at"]
    }

def sessionResponseEntity(session) -> dict:
    return {
        "id": str(session["_id"]),
        "user": str(session["user"]),
        "key": session["key"],
        #"active": session["active"],
        "parent": str(session["parent"]),
        "client_host": str(session["client_host"]),
        "client_port": session["client_port"],
        "created_at": session["created_at"],
        "refreshed_at": session["refreshed_at"]
    }

def sessionListEntity(sessions) -> list:
    return [sessionResponseEntity(session) for session in sessions]