// -----------------------------------------------------------------------------
// Copyright (c) 2016   Daniel Standage <daniel.standage@gmail.com>
//
// This file is part of contra (http://github.com/standage/contra) and is
// licensed under the MIT license: see LICENSE.txt.
// -----------------------------------------------------------------------------

#ifndef CONTRA_NODE
#define CONTRA_NODE

#include <memory>

namespace contra_cpp
{

template<typename Data>
class node
{
    public:
        std::unique_ptr< node<Data> > left;
        std::unique_ptr< node<Data> > right;
        Data data;
        int height;

        node<Data>(Data value)
            : left(nullptr), right(nullptr), data(value), height(-1) {}
        node<Data>(Data value, int ht)
            : left(nullptr), right(nullptr), data(value), height(ht) {}
};

} // namespace contra_cpp

#endif // define CONTRA_NODE
