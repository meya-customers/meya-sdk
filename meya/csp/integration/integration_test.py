import pytest

from meya.csp.integration import CspIntegration
from meya.csp.integration.integration import AgentAvatar
from meya.csp.integration.integration import AgentNameMode
from meya.csp.integration.integration import AgentSpec


@pytest.mark.parametrize(
    (
        "runtime_agent_name",
        "agent_config",
        "monogram_config",
        "expected_agent_name",
        "expected_monogram",
    ),
    [
        ("John Doe", "Test", "Aux", "Test", "Aux"),
        (None, "Test", "Aux", "Test", "Aux"),
        ("John", AgentNameMode.FULL, AgentNameMode.FIRST_INITIAL, "John", "J"),
        (
            "John Doe",
            AgentNameMode.FULL,
            AgentNameMode.FIRST_LAST_INITIAL,
            "John Doe",
            "John D",
        ),
        (
            "John Doe",
            AgentNameMode.FIRST_LAST_INITIAL,
            AgentNameMode.FIRST_LAST_INITIAL,
            "John D.",
            "John D",
        ),
        (
            "John The Unknown Doe",
            AgentNameMode.FIRST_LAST_INITIAL,
            AgentNameMode.FIRST_LAST_INITIAL,
            "John D.",
            "John D",
        ),
        ("John Doe", AgentNameMode.FIRST, AgentNameMode.FIRST, "John", "John"),
        (
            "John Doe",
            AgentNameMode.FIRST,
            AgentNameMode.FULL,
            "John",
            "John Doe",
        ),
        (
            "John The Unknown Doe",
            AgentNameMode.FIRST,
            AgentNameMode.FULL,
            "John",
            "John The Unknown Doe",
        ),
        (
            "John The Unknown Doe",
            AgentNameMode.FIRST_INITIAL,
            AgentNameMode.FULL,
            "J.",
            "John The Unknown Doe",
        ),
        (
            "John The Unknown Doe",
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "J. D.",
            "J D",
        ),
        (
            "John The Unknown ",
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "J. U.",
            "J U",
        ),
        (
            "John ",
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "J.",
            "J",
        ),
        (
            "John",
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "J.",
            "J",
        ),
        (
            "J",
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "J.",
            "J",
        ),
        (
            " D",
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "D.",
            "D",
        ),
        (" D", AgentNameMode.FULL, AgentNameMode.FULL, "D", "D"),
        (
            "",
            AgentNameMode.FULL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "Agent",
            "A",
        ),
        (
            "",
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            AgentNameMode.FIRST_INITIAL_LAST_INITIAL,
            "A.",
            "A",
        ),
        (
            "John John",
            AgentNameMode.FIRST_LAST_INITIAL,
            AgentNameMode.FIRST_LAST_INITIAL,
            "John J.",
            "John J",
        ),
    ],
)
def test_parse_agent_name(
    runtime_agent_name,
    agent_config,
    monogram_config,
    expected_agent_name,
    expected_monogram,
):
    csp = CspIntegration(
        agent=AgentSpec(
            name=agent_config, avatar=AgentAvatar(monogram=monogram_config)
        )
    )
    parsed_agent_name = csp._parse_agent_name(runtime_agent_name)
    assert parsed_agent_name == expected_agent_name
    parsed_monogram = csp._parse_monogram(runtime_agent_name)
    assert parsed_monogram == expected_monogram
