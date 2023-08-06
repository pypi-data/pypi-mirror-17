# -----------------------------------------------------------------------------
# Copyright (c) 2016   Daniel Standage <daniel.standage@gmail.com>
#
# This file is part of contra (http://github.com/standage/contra) and is
# licensed under the MIT license: see LICENSE.txt.
# -----------------------------------------------------------------------------

# distutils: language = c++
# distutils: sources = src/bstree.cpp
# cython: c_string_type=str, c_string_encoding=ascii

from libcpp cimport bool
from libcpp.string cimport string
from libc.stdint cimport int32_t, uint64_t, uint8_t

cdef extern from "<iostream>" namespace "std":
    cdef cppclass ostream:
        ostream() except +

cdef extern from "<sstream>" namespace "std":
    cdef cppclass stringstream(ostream):
        stringstream() except +
        string str()

cdef extern from 'bstree.hpp' namespace 'contra_cpp':
    cdef cppclass bstree[T]:
        bstree() except +
        bool insert(T value)
        bool search(T value)
        void remove(T value)
        size_t height(T value)
        void inorder(ostream& stream)
        void preorder(ostream& stream)
        void postorder(ostream& stream)
        unsigned int size()

cdef class BStree:
    cdef bstree[int32_t] tree
    def insert(self, int32_t value):
        return self.tree.insert(value)
    def search(self, int32_t value):
        return self.tree.search(value)
    def remove(self, int32_t value):
        return self.tree.remove(value)
    def height(self, int32_t value):
        return self.tree.height(value)
    def inorder(self):
        cdef stringstream ss
        self.tree.inorder(ss)
        return ss.str()
    def preorder(self):
        cdef stringstream ss
        self.tree.preorder(ss)
        return ss.str()
    def postorder(self):
        cdef stringstream ss
        self.tree.postorder(ss)
        return ss.str()
    def __repr__(self):
        return '<contra.BStree instance with {} values>'.format(len(self))
    def __str__(self):
        return self.inorder()
    def __len__(self):
        return self.tree.size()

cdef class BStreeLarge:
    cdef bstree[uint64_t] tree
    def insert(self, uint64_t value):
        return self.tree.insert(value)
    def search(self, uint64_t value):
        return self.tree.search(value)
    def remove(self, uint64_t value):
        return self.tree.remove(value)
    def height(self, uint64_t value):
        return self.tree.height(value)
    def inorder(self):
        cdef stringstream ss
        self.tree.inorder(ss)
        return ss.str()
    def preorder(self):
        cdef stringstream ss
        self.tree.preorder(ss)
        return ss.str()
    def postorder(self):
        cdef stringstream ss
        self.tree.postorder(ss)
        return ss.str()
    def __repr__(self):
        return '<contra.BStreeLarge instance with {} values>'.format(len(self))
    def __str__(self):
        return self.inorder()
    def __len__(self):
        return self.tree.size()

cdef class BStreeSmall:
    cdef bstree[uint8_t] tree
    def insert(self, uint8_t value):
        return self.tree.insert(value)
    def search(self, uint8_t value):
        return self.tree.search(value)
    def remove(self, uint8_t value):
        return self.tree.remove(value)
    def height(self, uint8_t value):
        return self.tree.height(value)
    def inorder(self):
        cdef stringstream ss
        self.tree.inorder(ss)
        return ss.str()
    def preorder(self):
        cdef stringstream ss
        self.tree.preorder(ss)
        return ss.str()
    def postorder(self):
        cdef stringstream ss
        self.tree.postorder(ss)
        return ss.str()
    def __repr__(self):
        return '<contra.BStreeSmall instance with {} values>'.format(len(self))
    def __str__(self):
        return self.inorder()
    def __len__(self):
        return self.tree.size()
