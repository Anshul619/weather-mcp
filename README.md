## Git Clone

````shell
git clone weather-mcp
cd weather-mcp
````

## Create and activate virtual environment

````shell
python3 -m venv .venv
source .venv/bin/activate
````

# Install Dependencies

````shell
pip install -r requirements.txt
````

# Run the server

````shell
source .venv/bin/activate
python weather_server.py
````

# Config for VS Code (Copilot)
- Add this to `~/.vscode/mcp.json` and restart VS code


````json
{
  "servers": {
    "WeatherMCP": {
      "type": "stdio",
      "command": "python",
      "args": ["path/to/weather_server.py"]
    }
  }
}
````

# Restart VS Code
- Quit and relaunch VS Code.
- Open the Copilot sidebar.
- You should now see WeatherMCP listed as an available MCP server.

# Verify Copilot sees your MCP server
- Open VS Code Command Palette (Cmd+Shift+P on Mac, Ctrl+Shift+P on Windows).
- Search for `Copilot: List MCP Servers` (this command was added when MCP support shipped).
- You should see WeatherMCP in the list.

If it’s missing:
- Check that your `mcp.json` path is correct.
- Check the log: View → Output → Copilot (dropdown) for MCP errors.


# Try it out

```shell
/weather get_weather {"city": "London"}
/weather get_forecast {"city": "London"}
/weather get_alerts {"state": "CA"}
```

Or just ask:

```
“Ask the WeatherMCP server for the weather in London.”
```

# Debugging tips
- If Copilot doesn’t show your server: check `~/.vscode/mcp.json` syntax (must be valid JSON).
- If the server crashes: run `python weather_server.py` manually in a terminal to see errors.
- You can also add debug `print()` calls in `handle_tool_call` to see incoming requests.

# Optional - Config for Claude Desktop
- Add this to `~/.mcp.json`

````json
{
  "servers": {
    "WeatherMCP": {
      "command": "python",
      "args": ["path/to/weather_server.py"],
      "type": "stdio"
    }
  }
}
````