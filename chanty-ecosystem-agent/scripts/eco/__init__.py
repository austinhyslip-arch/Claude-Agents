"""Chanty Ecosystem Agent: the deterministic core.

Everything in this package is deliberately boring. Scoring, state transitions,
gates, dedupe and suppression are the parts of the system that must behave the
same way every time, so they are plain Python with no model in the loop and no
third-party dependencies.

The agents (agents/*.md) do the reasoning. This package decides what is allowed.
"""

__version__ = "1.0.0"
