# test_print_calendar_unittest.py
import unittest
from io import StringIO
from contextlib import redirect_stdout

# ⬇️ Change this import to match your filename (without .py)
from calendar_printer import print_calendar


def _expected_calendar(days: int, start: int) -> str:
    """Build the exact string that print_calendar should emit."""
    header = "Sun Mon Tue Wed Thu Fri Sat\n"
    lines = [header]

    line = "    " * start
    for d in range(1, days + 1):
        line += f"{d:>3} "
        if (start + d) % 7 == 0:
            lines.append(line + "\n")
            line = ""
    # Function always prints a trailing newline
    lines.append(line + "\n")
    return "".join(lines)


def _run_and_capture(days: int, start: int) -> str:
    buf = StringIO()
    with redirect_stdout(buf):
        print_calendar(days, start)
    return buf.getvalue()


class TestPrintCalendar(unittest.TestCase):
    # ---------- Golden-path tests (like duration calculator’s table-driven style) ----------
    def test_golden_cases(self):
        cases = [
            (28, 0),  # exact 4 weeks starting Sunday
            (30, 2),  # starts Tuesday
            (31, 3),  # starts Wednesday
            (29, 6),  # starts Saturday, early wrap
            (30, 0),  # starts Sunday
            (31, 6),  # longest month starting Saturday
        ]
        for days, start in cases:
            with self.subTest(days=days, start=start):
                expected = _expected_calendar(days, start)
                got = _run_and_capture(days, start)
                self.assertEqual(got, expected)

    # ---------- Focused spot-checks ----------
    def test_header_is_correct(self):
        out = _run_and_capture(7, 0).splitlines()
        self.assertEqual(out[0], "Sun Mon Tue Wed Thu Fri Sat")

    def test_alignment_when_start_is_zero(self):
        out_lines = _run_and_capture(7, 0).splitlines()
        # First line of dates should start immediately (no leading spaces)
        self.assertFalse(out_lines[1].startswith("    "))

    def test_alignment_when_start_is_six(self):
        out_lines = _run_and_capture(1, 6).splitlines()
        # Six indents (4 spaces each) before "  1"
        self.assertTrue(out_lines[1].startswith(" " * 4 * 6))
        self.assertTrue(out_lines[1].strip().startswith("1"))

    def test_trailing_newline_present(self):
        out = _run_and_capture(30, 2)
        self.assertTrue(out.endswith("\n"))


if __name__ == "__main__":
    unittest.main()