from fastmcp import FastMCP
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
#starlette is a fast api framework
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastmcp.server.auth import BearerAuthProvider
from fastmcp.server.dependencies import get_access_token, AccessToken
from database import NoteRepository

import os

#load environment variables
load_dotenv()

#fastmcp makes easy to implement auth protical for mcp server
auth = BearerAuthProvider(
    jwks_uri=f"{os.getenv('STYTCH_DOMAIN')}/.well-known/jwks.json", #url to confirm the token is valid
    issuer=os.getenv("STYTCH_DOMAIN"),
    algorithm="RS256",
    audience=os.getenv("STYTCH_PROJECT_ID"),
)

#Building a notes tool that makes it easy for users to create notes and retrieve them

mcp = FastMCP(name="Notes App", version="1.0.0", auth=auth)

# doc screen in triple quotes is important for the MCP client to know what the tool does
#using database functions defined in database.py to add, retrieve, and delete notes
@mcp.tool
def get_my_notes() -> str:
    """Get all notes for the current user"""
    access_token: AccessToken = get_access_token()
    user_id = access_token.client_id

    notes = NoteRepository.get_notes_by_user(user_id)
    if not notes:
        return "no notes found"
    result = "Your notes:\n"

    for note in notes:
        result += f"{note.id}: {note.title}\nContent: {note.content}\n\n"
    return result

@mcp.tool
def add_note(title: str, content: str) -> str:
    """Add a note to the current user's notes"""
    access_token: AccessToken = get_access_token()
    user_id = access_token.client_id

    note = NoteRepository.create_note(user_id, title,content)
    return f"Note added: {note.content}"

@mcp.tool
def delete_note(note_id: int) -> str:
    """Delete a note from the current user's notes"""
    access_token: AccessToken = get_access_token()
    user_id = access_token.client_id

    note = NoteRepository.delete_note(note_id)

    return f"Note deleted: {note_id}"

@mcp.custom_route("/.well-known/oauth-protected-resource", methods=["GET", "OPTIONS"])
def oauth_metadata(request: Request) -> JSONResponse:
    base_url = str(request.base_url).rstrip("/") #so know client url to return the response
    return JSONResponse(
        {
            "resource": base_url,
            "authorization_servers": [os.getenv("STYTCH_DOMAIN")], #telling mcp server where auth server is
            "scopes_supported": ["read", "write"], #changes consent screen user sees
            "bearer_methods_supported": ["header", "body"], #options for where to look for the token
        }
    )

if __name__ == "__main__":
    mcp.run(
        transport="http",
        host="127.0.0.1", #localhost
        port=8000,
        middleware=[ #middleware is to connect to server when not on the same local host & allow anyone to connect to the server
            Middleware(
                CORSMiddleware,
                allow_origins=["*"],
                allow_credentials=True,
                allow_methods=["*"],
                allow_headers=["*"],
            )
        ],
        # reload=True,
        # reload_delay=1,
        # reload_dirs=["."],
        # reload_excludes=["*.pyc", "*.pyo", "*.pyd", "*.pyw", "*.pyz"],
        # reload_includes=["*.py"],
        # reload_ignore_patterns=["*.pyc", "*.pyo", "*.pyd", "*.pyw", "*.pyz"],
    )

    #uv run python ./main.py, ngrok http 8000, && claude transport before starting claude
    #Claude Code does not support running the server over "http" on localhost, so need ngrok to run the server over the internet
    #ngrok is a tool that creates a tunnel to the server so that it can be accessed from the internet
    # add /mcp to the url provided by ngrok to point to the mcp server on the local host (for the calude mcp add --transport http command)
    # allow dynamic client registration & enter http://localhost:5173 as url in the management > connected apps > settings section of stytch dashboard
    ##this url is where the front end is locally, to aloow the user to consent to auth since this app has it's own identity provider ;  but can use actual host url in production
    #in the stytch project, can go to Frontend SDK to enable SDK in test; ; edit domains under authorizded aplications to http://localhost:5173, then click on Javascript SDK to go to docs and get option for vanilla, next or react SDKs
    #front end is in the frontend folder, created using vite (npm create vite@latest -- frontend) and chose React as the framework and Javascript as the variant
    # also used npm i @stytch/react to install the stytch react sdk in the frontend folder
    # npm i @stytch/vanilla to install the stytch vanilla sdk in the frontend folder
    # can remove the assets folder from the react app/frontend folder and clear contents within the return statement in the app.jsx file