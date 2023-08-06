#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Build and manipulate CNF formulas

The module `contains facilities to generate cnf formulas, in
order to be printed in DIMACS or LaTeX formats. Such formulas are
ready to be fed to sat solvers.

The module implements the `CNF` object, which is the main entry point
to the `cnfformula` library. 



Copyright (C) 2012, 2013, 2014, 2015, 2016  Massimo Lauria <lauria.massimo@gmail.com>
https://github.com/MassimoLauria/cnfgen.git

"""


from __future__ import print_function
from itertools import product
from itertools import combinations,combinations_with_replacement
from collections import Counter
import re

from . import prjdata as pd
from .graphs import bipartite_sets,neighbors

_default_header="Generated with `cnfgen`\n(C) {}\n{}\n\n".format(pd.__copyright__,
                                                                 pd.__url__)

class CNF(object):
    """Propositional formulas in conjunctive normal form.

    A CNF  formula is a  sequence of  clauses, which are  sequences of
    literals. Each literal is either a variable or its negation.

    Use ``add_variable`` method to add a variable to the formula. Two
    variable with the same name are considered the same variable, add
    successive additions do not have any effect.

    Use ``add_clause`` to add new clauses to CNF. Clauses will be added
    multiple times in case of multiple insertion of the same clauses.

    For documentation purpose it is possible use have an additional
    comment header at the top of the formula, which will be
    *optionally* exported to LaTeX or dimacs.

    Implementation:  for efficiency reason clauses and variable can
    only be added, and not deleted. Furthermore order matters in
    the representation.

    Examples
    --------
    >>> c=CNF([ [(True,"x1"),(True,"x2"),(False,"x3")], \
              [(False,"x2"),(True,"x4")] ])
    >>> print( c.dimacs(export_header=False) )
    p cnf 4 2
    1 2 -3 0
    -2 4 0
    >>> c.add_clause( [(False,"x3"),(True,"x4"),(False,"x5")] )
    >>> print( c.dimacs(export_header=False))
    p cnf 5 3
    1 2 -3 0
    -2 4 0
    -3 4 -5 0
    """

    def __init__(self, clauses=None, header=None):
        """Propositional formulas in conjunctive normal form.

        Parameters
        ----------
        clauses : ordered list of clauses
            a clause with k literals list containing k pairs, each
            representing a literal (see `add_clause`). First element
            is the polarity and the second is the variable, which must
            be an hashable object.

            E.g. (not x3) or x4 or (not x2) is encoded as [(False,"x3"),(True,"x4"),False,"x2")]

        header: string, optional
            a preamble which documents the formula
        """

        self._header = header if header!=None else _default_header

        # Initial empty formula
        self._clauses         = []

        # Variable indexes <--> Variable names correspondence
        # first variable is indexed with 1.
        self._index2name      = [None]
        self._name2index      = dict()
        self._name2descr      = dict()

        # Internal coherence can be disrupted by some methods.  API
        # methods require it to be rechecked.
        self._coherent        = True

        # Load the initial data into the CNF
        for c in clauses or []:
            self.add_clause(c)


    # Formula contains an header property
    def _set_header(self, value):
        """Header setter"""
        self._header = value

    def _get_header(self):
        """Header getter"""
        return self._header

    header = property(_get_header, _set_header)

    #
    # Implementation of some standard methods
    #

    def __iter__(self):
        """Iterates over all clauses of the CNF
        """
        for cls in self._clauses:
            assert self._coherent
            yield self._uncompress_clause(cls)

    def __str__(self):
        """String representation of the formula
        """
        assert self._coherent
        return self._header

    def __len__(self):
        """Number of clauses in the formula
        """
        return len(self._clauses)


    #
    # Internal implementation methods, use at your own risk!
    #

    def _uncompress_clause(self, clause):
        """(INTERNAL USE) Uncompress a clause from the numeric representation.

        Arguments:
        - `clause`: clause to be uncompressed

        >>> c=CNF()
        >>> c.add_clause([(True,"x"),(False,"y")])
        >>> print(c._uncompress_clause([-1,-2]))
        [(False, 'x'), (False, 'y')]
        """
        return [ (l>0, self._index2name[abs(l)]) for l in clause ]

    def _compress_clause(self, clause):
        """Convert a clause to its numeric representation.

        For reason of efficiency, clauses are memorized as tuples of
        integers. Each integer correspond to a variable, with sign +1
        or -1 depending whether it represents a positive or negative
        literal. The correspondence between the numbers and the
        variables names depends on the formula itself

        Parameters
        ----------
        clause: list of pairs
            a clause, in the form of a list of literals, which are
            pairs (bool,string).

        Returns
        -------
        a tuple of int

        Examples
        --------
        >>> c=CNF()
        >>> c.add_clause([(True,"x"),(False,"y")])
        >>> print(c._compress_clause([(False, 'x'), (False, 'y')]))
        (-1, -2)

        """
        return tuple((1 if p else -1) * self._name2index[n] for p, n in clause)


    def _add_compressed_clauses(self, clauses):
        """(INTERNAL USE) Add to the CNF a list of compressed clauses.

        This method uses the internal compressed clause representation
        to add a large batch of data  into the CNF.  It does not check
        for internal  coherence conditions,  and it  does not  need to
        convert between  internal and external  clause representation,
        so it  is very fast.   When assertions  are tested, a  call to
        this method will  disable the standard API, since  the CNF can
        be in an inconsistent state.

        Whenever the high level API is used with an inconsisten state
        the code will fail some assertion.

        In particular it does not check if the indexes correspond to a
        variable in the formula.

        To test consistency and re-enable the API, please call method
        `CNF._check_coherence`.

        Arguments:
        - `clauses`: a sequence of compressed clauses.

        >>> c=CNF()

        We add the variables in advance, so that the internal status
        stays coherent.

        >>> c.add_variable("x")
        >>> c.add_variable("y")
        >>> c.add_variable("z")

        When we add some compressed clauses, we need to test the
        internal status of the object. If the test is positive, then
        the high level API is available again.

        >>> c._add_compressed_clauses([[-1,2,3],[-2,1],[1,-3]])
        >>> c._check_coherence()
        True
        >>> print(c.dimacs(export_header=False))
        p cnf 3 3
        -1 2 3 0
        -2 1 0
        1 -3 0

        If we call the internal API several times, we need to test the
        object only once.

        >>> c._add_compressed_clauses([[-2,-3]])
        >>> c._add_compressed_clauses([[-1, 2]])
        >>> c._check_coherence()
        True
        >>> print(c.dimacs(export_header=False))
        p cnf 3 5
        -1 2 3 0
        -2 1 0
        1 -3 0
        -2 -3 0
        -1 2 0
        """
        self._coherent = False
        self._clauses.extend(tuple(c) for c in clauses)


    def _check_coherence(self, force=False):
        """Check if the formula is internally consistent.

        Certain fast manipulation methods are not safe if used
        incorrectly, so the CNF object may be corrupted. This method
        tests if that was not the case.

        Arguments:
        - `force`: force check even if the formula claims coherence

        >>> c=CNF()
        >>> c.add_variable("x")
        >>> c.add_variable("y")

        We add clauses mentioning three variables, and the formula is
        not coherent.

        >>> c._add_compressed_clauses([(-1,2),(1,-2),(1,3)])
        >>> c._check_coherence()
        False

        We cannot use the API now

        >>> c.clauses()
        Traceback (most recent call last):
        AssertionError
        """
        if not force and self._coherent:
            return True

        varindex=self._name2index
        varnames=self._index2name
        
        # number of variables and clauses
        N=len(varindex.keys())
        
        # Consistency in the variable dictionary
        if N != len(varnames)-1:
            return False

        for i in range(1,N+1):
            if varindex[varnames[i]]!=i:
                return False


        # Count clauses and check literal representation
        for clause in self._clauses:
            for literal in clause:
                if not 0 < abs(literal) <= N:
                    return False

        # formula passed all tests
        self._coherent = True
        return True

    #
    # High level API: build the CNF
    #

    def add_clause(self,clause,
                   literal_repetitions=False,
                   opposite_literals=False,
                   auto_variables=True,
                   strict=False):
        """Add a clause to the CNF.

        The clause must be well formatted. Otherwise it raises
        `TypeError` if the clause is not well formatted.

        E.g. (not x3) or x4 or (not x2) is encoded as
             [(False,u"x3"),(True,u"x4"),(False,u"x2")]

        All variable mentioned in the clause will be added to the list
        of variables  of the CNF,  in the  order of appearance  in the
        clauses.

        Parameters
        ----------
        clause: list of (bool,str) 
            the clause to be added in the CNF

            A clause with k literals is a list with k pairs.
            First coords are the polarities, second coords are utf8
            encoded strings with variable names.

            Clause may contain repeated or opposite literal, but this
            behavior can be modified by the optional flags. 

            Clauses are added with repetition, i.e. if the same clause
            is added twice then it will occur twice in the
            formula too.

        literal_repetitions: bool, optional
            True if and only if the clause can have repeated literal.

            Useful for sanity check. If the flag is `False` and the
            clause contain two copies of the same literal, then
            `ValueError` is raised. (default: False)

        opposite_literals: bool, optional
            True if and only if the clause can have opposite literal.

            Useful for sanity check. If the flag is `False` and the
            clause contain two opposite literals, then `ValueError`
            is raised. (default: False)

        auto_variables: bool, optional
            If `True` the clause can contain new variables.

            New variables occurring in the clause will be added to the
            formula, unless the flag is `False`. In that case when
            a clause contains an unknow variables, `ValueError` is
            raised. (default: True)

        
        strict: bool, optional
            If `True` impose restrictions on the clause

            Setting this to `True` is equivalent to set
            `literal_repetitions`, `opposite_literals`,
            `auto_variables` to `False`. In case of conflicting
            setting, the more restrictive one hold.
        """
        assert self._coherent

        # A clause must be an immutable object
        try:
            hash(tuple(clause))
        except TypeError:
            raise TypeError("%s is not a well formatted clause" %clause)

        # Activate the most restrictive setting
        literal_repetitions = literal_repetitions and (not strict)
        opposite_literals   = opposite_literals and (not strict)
        auto_variables      = auto_variables and (not strict) 
        
        # Add all missing variables
        try:
            for _, var in clause:
                if var in self._name2index:
                    continue
                if not auto_variables:
                    raise ValueError("The clause contains an illegal variable %s" % var)
                else:
                    self.add_variable(var)
        except TypeError:
            raise TypeError("%s is not a well formatted clause" %clause)

        # Check literal repetitions
        if (not literal_repetitions) and max(Counter(clause).values() + [0])>1:
            counter  = Counter(clause)
            repeated = [l for (l,c) in counter.iteritems() if c>1]
            raise ValueError("Forbidden repeated literals %s" % repeated)

        # Check opposite literals
        if not opposite_literals:
            positive     = [v for (p,v) in clause if p ]
            intersection = [v for (p,v) in clause if not p and v in positive]
            if len(intersection):
                raise ValueError("Forbidden opposite literals for variables %s" % intersection)
        
        # Add the compressed clause
        self._clauses.append( self._compress_clause(clause) )


    def add_variable(self,var,description=None):
        """Add a variable to the formula (if not already resent).

        The variable must be `hashable`. I.e. it must be usable as key
        in a dictionary.  It raises `TypeError` if the variable cannot
        be hashed.

        Parameters
        ----------
        var: hashable
             the variable name to be added/updated. It can be any
             hashable object (i.e. a dictionary key).
        description: str, optional
             an explanation/description/comment about the variable.
        """
        assert self._coherent
        try:
            if not var in self._name2index:
                # name correpsond to the last variable so far
                self._index2name.append(var)
                self._name2index[var] = len(self._index2name)-1
        except TypeError:
            raise TypeError("%s is not a legal variable name" %var)

        # update description
        if description is not None:
            self._name2descr[var] = description

    #
    # High level API: read the CNF
    #

    def variables(self):
        """Returns (a copy of) the list of variable names.
        """
        assert self._coherent
        vars_iterator = iter(self._index2name)
        vars_iterator.next()
        return vars_iterator
    
    def clauses(self):
        """Return the list of clauses
        """
        assert self._coherent
        return self.__iter__()


    def dimacs(self, export_header=True, extra_text=None):
        """Produce the dimacs encoding of the formula

        The formula is rendered in the DIMACS format for CNF formulas,
        which is a particularly popular input format for SAT solvers [1]_.

        Parameters
        ----------
        export_header : bool
            determines whether the formula header should be inserted as
            a comment in the DIMACS output.

        extra_text : str, optional
            Additional text attached to the header

        Returns
        -------
        string
            the string contains the Dimacs code


        Examples
        --------
        >>> c=CNF([[(False,"x_1"),(True,"x_2"),(False,"x_3")],\
                   [(False,"x_2"),(False,"x_4")], \
                   [(True,"x_2"),(True,"x_3"),(False,"x_4")]])
        >>> print(c.dimacs(export_header=False))
        p cnf 4 3
        -1 2 -3 0
        -2 -4 0
        2 3 -4 0

        >>> c=CNF()
        >>> print(c.dimacs(export_header=False))
        p cnf 0 0
        <BLANKLINE>

        References
        ----------
        .. [1] http://www.satlib.org/Benchmarks/SAT/satformat.ps

        """
        from cStringIO import StringIO
        output = StringIO()
        self._dimacs_dump_clauses(output, export_header, extra_text)
        return output.getvalue()

    def _dimacs_dump_clauses(self, output=None, export_header=True, extra_text=None):
        """Dump the dimacs encoding of the formula to the file-like output

        This is for internal use only. It produces the dimacs output
        of the clauses, and write then on the output buffer, which is
        tipically a StringIO.
        """
        assert self._coherent

        # Count the number of variables and clauses
        n = len(self._index2name)-1
        m = len(self)

        # A nice header
        if export_header:
            for line in self.header.split("\n")[:-1]:
                output.write(("c "+line).rstrip()+"\n")

            if extra_text is not None:
                for line in extra_text.split("\n"):
                    output.write(("c "+line).rstrip()+"\n")


        # Formula specification
        output.write("p cnf {0} {1}".format(n, m))

        if len(self._clauses) == 0:
            output.write("\n")   # this newline makes `lingeling` solver happy

        # Clauses
        for cls in self._clauses:
            output.write("\n" + " ".join([str(l) for l in cls + (0,)]))

    def latex(self, export_header=True, extra_text=None, full_document=False):
        """Output a LaTeX version of the CNF formula

        The CNF formula is translated into the LaTeX markup language
        [1]_, using the names of the variable literally. The formula
        is rendered in the ``align`` environment, with one clause per
        row. Negated literals are rendered using the
        ``\\neg`` command.

        The output string is ready to be included in a document, but
        it does not include neither a preamble nor is nested inside
        ``\\begin{document}`` ... ``\\end{document}``.

        Parameters
        ----------
        export_header : bool, optional
            determines whether the formula header should be inserted as
            a LaTeX comment in the output. By default is True. 

        extra_text : str, optional
            Additional text attached to the abstract.

        full_document : bool, optional
            rather than just output the formula, output a document 
            that contains it. False by default.

        Returns
        -------
        string
            the string contains the LaTeX code

        Examples
        --------
        >>> c=CNF([[(False,"x_1"),(True,"x_2"),(False,"x_3")],\
                   [(False,"x_2"),(False,"x_4")], \
                   [(True,"x_2"),(True,"x_3"),(False,"x_4")]])
        >>> print(c.latex(export_header=False))
        \\begin{align}
        &       \\left( {\\overline{x}_1} \\lor            {x_2} \\lor {\\overline{x}_3} \\right) \\\\
        & \\land \\left( {\\overline{x}_2} \\lor {\\overline{x}_4} \\right) \\\\
        & \\land \\left(            {x_2} \\lor            {x_3} \\lor {\\overline{x}_4} \\right)
        \\end{align}
        >>> c=CNF()
        >>> print(c.latex(export_header=False))
        \\begin{align}
           \\top
        \\end{align}

        References
        ----------
        .. [1] http://www.latex-project.org/
        """
        assert self._coherent

        clauses_per_page = 40

        latex_preamble=r"""%
\documentclass[10pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath}
\usepackage{listings}
"""
        
        from cStringIO import StringIO
        output = StringIO()
        
        # formula header as a LaTeX comment
        if export_header:
            for s in self.header.split("\n")[:-1]:
                output.write( ("% "+s).rstrip()+"\n" )

        # document opening
        if full_document:
            output.write(latex_preamble)
            output.write("\\begin{document}\n")
            title=self.header.split('\n')[0]
            title=title.replace("_","\_")
            output.write("\\title{{{}}}\n".format(title))
            output.write("\\author{CNFgen formula generator}\n")
            output.write("\\maketitle\n")
            output.write("\\noindent\\textbf{Formula header:}\n")
            output.write("\\begin{lstlisting}[breaklines]\n")
            output.write(self.header)
            output.write("\\end{lstlisting}\n")
            output.write("\\bigskip\n")

        if extra_text is not None and full_document:
            output.write(extra_text)
                
        def map_literals(l):
            """Map literals to LaTeX string"""
            assert l!=0
            if l>0 :
                return  "           {"+str(self._index2name[l])+"}"
            else:
                name = self._index2name[-l]
                split_point=name.find("_")
                return "{\\overline{"+name[:split_point]+"}"+name[split_point:]+"}"

        def write_clause(cls, first,full_document):
            """Write the clause in LaTeX."""
            output.write("\n&" if first  else " \\\\\n&")
            output.write("       " if full_document or first else " \\land ")

            # build the latex clause
            if len(cls) == 0:
                output.write("\\square")
            elif full_document:
                output.write(" \\lor ".join(map_literals(l) for l in cls))
            else:
                output.write("\\left( " + \
                             " \\lor ".join(map_literals(l) for l in cls) + \
                             " \\right)")

        # Output the clauses
        clauses_number = len(self._clauses)
        if full_document:
            output.write("\\noindent\\textbf{{CNF with {} variables and and {} clauses:}}\n".\
                         format(len(self._name2index),clauses_number))

        output.write("\\begin{align}")
        
        if clauses_number==0:
            output.write("\n   \\top")
        else:
            for i,clause in enumerate(self._clauses):
                if i% clauses_per_page ==0 and i!=0 and full_document:
                    output.write("\n\\end{align}\\pagebreak")
                    output.write("\n\\begin{align}")
                    write_clause(clause, True,full_document)
                else:
                    write_clause(clause, i==0,full_document)

        output.write("\n\\end{align}")

        # document closing
        if full_document:
            output.write("\n\\end{document}")
  
        return output.getvalue()


    def is_satisfiable(self, cmd=None, sameas=None):
        """Determines whether a CNF is satisfiable or not.

        The formula is passed to a SAT solver, according to the
        optional command line ``cmd``. If no command line is
        specified, the known solvers are tried in succession until one
        is found.

        It is possible to use any drop-in replacement for these
        solvers, but in this case more information is needed on how to
        communicate with the solver. In particular ``minisat`` does not
        respect the standard DIMACS I/O conventions, and that holds
        also for ``glucose`` which is a drop-in replacement of
        ``minisat``.

        For the supported solver we can pick the right interface, but
        for other solvers it is impossible to guess. Nevertheless it
        is possible to indicate which interface to use, or more
        specifically which known solver interface to mimic.

        >>> F.is_satisfiable(cmd='minisat-style-solver',sameas='minisat')  # doctest: +SKIP
        >>> F.is_satisfiable(cmd='dimacs-style-solver',sameas='lingeling') # doctest: +SKIP

        Parameters
        ----------
        cmd : string,optional
            the actual command line used to invoke the SAT solver

        sameas : string, optional
            use the interface of one of the supported solvers. Useful
            when the solver used in the command line is not supported.

        Examples
        --------
        >>> F.is_satisfiable()                                              # doctest: +SKIP
        >>> F.is_satisfiable(cmd='minisat -no-pre')                         # doctest: +SKIP
        >>> F.is_satisfiable(cmd='glucose -pre')                            # doctest: +SKIP
        >>> F.is_satisfiable(cmd='lingeling --plain')                       # doctest: +SKIP
        >>> F.is_satisfiable(cmd='sat4j')                                   # doctest: +SKIP
        >>> F.is_satisfiable(cmd='my-hacked-minisat -pre',sameas='minisat') # doctest: +SKIP
        >>> F.is_satisfiable(cmd='patched-lingeling',sameas='lingeling')    # doctest: +SKIP

        Returns
        -------
        (boolean,assignment or None)
            A pair (answer,witness) where answer is either True when
            F is satisfiable, or False otherwise. If F is satisfiable
            the witness is a satisfiable assignment in form of
            a dictionary, otherwise it is None.

        Raises
        ------
        RuntimeError
           if it is not possible to correctly invoke the solver needed.

        ValueError
           if `sameas` is set and is not the name of a supported solver.

        TypeError
           if F is not a CNF object.

        See Also
        --------
        cnfformula.utils.solver.is_satisfiable : implementation independent of CNF object.
        cnfformula.utils.solver.supported_satsolvers : the SAT solver recognized by `cnfformula`.

        """
        from .utils import solver
        return solver.is_satisfiable(self, cmd=cmd, sameas=sameas)

    ###
    ### Various utility function for CNFs
    ###
    @classmethod
    def parity_constraint(cls,variables, constant):
        """Output the CNF encoding of a parity constraint
        
        E.g. X1 + X2 + X3 = 1 (mod 2) is encoded as
        
        ( X1 v  X2 v  X3)
        (~X1 v ~X2 v  X3)
        (~X1 v  X2 v ~X3)
        ( X1 v ~X2 v ~X3)

        Parameters
        ----------
        variables : array-like
            variables involved in the constraint
        constant : {0,1}
            the constant of the linear equation

        Returns
        -------
        a list of clauses

        Examples
        --------
        >>> CNF.parity_constraint(['a','b'],1)
        [[(True, 'a'), (True, 'b')], [(False, 'a'), (False, 'b')]]
        >>> CNF.parity_constraint(['a','b'],0)
        [[(True, 'a'), (False, 'b')], [(False, 'a'), (True, 'b')]]
        >>> CNF.parity_constraint(['a'],0)
        [[(False, 'a')]]
        """
        domains = tuple([((True, var), (False, var)) for var in variables])
        clauses = []
        for c in product(*domains):
            # Save only the clauses with the right polarity
            parity = sum(1-l[0] for l in c) % 2
            if parity != constant:
                clauses.append(list(c))
        return clauses


    @classmethod
    def _inequality_constraint_builder(cls,variables, k, greater=False):
        """Builder for inequality constraint
     
        This is a generic builder used to build all the inequality
        constraints. By default it build a "stricly less that", and if
        ``greater`` is True it builds a "strictly greater than".
        """
        clauses = []
        polarity = greater
        if greater:
            k = len(variables) - k
     
        if k > len(variables):
            return []
        elif k < 0:
            return [[]]
     
        for tpl in combinations(variables, k):
            clauses.append([(polarity, v) for v in tpl])
        return clauses
     
    @classmethod 
    def less_than_constraint(cls,variables, upperbound):
        """Clauses encoding a \"strictly less than\" constraint
     
        E.g. X1 + X2 + X3 + X4 < 3
     
        (~X1 v ~X2 v ~X3)
        (~X1 v ~X2 v ~X4)
        (~X1 v ~X3 v ~X4)
        (~X2 v ~X3 v ~X4)
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
        upperbound: int
           upper bound of the constraint
     
        Returns
        -------
            a list of clauses
     
        Examples
        --------
        >>> CNF.less_than_constraint(['a','b','c'],2)
        [[(False, 'a'), (False, 'b')], [(False, 'a'), (False, 'c')], [(False, 'b'), (False, 'c')]]
        >>> CNF.less_than_constraint(['a'],1)
        [[(False, 'a')]]
        >>> CNF.less_than_constraint(['a','b','c'],-1)
        [[]]
        >>> CNF.less_than_constraint(['a','b','c'],10)
        []
        """
        return cls._inequality_constraint_builder(variables, upperbound, greater=False)

    @classmethod
    def less_or_equal_constraint(cls,variables, upperbound):
        """Clauses encoding a \"less than or equal to\" constraint
     
        E.g. X1 + X2 + X3 + X4 <= 2
     
        (~X1 v ~X2 v ~X3)
        (~X1 v ~X2 v ~X4)
        (~X1 v ~X3 v ~X4)
        (~X2 v ~X3 v ~X4)
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
        upperbound: int
           upper bound of the constraint
     
        Returns
        -------
            a list of clauses
     
        Examples
        --------
        >>> CNF.less_than_constraint(['a','b','c'],3) == CNF.less_or_equal_constraint(['a','b','c'],2)
        True
        >>> CNF.less_or_equal_constraint(['a','b','c'],1)
        [[(False, 'a'), (False, 'b')], [(False, 'a'), (False, 'c')], [(False, 'b'), (False, 'c')]]
        >>> CNF.less_or_equal_constraint(['a','b'],0)
        [[(False, 'a')], [(False, 'b')]]
        >>> CNF.less_or_equal_constraint(['a','b','c'],-1)
        [[]]
        >>> CNF.less_or_equal_constraint(['a','b','c'],10)
        []
        """
        return cls._inequality_constraint_builder(variables, upperbound+1, greater=False)
     
    @classmethod
    def greater_than_constraint(cls, variables, lowerbound):
        """Clauses encoding a \"strictly greater than\" constraint
     
        E.g. X1 + X2 + X3 + X4 > 2
     
        (X1 v X2 v X3)
        (X1 v X2 v X4)
        (X1 v X3 v X4)
        (X2 v X3 v X4)
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
        lowerbound: int
           lower bound of the constraint
     
        Returns
        -------
            a list of clauses
     
        Examples
        --------
        >>> CNF.greater_than_constraint(['a','b','c'],2)
        [[(True, 'a')], [(True, 'b')], [(True, 'c')]]
        >>> CNF.greater_than_constraint(['a'],0)
        [[(True, 'a')]]
        >>> CNF.greater_than_constraint(['a','b','c'],-1)
        []
        >>> CNF.greater_than_constraint(['a','b','c'],3)
        [[]]
        """
        return cls._inequality_constraint_builder(variables, lowerbound, greater=True)
     
    @classmethod
    def greater_or_equal_constraint(cls, variables, lowerbound):
        """Clauses encoding a \"greater than or equal to\" constraint
     
        E.g. X1 + X2 + X3 + X4 > 1
     
        (X1 v X2 v X3)
        (X1 v X2 v X4)
        (X1 v X3 v X4)
        (X2 v X3 v X4)
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
        lowerbound: int
           lower bound of the constraint
     
        Returns
        -------
            a list of clauses
     
        Examples
        --------
        >>> CNF.greater_than_constraint(['a','b','c'],1) == CNF.greater_or_equal_constraint(['a','b','c'],2)
        True
        >>> CNF.greater_or_equal_constraint(['a','b','c'],3)
        [[(True, 'a')], [(True, 'b')], [(True, 'c')]]
        >>> CNF.greater_or_equal_constraint(['a'],0)
        []
        >>> CNF.greater_or_equal_constraint(['a','b','c'],4)
        [[]]
        """
        return cls._inequality_constraint_builder(variables, lowerbound - 1, greater=True)

    @classmethod
    def equal_to_constraint(cls, variables, value):
        """Clauses encoding a \"equal to\" constraint
     
        E.g. X1 + X2 + X3 + X4 = 1
     
        (X1 v X2 v X3 v X4)
        (~X1 v ~X2)
        (~X1 v ~X3)
        (~X1 v ~X4)
        (~X2 v ~X3)
        (~X2 v ~X4)
        (~X3 v ~X4)
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
        value: int
           target values
     
        Returns
        -------
            a list of clauses
        """
        return cls.less_or_equal_constraint(variables, value) + \
               cls.greater_or_equal_constraint(variables, value)
     
    @classmethod
    def loose_majority_constraint(cls, variables):
        """Clauses encoding a \"at least half\" constraint
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
     
        Returns
        -------
            a list of clauses
        """
        threshold = (len(variables)+1)/2
        return cls.greater_or_equal_constraint(variables, threshold)

    @classmethod
    def loose_minority_constraint(cls, variables):
        """Clauses encoding a \"at most half\" constraint
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
     
        Returns
        -------
            a list of clauses
        """
        threshold = len(variables)/2
        return cls.less_or_equal_constraint(variables, threshold)
     
    @classmethod
    def exactly_half_ceil(cls, variables):
        """Clauses encoding a \"exactly half\" constraint (rounded up)
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
     
        Returns
        -------
            a list of clauses
        """
        threshold = (len(variables)+1)/2
        return cls.equal_to_constraint(variables,threshold)
     
    @classmethod
    def exactly_half_floor(cls, variables):
        """Clauses encoding a \"exactly half\" constraint (rounded down)
     
        Parameters
        ----------
        variables : list of variables
           variables in the constraint
     
        Returns
        -------
            a list of clauses
        """
        threshold = len(variables)/2
        return cls.equal_to_constraint(variables,threshold)

    @classmethod
    def unary_mapping( cls, D, R,
                       var_name=None,
                       complete=True,
                       functional=False,
                       surjective=False,
                       injective=False):
        r"""Generator for the clauses of a mapping between to sets

        This generates of the constraints on variables :math:`v(i,j)`
        where :math:`i \in D` and :math:`j in R`, so that they
        represent a mapping (or a relation) between the two sets,
        expressed in unary (i.e. :math:`v(i,j)` expresses whether
        :math:`i` is mapped to :math:`j` or not).

        Parameters
        ----------
        D : iterable
            the domain of the mapping

        R : iterable
            the range of the mapping

        var_name: a function 
            given :math:`i` and :math`j` the function must produce the
            name of variable :math`v(i,j)`

        complete: bool
            every element of :math:`D` must have an image (default: true)

        functional: bool
            every element of :math:`D` must have at most one image (default: false)

        surjective: bool
            every element of :math:`R` must have a pre-image (default: false)

        injective: bool
            every element of :math:`R` must have at most one pre-image (default: false)
        
        Yields
        ------
            a sequence of clauses

        """
        def default_name(i,j):
            return "X_{{{0},{1}}}".format(i,j)
        
        if var_name is None:
            var_name = default_name
            
        # Completeness axioms
        if complete:
            for i in D:
                for c in CNF.greater_or_equal_constraint([var_name(i,j) for j in R], 1):
                    yield c
                    
        # Surjectivity axioms
        if surjective:
            for j in R:
                for c in CNF.greater_or_equal_constraint([var_name(i,j) for i in D], 1):
                    yield c

        # Injectivity axioms
        if injective:
            for j in R:
                for c in CNF.less_or_equal_constraint([var_name(i,j) for i in D],1):
                    yield c

        # Functionality axioms
        if functional:
            for i in D:
                for c in CNF.less_or_equal_constraint([var_name(i,j) for j in R],1):
                    yield c



    @classmethod
    def unary_subset_increasing(cls, Idx, S,
                                var_name=None):
        r"""Generator for the clauses to index a subset

        This generates the constraints on variables :math:`v(i,j)`
        that say that the elements of `Idx` are indexing a subset of
        elements in `S`. The mapping is guaranteed to be monotone
        increasing, i.e, if :math:`i_1 \leq i_2` and both
        :math:`v(i_1,j_1)` and :math:`v(i_2,j_2)` hold, then
        :math:`j_1 \leq j_2` holds too. Order is assumed by iterables
        in input.

        Parameters
        ----------
        Idx : iterable
            an list of indices

        S : iterable
            set where to pick the subset

        var_name: a function 
            given :math:`i` and :math`j` the function must produce the
            name of variable :math`v(i,j)`

        Yields
        ------
            a sequence of clauses

        """
        for c in cls.unary_mapping(Idx, S,var_name=var_name,
                                   functional=True,
                                   injective=False):
            yield c
            
        # Mapping is strictly monotone increasing (so it is also injective)
        localmaps = product(combinations(Idx,2),
                            combinations_with_replacement(S,2))

        for (a,b),(i,j) in localmaps:
            yield [(False,var_name(a,j)),(False,var_name(b,i))]

        
                    
    @classmethod
    def sparse_mapping( cls, B,
                       var_name=None,
                       complete=True,
                       functional=False,
                       surjective=False,
                       injective=False):
        r"""Generator for the clauses of a mapping according to a bipartite graph

        This generates of the constraints on variables :math:`v(i,j)`
        where :math:`i` is a left vertex of :math:`B` and :math:`j` is
        a right vertex of :math`B`, so that they represent a mapping
        (or a relation) between the left and right vertices, so that
        every pair in the ralation must be and edge of :math:`B`.
        (i.e. if :math:`v(i,j)` is true then :math:`(i,j)` must be an
        edge of the graph :math:`B`).

        Parameters
        ----------
        B : graph
            a bipartite graph

        var_name: a function 
            given :math:`i` and :math`j` the function must produce the
            name of variable :math`v(i,j)`

        complete: bool
            every element on the left must have an image (default: true)

        functional: bool
            every element on the left must have at most one image (default: false)

        surjective: bool
            every element on the right must have a pre-image (default: false)

        injective: bool
            every element on the right must have at most one pre-image (default: false)
        
        Yields
        ------
            a sequence of clauses

        """
        def default_name(i,j):
            return "X_{{{0},{1}}}".format(i,j)
        
        if var_name is None:
            var_name = default_name

        D,R = bipartite_sets(B)
        # Completeness axioms
        if complete:
            for i in D:
                for c in CNF.greater_or_equal_constraint([var_name(i,j) for j in neighbors(B,i)], 1):
                    yield c
                    
        # Surjectivity axioms
        if surjective:
            for j in R:
                for c in CNF.greater_or_equal_constraint([var_name(i,j) for i in neighbors(B,j)], 1):
                    yield c

        # Injectivity axioms
        if injective:
            for j in R:
                for c in CNF.less_or_equal_constraint([var_name(i,j) for i in neighbors(B,j)],1):
                    yield c

        # Functionality axioms
        if functional:
            for i in D:
                for c in CNF.less_or_equal_constraint([var_name(i,j) for j in neighbors(B,i)],1):
                    yield c



    @classmethod
    def binary_mapping( cls, D, k,
                        var_name=None,
                        injective=False,
                        cutoff=None):
        r"""Generator for the clauses of a binary mapping between D and :math:`\{0...1\}^k`

        This generates of the constraints on variables
        :math:`v(i,0)...v(i,k-1)` where :math:`i \in D` and
        :math:`v(i,0)...v(i,k-1)` is a binary of :math:`k` bits.
        And variables express the mapping (i.e.
        :math:`v(i,k-1)...v(i,0)` expresses that :math:`i` is mapped
        to that string).

        Parameters
        ----------
        D : iterable
            the domain of the mapping

        k : int
            the length of the bit strings

        var_name: a function 
            given :math:`i` and :math`b` the function must produce the
            name of variable :math`v(i,b)`

        injective: bool
            every bitstring must have at most one pre-image (default: false)
        
        cutoff: int
            forbid, as images, the bit strings encoding numbers larger
            than cutoff This is useful to represent a range which is
            not a power of two. For example a mapping to a range of
            [10] ca be represented with 4 bits, but the strings >=
            1010 must not be image of anything. (default: None)

        Yields
        ------
            a sequence of clauses

        """
        def default_name(i,b):
            return "Y_{{{0},{1}}}".format(i,b)

        if var_name is None:
            var_name = default_name

        if cutoff is None:
            cutoff = 2**k
            
        def build_or(i,bs):
            return [ ( bs[b]==0, var_name(i,k-1-b)) for b in xrange(k) ] 
        
        for j,bits in enumerate(product([0,1],repeat=k)):

            # Exclude high strings
            if j >= cutoff:
                for i in D:
                    yield build_or(i,bits) 
                
            elif injective:
            # Injectivity axioms
                for i1,i2 in combinations(D,2):
                    yield build_or(i1,bits) + build_or(i2,bits)

