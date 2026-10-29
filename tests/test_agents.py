from agents import build_reader_agent, build_search_agent, critic_prompt, writer_prompt

def test_prompts_structure():
    """Verify system and human messages exist in the prompt templates."""
    writer_messages = writer_prompt.format_messages(topic="Test Topic", research="Test Research")
    assert len(writer_messages) == 2
    assert "expert research writer" in writer_messages[0].content
    assert "Test Topic" in writer_messages[1].content
    assert "Test Research" in writer_messages[1].content

    critic_messages = critic_prompt.format_messages(report="Test Report Content")
    assert len(critic_messages) == 2
    assert "research critic" in critic_messages[0].content
    assert "Test Report Content" in critic_messages[1].content

def test_agents_construction():
    """Verify agents can be built with their corresponding tools."""
    search_agent = build_search_agent()
    assert search_agent is not None

    reader_agent = build_reader_agent()
    assert reader_agent is not None

