# import sys

import pytest

from confprint import _exceptions, err_print, prefix_printer


@pytest.fixture
def prefix_string() -> str:
    """Use string as prefix."""
    return "test"


@pytest.fixture
def text_string() -> str:
    """Use string as the input text."""
    return "This is a text string."


def test_err_print(capsys, text_string):
    """Test if err_print is using sys.stderr."""
    err_print(text_string)
    captured = capsys.readouterr()
    assert captured.err == f"{text_string}\n"


def test_prefix_printer_no_text(capsys, prefix_string):
    """Test if prefix_printer has no text."""
    p_test = prefix_printer(prefix_string)
    p_test()
    captured = capsys.readouterr()
    assert captured.out == f"[{prefix_string.upper()}]\n"


@pytest.mark.parametrize(
    "prefix", ["", "test", "done"], ids=["no prefix", "TEST", "DONE"]
)
def test_prefix_printer_prefix(prefix, capsys, text_string):
    """Test if prefix_printer has the correct prefix."""
    p_test = prefix_printer(f"{prefix}")
    p_test(text_string)
    captured = capsys.readouterr()
    assert captured.out == f"[{prefix.upper()}]: {text_string}\n"


def test_prefix_printer_stderr(capsys, text_string, prefix_string):
    """Test if prefix_printer is using sys.stderr."""
    p_test = prefix_printer(prefix_string, stderr=True)
    p_test(text_string)
    captured = capsys.readouterr()
    assert captured.err == f"[{prefix_string.upper()}]: {text_string}\n"


def test_prefix_printer_click(capsys, text_string, prefix_string):
    """Test if prefix_printer is using click.echo."""
    p_test = prefix_printer(prefix_string, click=True)
    p_test(text_string)
    captured = capsys.readouterr()
    assert captured.out == f"[{prefix_string.upper()}]: {text_string}\n"


def test_prefix_printer_stderr_click_failure(text_string, prefix_string):
    """Test if prefix_printer is set to use both click.echo and sys.stderr."""
    p_test = prefix_printer(prefix_string, stderr=True, click=True)
    with pytest.raises(_exceptions.PropertyError) as excinfo:
        p_test(text_string)
    assert "stderr and click cannot be True at the same time" in str(
        excinfo.value
    )


@pytest.mark.parametrize("upper", [True, False], ids=["upper", "unaltered"])
def test_prefix_printer_upper(capsys, text_string, prefix_string, upper):
    """Test if prefix_printer is capitalizing the prefix correctly."""
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
    """Test if prefix_printer is using the frames correctly."""
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
    """Test if prefix_printer is using multiline correctly."""
    p_test = prefix_printer(prefix_string)
    p_test(text)
    captured = capsys.readouterr()
    indented_text = text.replace(
        "\n", f"\n{' ' * (len(prefix_string)+len('[]: '))}"
    )
    assert captured.out == f"[{prefix_string.upper()}]: {indented_text}\n"


def test_prefix_printer_counter(capsys, text_string, prefix_string):
    """Test if prefix_printer is using the counter_start correctly."""
    p_test = prefix_printer(prefix_string, counter_start=-1)
    p_test(text_string)
    captured = capsys.readouterr()

    p_test0 = prefix_printer(prefix_string, counter_start=0)
    p_test0(text_string)
    captured0 = capsys.readouterr()

    p_test1 = prefix_printer(
        prefix_string, counter_start=1, global_counter=True
    )
    p_test1(text_string)
    captured1 = capsys.readouterr()

    assert captured.out == f"[{prefix_string.upper()}]: {text_string}\n"
    assert captured0.out == f"[{prefix_string.upper()}:0]: {text_string}\n"
    assert captured1.out == f"[{prefix_string.upper()}:1]: {text_string}\n"


def test_prefix_printer_local_counter(capsys, text_string, prefix_string):
    """Test if prefix_printer is using the local counter correctly."""
    p_test0 = prefix_printer(prefix_string, counter_start=0)
    p_test10 = prefix_printer(prefix_string, counter_start=10)

    p_test0(text_string)  # counter: 0
    captured0_0 = capsys.readouterr()
    p_test0(text_string)  # counter: 1
    captured0_1 = capsys.readouterr()

    p_test10(text_string)  # counter: 10
    captured10_0 = capsys.readouterr()
    p_test10(text_string)  # counter: 11
    captured10_1 = capsys.readouterr()

    p_test0(text_string)  # counter: 2
    captured0_2 = capsys.readouterr()

    assert captured0_0.out == f"[{prefix_string.upper()}:0]: {text_string}\n"
    assert captured0_1.out == f"[{prefix_string.upper()}:1]: {text_string}\n"
    assert captured10_0.out == f"[{prefix_string.upper()}:10]: {text_string}\n"
    assert captured10_1.out == f"[{prefix_string.upper()}:11]: {text_string}\n"
    assert captured0_2.out == f"[{prefix_string.upper()}:2]: {text_string}\n"


def test_prefix_printer_global_counter(capsys, text_string, prefix_string):
    """Test if prefix_printer is using the global counter correctly."""
    pg_test0 = prefix_printer(
        prefix_string,
        counter_start=0,
        global_counter=True,
    )
    pg_test0(text_string)  # counter: 0
    captured0_0 = capsys.readouterr()
    pg_test0(text_string)  # counter: 1
    captured0_1 = capsys.readouterr()

    pg_test10 = prefix_printer(
        prefix_string, counter_start=10, global_counter=True
    )
    pg_test10(text_string)  # counter: 10
    captured10_0 = capsys.readouterr()
    pg_test10(text_string)  # counter: 11
    captured10_1 = capsys.readouterr()

    pl_test100 = prefix_printer(prefix_string, counter_start=100)
    pl_test100(text_string)  # counter: 100
    captured100_0 = capsys.readouterr()
    pl_test100(text_string)  # counter: 101
    captured100_1 = capsys.readouterr()

    pl_test200 = prefix_printer(prefix_string, counter_start=200)
    pl_test200(text_string)  # counter: 200
    captured200_0 = capsys.readouterr()
    pl_test200(text_string)  # counter: 201
    captured200_1 = capsys.readouterr()

    assert captured0_0.out == f"[{prefix_string.upper()}:0]: {text_string}\n"
    assert captured0_1.out == f"[{prefix_string.upper()}:1]: {text_string}\n"
    assert captured10_0.out == f"[{prefix_string.upper()}:10]: {text_string}\n"
    assert captured10_1.out == f"[{prefix_string.upper()}:11]: {text_string}\n"
    assert (
        captured100_0.out == f"[{prefix_string.upper()}:100]: {text_string}\n"
    )
    assert (
        captured100_1.out == f"[{prefix_string.upper()}:101]: {text_string}\n"
    )
    assert (
        captured200_0.out == f"[{prefix_string.upper()}:200]: {text_string}\n"
    )
    assert (
        captured200_1.out == f"[{prefix_string.upper()}:201]: {text_string}\n"
    )
