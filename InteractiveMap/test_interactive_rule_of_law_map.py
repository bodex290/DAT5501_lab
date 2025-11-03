# test_interactive_rule_of_law_map.py
import importlib.util
import io
import os
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT_FILENAME = "interactive_rule_of_law_map.py"


def _load_module_from_path(module_name: str, file_path: Path):
    """Load a Python module from an explicit file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load spec for {file_path}")
    mod = importlib.util.module_from_spec(spec)
    # exec_module runs the top-level code of the target file
    spec.loader.exec_module(mod)
    sys.modules[module_name] = mod
    return mod


class FakeFig:
    """Minimal fake Plotly Figure with just the attributes/methods the script uses."""
    def __init__(self, df_for_frames):
        years = sorted(int(y) for y in df_for_frames["year"].dropna().unique())
        self.frames = [types.SimpleNamespace(name=str(y)) for y in years]
        self.layout = types.SimpleNamespace(sliders=[types.SimpleNamespace(active=0)])
        self._updated_layout_kwargs = None
        self._updated_traces_kwargs = None
        self._written_html_path = None

    def update_layout(self, **kwargs):
        self._updated_layout_kwargs = kwargs

    def update_traces(self, **kwargs):
        self._updated_traces_kwargs = kwargs

    def write_html(self, path, include_plotlyjs="cdn", full_html=True):
        with open(path, "w", encoding="utf-8") as f:
            f.write("<!doctype html><title>fake</title><p>plot saved</p>")
        self._written_html_path = path

    def show(self):
        pass  # no-op


class InteractiveRuleOfLawMapTests(unittest.TestCase):
    def setUp(self):
        # Work in a temp directory so the script writes its HTML here
        self.tmpdir = tempfile.TemporaryDirectory()
        self._cwd = os.getcwd()
        os.chdir(self.tmpdir.name)

        # Find the script file next to this test file
        self.test_dir = Path(__file__).resolve().parent
        self.script_path = self.test_dir / SCRIPT_FILENAME
        if not self.script_path.exists():
            raise FileNotFoundError(
                f"Could not find {SCRIPT_FILENAME} next to the test at {self.script_path}"
            )

    def tearDown(self):
        os.chdir(self._cwd)
        self.tmpdir.cleanup()

    # ---- helpers

    def _mock_requests_get(self, csv_text: str):
        class _Resp:
            def __init__(self, text):
                self.text = text
                self.status_code = 200

            def raise_for_status(self):
                if self.status_code != 200:
                    raise RuntimeError("HTTP error")

        return _Resp(csv_text)

    def _patch_px_with_fake(self):
        captured = {"df": None}

        def fake_choropleth(
            df,
            locations=None,
            color=None,
            hover_name=None,
            animation_frame=None,
            color_continuous_scale=None,
            range_color=None,
            projection=None,
            title=None,
        ):
            captured["df"] = df.copy()
            return FakeFig(df)

        return captured, patch("plotly.express.choropleth", side_effect=fake_choropleth)

    # ---- tests

    def test_creates_html_and_sets_slider_to_latest_year(self):
        csv = """Entity,Code,Year,rule-of-law-index
Country A,CTA,2020,0.50
Country A,CTA,2021,0.60
Country B,CTB,2021,0.70
"""
        from contextlib import redirect_stdout
        buf = io.StringIO()

        captured_px, px_patcher = self._patch_px_with_fake()
        # Use a unique module name per test run to avoid caching quirks
        module_name = "interactive_rule_of_law_map_testmod1"

        with patch("requests.get", side_effect=lambda *a, **k: self._mock_requests_get(csv)), \
             px_patcher, \
             redirect_stdout(buf):

            mod = _load_module_from_path(module_name, self.script_path)

        # 1) HTML file was written
        self.assertTrue(os.path.exists(mod.HTML_OUT), "Expected HTML output file to exist.")
        with open(mod.HTML_OUT, "r", encoding="utf-8") as f:
            self.assertIn("plot saved", f.read())

        # 2) Only 3-letter codes were passed to choropleth
        df_passed = captured_px["df"]
        self.assertIsNotNone(df_passed, "px.choropleth was not called.")
        self.assertTrue((df_passed["code"].astype(str).str.len() == 3).all())

        # 3) Latest year is active on the slider
        fig = mod.fig
        frame_labels = [int(fr.name) for fr in fig.frames]
        latest_year = max(frame_labels)
        active_idx = fig.layout.sliders[0].active
        self.assertEqual(frame_labels[active_idx], latest_year)

        # 4) Hover template was set
        self.assertIsNotNone(fig._updated_traces_kwargs)
        self.assertIn("hovertemplate", fig._updated_traces_kwargs)

        # 5) Console message includes the saved path
        out = buf.getvalue()
        self.assertIn("Saved interactive map to:", out)
        self.assertIn(mod.HTML_OUT, out)

    def test_raises_runtime_error_when_no_indicator_column(self):
        csv = "Entity,Code,Year\nXland,XLN,2021\n"
        captured_px, px_patcher = self._patch_px_with_fake()
        module_name = "interactive_rule_of_law_map_testmod2"

        with patch("requests.get", side_effect=lambda *a, **k: self._mock_requests_get(csv)), \
             px_patcher:

            with self.assertRaises(RuntimeError) as ctx:
                _load_module_from_path(module_name, self.script_path)

        self.assertIn("No indicator column found", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()