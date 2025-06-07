import pytest
import json

from sf_convert.command_line.UtilExec import create_parser, checkfmts


class TestCliUtil:
    def test_parser_default(self):
        """ Tests parser no parameters"""

        # Nothing - only func
        parser = create_parser()
        args = parser.parse_args([])
        assert len(vars(args)) == 1
        assert hasattr(args, "func")

    def test_parser_wrong(self, capsys):
        """ Tests parser wrong parameter"""

        # Error one
        parser = create_parser()
        with pytest.raises(SystemExit) as e:
            parser.parse_args(["something"])
        assert e.type == SystemExit
        assert e.value.code == 2
        assert "checkfmts" in capsys.readouterr().err

    def test_parser_checkfmt_noparam(self, capsys):
        """ Tests parser checkfmt no parameter"""

        # Error one
        parser = create_parser()
        with pytest.raises(SystemExit) as e:
            parser.parse_args(["checkfmts"])
        assert e.type == SystemExit
        assert e.value.code == 2
        assert "the following arguments are required: --sf" in capsys.readouterr().err

    def test_parser_checkfmt_param(self, cif_5pny_data_path):
        """ Tests parser checkfmt no parameter"""

        parser = create_parser()
        args = parser.parse_args(["checkfmts", "--sf", cif_5pny_data_path])
        assert len(vars(args)) == 4
        assert hasattr(args, "func")
        assert args.sf == [cif_5pny_data_path]
        assert args.json is False
        assert args.text is False

    def test_parser_checkfmt_param_json(self, cif_5pny_data_path):
        """ Tests parser checkfmt no parameter"""

        parser = create_parser()
        args = parser.parse_args(["checkfmts", "--sf", cif_5pny_data_path, "--json"])
        assert len(vars(args)) == 4
        assert hasattr(args, "func")
        assert args.sf == [cif_5pny_data_path]
        assert args.json is True
        assert args.text is False

    def test_parser_checkfmt_param_text(self, cif_5pny_data_path):
        """ Tests parser checkfmt no parameter"""

        parser = create_parser()
        args = parser.parse_args(["checkfmts", "--sf", cif_5pny_data_path, "--text"])
        assert len(vars(args)) == 4
        assert hasattr(args, "func")
        assert args.sf == [cif_5pny_data_path]
        assert args.json is False
        assert args.text is True

    def test_checkfmt_output_text(self, capsys, cif_5pny_data_path):
        """ Tests parser checkfmt no parameter"""

        parser = create_parser()
        args = parser.parse_args(["checkfmts", "--sf", cif_5pny_data_path, "--text"])
        ret = checkfmts(args)
        assert ret == 0
        assert "mmCIF" in capsys.readouterr().out

    def test_checkfmt_output_json(self, capsys, cif_5pny_data_path):
        """ Tests parser checkfmt no parameter"""

        parser = create_parser()
        args = parser.parse_args(["checkfmts", "--sf", cif_5pny_data_path, "--json"])
        ret = checkfmts(args)
        assert ret == 0
        out = capsys.readouterr().out
        parse_out = json.loads(out)
        assert len(parse_out) == 1
        first = parse_out[0]
        assert first[0] == cif_5pny_data_path
        assert first[1] == "mmCIF"
