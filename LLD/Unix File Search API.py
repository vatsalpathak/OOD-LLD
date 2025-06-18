"""
Problem Summary:
Design a Unix File Search API that allows searching files with multiple constraints such as:
- file name
- extension
- size
- etc.

Key requirements:
- The solution should be easily extendable to add new constraints.
- Should support combining constraints using AND/OR logic.

Recommended Design Pattern:
- Use the Specification Pattern.
- Each constraint is implemented as a Specification class.
- Combine constraints using logical combinators (AndSpecification, OrSpecification).

This design supports both simplicity and maintainability.
"""

from abc import ABC,abstractmethod

class File:
    def __init__(self, name,extension,size):
        self.name = name
        self.extension = extension
        self.size = size

    def __repr__(self):
        return f"File(name={self.name}, extension={self.extension}, size={self.size})"

class Specification(ABC):
    @abstractmethod
    def is_satisfied(file):
        pass

class NameSpecification(Specification):
    def __init__(self, name: str):
        self.name = name

    def is_satisfied(self,file):
        return file.name == self.name

class ExtensionSpecification(Specification):
    def __init__(self, extension: str):
        self.extension = extension

    def is_satisfied(self,file):
        return file.extension == self.extension
    
class SizeSpecification(Specification):
    def __init__(self, size: str):
        self.size = size

    def is_satisfied(self,file):
        return file.size == self.size

class AndSpecification(Specification):
    def __init__(self, *specs):
        self.specs = specs
    
    def is_satisfied(self,file):
        return all(spec.is_satisfied(file) for spec in self.specs)
    
class OrSpecification(Specification):
    def __init__(self, *specs):
        self.specs = specs
    
    def is_satisfied(self,file):
        return any(spec.is_satisfied(file) for spec in self.specs)
    
class FileSearch:
    def __init__(self, files):
        self.files = files

    def filter(self, spec: Specification):
        return [file for file in self.files if spec.is_satisfied(file)]
    
if __name__ == "__main__":
    # Sample files
    files = [
        File("report", "pdf", 200),
        File("notes", "txt", 150),
        File("presentation", "ppt", 300),
        File("document", "txt", 100),
        File("data", "csv", 200)
    ]

    search = FileSearch(files)

    # Search: all .txt files
    txt_spec = ExtensionSpecification("txt")
    txt_files = search.filter(txt_spec)
    print("\nTXT files:", txt_files)

    # Search: files with name 'report'
    report_spec = NameSpecification("report")
    report_files = search.filter(report_spec)
    print("\nFiles named 'report':", report_files)

    # Search: files with size 200 AND extension 'csv'
    size_spec = SizeSpecification(200)
    csv_spec = ExtensionSpecification("csv")
    combined_and = AndSpecification(size_spec, csv_spec)
    and_result = search.filter(combined_and)
    print("\nFiles with size=200 AND extension='csv':", and_result)

    # Search: files named 'notes' OR extension 'ppt'
    notes_spec = NameSpecification("notes")
    ppt_spec = ExtensionSpecification("ppt")
    combined_or = OrSpecification(notes_spec, ppt_spec)
    or_result = search.filter(combined_or)
    print("\nFiles named 'notes' OR extension='ppt':", or_result)
