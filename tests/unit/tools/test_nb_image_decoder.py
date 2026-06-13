import base64
from pathlib import Path
from unittest.mock import patch

from crewai_book.tools.nb_image_decoder import decode_and_save_image

def test_decode_and_save_image_success(tmp_path: Path) -> None:
    dummy_data = b"dummy png data"
    b64_data = base64.b64encode(dummy_data).decode("utf-8")
    
    data = {"image/png": b64_data}
    success, ext, path = decode_and_save_image(data, tmp_path, "base", 1)
    
    assert success is True
    assert ext == "png"
    assert path is not None
    assert path == tmp_path / "base_fig_1.png"
    assert path.read_bytes() == dummy_data

def test_decode_and_save_image_pdf(tmp_path: Path) -> None:
    dummy_data = b"dummy pdf data"
    b64_data = base64.b64encode(dummy_data).decode("utf-8")
    
    data = {"application/pdf": b64_data}
    success, ext, path = decode_and_save_image(data, tmp_path, "base", 2)
    
    assert success is True
    assert ext == "pdf"
    assert path is not None
    assert path == tmp_path / "base_fig_2.pdf"
    assert path.read_bytes() == dummy_data

def test_decode_and_save_image_list_chunked(tmp_path: Path) -> None:
    dummy_data = b"dummy data chunked"
    b64_data = base64.b64encode(dummy_data).decode("utf-8")
    
    b64_list = [b64_data[:5], b64_data[5:]]
    
    data = {"image/png": b64_list}
    success, ext, path = decode_and_save_image(data, tmp_path, "base", 3)
    
    assert success is True
    assert path is not None
    assert path.read_bytes() == dummy_data

def test_decode_and_save_image_no_image_data(tmp_path: Path) -> None:
    data = {"text/plain": "Some text"}
    success, ext, path = decode_and_save_image(data, tmp_path, "base", 1)
    assert success is False

def test_decode_and_save_image_none_data(tmp_path: Path) -> None:
    data = {"image/png": None}
    success, ext, path = decode_and_save_image(data, tmp_path, "base", 1)
    assert success is False

def test_decode_and_save_image_invalid_type(tmp_path: Path) -> None:
    data = {"image/png": 12345}  # Invalid type
    success, ext, path = decode_and_save_image(data, tmp_path, "base", 1)
    assert success is False

def test_decode_and_save_image_decode_error(tmp_path: Path) -> None:
    data = {"image/png": "invalid-base64-!!!"}
    success, ext, path = decode_and_save_image(data, tmp_path, "base", 1)
    assert success is False

@patch("crewai_book.tools.nb_image_decoder.logger")
def test_decode_and_save_image_write_error(mock_logger, tmp_path: Path) -> None:
    dummy_data = b"dummy"
    b64_data = base64.b64encode(dummy_data).decode("utf-8")
    data = {"image/png": b64_data}
    
    with patch("builtins.open", side_effect=PermissionError("Mock Permission")):
        success, ext, path = decode_and_save_image(data, tmp_path, "base", 1)
        
    assert success is False
    mock_logger.error.assert_called_once()
