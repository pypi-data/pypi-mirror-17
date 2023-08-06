#include <stdint.h>
#include "bstree.hpp"
#include "node.hpp"

namespace contra_cpp
{

template<typename Data>
bool bstree<Data>::insert(Data value)
{
    return insert(_root, value, -1);
}

template<typename Data>
bool bstree<Data>::search(Data value)
{
    return search(_root, value);
}

template<typename Data>
void bstree<Data>::remove(Data value)
{
    _root = remove(_root, value);
}

template<typename Data>
size_t bstree<Data>::size()
{
    return _count;
}

template<typename Data>
int bstree<Data>::height(Data value)
{
    return height(_root, value);
}

template<typename Data>
void bstree<Data>::inorder(std::ostream& stream)
{
    stream << "[";
    inorder(_root, stream);
    stream << " ]" << std::endl;
}

template<typename Data>
void bstree<Data>::preorder(std::ostream& stream)
{
    stream << "[";
    preorder(_root, stream);
    stream << " ]" << std::endl;
}

template<typename Data>
void bstree<Data>::postorder(std::ostream& stream)
{
    stream << "[";
    postorder(_root, stream);
    stream << " ]" << std::endl;
}

template<typename Data>
bool bstree<Data>::insert(nodeptr& root, Data value, int height)
{
    if (!root) {
        root = nodeptr(new node<Data>(value, height + 1));
//std::cerr << "DEBUG value=" << value << " root->data=" << root->data << '\n';
        _count++;
        return true;
    }
    else if (value > root->data) {
        return insert(root->right, value, height + 1);
    }
    else if (value < root->data) {
        return insert(root->left, value, height + 1);
    }
    return false;
}

template<typename Data>
bool bstree<Data>::search(nodeptr& root, Data value)
{
    if (!root) {
        return false;
    }
    else if (value == root->data) {
        return true;
    }
    else if (value > root->data) {
        return search(root->right, value);
    }
    else {
        return search(root->left, value);
    }

}

template<typename Data>
std::unique_ptr< node<Data> > bstree<Data>::remove(
    std::unique_ptr< node<Data> >& root,
    Data value, bool decr
)
{
    if (!root) {
        return std::move(root);
    }
    else if (value > root->data) {
        root->right = remove(root->right, value, decr);
    }
    else if (value < root->data) {
        root->left = remove(root->left, value, decr);
    }
    else {
        nodeptr temp = std::move(root);
        if (temp->left == temp->right) {
            _count--;
            return nodeptr();
        }
        if (!temp->left) {
            _count--;
            if(decr)
                decr_height(temp->right);
            return std::move(temp->right);
        }
        if (!temp->right) {
            _count--;
            if(decr)
                decr_height(temp->left);
            return std::move(temp->left);
        }

        int height = temp->height;
        nodeptr minright = minimum(temp->right);
        minright->height = height;
        minright->left = std::move(temp->left);
        minright->right = remove(temp, value, false);
        return minright;
    }
    return std::move(root);
}

template<typename Data>
std::unique_ptr< node<Data> > bstree<Data>::minimum(
    std::unique_ptr< node<Data> >& root
)
{
    if (!root || !root->left) {
        return std::move(root);
    }
    return minimum(root->left);
}

template<typename Data>
int bstree<Data>::height(nodeptr& root, Data value)
{
    if (!root) {
        return -1;
    }
    else if (value == root->data) {
        return root->height;
    }
    else if (value > root->data) {
        return height(root->right, value);
    }
    else {
        return height(root->left, value);
    }
}

template<typename Data>
void bstree<Data>::decr_height(nodeptr& root)
{
    if (!root) {
        return;
    }
    root->height -= 1;
    decr_height(root->left);
    decr_height(root->right);
}

template<typename Data>
void bstree<Data>::inorder(nodeptr& root, std::ostream& stream)
{
    // By default std::cout prints some integer types (such as uint8_t) as
    // character values rather than numerical values. We force printing as
    // numerical value by prepending root->data with a + symbol. See
    // http://stackoverflow.com/a/31991844/459780.
    if(root) {
        inorder(root->left, stream);
        stream << " " << +root->data;
        inorder(root->right, stream);
    }
}

template<typename Data>
void bstree<Data>::preorder(nodeptr& root, std::ostream& stream)
{
    if(root) {
        stream << " " << +root->data;
        preorder(root->left, stream);
        preorder(root->right, stream);
    }
}

template<typename Data>
void bstree<Data>::postorder(nodeptr& root, std::ostream& stream)
{
    if(root) {
        postorder(root->left, stream);
        postorder(root->right, stream);
        stream << " " << +root->data;
    }
}

template class bstree<int32_t>;
template class bstree<uint64_t>;
template class bstree<uint8_t>;
} // namespace contra_cpp
