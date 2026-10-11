"""Model Context Protocol server for the traffic-flow simulator."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .model import TrafficModel


mcp = FastMCP("traffic-flow-simulator")
model = TrafficModel(seed=27)


@mcp.tool()
def get_simulation_status() -> dict[str, object]:
    """Return the current signal, traffic, and simulator state."""
    return model.status()


@mcp.tool()
def set_signal(color: str) -> dict[str, object]:
    """Set the traffic signal to green or red and disable automatic cycling."""
    normalized = color.strip().lower()
    if normalized not in {"green", "red"}:
        raise ValueError("color must be 'green' or 'red'")
    model.signal_green = normalized == "green"
    model.auto_signal = False
    return model.status()


@mcp.tool()
def set_auto_signal(enabled: bool) -> dict[str, object]:
    """Enable or disable the 300-frame automatic signal cycle."""
    model.auto_signal = enabled
    model.signal_timer = 0
    return model.status()


@mcp.tool()
def set_paused(paused: bool) -> dict[str, object]:
    """Pause or resume vehicle movement."""
    model.paused = paused
    return model.status()


@mcp.tool()
def set_speed_boost(enabled: bool) -> dict[str, object]:
    """Enable or disable the two-times speed mode."""
    model.speed_boost = enabled
    return model.status()


@mcp.tool()
def advance_simulation(steps: int = 1) -> dict[str, object]:
    """Advance the simulation by up to 1000 frames and return its state."""
    model.tick(steps)
    return model.status()


@mcp.tool()
def inspect_car(index: int) -> dict[str, object]:
    """Inspect one car by its zero-based index."""
    return model.inspect(index)


@mcp.tool()
def reset_simulation() -> dict[str, object]:
    """Reset all cars and restore the deterministic starting scene."""
    model.reset()
    return model.status()


if __name__ == "__main__":
    mcp.run()


def main() -> None:
    """Start the server over MCP's standard-input transport."""
    mcp.run()