// -----------------------------------------------------------------------------
// Copyright (c) 2016   Daniel Standage <daniel.standage@gmail.com>
//
// This file is part of contra (http://github.com/standage/contra) and is
// licensed under the MIT license: see LICENSE.txt.
// -----------------------------------------------------------------------------

#ifndef CONTRA_BS_TREE
#define CONTRA_BS_TREE

#include <iostream>
#include <ostream>
#include "node.hpp"

namespace contra_cpp
{

template<typename Data>
class bstree
{
    public:
        bstree<Data>() : _root(nullptr), _count(0) {}

        bool insert(Data value);
        bool search(Data value);
        void remove(Data value);
        size_t size();
        int height(Data value);

        void inorder(std::ostream& stream = std::cout);
        void preorder(std::ostream& stream = std::cout);
        void postorder(std::ostream& stream = std::cout);

    protected:
        typedef std::unique_ptr< node<Data> > nodeptr;
        nodeptr _root;
        size_t _count;

        bool insert(nodeptr& root, Data value, int height);
        bool search(nodeptr& root, Data value);
        nodeptr remove(nodeptr& root, Data value, bool decr = true);
        nodeptr minimum(nodeptr& root);
        int height(nodeptr& root, Data value);
        void decr_height(nodeptr& root);

        void inorder(nodeptr& root, std::ostream& stream);
        void preorder(nodeptr& root, std::ostream& stream);
        void postorder(nodeptr& root, std::ostream& stream);

}; // class bstree

} // namespace contra_cpp

#endif // define CONTRA_BS_TREE
