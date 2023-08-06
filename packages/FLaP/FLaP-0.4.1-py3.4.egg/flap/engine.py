#
# This file is part of Flap.
#
# Flap is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Flap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Flap.  If not, see <http://www.gnu.org/licenses/>.
#

from flap.util.oofs import MissingFile
from flap.util.path import Path


class Processor:
    """
    Exposes a list of fragments, likely as a generator.
    """

    def fragments(self):
        pass


class Listener:
    """
    May react to specific fragments
    """

    def on_fragment(self, fragment):
        pass


class Fragment:
    """
    A fragment of text, taken from a line in a file
    """
    
    def __init__(self, file, lineNumber=1, text=None):
        if lineNumber < 1:
            raise ValueError("Line number must be strictly positive (found %d)" % lineNumber)
        self._lineNumber = lineNumber
        if file.isMissing():
            raise ValueError("Missing file '%s'" % file.fullname())
        self._file = file
        self._text = text if text is not None else self._file.content()

    def line_number(self):
        return self._lineNumber

    def file(self):
        return self._file
    
    def text(self):
        return self._text
    
    def is_commented_out(self):
        return self._text.strip().startswith("%")

    def extract(self, match, desired_group=0):
        """
        :return: a sub fragment corresponding to the given match in the container fragment
        """
        line_number = self.line_number() + self[:match.start()].text().count("\n")
        text = match.group(desired_group)
        return Fragment(self.file(), line_number, text)

    def replace(self, searched, replacement):
        changed_text = self.text().replace(searched, replacement)
        return Fragment(self._file, self.line_number(), changed_text)

    def __getitem__(self, key):
        return Fragment(self._file, self._lineNumber, self._text[key])

    def __repr__(self):
        return self._text


class Flap:
    """
    The Flap engine. Does the flattening of LaTeX projects, including merging
    included files, moving graphics and resources files such as classes, styles 
    and bibliography 
    """

    DEFAULT_OUTPUT_FILE = "merged.tex"
    
    def __init__(self, file_system, factory, listener=Listener()):
        self._file_system = file_system
        self._listener = listener
        self._included_files = []
        self._graphics_directory = None
        self._create = factory
        self._merged_file = self.DEFAULT_OUTPUT_FILE
        self._root = MissingFile("main.tex")

    def flatten(self, root, output):
        self.find_output_directory(output)
        self.open_file(root)
        self.merge_latex_source()
        self.copy_resource_files()

    def find_output_directory(self, output):
        if output is None: return
        if output.has_extension():
            self._merged_file = output.fullname()
            self._output = output.container()
        else:
            self._merged_file = self.DEFAULT_OUTPUT_FILE
            self._output = output

    def open_file(self, source):
        self._root = self._file_system.open(source)
        if self._root.isMissing():
            raise ValueError("The file '%s' could not be found." % source)

    def merge_latex_source(self):
        merged = ''.join((each.text() for each in self._fragments()))
        self._file_system.create_file(self._output / self._merged_file, merged)

    def _fragments(self):
        return self._create.flap_pipeline(self, self._root).fragments()

    def copy_resource_files(self):
        project = self._root.container()
        for eachFile in project.files():
            if self._is_resource(eachFile):
                self._file_system.copy(eachFile, self._output)

    @staticmethod
    def _is_resource(file):
        return file.has_extension() and \
               file.extension() in Flap.RESOURCE_FILES

    RESOURCE_FILES = ["cls", "sty", "bst"]

    def is_ignored(self, file):
        return self._included_files and \
               file not in self._included_files

    def _root_directory(self):
        return self._root.container()

    def find_tex_source(self, fragment, path, extensions):
        return self._find(path, self._root_directory(), extensions, TexFileNotFound(fragment))

    def find_graphics(self, fragment, path, extensions_by_priority):
        return self._find(path, self.graphics_directory(), extensions_by_priority, GraphicNotFound(fragment))

    def find_resource(self, fragment, path, extensions_by_priority):
        return self._find(path, self._root_directory(), extensions_by_priority, ResourceNotFound(fragment))

    @staticmethod
    def _find(path, directory, extensions, error):
        candidates = directory.files_that_matches(Path.fromText(path))
        for any_possible_extension in extensions:
            for any_resource in candidates:
                if any_resource.has_extension(any_possible_extension):
                    return any_resource
        raise error

    def raw_fragments_from(self, file):
        return self._create.input_merger(file, self).fragments()

    def relocate(self, resource):
        new_path = resource._path.relative_to(self._root_directory()._path)
        new_file_name = str(new_path).replace("/", "_")
        self._file_system.copy(resource, self._output / new_file_name)
        return str(new_path.without_extension()).replace("/", "_")

    def on_fragment(self, fragment):
        self._listener.on_fragment(fragment)

    def restrict_inclusion_to(self, included_files):
        self._included_files = [each_file.strip() for each_file in included_files]

    def set_graphics_directory(self, path_to_graphics):
        path = self._root_directory().path() / path_to_graphics
        self._graphics_directory = self._file_system.open(path)

    def graphics_directory(self):
        if self._graphics_directory:
            return self._graphics_directory
        return self._root_directory()


class ResourceNotFound(Exception):

    def __init__(self, fragment):
        self._fragment = fragment

    def fragment(self):
        return self._fragment


class GraphicNotFound(ResourceNotFound):
    """
    Exception thrown when a graphic file cannot be found
    """
    def __init__(self, fragment):
        super().__init__(fragment)


class TexFileNotFound(ResourceNotFound):
    """
    Exception thrown when a LaTeX source file cannot be found
    """

    def __init__(self, fragment):
        super().__init__(fragment)
