import argparse
from mmcif.io.IoAdapterCore import IoAdapterCore
from mmcif.api.PdbxContainers import ContainerBase
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
        self.__ordered_categories = ['entry', 'cell', 'symmetry', 'audit', 'refln']  # Add this line



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
        # print("###################")
        # print(type(self.__containers))
        # print(type(self.__containers[self.__default_block_number]))
        # print("###################")

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
        

    # def addCategory(self, category_name, attributes_values):
    #     default_block = self.getBlockByIndex(self.__default_block_number)
    #     if default_block is not None:
    #         # If the category exists in the block, append attributes and values
    #         if default_block.hasAttribute(category_name):
    #             category = default_block.getCategory(category_name)
    #             for attr, val in attributes_values.items():
    #                 category.appendAttribute(attr)
    #                 category.append(val)
    #         # If the category doesn't exist in the block, create it and add attributes and values
    #         else:
    #             default_block.appendCategory(category_name, attributes_values)
    #     else:
    #         print("Failed to add category. Default block not found.")

    # def addCategoryToBlock(self, block_name, category_name, attributes_values):
    #     block_number, block = self.getBlock(block_name)
    #     if block is not None:
    #         # If the category exists in the block, append attributes and values
    #         if block.hasAttribute(category_name):
    #             category = block.getCategory(category_name)
    #             for attr, val in attributes_values.items():
    #                 category.appendAttribute(attr)
    #                 category.append(val)
    #         # If the category doesn't exist in the block, create it and add attributes and values
    #         else:
    #             block.appendCategory(category_name, attributes_values)
    #     else:
    #         print(f"Failed to add category. Block '{block_name}' not found.")


    # def addData(self, block_name, category, attributes, values):
    #     """
    #     Adds data to the specified block in the CIF file.

    #     Parameters:
    #     block_name (str): The name of the block to which data is to be added.
    #     category (str): The category of the data to be added.
    #     attributes (list[str]): The attributes of the data to be added.
    #     values (list[str]): The corresponding values of the attributes.

    #     Returns:
    #     None
    #     """
    #     block_number, block = self.getBlock(block_name)

    #     if block is None:
    #         print(f"Block '{block_name}' not found.")
    #         return

    #     # Create a new category
    #     new_category = DataContainer(category)

    #     # Add attributes and their respective values to the category
    #     for attribute, value in zip(attributes, values):
    #         new_category.appendAttribute(CifName(attribute))
    #         new_category.append([value])

    #     # Add the category to the block
    #     block.append(new_category)

    # def addData(self, block_name, category_name, data_dict):
    #     """
    #     This function adds a category with its data to a specific block.
        
    #     Parameters:
    #     block_name (str): The name of the block to which the category should be added.
    #     category_name (str): The name of the category to be added.
    #     data_dict (dict): A dictionary where the keys are the attribute names and the values are their respective values.
        
    #     Returns:
    #     None
    #     """
    #     block_number, block = self.getBlock(block_name)
    #     if block is None:
    #         print(f"Block {block_name} does not exist.")
    #         return
    #     new_category = ContainerBase(category_name)
    #     for attribute, value in data_dict.items():
    #         new_category.appendAttribute(attribute)
    #         new_category.append([value])
    #     block.append(new_category)

    # def addData(self, block_name, category_name, data_dict):
    #     """
    #     This function adds a category with its data to a specific block.
        
    #     Parameters:
    #     block_name (str): The name of the block to which the category should be added.
    #     category_name (str): The name of the category to be added.
    #     data_dict (dict): A dictionary where the keys are the attribute names and the values are their respective values.
        
    #     Returns:
    #     None
    #     """
    #     block_number, block = self.getBlock(block_name)
    #     if block is None:
    #         print(f"Block {block_name} does not exist.")
    #         return
    #     new_category = ContainerBase(category_name)
    #     for attribute in data_dict.keys():
    #         new_category.appendAttribute(attribute)
    #     new_category.append(list(data_dict.values()))
    #     block.append(new_category)


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

    # def reorderBlocks(self):
    #     """
    #     Reorder the blocks in the containers list based on self.__ordered_containers.

    #     Returns:
    #     None
    #     """
    #     container_dict = {container.getName(): container for container in self.__containers}
    #     ordered_containers = []
    #     for block_name in self.__ordered_containers:
    #         if block_name in container_dict:
    #             ordered_containers.append(container_dict[block_name])
    #     remaining_blocks = [container for container in self.__containers if container not in ordered_containers]
    #     self.__containers = ordered_containers + remaining_blocks

    # def reorderBlocks(self):
    #     """
    #     Reorder the blocks in the containers list based on self.__ordered_containers.

    #     Returns:
    #     None
    #     """
    #     print("#################################################################################################")
    #     print("Existing block names:", self.getBlocksNames())  # For debugging

    #     container_dict = {container.getName(): container for container in self.__containers}
    #     ordered_containers = []
    #     for block_name in self.__ordered_containers:
    #         if block_name in container_dict:
    #             ordered_containers.append(container_dict[block_name])
    #         else:
    #             print(f"Block {block_name} not found in containers.")  # For debugging
    #     remaining_blocks = [container for container in self.__containers if container not in ordered_containers]
    #     self.__containers = ordered_containers + remaining_blocks
    #     print("Final block names:", self.getBlocksNames())
    #     print("#################################################################################################")

    # def reorderCategories(self):
    #     """
    #     Reorder the categories in the default block based on self.__ordered_categories.

    #     Returns:
    #     None
    #     """
    #     default_block = self.__containers[self.__default_block_number]
    #     #category_dict = {category.getName(): category for category in default_block}
    #     category_dict = self.getCategories()
    #     ordered_categories_list = []
    #     for category_name in self.__ordered_categories:
    #         if category_name in category_dict:
    #             ordered_categories_list.append(category_dict[category_name])
    #         else:
    #             print(f"Category {category_name} not found in block.")
    #     remaining_categories = [category for category in default_block if category not in ordered_categories_list]
    #     new_block = ContainerBase(default_block.getName())
    #     for category in ordered_categories_list + remaining_categories:
    #         new_block.append(category)
    #     self.__containers[self.__default_block_number] = new_block

    # def reorderCategories(self):
    #     """
    #     Reorder the categories in the default block based on self.__ordered_categories.

    #     Returns:
    #     None
    #     """
    #     default_block = self.__containers[self.__default_block_number]
    #     categories_names = default_block.getObjNameList()
    #     category_dict = {name: default_block.getObj(name) for name in categories_names}
    #     ordered_categories_list = []
    #     for category_name in self.__ordered_categories:
    #         if category_name in category_dict:
    #             ordered_categories_list.append(category_dict[category_name])
    #         else:
    #             print(f"Category {category_name} not found in block.")
    #     remaining_categories = [category_dict[name] for name in categories_names if name not in self.__ordered_categories]
    #     new_block = ContainerBase(default_block.getName())
    #     for category in ordered_categories_list + remaining_categories:
    #         new_block.append(category)
    #     self.__containers[self.__default_block_number] = new_block

    # def reorderCategories(self):
    #     """
    #     Reorder the categories in the default block based on self.__ordered_categories.

    #     Returns:
    #     None
    #     """
    #     default_block = self.__containers[self.__default_block_number]
    #     categories_names = default_block.getObjNameList()
    #     category_dict = {name: default_block.getObj(name) for name in categories_names}
    #     ordered_categories_list = []
    #     for category_name in self.__ordered_categories:
    #         if category_name in category_dict:
    #             ordered_categories_list.append(category_dict[category_name])
    #         else:
    #             print(f"Category {category_name} not found in block.")
    #     remaining_categories = [category_dict[name] for name in categories_names if name not in self.__ordered_categories]
    #     new_block = ContainerBase(default_block.getName())
    #     for category in ordered_categories_list + remaining_categories:
    #         new_block.append(category)
    #     self.__containers[self.__default_block_number] = new_block

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

        print("#################################################################################################")









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