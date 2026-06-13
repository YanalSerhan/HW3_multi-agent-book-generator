# pyrefly: ignore [missing-import]
from pathlib import Path
from unittest.mock import MagicMock

# pyrefly: ignore [missing-import]
import pytest

from crewai_book.sdk.aux_processor import post_process_aux_files


def test_post_process_aux_files(tmp_path: Path) -> None:
    latex_dir = tmp_path
    base_name = "test_book"
    tex_file = latex_dir / f"{base_name}.tex"
    toc_file = latex_dir / f"{base_name}.toc"

    original_toc = r"""\select@language{english}
\contentsline {chapter}{\numberline {1}Introduction}{1}{chapter.1}
\select@language{hebrew}
\contentsline {chapter}{\numberline {2}פרק בעברית}{5}{chapter.2}
\xpg@aux{dummy}{english}
"""
    toc_file.write_text(original_toc, encoding="utf-8")

    logger_mock = MagicMock()
    post_process_aux_files(tex_file, logger=logger_mock)

    processed_toc = toc_file.read_text(encoding="utf-8")

    assert r"\select@language{english}" not in processed_toc
    assert r"\select@language{hebrew}" not in processed_toc
    assert r"\xpg@aux{dummy}{english}" not in processed_toc

    assert r"\texthebrew{פרק בעברית}" in processed_toc
    assert r"\texthebrew{Introduction}" not in processed_toc

    logger_mock.warning.assert_not_called()

def test_post_process_aux_files_missing_file(tmp_path: Path) -> None:
    tex_file = tmp_path / "missing.tex"
    logger_mock = MagicMock()

    post_process_aux_files(tex_file, logger=logger_mock)
    logger_mock.warning.assert_not_called()

def test_post_process_aux_files_exception(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    tex_file = tmp_path / "test.tex"
    toc_file = tmp_path / "test.toc"

    toc_file.write_text("dummy", encoding="utf-8")

    logger_mock = MagicMock()

    monkeypatch.setattr(Path, "read_text", MagicMock(side_effect=PermissionError("Mocked Permission Error")))
    post_process_aux_files(tex_file, logger=logger_mock)

    logger_mock.warning.assert_called_once()
    assert "Failed to post-process auxiliary file" in logger_mock.warning.call_args[0][0]
