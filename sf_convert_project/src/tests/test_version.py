from sf_convert.sffile.sf_file import StructureFactorFile


class TestVersion:
    @staticmethod
    def test_get_version():
        """
        Tests if we can retrieve the version number.

        Returns:
            None
        """
        pass

    @staticmethod
    def test_instantiate():
        """
        Tests if we can instantiate the StructureFactorFile class.

        Returns:
            None
        """
        s = StructureFactorFile()
        assert s
