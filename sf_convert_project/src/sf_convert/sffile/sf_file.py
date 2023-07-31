import argparse
from mmcif.io.IoAdapterCore import IoAdapterCore
from mmcif.api.PdbxContainers import ContainerBase, DataContainer
from mmcif.api.DataCategoryBase import DataCategoryBase
from pathlib import Path

import sys
export_path = Path('/Users/vivek/Library/CloudStorage/OneDrive-RutgersUniversity/Desktop files/Summer/py-rcsb_apps_sfconvert/sf_convert_project/src/sf_convert/export')
sys.path.append(str(export_path))
from cns_export import CNSConverter
from mtz_export import MTZConverter

class StructureFactorFile:
    def __init__(self):
        self.__data_blocks = []  # Contains the data blocks in the file
        self.__file_io = IoAdapterCore()  # Handles file input/output
        self.__default_block_index = 0  # The index of the default data block

    def read_file(self, filename):
        try:
            self.__data_blocks = self.__file_io.readFile(filename)
        except Exception as e:
            raise RuntimeError(f"Failed to read file {filename}") from e

    def get_block_by_index(self, block_index):
        if 0 <= block_index < len(self.__data_blocks):
            return self.__data_blocks[block_index]
        else:
            print(f"Block index {block_index} is not valid. It should be between 0 and {len(self.__data_blocks) - 1}.")
            return None 

    def get_number_of_blocks(self):
        return len(self.__data_blocks)

    def write_file(self, filename):
        self.__file_io.writeFile(filename, self.__data_blocks)

    def get_all_block_names(self):
        return [block.getName() for block in self.__data_blocks]

    def get_block_by_name(self, name):
        for idx, block in enumerate(self.__data_blocks):
            if block.getName() == name:
                return idx, block
        return None, None

    def get_category_object(self, category, block_name=None):
        if block_name is None:
            block_index = self.__default_block_index
            return self.__data_blocks[block_index].getObj(category)
        else:
            block_index, block_res = self.get_block_by_name(block_name)
            if block_res is None:
                return None
            return block_res.getObj(category)

    def set_default_block(self, block_name):
        block_index, _ = self.get_block_by_name(block_name)
        if block_index is not None:
            self.__default_block_index = block_index

    def get_category_names(self, block_name=None):
        if block_name == "Default" or block_name == None:
            block_index = self.__default_block_index
            return self.__data_blocks[block_index].getObjNameList()
        else:
            block_index, block_res = self.get_block_by_name(block_name)
            if block_res is None:
                return None
            return block_res.getObjNameList()

    def append_category_to_block(self, category, block_name=None):
        if block_name is None:
            block = self.__data_blocks[self.__default_block_index]
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return
        block.append(category)

    def remove_category_by_name(self, category_name, block_name=None):
        if block_name is None:
            block = self.__data_blocks[self.__default_block_index]
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return False
        removed_category = block.remove(category_name)
        #print(removed_category)
        return removed_category #is not None

    def add_data_to_block(self, category_name, data_dict, block_name=None):
        """
        This function adds a category with its data to a specific block.
        If no block name is provided, data will be added to the default block.
        
        Parameters:
        category_name (str): The name of the category to be added.
        data_dict (dict): A dictionary where the keys are the attribute names and the values are their respective values.
        block_name (str, optional): The name of the block to which the category should be added. Defaults to None.
        
        Returns:
        None
        """
        if block_name is None:
            block = self.__data_blocks[self.__default_block_index]
        else:
            _, block = self.get_block_by_name(block_name)
            if block is None:
                print(f"Block {block_name} does not exist.")
                return
        new_category = DataCategoryBase(category_name)
        for attribute in data_dict.keys():
            new_category.appendAttribute(attribute)
        new_category.append(list(data_dict.values()))
        block.append(new_category)

    def remove_duplicates_in_category(self, category_name, block_name=None):
            if block_name is None:
                block = self.get_block_by_index(self.default_block_index)
            else:
                _, block = self.get_block_by_name(block_name)
                if block is None:
                    print(f"Block {block_name} does not exist.")
                    return False

            category = block.getObj(category_name)
            if category is None:
                print(f"Category {category_name} does not exist in block {block.getName()}.")
                return False

            initial_row_count = category.getRowCount()
            seen = set()
            category.data[:] = [x for x in category.data if tuple(x) not in seen and not seen.add(tuple(x))]
            final_row_count = category.getRowCount()

            return initial_row_count != final_row_count
