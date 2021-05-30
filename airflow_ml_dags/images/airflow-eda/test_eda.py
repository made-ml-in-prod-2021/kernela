import os

import numpy as np
from click.testing import CliRunner
from eda import report

TEST_DATA = os.path.join("..", "test_data", "data.csv")


def test_eda(tmpdir):
    out_dir = tmpdir.mkdir("report")
    runner = CliRunner()
    result = runner.invoke(
        report, ["--input_path", TEST_DATA, "--report_dir", str(out_dir)])

    assert result.exit_code == 0
    report_path = out_dir / "eda.html"
    assert os.path.isfile(report_path)
