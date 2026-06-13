"""Pipeline execution entry point."""

import uuid
from pathlib import Path

from ..domain.state import PipelineState
from ..observability.logger import get_logger
from ..services.content_service import ContentService
from ..shared.constants import OUTPUT_DIR
from .gate_models import PipelineStage
from .pipeline_utils import _evaluate_gates_for_stage

logger = get_logger("workflows.pipeline")

MAX_RETRIES = 2


def run_pipeline(topic: str, output_dir: str | Path | None = None) -> PipelineState:
    """Run the complete book generation pipeline with integrated Quality Gates."""
    out_path = Path(output_dir) if output_dir else OUTPUT_DIR

    out_path.mkdir(parents=True, exist_ok=True)
    (out_path / "latex").mkdir(parents=True, exist_ok=True)

    run_id = str(uuid.uuid4())[:8]
    state = PipelineState(topic=topic, run_id=run_id)
    logger.info(f"Starting pipeline run {run_id} for: {topic}")

    content_service = ContentService()

    # --- KNOWLEDGE EXTRACTION ---
    from ..config.settings import config_manager
    from ..tools.nb_extractor import NotebookExtractor

    setup_config = config_manager.get_setup()
    knowledge_sources = setup_config.get("knowledge_sources", [])
    if knowledge_sources:
        logger.info("Extracting knowledge sources...")
        extractor = NotebookExtractor()
        for source in knowledge_sources:
            extracted_path = extractor.extract(source)
            if extracted_path:
                logger.info(f"Successfully extracted {source}")
            else:
                logger.warning(f"Failed to extract {source}")

    # --- TOPIC CONFIRMATION CHECKPOINT ---
    from ..config.settings import settings

    if getattr(settings, "human_review_outline", False):
        print("\n" + "=" * 50)
        print(f"PRE-FLIGHT TOPIC CONFIRMATION: {topic}")
        print("=" * 50)
        ans = input("Proceed with this topic? [y = continue / n = abort run]: ")
        if ans.strip().lower() == "n":
            print("Run aborted by user.")
            import sys

            sys.exit(0)

    # --- RESEARCH STAGE ---
    from .pipeline_stages import (
        run_editorial_stage,
        run_main_stage,
        run_post_processing_stage,
        run_research_stage,
    )

    if not run_research_stage(state, topic, out_path):
        return state

    # --- MAIN STAGE ---
    if not run_main_stage(state, topic, out_path):
        return state

    # --- POST-PROCESSING ---
    if not run_post_processing_stage(state, out_path):
        return state

    # --- EDITORIAL STAGE ---
    if not run_editorial_stage(state, content_service, out_path):
        return state

    # --- QA SIGN-OFF ---
    state.current_stage = PipelineStage.QA.value
    res = _evaluate_gates_for_stage(state, PipelineStage.QA)

    if res is True:
        state.current_stage = "complete"
        logger.info(f"Pipeline run {run_id} completed successfully.")

    return state
