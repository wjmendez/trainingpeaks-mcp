"""Protocol-level tests: drive the real MCP server through an in-memory client.

The functional tests call ``list_tools`` / ``call_tool`` directly. These tests
make sure the handlers are actually wired into the ``Server`` instance, which
is the part that breaks when the ``mcp`` SDK changes its registration API.
"""

import json

from mcp.client import Client

from tp_mcp.server import TOOLS, server


async def test_list_tools_over_protocol():
    async with Client(server) as client:
        result = await client.list_tools()

    assert {t.name for t in result.tools} == {t.name for t in TOOLS}


async def test_call_tool_over_protocol_returns_validation_error():
    async with Client(server) as client:
        result = await client.call_tool("tp_get_workouts", {"start_date": "nope", "end_date": "2025-01-01"})

    payload = json.loads(result.content[0].text)
    assert payload["error_code"] == "VALIDATION_ERROR"


async def test_call_tool_over_protocol_unknown_tool():
    async with Client(server) as client:
        result = await client.call_tool("nonexistent_tool", {})

    payload = json.loads(result.content[0].text)
    assert payload["error_code"] == "UNKNOWN_TOOL"
