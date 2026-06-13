from pathlib import Path

from crewai_book.domain.state import PipelineState
from crewai_book.workflows.pipeline_stages import (
    create_editorial_crew,
    create_main_crew,
    create_research_crew,
)


def test_create_research_crew() -> None:
    state = PipelineState(topic="test", run_id="r1")
    crew = create_research_crew("test", Path("out"))
    assert crew is not None
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3

def test_create_main_crew() -> None:
    state = PipelineState(topic="test", run_id="r1")

    crew = create_main_crew("test", Path("out"))

    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0

def test_create_editorial_crew() -> None:
    state = PipelineState(topic="test", run_id="r1")
    crew = create_editorial_crew(Path("out"))

    assert crew is not None
    assert len(crew.agents) > 0
    assert len(crew.tasks) > 0
