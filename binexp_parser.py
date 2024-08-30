#!/usr/bin/python3
import os
from os.path import join as osjoin

import unittest

from enum import Enum

# Use these to distinguish node types, note that you might want to further
# distinguish between the addition and multiplication operators
NodeType = Enum('BinOpNodeType', ['number', 'plus', 'mult'])

class BinOpAst():
    """
    A somewhat quick and dirty structure to represent a binary operator AST.

    Reads input as a list of tokens in prefix notation, converts into internal representation,
    then can convert to prefix, postfix, or infix string output.
    """
    def __init__(self, prefix_list):
        """
        Initialize a binary operator AST from a given list in prefix notation.
        Destroys the list that is passed in.
        """
        self.val = prefix_list.pop(0)
        if self.val.isnumeric():
            self.type = NodeType.number
            self.left = False
            self.right = False
        elif self.val == '+':
            self.type = NodeType.plus
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)
        else:
            self.type = NodeType.mult
            self.left = BinOpAst(prefix_list)
            self.right = BinOpAst(prefix_list)

    def __str__(self, indent=0):
        """
        Convert the binary tree printable string where indentation level indicates
        parent/child relationships
        """
        ilvl = '  '*indent
        left = '\n  ' + ilvl + self.left.__str__(indent+1) if self.left else ''
        right = '\n  ' + ilvl + self.right.__str__(indent+1) if self.right else ''
        return f"{ilvl}{self.val}{left}{right}"

    def __repr__(self):
        """Generate the repr from the string"""
        return str(self)

    def prefix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        # getting weird bug so I had to rewrite
        # base case: if no right/left
        if not self.right:
            return self.val
        # recurse normally
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.plus:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()
            case NodeType.mult:
                return self.val + ' ' + self.left.prefix_str() + ' ' + self.right.prefix_str()

    def infix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.plus:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
            case NodeType.mult:
                return '(' + self.left.infix_str() + ' ' + self.val + ' ' + self.right.infix_str() + ')'
            
    def postfix_str(self):
        """
        Convert the BinOpAst to a prefix notation string.
        Make use of new Python 3.10 case!
        """
        match self.type:
            case NodeType.number:
                return self.val
            case NodeType.plus:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val
            case NodeType.mult:
                return self.left.postfix_str() + ' ' + self.right.postfix_str() + ' ' + self.val

    def additive_identity(self):
        """
        Reduce additive identities
        x + 0 = x
        """
        # + 0 x returns x
        # needs to walk through the tree recursively
        # base case: we are at leaf node
        if not self.right:
            return self
        # if node is a plus sign, recurse
        # specifically if one of the children is a 0 return only the opposite child
        if self.type == NodeType.plus:
            if self.right.val == '0':
                # in this case we are at end of tree as val = 0 is always a leaf
                self.val = self.left.val
                self.type = self.left.type
                self.right = False
                self.left = False
                return self
            elif self.left.val == '0':
                self.val = self.right.val
                self.type = self.right.type
                self.left = self.right.left
                self.right = self.right.right
                return self.additive_identity()
            else:
                return self.right.additive_identity()
        # else return the right child to progress down the tree
        else:
            return self.right.additive_identity()

     
    def multiplicative_identity(self):
        """
        Reduce multiplicative identities
        x * 1 = x
        """
        # * 1 x returns x
        # needs to walk through the tree recursively
        # base case: we are at leaf node
        if not self.right:
            return self
        # if node is a mult sign, recurse
        # specifically if one of the children is a 1 return only the opposite child
        if self.type == NodeType.mult:
            if self.right.val == '1':
                # in this case we are at end of tree as val = 1 is always a leaf
                self.val = self.left.val
                self.type = self.left.type
                self.right = False
                self.left = False
                return self
            elif self.left.val == '1':
                self.val = self.right.val
                self.type = self.right.type
                self.left = self.right.left
                self.right = self.right.right
                return self.multiplicative_identity()
            else:
                # regular mult expression, continue recursion
                return self.right.multiplicative_identity()
        # else return the right child to progress down the tree
        else:
            return self.right.multiplicative_identity()
    
    def mult_by_zero(self):
        """
        Reduce multiplication by zero
        x * 0 = 0
        """
        # * 0 x returns 0
        # needs to walk through the tree recursively
        # base case: we are at leaf node
        if not self.right:
            return self
        # if node is a mult sign, recurse
        # specifically if one of the children is a 0 return 0
        if self.type == NodeType.mult:
            if self.right.val == '0':
                # in this case we are at end of tree as val = 0 is always a leaf
                self.val = '0'
                self.type = NodeType.number
                self.right = False
                self.left = False
                return self
            elif self.left.val == '0':
                self.val = '0'
                self.type = NodeType.number
                self.left = self.right.left
                self.right = self.right.right
                return self.mult_by_zero()
            else:
                # regular mult expression, continue recursion
                return self.right.mult_by_zero()
        # else return the right child to progress down the tree
        else:
            return self.right.mult_by_zero()
    
    def constant_fold(self):
        """
        Fold constants,
        e.g. 1 + 2 = 3
        e.g. x + 2 = x + 2
        """
        # Optionally, IMPLEMENT ME! This is a bit more challenging. 
        # You also likely want to add an additional node type to your AST
        # to represent identifiers.
        pass            

    def simplify_binops(self):
        """
        Simplify binary trees with the following:
        1) Additive identity, e.g. x + 0 = x
        2) Multiplicative identity, e.g. x * 1 = x
        3) Extra #1: Multiplication by 0, e.g. x * 0 = 0
        4) Extra #2: Constant folding, e.g. statically we can reduce 1 + 1 to 2, but not x + 1 to anything
        """
        # I am calling everything twice because my code doesn't reduce level 1 trees
        # I assume it is an issue with recursion, but calling twice resolves it
        self.additive_identity()
        self.multiplicative_identity()
        self.mult_by_zero()
        self.additive_identity()
        self.multiplicative_identity()
        self.mult_by_zero()
        # self.constant_fold()

def testbench():
    testbench = osjoin('testbench')
    for test_op in os.listdir(testbench):
        print('--------  Testing Op: {}  --------'.format(test_op))
        ins = osjoin('inputs')
        outs = osjoin('outputs')
        for test_name in os.listdir(osjoin(testbench, test_op, ins)):
            print('Testing File: {}'.format(test_name))
            with open(osjoin(testbench, test_op, ins, test_name)) as fin:
                line = fin.read()
                input = line.split()
            with open(osjoin(testbench, test_op, outs, test_name)) as fout:
                expected = fout.read()
            test = BinOpAst(input)
            match test_op:
                case 'arith_id':
                    test.additive_identity()
                    output = test.prefix_str()
                case 'mult_id':
                    test.multiplicative_identity()
                    output = test.prefix_str()
                case 'mult_by_zero':
                    output = test.mult_by_zero().prefix_str()
                case 'combined':
                    test.simplify_binops()
                    output = test.prefix_str()
            try:
                assert output == expected
                print('++++  Test Case Passed  ++++')
                print('Input: {}'.format(line))
                print('Expected: {}'.format(expected))
                print('Output: {}'.format(output))
                print('++++++++++++++++++++++++++++\n')
            except AssertionError:
                print('XXXX  Test Case Failed  XXXX')
                print('Input: {}'.format(line))
                print('Expected: {}'.format(expected))
                print('Output: {}'.format(output))
                print('XXXXXXXXXXXXXXXXXXXXXXXXXXXX\n')
        print("--------------------------------------\n")

if __name__ == "__main__":
    testbench()
