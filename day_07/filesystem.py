# Authored by Carlos Serra-Toro (https://carlosserratoro.com)
# See the file LICENSE for the licence
import os


class FileSystem:
    def __init__(self):
        self._root = None  # The root of the filesystem.
        self._current_dir = None  # The directory we are currently at.

    def add_directory(self, dir_name):
        """Add a directory to the current directory"""
        if dir_name not in {c._name for c in self._current_dir._children}:
            d = File(name=dir_name, parent=self._current_dir, is_dir=True)
            self._current_dir.add_children(d)

    def add_file(self, file_name, file_size):
        """Add a file to the current directory, update the size"""
        if file_name not in {c._name for c in self._current_dir._children}:
            d = File(name=file_name, parent=self._current_dir, size=file_size)
            self._current_dir.add_children(d)

            self._current_dir._size += file_size
            parent = self._current_dir._parent
            while parent:
                parent._size += file_size
                parent = parent._parent

    def move_up(self):
        """Move one level up in the file directory"""
        self._current_dir = self._current_dir._parent

    def move_to(self, dir_name):
        """Move to a directory inside the current one"""
        d = File(name=dir_name, parent=self._current_dir, is_dir=True)
        if not self._root:
            self._root = d
            self._current_dir = d
        elif dir_name not in {c._name for c in self._current_dir._children}:
            self.add_directory(dir_name)
        else:
            self._set_current_dir(dir_name)

    def _set_current_dir(self, dir_name):
        for target in self._current_dir._children:
            if target._name == dir_name:
                self._current_dir = target
                break

    def _traverse(self, o, node, level=0):
        indentation = ' ' * 2 * level
        if node._is_dir:
            o.append('%s- %s' % (indentation, node))
            for children in node._children:
                self._traverse(o, children, level+1)
        else:
            o.append('%s- %s' % (indentation, node))

    def __iter__(self):
        s = [self._root]
        while s:
            node = s.pop()
            s.extend(node._children)
            yield node

    def __str__(self):
        o = []
        self._traverse(o, self._root)
        return os.linesep.join(o)


class File:
    def __init__(self, name, parent, is_dir=False, size=0):
        self._name = name
        self._parent = parent
        self._is_dir = is_dir
        self._size = size
        self._children = []

    def add_children(self, children):
        self._children.append(children)

    def __eq__(self, other):
        return (
            self._name == other._name
            and self._is_dir == other._is_dir
            and self._parent == other._parent
        )

    def __str__(self):
        return '%s (%s, size=%d)' % (
            self._name,
            'dir' if self._is_dir else 'file',
            self._size
        )
