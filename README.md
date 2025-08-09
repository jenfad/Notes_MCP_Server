# MCP Server Creation - Notes App

A full-stack application that demonstrates how to create a Model Context Protocol (MCP) server with authentication, a React frontend, and a Python backend with SQLite database.

https://www.loom.com/share/12b6eeecdc404862a03cf5c804315aaa?sid=d9a7c09c-4356-4092-8fc8-3a1b6123e071

## 🏗️ Project Architecture

This project consists of three main components:
- **Backend**: Python FastMCP server with SQLite database
- **Frontend**: React application with Stytch authentication
- **External Services**: Stytch for authentication, ngrok for tunneling

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- Node.js 18+
- ngrok CLI tool
- Stytch account and project

### Backend Setup
```bash
cd backend
uv sync  # Install Python dependencies
uv run python main.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### Start ngrok Tunnel
```bash
ngrok http 8000
```

## 🔧 Backend (Python FastMCP Server)

The backend is built using FastMCP, a framework for creating MCP servers with built-in authentication support.

### Key Features
- **FastMCP Server**: Implements the Model Context Protocol
- **SQLite Database**: Stores user notes with SQLAlchemy ORM
- **JWT Authentication**: Uses Stytch for secure user authentication
- **CORS Support**: Configured for cross-origin requests

### Database Schema
```python
class Note(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
```

### MCP Tools Available
- `get_my_notes()`: Retrieve all notes for the authenticated user
- `add_note(title, content)`: Create a new note
- `delete_note(note_id)`: Remove a note by ID

### Dependencies
- `fastmcp>=2.10.6`: MCP server framework
- `sqlalchemy>=2.0.42`: Database ORM
- `stytch>=13.12.0`: Authentication service
- `dotenv>=0.9.9`: Environment variable management

## 🎨 Frontend (React + Stytch)

The frontend is a React application built with Vite that provides a user interface for authentication and note management.

### Key Features
- **Stytch Authentication**: password-based login
- **Responsive Design**: Centered layout with modern styling
- **Protected Routes**: Authentication-based access control

### Authentication Providers
- Password-based authentication
- Note: need to set redirect urls with Stytch if using Magic link or Oauth authentication



### Dependencies
- `@stytch/react`: Stytch React SDK
- `react`: React framework
- `vite`: Build tool and dev server

## 🔐 External Services Setup

### Stytch Authentication

1. **Create Stytch Project**
   - Sign up at [stytch.com](https://stytch.com)
   - Create a new project
   - Note your Project ID, Secret and Domain

2. **Configure Frontend SDK**
   - Go to Frontend SDK in Stytch dashboard
   - Enable SDK in test mode
   - Add authorized domains (e.g., `http://localhost:5173` for development)

3. **Environment Variables**
   Create a `.env` file in the backend directory:
   ```env
   STYTCH_DOMAIN=https://your-project.stytch.com
   STYTCH_PROJECT_ID=your-project-id
   ```

4. **OAuth Configuration**
   - Configure OAuth providers (Google, Facebook)
   - Set redirect URLs for login/signup
   - Enable dynamic client registration

### ngrok Tunneling

ngrok creates a secure tunnel to your local server, making it accessible from the internet.

1. **Install ngrok**
   ```bash
   # macOS
   brew install ngrok
   
   # Or download from https://ngrok.com/
   ```

2. **Start Tunnel**
   ```bash
   ngrok http 8000
   ```

3. **Use Tunnel URL**
   - Copy the HTTPS URL provided by ngrok
   - Add `/mcp` to the URL when configuring Claude
   - Example: `https://abc123.ngrok-free.app/mcp`

## 🤖 Claude MCP Integration

To connect Claude to your MCP server:

1. **Start Backend**: `uv run python main.py`
2. **Start ngrok**: `ngrok http 8000`
3. **Add MCP Server in Claude**:
   ```bash
   claude mcp add --transport http --url https://your-ngrok-url.ngrok-free.app/mcp
   ```
4. **Authentication with Claude**: 'claude' then run /mcp to authenticate 

## 📁 Project Structure

```
MCP_Server_Creation/
├── backend/
│   ├── main.py              # FastMCP server entry point
│   ├── database.py          # Database models and repository
│   ├── pyproject.toml       # Python dependencies
│   └── notes.db            # SQLite database file
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # Main React component
│   │   └── main.jsx        # React entry point
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
└── README.md               # This file
```

## 🔄 Development Workflow

1. **Backend Development**
   - Make changes to `main.py` or `database.py`
   - Restart the server: `uv run python main.py`

2. **Frontend Development**
   - Make changes to React components
   - Vite will hot-reload automatically

3. **Testing MCP Integration**
   - Ensure backend is running
   - Ensure ngrok tunnel is active
   - Test MCP tools through Claude

## 🚨 Important Notes

- **Localhost Limitation**: Claude Code doesn't support localhost MCP servers, ngrok can help redirect an external uri to a local port
- **ngrok Required**: Always use ngrok for external access during development
- **Stytch Configuration**: Ensure authorized domains match your development URLs
- **Environment Variables**: Keep `.env` file secure and either never commit to version control OR remove secrets before committing

## 🆘 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed with `uv sync`
2. **Authentication Failures**: Check Stytch project configuration and environment variables
3. **CORS Errors**: Verify CORS middleware configuration in backend
4. **ngrok Connection Issues**: Ensure backend is running on port 8000 before starting ngrok

### Getting Help

- Check Stytch documentation: [docs.stytch.com](https://docs.stytch.com)
- FastMCP documentation: [github.com/fastmcp/fastmcp](https://github.com/fastmcp/fastmcp)
- ngrok documentation: [ngrok.com/docs](https://ngrok.com/docs)
