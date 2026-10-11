# Traffic Flow Simulator

This project is a 3D traffic-flow simulator based on the original PyOpenGL
course project. It exposes the simulation as a **Model Context Protocol (MCP)**
server so an MCP-compatible AI client can inspect and control the traffic scene.

## MCP tools

- `get_simulation_status` returns all cars and current simulator flags.
- `set_signal` and `set_auto_signal` control the traffic light.
- `set_paused` and `set_speed_boost` control movement.
- `advance_simulation` advances up to 1,000 frames.
- `inspect_car` reports one car's lane, speed, and distance to the car ahead.
- `reset_simulation` restores the deterministic starting scene.

## Setup

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
```

The MCP server uses stdio transport:

```powershell
traffic-mcp
```

For an MCP client configuration, point the command at the repository's virtual
environment executable:

```json
{
  "mcpServers": {
    "traffic-flow": {
      "command": "F:\\path\\to\\Computer-Graphics-Gaming-Project\\.venv\\Scripts\\traffic-mcp.exe"
    }
  }
}
```

## Tests

```powershell
python -m unittest discover -s tests
```

## Graphics controls

The included OpenGL visual client supports manual signal control (`G`/`R`),
automatic signals (`A`), speed boost (`V`), pause (`B`), night-mode state
switching (`N`), and camera movement with the arrow keys. Press `Q` to quit.

PyOpenGL/GLUT availability depends on the operating system. The MCP model is
headless and can be tested without an OpenGL context.

Launch the included visual client with:

```powershell
python -m traffic_mcp.visual_client
```

## Project layout

```text
src/traffic_mcp/model.py   # deterministic simulation state
src/traffic_mcp/server.py  # MCP tools and stdio entry point
src/traffic_mcp/visual_client.py # PyOpenGL visual client
tests/test_model.py        # model behavior tests
```