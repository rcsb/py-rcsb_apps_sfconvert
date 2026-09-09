from __future__ import annotations

import os
from pathlib import Path

import pytest
from mmcif.io.IoAdapterCore import IoAdapterCore

from sf_convert.utils.pinfo_file import PInfoLogger, PStreamLogger


def _read_sf_convert_category(cif_path: str) -> tuple[str, str]:
    """Reads back a sf_information.cif file and returns (error, sf_information)."""
    ioa = IoAdapterCore()
    containers = ioa.readFile(cif_path)
    cat = containers[0].getObj("sf_convert")
    return cat.getValue("error", 0), cat.getValue("sf_information", 0)


class TestPStreamLogger:
    @staticmethod
    def test_pinfo_warning_writes_to_lf1(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger()
        logger.pinfo("Warning: something bad", 1)

        assert logger._lf1.getvalue() == "Warning: something bad\n"  # pylint: disable=protected-access
        assert logger._lf2.getvalue() == ""  # pylint: disable=protected-access
        assert "Warning: something bad" in capsys.readouterr().out

    @staticmethod
    def test_pinfo_error_writes_to_lf1(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger()
        logger.pinfo("Error: boom", 2)

        assert logger._lf1.getvalue() == "Error: boom\n"  # pylint: disable=protected-access
        assert "Error: boom" in capsys.readouterr().out

    @staticmethod
    def test_pinfo_pid0_writes_to_lf2_and_prints(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger()
        logger.pinfo("plain info", 0)

        assert logger._lf1.getvalue() == ""  # pylint: disable=protected-access
        assert logger._lf2.getvalue() == "plain info\n"  # pylint: disable=protected-access
        assert "plain info" in capsys.readouterr().out

    @staticmethod
    def test_pinfo_pid1_writes_to_lf2_only(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger()
        logger.pinfo("quiet info", 1)

        assert logger._lf2.getvalue() == "quiet info\n"  # pylint: disable=protected-access
        assert capsys.readouterr().out == ""

    @staticmethod
    def test_pinfo_pid2_prints_only(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger()
        logger.pinfo("console only", 2)

        assert logger._lf1.getvalue() == ""  # pylint: disable=protected-access
        assert logger._lf2.getvalue() == ""  # pylint: disable=protected-access
        assert "console only" in capsys.readouterr().out

    @staticmethod
    def test_output_reports_diag_written(tmp_path: Path) -> None:
        logger = PStreamLogger()
        logger.pinfo("Warning: header issue", 1)
        logger.pinfo("Error: fatal issue", 1)

        diag_path = str(tmp_path / "diag.txt")
        sfinfo_path = str(tmp_path / "sf_information.cif")

        logger.output_reports(sfinfo=sfinfo_path, diag=diag_path)

        with open(diag_path) as fin:
            lines = fin.read().splitlines()

        assert lines == ["Warning: header issue", "Error: fatal issue"]

    @staticmethod
    def test_output_reports_diag_no_messages(tmp_path: Path) -> None:
        logger = PStreamLogger()

        diag_path = str(tmp_path / "diag.txt")
        sfinfo_path = str(tmp_path / "sf_information.cif")

        logger.output_reports(sfinfo=sfinfo_path, diag=diag_path)

        with open(diag_path) as fin:
            content = fin.read()

        assert content == "No Error/Warning messages were found.\n"

    @staticmethod
    def test_output_reports_no_diag_requested(tmp_path: Path) -> None:
        logger = PStreamLogger()
        logger.pinfo("Warning: header issue", 1)

        sfinfo_path = str(tmp_path / "sf_information.cif")

        logger.output_reports(sfinfo=sfinfo_path, diag=None)

        assert os.path.exists(sfinfo_path)

    @staticmethod
    def test_output_sf_info_contents(tmp_path: Path) -> None:
        logger = PStreamLogger()
        logger.pinfo("Warning: header issue", 1)
        logger.pinfo("some diagnostic info", 1)

        sfinfo_path = str(tmp_path / "sf_information.cif")
        logger.output_reports(sfinfo=sfinfo_path)

        err, info = _read_sf_convert_category(sfinfo_path)
        assert err == "Warning: header issue\n"
        assert info == "some diagnostic info\n"

    @staticmethod
    def test_output_sf_info_defaults_empty_info_to_newline(tmp_path: Path) -> None:
        logger = PStreamLogger()

        sfinfo_path = str(tmp_path / "sf_information.cif")
        logger.output_reports(sfinfo=sfinfo_path)

        # An empty error string round-trips through the CIF writer as the
        # "?" missing-value marker rather than an empty string.
        err, info = _read_sf_convert_category(sfinfo_path)
        assert err == "?"
        assert info == "\n"


class TestOnlyFirstBlock:
    # onlyfirstblock keeps messages tagged as block 1 and suppresses logging for every other block.
    @staticmethod
    def test_default_does_not_skip_any_block() -> None:
        logger = PStreamLogger()
        logger.pinfo("Warning: block2", 1, block=2)

        assert logger._lf1.getvalue() == "Warning: block2\n"  # pylint: disable=protected-access

    @staticmethod
    def test_does_not_skip_first_block() -> None:
        logger = PStreamLogger(onlyfirstblock=True)
        logger.pinfo("Warning: block1", 1, block=0)

        assert logger._lf1.getvalue() == "Warning: block1\n"  # pylint: disable=protected-access

    @staticmethod
    def test_skips_warning_log_for_other_blocks_but_still_prints(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger(onlyfirstblock=True)
        logger.pinfo("Warning: block2", 1, block=1)

        assert logger._lf1.getvalue() == ""  # pylint: disable=protected-access
        assert "Warning: block2" in capsys.readouterr().out

    @staticmethod
    def test_does_not_skip_when_block_is_none() -> None:
        logger = PStreamLogger(onlyfirstblock=True)
        logger.pinfo("Warning: no block", 1)

        assert logger._lf1.getvalue() == "Warning: no block\n"  # pylint: disable=protected-access

    @staticmethod
    def test_pid0_skips_lf2_write_but_still_prints(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger(onlyfirstblock=True)
        logger.pinfo("plain info", 0, block=1)

        assert logger._lf2.getvalue() == ""  # pylint: disable=protected-access
        assert "plain info" in capsys.readouterr().out

    @staticmethod
    def test_pid1_skips_lf2_write_silently(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger(onlyfirstblock=True)
        logger.pinfo("quiet info", 1, block=1)

        assert logger._lf2.getvalue() == ""  # pylint: disable=protected-access
        assert capsys.readouterr().out == ""

    @staticmethod
    def test_pid2_skips_print_entirely(capsys: pytest.CaptureFixture[str]) -> None:
        logger = PStreamLogger(onlyfirstblock=True)
        logger.pinfo("console only", 2, block=1)

        assert capsys.readouterr().out == ""

    @staticmethod
    def test_pinfo_logger_accepts_onlyfirstblock_kwarg(tmp_path: Path) -> None:
        log1 = str(tmp_path / "f1.log")
        log2 = str(tmp_path / "f2.log")

        logger = PInfoLogger(log1, log2, onlyfirstblock=True)
        logger.pinfo("Warning: on disk", 1, block=1)
        logger._lf1.flush()  # pylint: disable=protected-access

        with open(log1) as fin:
            assert fin.read() == ""


class TestPInfoLogger:
    @staticmethod
    def test_creates_log_files(tmp_path: Path) -> None:
        log1 = str(tmp_path / "f1.log")
        log2 = str(tmp_path / "f2.log")

        logger = PInfoLogger(log1, log2)

        assert os.path.exists(log1)
        assert os.path.exists(log2)

        logger.pinfo("Warning: on disk", 1)
        logger._lf1.flush()  # pylint: disable=protected-access

        with open(log1) as fin:
            assert fin.read() == "Warning: on disk\n"

    @staticmethod
    def test_clear_logs_removes_existing_files(tmp_path: Path) -> None:
        log1 = str(tmp_path / "f1.log")
        log2 = str(tmp_path / "f2.log")

        with open(log1, "w") as fout:
            fout.write("stale content")
        with open(log2, "w") as fout:
            fout.write("stale content")

        PInfoLogger(log1, log2)

        with open(log1) as fin:
            assert fin.read() == ""
        with open(log2) as fin:
            assert fin.read() == ""

    @staticmethod
    def test_init_raises_when_log_dir_missing(tmp_path: Path) -> None:
        # clear_logs() silently no-ops on a path in a missing directory,
        # but the subsequent open() for writing still raises.
        missing_dir_path = str(tmp_path / "does" / "not" / "exist" / "f1.log")
        log2 = str(tmp_path / "f2.log")

        with pytest.raises(FileNotFoundError):
            PInfoLogger(missing_dir_path, log2)
