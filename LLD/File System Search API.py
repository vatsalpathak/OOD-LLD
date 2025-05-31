# Question
# Design and implement a File System Search API that allows users to search for files based on name, extension, or size.
# Your system should:
# Represent a file system with files and directories.
# Allow filtering based on:
# File name (e.g. readme)
# File extension (e.g. txt, pdf)
# File size using operators like >, <, >=, ==, etc.
# Support combining multiple filters using logical AND/OR conditions.
# Traverse all subdirectories recursively to apply the search.

from abc import ABC, abstractmethod

class File:
    def __init__(self,name,extension,size) -> None:
        self.name = name
        self.extension = extension
        self.size = size 

    def __str__(self):
        return f"{self.name}.{self.extension} ({self.size}KB)"


class Filter(ABC):
    @abstractmethod
    def match(self, file):
        pass

class NameFilter(Filter):
    def __init__(self, name):
        self.name = name

    def match(self, file):
        return file.name == self.name

class ExtensionFilter(Filter):
    def __init__(self, extension):
        self.extension = extension

    def match(self, file):
        return file.extension == self.extension

class SizeFilter(Filter):
    def __init__(self, size,operator):
        self.size = size
        self.operator = operator

    def match(self, file):
        return eval(f"{file.size} {self.operator} {self.size}")

class FileSystem:
    def __init__(self,name,isDirectory) -> None:
        self.name = name
        self.isDirectory = isDirectory
        self.files = [] 
        self.subDirectories = [] 

    def print_structure(self, indent=0):
        prefix = "  " * indent
        print(f"{prefix}{'[DIR]' if self.isDirectory else '[FILE]'} {self.name}")
        
        for file in self.files:
            print(f"{prefix}  └── {file}")  # uses __str__ from File

        for sub in self.subDirectories:
            sub.print_structure(indent + 1)


class Search:
    def __init__(self,root_directory,filters,condition='AND'):
        self.root = root_directory
        self.filters = filters
        self.condition = condition

    def check_conditions(self, file):
        if self.condition == "AND":
            return all(f.match(file) for f in self.filters)
        else:
            return any(f.match(file) for f in self.filters)
        
    def find_files(self):
        result = []

        def dfs(directory):
            # Check each file
            for file in directory.files:
                if self.check_conditions(file):
                    result.append(file.name)
            # Recurse into subdirectories
            for sub in directory.subDirectories:
                dfs(sub)

        dfs(self.root)
        return result



if __name__ == "__main__":
    # Create files
    f1 = File("readme", "txt", 10)
    f2 = File("report", "pdf", 20)
    f3 = File("main", "py", 5)
    f4 = File("notes", "txt", 25)

    # Root directory
    root = FileSystem("/", True)
    root.files.extend([f1, f2])

    # Subdirectory
    sub = FileSystem("sub", True)
    sub.files.append(f3)

    # Nested subdirectory
    nested = FileSystem("nested", True)
    nested.files.append(f4)

    # Attach subdirectories
    sub.subDirectories.append(nested)
    root.subDirectories.append(sub)

    # Visualize file system structure
    print("File System Structure:\n")
    root.print_structure()

    # Perform a search
    filters = [ExtensionFilter("txt"), SizeFilter(15, ">=")]
    search = Search(root, filters, condition="AND")
    print("\nMatching files:", search.find_files())  # Expect: ['notes']
