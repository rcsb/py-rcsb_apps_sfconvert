import argparse
from mmcif.io.IoAdapterCore import IoAdapterCore
from pathlib import Path
#from export.cns_export import CNSConverter

import sys
path_to_append = Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/export')
sys.path.append(str(path_to_append))
from cns_export import CNSConverter
from mtz_export2 import MTZConverter

class sf_convert:
    def __init__(self):
        self.__containers = []  # Using name mangling to avoid accidental modification
        self.__io_core = IoAdapterCore()  # Also using name mangling for the io_core instance
        self.__default_block_number = 0  # Initializing default block number to 0

    def readFile(self, filename):
        try:
            self.__containers = self.__io_core.readFile(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to read file {filename}") from e


    def readBlock(self, filename, block_number):
        self.readFile(filename)
        if 0 <= block_number < len(self.__containers):
            return self.__containers[block_number]
        else:
            print(f"Block number {block_number} is not valid. It should be between 0 and {len(self.__containers) - 1}.")
            return None

    def getBlockByIndex(self, block_number):
        if 0 <= block_number < len(self.__containers):
            container = self.__containers[block_number]
            return container
        else:
            print(f"Block number {block_number} is not valid. It should be between 0 and {len(self.__containers) - 1}.")
            return None 
        
    def getBlocksCount(self):
        return len(self.__containers)


    def writeFile(self, filename):
        self.__io_core.writeFile(filename, self.__containers)

    def getBlocksNames(self):
        return [container.getName() for container in self.__containers]

    def getBlock(self, name):
        for idx, container in enumerate(self.__containers):
            if container.getName() == name:
                return idx, container
        return None
    
    def getObj(self, category, block_name=None):
        if block_name is None:
            block_number = self.__default_block_number
            return self.__containers[block_number].getObj(category)
        else:
            block_number, block_res = self.getBlock(block_name)
            if block_res is None:
                return None
            return block_res.getObj(category)

    def setDefaultBlock(self, block_name):
        block_number, _ = self.getBlock(block_name)
        if block_number is not None:
            self.__default_block_number = block_number

    def getCategories(self, block_name=None):
        if block_name == "Default":
            block_number = self.__default_block_number
            return self.__containers[block_number].getObjNameList()
        else:
            block_number, block_res = self.getBlock(block_name)
            if block_res is None:
                return None
            return block_res.getObjNameList()


def main():
    parser = argparse.ArgumentParser(description='SFFile operations')
    parser.add_argument('-r', '--read', metavar='filename', help='Read from an mmCIF file')
    parser.add_argument('-w', '--write', metavar='filename', help='Write to an mmCIF file')
    parser.add_argument('-g', '--getBlocksNames', action='store_true', help='Get block names')
    # parser.add_argument('-o', '--getObj', nargs='+', metavar=('category', 'block_name'),
    #                     help='Get object from a block or the default block if not specified')
    parser.add_argument('-s', '--setDefaultBlock', metavar='block_name', help='Set default block')
    parser.add_argument('-c', '--getCategories', nargs='?', metavar='block_name', const="Default", help='Get categories by optional block name')
    # ---------------------------------------------------------------------------------------------
    parser.add_argument('-o', type=str, help='Output format')
    parser.add_argument('-sf', type=str, help='Source file')


    args = parser.parse_args()

    sf_file = sf_convert()

    if args.read:
        sf_file.readFile(args.read)
    if args.write:
        sf_file.writeFile(args.write)
    if args.getBlocksNames:
        print(sf_file.getBlocksNames())
    # if args.getObj:
    #     if len(args.getObj) == 2:
    #         category, block_name = args.getObj
    #         print(sf_file.getObj(category, block_name))
    #     else:
    #         category = args.getObj[0]
    #         print(sf_file.getObj(category))
    if args.setDefaultBlock:
        sf_file.setDefaultBlock(args.setDefaultBlock)
    if args.getCategories:
        print(sf_file.getCategories(args.getCategories))

    # ---------------------------------------------------------------------------------------------

    if args.o == 'CNS':
        sffile = sf_convert()
        sffile.readFile(str(Path(args.sf)))
        CNSexport = CNSConverter(sffile, str(Path("your_output_file.txt")))
        CNSexport.convert()

    elif args.o == 'MTZ':
        converter = MTZConverter(str(Path(args.sf)))
        converter.load_cif()
        converter.determine_mappings()
        converter.convert_to_mtz('output.mtz')


if __name__ == '__main__':
    main()