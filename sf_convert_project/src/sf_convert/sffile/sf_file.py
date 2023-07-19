import argparse
from mmcif.io.IoAdapterCore import IoAdapterCore
from mmcif.api.PdbxContainers import ContainerBase
from mmcif.api.PdbxContainers import DataContainer
from mmcif.api.DataCategoryBase import DataCategoryBase
# mmcif.api.PdbxContainers

from pathlib import Path
#from export.cns_export import CNSConverter

import sys
path_to_append = Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/export')
sys.path.append(str(path_to_append))
from cns_export import CNSConverter
from mtz_export import MTZConverter

class SFFile:
    def __init__(self):
        self.__containers = []  # Using name mangling to avoid accidental modification
        self.__io_core = IoAdapterCore()  # Also using name mangling for the io_core instance
        self.__default_block_number = 0  # Initializing default block number to 0
        #self.__ordered_containers = ['entry', 'cell', 'symmetry', 'audit', 'refln']  # Add this line


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
        return None, None
    
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
        if block_name == "Default" or block_name == None:
            block_number = self.__default_block_number
            return self.__containers[block_number].getObjNameList()
        else:
            block_number, block_res = self.getBlock(block_name)
            if block_res is None:
                return None
            return block_res.getObjNameList()

    def add_category(self, category, block_name=None):
        if block_name is None:
            container = self.__containers[self.__default_block_number]
            container.append(category)
        else:
            _, block = self.getBlock(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return
            
            block.append(category)


    def addData(self, category_name, data_dict):
        """
        This function adds a category with its data to the default block.
        
        Parameters:
        category_name (str): The name of the category to be added.
        data_dict (dict): A dictionary where the keys are the attribute names and the values are their respective values.
        
        Returns:
        None
        """
        default_block = self.__containers[self.__default_block_number]
        new_category = DataCategoryBase(category_name)
        for attribute in data_dict.keys():
            new_category.appendAttribute(attribute)
        new_category.append(list(data_dict.values()))
        default_block.append(new_category)

    def addDataToBlock(self, block_name, category_name, data_dict):
        """
        This function adds a category with its data to a specific block.
        
        Parameters:
        block_name (str): The name of the block to which the category should be added.
        category_name (str): The name of the category to be added.
        data_dict (dict): A dictionary where the keys are the attribute names and the values are their respective values.
        
        Returns:
        None
        """
        _, block = self.getBlock(block_name)
        if block is None:
            print(f"Block {block_name} does not exist.")
            return
        new_category = DataCategoryBase(category_name)
        for attribute in data_dict.keys():
            new_category.appendAttribute(attribute)
        new_category.append(list(data_dict.values()))
        block.append(new_category)

    def reorder_objects(self, new_order, block_name=None):

        if block_name == "Default" or block_name == None:
            block_number = self.__default_block_number
            old_container = self.__containers[block_number]
        else:
            block_number, block_res = self.getBlock(block_name)
            if block_res is None:
                return None
            old_container = block_res


        new_container = ContainerBase(old_container.getName())
        new_container.setType(old_container.getType())
        
        # Copy properties
        for prop_name in old_container.getPropCatalog():
            new_container.setProp(prop_name, old_container.getProp(prop_name))
        
        # Add objects in new order
        for name in new_order:
            if old_container.exists(name):
                new_container.append(old_container.getObj(name))

        # Add any remaining objects not included in new_order
        for name in old_container.getObjNameList():
            if name not in new_order:
                new_container.append(old_container.getObj(name))

        # Replace old container with new container
        if block_name == "Default" or block_name == None:
            block_number = self.__default_block_number
            self.__containers[block_number] = new_container
        else:
            block_number, block_res = self.getBlock(block_name)
            if block_res is None:
                return None
            elif(not block_number):self.__containers[int(block_number)] = new_container








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

    sf_file = SFFile()

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
        sffile = SFFile()
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
