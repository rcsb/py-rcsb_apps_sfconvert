from sf_convert.sffile.sf_file import SFFile

class TestVersion:
    @staticmethod
    def test_get_version():
        """ Tests if we can retrieve version number """
        pass
    @staticmethod
    def test_instantiate():
        s = SFFile()
        assert s
