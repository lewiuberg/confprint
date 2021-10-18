# import sys

import pytest

from confprint import _exceptions, err_print, prefix_printer


@pytest.fixture
def prefix_string() -> str:
    return "test"


@pytest.fixture
def text_string() -> str:
    return "This is a text string."


# Test if err_print is using sys.stderr
def test_err_print(capsys, text_string):
    err_print(text_string)
    captured = capsys.readouterr()
    assert captured.err == f"{text_string}\n"


def test_prefix_printer_no_text(capsys, prefix_string):
    p_test = prefix_printer(prefix_string)
    p_test()
    captured = capsys.readouterr()
    assert captured.out == f"[{prefix_string.upper()}]\n"


@pytest.mark.parametrize(
    "prefix", ["", "test", "done"], ids=["no prefix", "TEST", "DONE"]
)
def test_prefix_printer_prefix(prefix, capsys, text_string):
    p_test = prefix_printer(f"{prefix}")
    p_test(text_string)
    captured = capsys.readouterr()
    assert captured.out == f"[{prefix.upper()}]: {text_string}\n"


def test_prefix_printer_stderr(capsys, text_string, prefix_string):
    p_test = prefix_printer(prefix_string, stderr=True)
    p_test(text_string)
    captured = capsys.readouterr()
    assert captured.err == f"[{prefix_string.upper()}]: {text_string}\n"


def test_prefix_printer_click(capsys, text_string, prefix_string):
    p_test = prefix_printer(prefix_string, click=True)
    p_test(text_string)
    captured = capsys.readouterr()
    assert captured.out == f"[{prefix_string.upper()}]: {text_string}\n"


def test_prefix_printer_stderr_click_failure(text_string, prefix_string):
    p_test = prefix_printer(prefix_string, stderr=True, click=True)
    with pytest.raises(_exceptions.PropertyError) as excinfo:
        p_test(text_string)
    assert "stderr and click cannot be True at the same time" in str(
        excinfo.value
    )


@pytest.mark.parametrize("upper", [True, False], ids=["upper", "unaltered"])
def test_prefix_printer_upper(capsys, text_string, prefix_string, upper):
    p_test = prefix_printer(prefix_string, upper=upper)
    p_test(text_string)
    captured = capsys.readouterr()
    if upper:
        assert captured.out == f"[{prefix_string.upper()}]: {text_string}\n"
    else:
        assert captured.out == f"[{prefix_string}]: {text_string}\n"


@pytest.mark.parametrize(
    argnames="left_frame, right_frame",
    argvalues=(params := {"(": ")", "[": "]", "{": "}"}).items(),
    ids=[f" {k}{v} " for k, v in params.items()],
)
def test_prefix_printer_frame(
    capsys, prefix_string, text_string, left_frame, right_frame
):
    p_test = prefix_printer(
        "test", frame_left=left_frame, frame_right=right_frame
    )
    p_test(text_string)
    captured = capsys.readouterr()
    assert (
        captured.out == f"{left_frame}{prefix_string.upper()}{right_frame}: "
        f"{text_string}\n"
    )


@pytest.mark.parametrize(
    "text",
    [
        "This is a\nmultiline text.",
        """This is a
also multiline text.""",
    ],
    ids=["newline multiline", "quated multiline"],
)
def test_prefix_printer_multiline(capsys, text, prefix_string):
    p_test = prefix_printer(prefix_string)
    p_test(text)
    captured = capsys.readouterr()
    indented_text = text.replace(
        "\n", f"\n{' ' * (len(prefix_string)+len('[]: '))}"
    )
    assert captured.out == f"[{prefix_string.upper()}]: {indented_text}\n"


def test_prefix_printer_counter(capsys, text_string, prefix_string):
    p_test = prefix_printer(prefix_string, counter_start=-1)
    p_test(text_string)
    captured = capsys.readouterr()

    p_test0 = prefix_printer(prefix_string, counter_start=0)
    p_test0(text_string)
    captured0 = capsys.readouterr()

    p_test1 = prefix_printer(prefix_string, counter_start=1)
    p_test1(text_string)
    captured1 = capsys.readouterr()

    assert captured.out == f"[{prefix_string.upper()}]: {text_string}\n"
    assert captured0.out == f"[{prefix_string.upper()}:0]: {text_string}\n"
    assert captured1.out == f"[{prefix_string.upper()}:1]: {text_string}\n"
