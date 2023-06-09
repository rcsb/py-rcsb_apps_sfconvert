import argparse
from mmcif.io.IoAdapterCore import IoAdapterCore

class SFFile:
    def __init__(self):
        self.containers = []
        self.io_core = IoAdapterCore()

    def readFile(self, filename):
        self.containers = self.io_core.readFile(filename)

    def writeFile(self, filename):
        self.io_core.writeFile(filename, self.containers)

    def getBlocksNames(self):
        return [container.getName() for container in self.containers]

    def getBlock(self, name):
        for container in self.containers:
            if container.getName() == name:
                return container
        return None

    def getObj(self, block_name, category):
        block = self.getBlock(block_name)
        if block is None:
            return None
        return block.getObj(category)

    def setDefaultBlock(self, block_name):
        default_block = self.getBlock(block_name)
        if default_block is not None:
            self.containers.insert(0, self.containers.pop(self.containers.index(default_block)))

    def getDefaultObj(self, category):
        if len(self.containers) > 0:
            return self.containers[0].getObj(category)
        return None

    def getObjBlock(self, block_name, category):
        return self.getObj(block_name, category)

    def getCategories(self, block_name):
        block = self.getBlock(block_name)
        if block is not None:
            return block.getObjNameList()
        return None

def main():
    parser = argparse.ArgumentParser(description='Manipulate mmCIF files.')
    parser.add_argument('-r', '--read', metavar='filename', help='Read from an mmCIF file')
    parser.add_argument('-w', '--write', metavar='filename', help='Write to an mmCIF file')
    parser.add_argument('-b', '--block', metavar='block_name', help='Get block by name')
    parser.add_argument('-o', '--object', nargs=2, metavar=('block_name', 'category'), help='Get object from a block')
    parser.add_argument('-d', '--default', metavar='block_name', help='Set default block')
    parser.add_argument('-g', '--get', metavar='category', help='Get object from default block')
    parser.add_argument('-ob', '--objblock', nargs=2, metavar=('block_name', 'category'), help='Get object from a block')
    parser.add_argument('-l', '--list', action='store_true', help='List all blocks')
    parser.add_argument('-c', '--categories', metavar='block_name', help='List all categories in a block')

    args = parser.parse_args()

    sf_file = SFFile()

    if args.read:
        sf_file.readFile(args.read)
    if args.write:
        sf_file.writeFile(args.write)
    if args.block:
        print(sf_file.getBlock(args.block))
    if args.object:
        print(sf_file.getObj(*args.object))
    if args.default:
        sf_file.setDefaultBlock(args.default)
    if args.get:
        print(sf_file.getDefaultObj(args.get))
    if args.objblock:
        print(sf_file.getObjBlock(*args.objblock))
    if args.list:
        print(sf_file.getBlocksNames())
    if args.categories:
        print(sf_file.getCategories(args.categories))

if __name__ == "__main__":
    main()