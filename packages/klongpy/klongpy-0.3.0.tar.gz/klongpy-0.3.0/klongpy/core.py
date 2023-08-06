import functools
import itertools
import random
import re
from collections import deque

import numpy as np

from .utils.ro_dict import ReadonlyDict

np.seterr(divide='ignore')

# TOOO:
# cycle through params for take, split
# add scan family support
# add channel family support
# add system commands
# add debug support


class KGSym(str):
    def __repr__(self):
        return f":{super(KGSym,self).__str__()}"
    def __eq__(self, o):
        return isinstance(o,KGSym) and self.__str__() == o.__str__()
    def __hash__(self):
        return super(KGSym,self).__hash__()

class KGFn():
    def __init__(self, a, args, arity):
        self.a = a
        self.args = args
        self.arity = arity


class KGCall(KGFn):
    def __init__(self, a, args, arity):
        super().__init__(a,args,arity)


class KGOp():
    def __init__(self, a, arity):
        self.a = a
        self.arity = arity


class KGAdverb():
    def __init__(self, a, arity):
        self.a = a
        self.arity = arity


class KGChar(str):
    pass


class KGCond(list):
    pass


class KGLambda():
    def __init__(self, fn):
        for n in fn.__code__.co_varnames:
            if n not in reserved_fn_args:
                raise KeyError(f"lambda argument {n} must be x, y or z")
        self.fn = fn

    def __call__(self, ctx):
        args = [find_context_var(ctx, KGSym(x)) for x in self.fn.__code__.co_varnames]
        return self.fn(*args)

    def get_arity(self):
        return len(self.fn.__code__.co_varnames)


class UnresolvedArgument(Exception):
    pass


class RangeError(Exception):
    def __init__(self, i):
        self.i = i


reserved_fn_args = ['x','y','z']
reserved_fn_symbols = {KGSym(n) for n in reserved_fn_args}
reserved_fn_symbol_map = {n:KGSym(n) for n in reserved_fn_args}


def die(m=None):
    raise RuntimeError(m)


def is_list(x):
    return isinstance(x,(list, np.ndarray))


def is_iterable(x):
    return is_list(x) or (isinstance(x,str) and not isinstance(x, (KGSym, KGChar)))


def is_empty(a):
    return is_iterable(a) and len(a) == 0


def is_dict(x):
    return isinstance(x, dict)


def to_list(a):
    return a if isinstance(a, list) else a.tolist() if isinstance(a, np.ndarray) else [a]


def is_float(x):
    try:
        if is_list(x):
            return False
        return isinstance(x, (np.floating, float, int))
    except:
        return False


def is_integer(x):
    try:
        if is_list(x):
            return False
        return isinstance(x, (np.integer, int))
    except:
        return False


def is_number(a):
    return is_integer(a) or is_float(a)


def in_map(x, v):
    try:
        return x in v
    except:
        return False


def has_none(a):
    if safe_eq(a, None) or not isinstance(a,list):
        return False
    for q in a:
        if q is None:
            return True
    return False


def cmatch(t, i, c):
    return i < len(t) and t[i] == c


def cmatch2(t, i, a, b):
    return cmatch(t, i, a) and cmatch(t, i+1, b)


def cpeek(t,i):
    return t[i] if i < len(t) else None


def cpeek2(t,i):
    return t[i:i+2] if i < (len(t)-1) else None


class UnexpectedChar(Exception):
    def __init__(self, t, i, c):
        self.t = t
        self.i = i
        self.c = c

class UnexpectedEOF(Exception):
    def __init__(self, t, i):
        self.t = t
        self.i = i


def cexpect(t, i, c):
    if not cmatch(t, i, c):
        raise UnexpectedChar(t, i, c)
    return i + 1


def cexpect2(t, i, a, b):
    if not cmatch(t, i, a):
        raise UnexpectedChar(t, i, a)
    if not cmatch(t, i+1, b):
        raise UnexpectedChar(t, i, b)
    return i + 2


def safe_eq(a,b):
    return isinstance(a,type(b)) and a == b


def rec_flatten(a):
    if not is_list(a) or len(a) == 0:
        return a
    r = np.asarray([(rec_flatten(x) if isinstance(x,np.ndarray) else x) for x in a]).flatten()
    return np.hstack(r) if len(r) > 1 else r


def rec_fn(a,f):
    return np.asarray([rec_fn(x, f) for x in a], dtype=object) if is_list(a) else f(a)


def vec_fn(a, f):
    """apply vector function to array with nested array support"""
    # dtype == O for heterogeneous (nested) arrays otherwise apply the function directly for vectorization perf
    if isinstance(a, np.ndarray) and a.dtype == 'O':
        return np.asarray([((vec_fn(x, f)) if is_list(x) else f(x)) for x in a] if is_list(a) else f(a), dtype=object)
    return f(a)


def rec_fn2(a,b,f):
    return np.asarray([rec_fn2(x, y, f) for x,y in zip(a,b)], dtype=object) if is_list(a) and is_list(b) else f(a,b)

# 1 vec[A],vec[B]
# 2 vec[A],obj_vec[B]
# 3 vec[A],scalar[B]
# 4 obj_vec[A],vec[B] (may either be vec[B] or obj_vec[B])
# 5 obj_vec[A],scalar[B]
# 6 scalar[A],vec[B]
# 7 scalar[A],obj_vec[B]
# 8 scalar[A],scalar[B]
def vec_fn2(a, b, f):
    if isinstance(a,np.ndarray):
        if a.dtype != 'O':
            if isinstance(b,np.ndarray):
                if b.dtype != 'O':
                    # 1
                    return f(a,b)
                else:
                    # 2
                    assert len(a) == len(b)
                    return np.asarray([vec_fn2(x, y, f) for x,y in zip(a,b)], dtype=object)
            else:
                # 3
                return f(a,b)
        else:
            if isinstance(b,np.ndarray):
                # 4
                assert len(a) == len(b)
                return np.asarray([vec_fn2(x, y, f) for x,y in zip(a,b)], dtype=object)
            else:
                # 5
                return np.asarray([vec_fn2(x,b,f) for x in a], dtype=object)
    else:
        if isinstance(b,np.ndarray):
            if b.dtype != 'O':
                # 6
                return f(a,b)
            else:
                # 7
                return np.asarray([vec_fn2(a,x,f) for x in b], dtype=object)
        else:
            # 8
            return f(a,b)


def is_symbolic(c):
    return isinstance(c, str) and (c.isalpha() or c.isdigit() or c == '.')


def is_char(x):
    return isinstance(x, KGChar)


def is_atom(x):
    """ All objects except for non-empty lists and non-empty strings are atoms. """
    return is_empty(x) if is_iterable(x) else True


def kg_truth(x):
    return x*1


def str_to_chr_arr(s):
    return np.asarray([KGChar(x) for x in s],dtype=object)


def read_num(t, i=0):
    p = i
    use_float = False
    if t[i] == '-':
        i += 1
    while i < len(t):
        if t[i] == '.' or t[i] == 'e':
            assert use_float == False
            use_float = True
        elif not t[i].isnumeric():
            break
        i += 1
    return i, float(t[p:i]) if use_float else int(t[p:i])


def read_char(t, i):
    i = cexpect2(t, i, '0', 'c')
    if i >= len(t):
        raise UnexpectedEOF(t, i)
    return i+1, KGChar(t[i])


def read_sym(t, i=0):
    p = i
    while i < len(t) and is_symbolic(t[i]):
        i += 1
    x = str(t[p:i])
    return i, reserved_fn_symbol_map.get(x) or KGSym(x)


def read_comment(t, i=0):
    while not cmatch(t, i, '"'):
        i += 1
    return i


def skip_space(t, i=0):
    while i < len(t) and t[i].isspace():
        i += 1
    return i


def skip(t, i=0):
    i = skip_space(t,i)
    if cmatch2(t, i, ':', '"'):
        i = read_comment(t, i+2)
    return i


def cast_malformed_array(arr):
    """
    This is basically a hack to cast lists into numpy arrays when they are
    shaped in such that they cannot be broadcast directly.  Here, we recast
    all the internal arrays to lists and then wrap the entire thing as as
    an object array.
    """
    def _e(a,f):
        return [_e(x, f) for x in a] if is_list(a) else f(a)
    r = _e(arr, lambda x: x.tolist() if isinstance(x,np.ndarray) else x)
    return np.asarray(r,dtype=object)


def read_list(t, delim, i=0):
    """

        # A list is any number of class lexemes (or lists) delimited by
        # square brackets.

        L := '[' (C|L)* ']'

    """

    arr = []
    obj_arr = False
    while not cmatch(t,i,delim) and i < len(t):
        # TODO: make cleaner: kind of a hack to pass in read_neg but
        #       we can knowingly read neg numbers in list context
        i, q = kg_token(t, i, read_neg=True)
        if safe_eq(q, '['):
            i,q = read_list(t, ']', i)
        obj_arr = obj_arr or isinstance(q, (np.ndarray, str))
        arr.append(q)
    if cmatch(t,i,delim):
        i += 1
    try:
        return i, np.asarray(arr,dtype=object) if obj_arr else np.asarray(arr)
    except ValueError:
        return i,cast_malformed_array(arr)


def read_string(t, i=0):
    """

    ".*"                                                    [String]

    A string is (almost) any sequence of characters enclosed by
    double quote characters. To include a double quote character in
    a string, it has to be duplicated, so the above regex is not
    entirely correct. A comment is a shifted string (see below).
    Examples: ""
                "hello, world"
                "say ""hello""!"

    Note: this comforms to the KG read_string impl.
          perf tests show that the final join is fast for short strings

    """
    r = []
    while i < len(t):
        c = t[i]
        if c == '"':
            i += 1
            if not cmatch(t,i,'"'):
                break
        r.append(c)
        i += 1
    return i,"".join(r)


def read_cond(klong, t, i=0):
    """

        # A conditional expression has two forms: :[e1;e2;e3] means "if
        # e1 is true, evaluate to e2, else evaluate to e3".
        # :[e1;e2:|e3;e4;e5] is short for :[e1;e2:[e3;e4;e5]], i.e. the
        # ":|" acts as an "else-if" operator. There may be any number of
        # ":|" operators in a conditional.

        c := ':[' ( e ';' e ':|' )* e ';' e ';' e ']'

    """
    r = []
    i,n = klong._expr(t, i)
    r.append(n)
    i = cexpect(t, i, ';')
    i,n = klong._expr(t, i)
    r.append(n)
    if cmatch2(t,i,':','|'):
        i,n = read_cond(klong,t,i+2)
        r.append(n)
    else:
        i = cexpect(t, i, ';')
        i,n = klong._expr(t, i)
        r.append(n)
        i = cexpect(t, i, ']')
    return i, KGCond(r)


def list_to_dict(a):
    return {x[0]:x[1] for x in a}


def kg_token(t, i=0, read_neg=False):
    """

    # Lexeme classes are the sets of the lexemes specified in the
    # previous section, except for operators.

    C := I   # integer
       | H   # character
       | R   # real number
       | S   # string
       | V   # variable (symbol)
       | Y   # (quoted) symbol

    """
    i = skip(t, i)
    if i >= len(t):
        return i, None
    a = t[i]
    if cmatch2(t, i, '0', 'c'):
        return read_char(t, i)
    elif a.isnumeric() or (read_neg and (a == '-' and (i+1) < len(t) and t[i+1].isnumeric())):
        return read_num(t, i)
    elif a == '"':
        return read_string(t, i+1)
    elif a == ':' and (i+1 < len(t)):
        if t[i+1].isalpha() or t[i+1] == '.':
            return read_sym(t,i+1)
        elif t[i+1].isnumeric() or t[i+1] == '"':
            return kg_token(t, i+1)
        return i+2,f":{t[i+1]}"
    elif is_symbolic(a):
        return read_sym(t, i)
    return i+1, a


def peek_adverb(t,i=0):
    x = cpeek2(t,i)
    if is_adverb(x):
        return i+2,x
    x = cpeek(t,i)
    if is_adverb(x):
        return i+1,x
    return i,None


def eval_dyad_match(a,b):
    """

        a~b                                                      [Match]

        "~" is like "=", but can also compare lists and real numbers. It
        uses "=" (Equal) to compare integers, characters, symbols and
        strings.

        Two real numbers "a" and "b" match, if they are "sufficiently
        similar", where the exact definition of "sufficiently similar"
        is too complex to be discussed here. For the curious reader:
        the current implementation uses a relative epsilon algorithm.
        For instance, given

        sq2::{(x+2%x)%2}:~1 :"square root of 2"

        the following expression will be true:

        sq2~sq2+10*.e

        although the operands of Match differ by 10 times Epsilon.

        Two lists match if all of their elements match pairwise. "~"
        descends into sublists.

        Examples:                  1~1  -->  1
                           "foo"~"foo"  -->  1
                             :foo~:foo  -->  1
                               0cx~0cx  -->  1
                       [1 2 3]~[1 2 3]  -->  1
                   [1 [2] 3]~[1 [4] 3]  -->  0

    """
    r = vec_fn2(a, b, lambda x,y: (np.isclose(x,y) if (is_number(x) and is_number(y)) else np.all(np.asarray(x,dtype=object) == np.asarray(y,dtype=object))))
    return kg_truth(rec_flatten(r).all())


def eval_monad_groupby(a):
    """

        =a                                                       [Group]

        Return a list of lists ("groups") where each group contains the
        index of each occurrence of one element within "a". "a" must be
        a list or string. The indices of all elements of "a" that are
        equal according to "~" (Match) will appear in the same group in
        ascending order.

        ="" and =[] will yield [].

        Examples:   =[1 2 3 4]  -->  [[0] [1] [2] [3]]
                  ="hello foo"  -->  [[0] [1] [2 3] [4 7 8] [5] [6]]

    """
    q = np.asarray(str_to_chr_arr(a) if isinstance(a, str) else a)
    if len(q) == 0:
        return q
    a = q.argsort()
    u = np.unique(q[a], return_index=True)
    r = np.split(a, u[1][1:])
    return np.asarray(r, dtype=object)


def eval_dyad_find(a, b):
    """

        a?b                                                       [Find]

        Find each occurrence of "b" in "a". "a" must be a list, string,
        or dictionary. When "a" is a dictionary, return the value
        associated with the given key. When "a" is a list or string,
        return a list containing the position of each match.

        When both "a" and "b" are strings, return a list containing each
        position of the substring "b" inside of "a". The empty string ""
        is contained between any two characters of a string, even before
        the first and after the last character.

        In any case a return value of nil indicates that "b" is not
        contained in "a", except when "a" is a dictionary. When a key
        cannot be found in a dictionary, Find will return :undefined.
        (See [Undefined].)

        Examples: [1 2 3 1 2 1]?1  -->  [0 3 5]
                        [1 2 3]?4  -->  []
                      "hello"?0cl  -->  [2 3]
                    "xyyyyz"?"yy"  -->  [1 2 3]
                            ""?""  -->  [0]
                      :{[1 []]}?1  -->  []

    """
    if isinstance(a,str):
        return np.asarray([m.start() for m in re.finditer(f"(?={b})", a)])
    elif is_dict(a):
        return a.get(b) or np.inf # TODO: use undefined type
    return np.where(np.asarray(a) == b)[0]


def eval_dyad_drop(a, b):
    """

        a_b                                                       [Drop]

        When "b" is a list or string, drop "a" elements or characters
        from it, returning the remaining list. Dropping more elements
        than contained in "b" will yield the empty list/string. A
        negative value for "a" will drop elements from the end of "b".

        When "b" is a dictionary, remove the entry with the key "a" from
        it. Dictionary removal is in situ, i.e. the dictionary will be
        modified. Other objects will be copied.

        Examples: 3_[1 2 3 4 5]  -->  [4 5]
                  (-3)_"abcdef"  -->  "abc"
                     17_[1 2 3]  -->  []
                       (-5)_"x"  -->  ""

    """
    if is_dict(b):
        try:
            del b[a] # biased towards presence perf
        except KeyError:
            pass
        return b
    return b[a:] if a >= 0 else b[:a]


def eval_monad_shape(a):
    """

        ^a                                                       [Shape]

        Return the shape of "a". The shape of an atom is 0. The shape of
        a list L of atoms is ,#L. Such a list is also called a 1-array
        or a vector. The shape of a list of lists of equal length (M) is
        (#M),#*M. Such a list is called a 2-array or a matrix. A list of
        lists of unequal length is a vector.

        This principle is extended to higher dimensions. An N-array A is
        is an array with equal-sized sub-arrays in each dimension. Its
        shape is (#A),(#*A),...,(#*...*A), where there are N-1 "*"
        operators in the last group of that expression. All shapes are
        written in row-major notation.

        For example:

        [1 2 3 4 5]    is a vector (shape [5])

        [[1 2]
         [2 4]
         [5 6]]        is a matrix (shape [3 2])

        [[[1 2 3 4]
          [5 6 7 8]]
         [[9 0 1 2]
          [3 4 5 6]]
         [[7 8 9 0]
          [1 2 3 4]]]  is a 3-array (shape [3 2 4])

        [[1] [2 3]]    is a vector (shape [2])

        The shape of a string S is ,#S. A list of equally-sized strings
        is a matrix of characters. Strings may form the innermost level
        of higher-dimensional arrays.

        Examples:        ^1  -->  0
                      ^:xyz  -->  0
                       ^[0]  -->  [1]
                   ^[1 2 3]  -->  [3]
                   ^"hello"  -->  [5]
                   ^[[1 2]
                     [3 4]
                     [5 6]]  -->  [3 2]
                   ^[1 [2]]  -->  [2]
                  ^["abcd"
                    "efgh"]  -->  [2 4]

    """

    def _a(x): # use numpy's natural shape by replacing all strings with arrays
        return np.asarray([np.empty(len(y)) if isinstance(y,str) else (_a(y) if is_list(y) else y) for y in x])
    return 0 if is_atom(a) else np.asarray([len(a)]) if isinstance(a,str) else np.asarray(_a(a).shape)


def eval_dyad_at_index(klong, a, b):
    """

        a@b                                                   [At/Index]
        a@b                                                   [At/Apply]

        Extract one or multiple elements from "a" at (zero-based)
        positions given in "b". In this case "a" may be a list or a
        string.

        When "b" is an integer, extract a single element at the given
        position and return it.

        When "b" is a list, return a list containing the extracted
        elements. All members of "b" must be integers in this case.
        The order of indices in "b" does not matter. The same index
        may occur multiple times.

        When "a" is a function, "b" (if it is an atom) or the members
        of "b" (if it is a list) will be passed as arguments to the
        function and the result will be returned.

        Examples:         [1 2 3 4 5]@2  -->  3
                    [1 2 3 4 5]@[1 2 3]  -->  [2 3 4]
                    [1 2 3 4 5]@[0 0 0]  -->  [1 1 1]
                  "hello world"@[3 7 2]  -->  "lol"
                               {x}@:foo  -->  :foo
                         {y+x*x}@[2 3]   -->  7

    """
    if isinstance(a, (KGFn, KGSym)):
        # TODO: fix arity
        return klong.eval(KGCall(a, b.tolist() if isinstance(b,np.ndarray) else b, arity=2))
    j = isinstance(a,str)
    a = str_to_chr_arr(a) if j else a
    if is_list(b):
        if is_empty(b):
            return a
        # TODO: return None for missing keys?
        r = np.asarray([a[x] for x in b])
    elif is_integer(b):
        r = a[b]
    else:
        r = a
    return "".join(r) if j else r


def eval_dyad_define(klong, n, v):
    """

        a::b                                                    [Define]

        Assign "b" to the variable "a" and return "b". When a local
        variable named "a" exists, the value will be assigned to it,
        otherwise the global variable "a" will be assigned the value.

        Note that :: cannot be used to assign values to the function
        variables "x", "y", and "z" (they are read-only).

        Examples:        a::[1 2 3];a  -->  [1 2 3]
                  a::1;{[a];a::2}();a  -->  1

    """
    klong[n] = v
    return v


def eval_dyad_split(a, b):
    """

        a:#b                                                     [Split]

        Split a list or string "b" into segments of the sizes given in
        "a". If "a" is an integer, all segments will be of the same size.
        If "a" is a list of more than one element, sizes will be taken
        from that list. When there are more segments than sizes, :# will
        cycle through "a". The last segment may be shorter than
        specified.

        Examples:         2:#[1 2 3 4]  -->  [[1 2] [3 4]]
                          3:#[1 2 3 4]  -->  [[1 2 3] [4]]
                          3:#"abcdefg"  -->  ["abc" "def" "g"]
                  [1 2]:#[1 2 3 4 5 6]  -->  [[1] [2 3] [4] [5 6]]

    """
    if len(b) == 0:
        return np.asarray([])

    j = isinstance(b, str)
    b = str_to_chr_arr(b) if j else b

    a = a if isinstance(a,np.ndarray) else [a]
    if len(a) == 1:
        if a[0] >= len(b):
            r = [b]
        else:
            k = len(b) // a[0]
            if (k*a[0]) < len(b):
                k += 1
            r = np.array_split(b, k)
    else:
        p, q = 0, 0
        r = []
        while q < len(b):
            r.append(b[q:q+a[p]])
            q += a[p]
            p += 1
            if p >= len(a):
                p = 0

    return np.asarray(["".join(x) for x in r]) if j else np.asarray(r)


def eval_dyad_cut(a, b):
    """

        a:_b                                                       [Cut]

        Cut the list "b" before the elements at positions given in "a".
        "a" must be an integer or a list of integers. When it is a list
        of integers, its elements must be in monotonically increasing
        order. :_ returns a new list containing consecutive segments of
        "b".

        When "a" is zero or #b or contains two subsequent equal indices,
        nil (or an empty string if "b" is a string) will be inserted.

        Examples:      2:_[1 2 3 4]  -->  [[1 2] [3 4]]
                  [2 3 5]:_"abcdef"  -->  ["ab" "c" "de" "f"]
                             0:_[1]  -->  [[] [1]]
                           3:_"abc"  -->  ["abc" ""]
                       [1 1]:_[1 2]  -->  [[1] [] [2]]

    """
    j = isinstance(b, str)
    b = np.asarray(str_to_chr_arr(b) if j else b)
    a = a if isinstance(a,np.ndarray) else [a]
    r = np.array_split(b, a)
    if len(b) == 0 and len(a) > 0:
        r = r[1:]
    return np.asarray(["".join(x) for x in r]) if j else np.asarray(r)


def eval_dyad_amend(a, b):
    """

        a:=b                                                     [Amend]

        "a" must be a list or string and "b" must be a list where the
        first element can have any type and the remaining elements must
        be integers. It returns a new object of a's type where a@b2
        through a@bN are replaced by b1. When "a" is a string, b1 must
        be a character or a string. The first element of "a" has an
        index of 0.

        When both "a" and b1 are strings, Amend replaces each substring
        of "a" starting at b2..bN by b1. Note that no index b2..bN must
        be larger than #a or a range error will occur. When b1 is
        replaced at a position past (#a)-#b1, the amended string will
        grow by the required amount. For instance:

        "aa":="bc",1 --> "abc".

        Examples:    "-----":=0cx,[1 3]  -->  "-x-x-"
                           [1 2 3]:=0,1  -->  [1 0 3]
                  "-------":="xx",[1 4]  -->  "-xx-xx-"
                         "abc":="def",3  -->  "abcdef"

    """
    if not isinstance(a, (str,list,np.ndarray)):
        raise RuntimeError(f"a must be list or str: {a}")
    if len(b) <= 1:
        return a
    if isinstance(a, str):
        r = str_to_chr_arr(a)
        q = str_to_chr_arr(b[0])
        for i in b[1:]:
            try:
                r[i:i+len(q)] = q
            except ValueError:
                r = r.astype(object)
                if i > len(r):
                    RangeError(i)
                elif i == len(r):
                    r = np.append(r, b[0])
                else:
                    r[i] = b[0]
        return "".join(["".join(x) for x in r])
    r = np.array(a)
    if isinstance(b[0],np.ndarray):
        if len(b[0]) > 1:
            r = r.tolist()
            for i in b[1:]:
                r[i] = b[0]
            r = np.asarray(r)
        else:
            r = r.astype(dtype=object)
            r[np.asarray(b[1:],dtype=int)] = b[0]
    else:
        r[np.asarray(b[1:],dtype=int)] = b[0]
    return r


def eval_dyad_amend_in_depth(a, b):
    """

        a:-b                                            [Amend-in-Depth]

        :- is like :=, but "a" may be a multi-dimensional array. The :-
        operator replaces one single element in that array. The sequence
        of indices b1..bN is used to locate the target element in an
        N-dimensional array. The number of indices must match the rank
        of the array.

        Example: [[1 2] [3 4]]:-42,[0 1]  -->  [[1 42] [3 4]]
                      [[[0]]]:-1,[0 0 0]  -->  [[[1]]]

    """
    def _e(p, q, v):
        if isinstance(q,np.ndarray) and len(q) > 1:
            r = _e(p[q[0]], q[1:] if len(q) > 2 else q[1], v)
            p = np.array(p, dtype=r.dtype)
            p[q[0]] = r
            return p
        else:
            p = np.array(p, dtype=object) if isinstance(v, (str, KGSym)) else np.array(p)
            p[q] = v
            return p
    return _e(a, b[1:], b[0])


def eval_dyad_rotate(a, b):
    """

        a:+b                                                    [Rotate]

        Rotate the list or string "b" by "a" elements. "a" must be an
        integer. When "a" is positive, rotate elements to the "right",
        i.e. drop elements from the end of "b" and append them to the
        front. When "a" is negative, rotate "b" to the left, i.e. drop
        from the beginning, append to the end.

        "a" may be greater than #b. In this case, the number of elements
        rotated will be a!#b.

        Note that n:+M rotates the rows of a matrix M (i.e. it rotates
        it vertically); to rotate its columns (horizontally), use n:+:\M
        (Rotate-Each-Left).

        Examples:           1:+[1 2 3 4 5]     -->  [5 1 2 3 4]
                            (-1):+[1 2 3 4 5]  -->  [2 3 4 5 1]
                       1:+[[1 2] [4 5] [5 6]]  -->  [[1 2] [4 5] [5 6]]
                   {1:+x}'[[1 2] [4 5] [5 6]]  -->  [[2 1] [5 4] [6 5]]

    """
    if a == 0 or not is_iterable(b):
        return b
    j = isinstance(b, str)
    b = str_to_chr_arr(b) if j else b
    r = np.roll(b, a)
    return "".join(r) if j else r


def eval_dyad_reshape(a, b):
    """

        a:^b                                                   [Reshape]

        :^ reshapes "b" to the shape specified in "a". The shape is
        specified in the form returned by the "^" (Shape) operator: a
        list of dimensions in row-major order.

        The operand "b" may be in any shape. The elements of the new
        array will be taken from "b" in sequential order:

        [3 3]:^[1 2 3 4 5 6 7 8 9]  -->  [[1 2 3]
                                          [4 5 6]
                                          [7 8 9]]

        When the source array contains more elements that can be stored
        in an array of the shape "a", excess elements in "b" will be
        ignored. When the source array contains too few elements, :^
        will cycle through the source object, repeating the elements
        found there:

        [3 3]:^[0 1]  -->  [[0 1 0]
                            [1 0 1]
                            [0 1 0]

        When the value -1 appears in the shape parameter "a", it denotes
        half the size of the source vector, e.g.:

        [-1 2]:^!10  -->  [[0 1] [2 3] [4 5] [6 7] [8 9]]
        [2 -1]:^!10  -->  [[0 1 2 3 4] [5 6 7 8 9]]

        Both "a" and "b" may be atoms:

        5:^1  -->  [1 1 1 1 1]

        but when "b" is an atom (or a single-argument vector), then "a"
        may not contain the value -1.

        0:^x is an identity operation returning x.

        Examples:           5:^:x  -->  [:x :x :x :x :x]
                         [3]:^[1]  -->  [1 1 1]
                  [2 2 2]:^[1 2 3] -->  [[[1 2] [3 1]] [[2 3] [1 2]]]
                    [2]:^[[1 2 3]] -->  [[1 2 3] [1 2 3]]

    """
    j = isinstance(b, str)
    b = str_to_chr_arr(b) if j else b
    if isinstance(a, np.ndarray):
        if isinstance(b, np.ndarray):
            y = np.where(a < 0)[0]
            if len(y) > 0:
                a = np.copy(a)
                a[y] = b.size // 2
            b_s = b.size
            a_s = np.prod(a)
            if a_s > b_s:
                b = np.tile(b.flatten(), (a_s // b_s))
                b = np.concatenate((b, b[:a_s - b.size]))
                b_s = b.size
                r = b.reshape(a)
                r = np.asarray(["".join(x) for x in r]) if j else r
                j = False
            elif a_s == b_s:
                r = b.reshape(a)
            else:
                r = np.resize(b, a)
        else:
            r = np.ones(a)*b
    else:
        if a == 0:
            r = b
        elif isinstance(b, np.ndarray):
            if a < b.shape[0]:
                r = np.resize(b, (a,))
            else:
                ns = np.ones(len(b.shape),dtype=int)
                ns[0] = a // b.shape[0]
                r = np.concatenate((np.tile(b,ns), b[:a - b.shape[0]*ns[0]]))
        else:
            r = np.ones((a,))*b
    return "".join(r) if j else r


def eval_adverb_each(f, a):
    """

        f'a                                                       [Each]

        If "a" is a list, apply "f" to each member of "a":

        f'a  -->  f(a1),...,f(aN)

        If "a" is an atom, return f(a). If "a" is [], ignore "f" and
        return [].

        If "a" is a dictionary, apply "f" to each tuple stored in the
        dictionary. The resulting list will be in some random order.
        Applying {x} (the identity function) to a dictionary turns it
        into a list of tuples.

        Example: -'[1 2 3]  -->  [-1 -2 -3]

    """
    if isinstance(a,str):
        if is_empty(a):
            return a
        r = np.asarray([f(x) for x in str_to_chr_arr(a)])
        return ''.join(r) if r.dtype == '<U1' else r
    if is_iterable(a):
        return a if is_empty(a) else np.asarray([f(x) for x in a])
    elif is_dict(a):
        return np.asarray([f(np.asarray(x)) for x in a.items()])
    return f(a)


def eval_adverb_each2(f, a, b):
    """

        a f'b                                                   [Each-2]

        Each-2 is like each, but applies "f" pairwise to elements of "a"
        and "b":

        a f'b  -->  f(a1;b1),...,f(aN;bN)

        If both "a" and "b" are atoms, return f(a;b). If either "a" or
        "b" is [], ignore "f" and return []. When the lengths of "a" and
        "b" differ, ignore any excess elements of the longer list.

        Example: [1 2 3],'[4 5 6]  -->  [[1 4] [2 5] [3 6]]

    """
    if is_empty(a) or is_empty(b):
        return np.asarray([]) if is_list(a) or is_list(b) else ""
    if is_atom(a) and is_atom(b):
        return f(a,b)
    r = np.asarray([f(x,y) for x,y in zip(a,b)])
    return ''.join(r) if r.dtype == '<U1' else r


def eval_adverb_each_left(f, a, b):
    """
        a f:\b                                              [Each-Left]
        a f:/b                                              [Each-Right]

        If "b" is a list, both of these adverbs combine "a" with each
        element of "b", where :\ uses "a" as the left operand of "f",
        and :/ uses it as its right operand:

        a f:\b  -->  f(a;b1),...,f(a;bN)
        a f:/b  -->  f(b1;a),...,f(bN;a)

        If "b" is an atom, then

        a f:\b  -->  f(a;b)
        a f:/b  -->  f(b;a)

        When "b" is [], ignore "a" and "f" and return [].

        Examples: 1,:\[2 3 4]  -->  [[1 2] [1 3] [1 4]]
                  1,:/[2 3 4]  -->  [[2 1] [3 1] [4 1]]
    """
    b = str_to_chr_arr(b) if isinstance(b,str) else b
    return np.asarray([f(a,x) for x in b])


def eval_adverb_each_right(f, a, b):
    """
    see: eval_dyad_adverb_each_left
    """
    b = str_to_chr_arr(b) if isinstance(b,str) else b
    return np.asarray([f(x,a) for x in b])



def eval_adverb_each_pair(f, a):
    """

        f:'a                                                 [Each-Pair]

        If "a" is a list of more than one element, apply "f" to each
        consecutive pair of "a":

        f:'a  -->  f(a1;a2),f(a2;a3),...,f(aN-1;aN)

        If "a" is an atom or a single-element list, ignore "f" and
        return "a".

        Example: ,:'[1 2 3 4]  -->  [[1 2] [2 3] [3 4]]

    """
    if is_atom(a) or (is_list and len(a) == 1):
        return a
    j = isinstance(a, str)
    a = str_to_chr_arr(a) if j else a
    r = np.asarray([f(x,y) for x,y in zip(a[::],a[1::])])
    return r


def eval_adverb_over(f, a):
    """
        f/a                                                       [Over]

        If "a" is a list, fold "f" over "a":

        f/a  -->  f(...f(f(a1;a2);a3)...;aN))
        +/a  -->  ((...(a1+a2)+...)+aN)

        If "a" is a single-element list, return the single element.

        If "a" is an atom, ignore "f" and return "a".

        Example: +/[1 2 3 4]  -->  10
    """
    if is_atom(a):
        return a
    if len(a) == 1:
        return a[0]
    if safe_eq(f, eval_dyad_add):
        return np.add.reduce(a)
    elif safe_eq(f, eval_dyad_subtract):
        return np.subtract.reduce(a)
    elif safe_eq(f, eval_dyad_multiply):
        return np.multiple.reduce(a)
    elif safe_eq(f, eval_dyad_divide):
        return np.divide.reduce(a)
    return functools.reduce(f, a)


def eval_adverb_over_neutral(f, a, b):
    """

        a f/b                                             [Over-Neutral]

        This is like "/", but with a neutral element "a" that will be
        returned when "b" is [] or combined with the first element of
        "b" otherwise:

        a f/[]  -->  a
        a f/b   -->  f(...f(f(a;b1);b2)...;bN)

        For example, +/[] will give [], but 0+/[] will give 0.

        Of course, dyadic "/" can also be used to abbreviate an
        expression by supplying a not-so-neutral "neutral element".
        For instance, a++/b can be abbreviated to a+/b.

        If both "a" and "b" are atoms, "a f/b" will give f(a;b).

        Formally, "a f/b" is equal to f/a,b

        Example: 0,/[1 2 3]  -->  [0 1 2 3]
                 1+/[2 3 4]  -->  10

    """
    if is_empty(b):
        return a
    if is_atom(b):
        return f(a,b)
    return functools.reduce(f,b[1:],f(a,b[0]))


def eval_adverb_converge(f, a):
    """
        f:~a                                                  [Converge]

        Find the fixpoint of f(a), if any. The fixpoint of "f" is a value
        "a" for which f(a) = a. For example,

        {(x+2%x)%2}:~2

        converges toward the square root of two using Newton's method.
        Starting with x=2:

        (2+2%2)%2              -->  1.5
        (1.5+2%1.5)%2          -->  1.41666
        (1.41666+2%1.41666)%2  -->  1.41421  :"next value is the same"
        (1.41421+2%1.41421)%2  -->  1.41421

        (Of course, the precision of the actual implementation will
         probably be higher.)

        Example: ,/:~["f" ["l" "at"] "ten"]  -->  "flatten"

    """
    def _e(p,q):
        if type(p) != type(q):
            return False
        if is_number(p):
            return np.isclose(p,q)
        elif isinstance(p,np.ndarray):
            return (p.shape == q.shape) and (np.isclose(p,q)).all()
        return p == q
    x = f(a)
    xx = f(x)
    while not _e(x,xx):
        x = xx
        xx = f(x)
    return x


def eval_adverb_while(klong, f, a, b):
    """

        a f:~b                                                   [While]

        Compute b::f(b) while a(b) is true. Formally:

        - if a(b) is false, return b
        - else assign b::f(b) and start over

        Example: {x<1000}{x*2}:~1  -->  1024

    """
    # TODO: fix arity
    while klong.eval(KGCall(a, b, arity=1)):
        b = f(b)
    return b


def eval_dyad_adverb_iterate(f, a, b):
    """

        a f:*b                                                 [Iterate]

        Apply "f" recursively to "b" "a" times. More formally:

        - if "a" is zero, return b
        - else assign b::f(b) and a::a-1 and start over

        Example: 3{1,x}:*[]  -->  [1 1 1]

    """
    while not safe_eq(a, 0):
        b = f(b)
        a = a - 1
    return b


def eval_adverb_scan_over_neutral(f, a, b):
    """

        f\a                                                  [Scan-Over]
        a f\b                                        [Scan-Over-Neutral]

        "\" is like "/", but collects intermediate results in a list and
        returns that list. In the resulting list,

        - the first slot will contain a1
        - the second slot will contain f(a1;a2)
        - the third slot will contain f(f(a1;a2);a3)
        - the last slot will contain f(...f(a1;a2)...;aN)
          (which is the result of f/a)

        If only one single argument is supplied, the argument will be
        returned in a list, e.g.: +\1 --> [1].

        "a f\b" is equal to f\a,b.

        Examples:  ,\[1 2 3]  -->  [1 [1 2] [1 2 3]]
                  0,\[1 2 3]  -->  [0 [0 1] [0 1 2] [0 1 2 3]]
    """
    if is_empty(b):
        return a
    if is_atom(b):
        b = [b]
    b = [f(a,b[0]), *b[1:]]
    q = np.asarray(list(itertools.accumulate(b,f)))
    r = [a, *q]
    try:
        return np.asarray(r)
    except ValueError:
        return cast_malformed_array(r)


def eval_adverb_scan_over(f, a):
    """
        see eval_adverb_scan_over_neutral
    """
    if is_atom(a):
        return a
    if safe_eq(f, eval_dyad_add):
        return np.add.accumulate(a)
    elif safe_eq(f, eval_dyad_subtract):
        return np.subtract.accumulate(a)
    elif safe_eq(f, eval_dyad_multiply):
        return np.multiple.accumulate(a)
    elif safe_eq(f, eval_dyad_divide):
        return np.divide.accumulate(a)
    r = list(itertools.accumulate(a, f))
    try:
        return np.asarray(r)
    except ValueError:
        return cast_malformed_array(r)


def eval_adverb_scan_converging(f, a):
    """

        f\~a                                           [Scan-Converging]

        Monadic \~ is like monadic :~, but returns a list of all
        intermediate results instead of just the end result. The
        last element of the list will be same as the result of a
        corresponding :~ application. For instance:

        {(x+2%x)%2}\~2

        will produce a list containing a series that converges toward
        the square root of 2.

        Example: ,/\~["a" ["b"] "c"]  -->  [["a" ["b"] "c"]
                                            ["a" "b" "c"]
                                            "abc"]

    """
    def _e(p,q):
        if is_number(p) and is_number(q):
            return np.isclose(p,q)
        if type(p) != type(q):
            return False
        if isinstance(p,np.ndarray):
            return (p.dtype == q.dtype) and (p.shape == q.shape) and (np.isclose(p,q)).all()
        return p == q
    r = [a]
    x = a
    xx = f(a)
    r.append(xx)
    while not _e(x,xx):
        x = xx
        xx = f(x)
        r.append(xx)
    r.pop()
    try:
        return np.asarray(r)
    except ValueError:
        return cast_malformed_array(r)


def eval_adverb_scan_while(klong, f, a, b):
    """

        a f\~b                                              [Scan-While]

        This adverb is (almost) like is non-scanning counterpart, :~,
        but it collects intermediate results in a list and returns that
        list.

        However, \~ will only collect values of X that satisfy a(X),
        while :~ will return the first value that does *not* satisfy
        a(X). E.g.:

        {x<10}{x+1}:~1  -->  10
        {x<10}{x+1}:\1  -->  [1 2 3 4 5 6 7 8 9]

        Example: {x<100}{x*2}\~1  -->  [1 2 4 8 16 32 64]

    """
    r = [b]
    # TODO: fix arity
    while klong.eval(KGCall(a, b, arity=1)):
        b = f(b)
        r.append(b)
    r.pop()
    try:
        return np.asarray(r)
    except ValueError:
        return cast_malformed_array(r)


def eval_adverb_scan_iterating(f, a, b):
    """

        a f\*b                                          [Scan-Iterating]

        This adverbs is like its non-scanning counterpart, but collects
        intermediate results in a list and return that list.

        Example: 3{1,x}\*[]  -->  [[] [1] [1 1] [1 1 1]]

    """
    if safe_eq(a,0):
        return b
    r = [b]
    while not safe_eq(a, 0):
        b = f(b)
        r.append(b)
        a = a - 1
    try:
        return np.asarray(r)
    except ValueError:
        return cast_malformed_array(r)


def eval_dyad_take(a, b):
    """

        a#b                                                       [Take]

        Extract "a" elements from the front of "b". "a" must be an
        integer and "b" must be a list or string. If "a" is negative,
        extract elements from the end of "b". Extracting more elements
        than contained in "b" will fill the extra slots by cycling
        through "b". Taking 0 elements will result in an empty list
        or string.

        Examples:     1#[1 2 3]  -->  [1]
                      2#[1 2 3]  -->  [1 2]
                      5#[1 2 3]  -->  [1 2 3 1 2]
                   (-2)#[1 2 3]  -->  [2 3]
                   (-5)#[1 2 3]  -->  [2 3 1 2 3]
                     3#"abcdef"  -->  "abc"
                  (-3)#"abcdef"  -->  "def"
                           0#[]  -->  []
                           0#""  -->  ""

    """
    j = isinstance(b,str)
    b = str_to_chr_arr(b) if j else b
    aa = np.abs(a)
    if aa > b.size:
        b = np.tile(b,aa // len(b))
        b = np.concatenate((b, b[:aa-b.size]) if a > 0 else (b[-(aa-b.size):],b))
    r = b[a:] if a < 0 else b[:a]
    return "".join(r) if j else r


def eval_dyad_join(a, b):
    """

        a,b                                                       [Join]

        The "," operator joins objects of any type, forming lists or
        strings.

        If "a" and "b" are lists, append them.
        If "a" is a list and "b" is not, attach "b" at the end of "a".
        If "a" is a not list and "b" is one, attach "a" to the front of
        "b".
        If "a" and "b" are strings, append them.
        If "a" is a string and "b" is a char, attach "b" to the end of
        "a".
        If "a" is a char and "b" is a string, attach "a" to the front of
        "b".

        If "a" is a dictionary and "b" is a tuple (a list of two members)
        or vice versa, add the tuple to the dictionary. Any entry with
        the same key will be replaced by the new entry. The head of the
        tuple is the key and the second element is the payload.

        Otherwise, create a tuple containing "a" and "b" in that order.

        Join always returns a fresh list, but dictionaries will be
        updated by replacing old entries in situ.

        Examples:  [1 2 3],[4 5 6]  -->  [1 2 3 4 5 6]
                           1,[2 3]  -->  [1 2 3]
                           [1 2],3  -->  [1 2 3]
                       "abc","def"  -->  "abcdef"
                          "ab",0cc  -->  "abc"
                          0ca,"bc"  -->  "abc"
                               1,2  -->  [1 2]
                             "a",1  -->  ["a" 1]
                       [[1 2 3]],4  -->  [[1 2 3] 4]
                           1,2,3,4  -->  [1 2 3 4]
                    [1 2],:{[1 0]}  -->  :{[1 2]}
                    :{[1 0]},[1 2]  -->  :{[1 2]}

    """
    if isinstance(a,str) and isinstance(b,str):
        return a+b
    if isinstance(a,dict):
        a[b[0]] = b[1]
        return a
    if isinstance(b,dict):
        b[a[0]] = a[1]
        return b
    aa = a if isinstance(a, list) else ([a[0]] if len(a.shape) > 1 and a.shape[0] == 1 else a.tolist() if len(a.shape) == 1 else [a]) if isinstance(a, np.ndarray) else [a]
    bb = b if isinstance(b, list) else ([b[0]] if len(b.shape) > 1 and b.shape[0] == 1 else b.tolist() if len(b.shape) == 1 else [b]) if isinstance(b, np.ndarray) else [b]

    r = np.asarray([*aa,*bb])
    return r


def eval_monad_list(a):
    """

        ,a                                                        [List]

        "," packages any object in a single-element list.

        Examples:    ,1  -->  [1]
                  ,:foo  -->  [:foo]
                  ,"xyz" -->  ["xyz"]
                   ,[1]  -->  [[1]]
    """
    return str(a) if isinstance(a, KGChar) else np.asarray([a],dtype=object) # np interpets ':foo" as ':fo"


def eval_monad_not(a):
    """

        ~a                                                         [Not]

        Return the negative truth value of "a", as explained in the
        section on CONDITIONALS. It will return 1 for 0, [], and "",
        and 0 for all other values.

        Examples:    ~0  -->  1
                     ~1  -->  0
                    ~[]  -->  1
                  ~:foo  -->  0

    """
    def _neg(x):
        return 1 if is_empty(x) else 0 if is_dict(x) or isinstance(x, (KGFn, KGSym)) else kg_truth(np.logical_not(np.asarray(x, dtype=object)))
    return vec_fn(a, _neg) if not is_empty(a) else _neg(a)


def eval_dyad_form(a, b):
    """

        a:$b                                                      [Form]

        Convert string "b" to the type of the object of "a". When "b"
        can be converted to the desired type, an object of that type
        will be returned. When such a conversion is not possible, :$
        will return :undefined.

        When "a" is an integer, "b" may not represent a real number.
        When "a" is a real number, a real number will be returned, even
        if "b" represents an integer. When "a" is a character, "b" must
        contain exactly one character. When "a" is a symbol, "b" must
        contain the name of a valid symbol (optionally including a
        leading ":" character).

        :$ is an atomic operator.

        Examples:     1:$"-123"  -->  -123
                    1.0:$"1.23"  -->  1.23
                       0c0:$"x"  -->  0cx
                   "":$"string"  -->  "string"
                   :x:$"symbol"  -->  :symbol
                  :x:$":symbol"  -->  :symbol

    """
    if isinstance(a,KGSym):
        if is_empty(b):
            return np.inf
        return KGSym(b[1:] if isinstance(b,str) and b.startswith(":") else b)
    if is_integer(a):
        def _is_float(b):
            try:
                float(b)
                return True
            except:
                return False
        if is_float(b) or is_empty(b) or ('.' in b and _is_float(b)):
            return np.inf
        return int(b)
    if is_float(a):
        if is_empty(b):
            return np.inf
        return float(b)
    if isinstance(a,KGChar):
        b = str(b)
        if len(b) != 1:
            return np.inf
        return KGChar(str(b)[0])
    return b


def eval_dyad_format2(a, b):
    """

        a$b                                                    [Format2]

        Dyadic "$" is like its monadic cousin, but also pads its result
        with blanks. The minimal size of the output string is specified
        in "a", which must be an integer. "b" is the object to format.
        When the value of "a" is negative, the result string is padded
        to the right, else it is padded to the left.

        When "a" is real number of the form n.m and "b" is also a real
        number, the representation of "b" will have "n" integer digits
        and "m" fractional digits. The integer part will be padded with
        blanks and the fractional part will be padded with zeros.

        "$" is an atomic operator.

        Examples:     0$123  -->  "123"
                  (-5)$-123  -->  " -123"
                    5$"xyz"  -->  "xyz  "
                  (-5)$:foo  -->  " :foo"
                 5.3$123.45  -->  "  123.450"

    """
    if safe_eq(int(a), 0):
        return str(b)
    if (is_float(b) and not isinstance(b,int)) and (is_float(a) and not isinstance(a,int)):
        b = "{:Xf}".replace("X",str(a)).format(b)
        p = b.split('.')
        p[0] = p[0].rjust(int(a))
        b = ".".join(p)
        return b
    b = f":{b}" if isinstance(b, KGSym) else b
    r = str(b).ljust(abs(a)) if a >= 0 else str(b).rjust(abs(a))
    return r


def eval_monad_format(a):
    """

        $a                                                      [Format]

        Write the external representation of "a" to a string and return
        it. The "external representation" of an object is the form in
        which Klong would display it.

        "$" is an atomic operator.

        Examples:    $123  -->  "123"
                  $123.45  -->  "123.45"
                  $"test"  -->  "test"
                     $0cx  -->  "x"
                    $:foo  -->  ":foo"

    """
    return f":{a}" if isinstance(a, KGSym) else vec_fn(a, eval_monad_format) if is_list(a) else str(a)


def eval_monad_enumerate(a):
    """

        !a                                                   [Enumerate]

        Create a list of integers from 0 to a-1. !0 gives [].

        Examples: !0   -->  []
                  !1   -->  [1]
                  !10  -->  [0 1 2 3 4 5 6 7 8 9]

    """
    return np.arange(a)


def eval_monad_size(a):
    """

        #a                                                        [Size]

        Return the size/magnitude of "a".

        For lists, the size of "a" is the number of its elements.
        For strings, the size is the number of characters.
        For numbers, the size is the magnitude (absolute value).
        For characters, the size is the ASCII code.

        Examples:     #[1 2 3]  -->  3
                  #[1 [2 3] 4]  -->  3
                  #"123456789"  -->  9
                         #-123  -->  123
                          #0cA  -->  65

    """
    return np.abs(a) if is_number(a) else ord(a) if is_char(a) else len(a)


def eval_monad_reciprocal(a):
    """

        %a                                                  [Reciprocal]

        Return 1%a. "a" must be a number.

        "%" is an atomic operator.

        Examples:    %1  -->  1.0
                     %2  -->  0.5
                   %0.1  -->  10.0

    """
    return vec_fn(a, lambda x: np.reciprocal(np.asarray(x,dtype=float)))


def eval_monad_expand_where(a):
    """

        &a                                                [Expand/Where]

        Expand "a" to a list of subsequent integers X, starting at 0,
        where each XI is included aI times. When "a" is zero or an
        empty list, return nil. When "a" is a positive integer, return
        a list of that many zeros.

        In combination with predicates this function is also called
        Where, since it compresses a list of boolean values to indices,
        e.g.:

         [1 2 3 4 5]=[0 2 0 4 5]  -->  [0 1 0 1 1]
        &[1 2 3 4 5]=[0 2 0 4 5]  -->  [1 3 4]

        Examples:           &0  -->   []
                            &5  -->   [0 0 0 0 0]
                      &[1 2 3]  -->   [0 1 1 2 2 2]
                  &[0 1 0 1 0]  -->   [1 3]

    """
    return np.concatenate([np.zeros(x, dtype=int) + i for i,x in enumerate(a if is_list(a) else [a])])


def eval_monad_first(a):
    """

        *a                                                       [First]

        Return the first element of "a", i.e. the first element of a
        list or the first character of a string. When "a" is an atom,
        return that atom.

        Examples:  *[1 2 3]  -->  1
                     *"abc"  --> 0ca
                        *""  -->  ""
                        *[]  -->  []
                         *1  -->  1

    """
    return a if is_empty(a) or not is_iterable(a) else a[0]


def eval_monad_transpose(a):
    """

        +a                                                   [Transpose]

        Return the transpose of the matrix (2-array) "a".

        Examples:     +[[1] [2] [3]]  -->  [[1 2 3]]
                  +[[1 2 3] [4 5 6]]  -->  [[1 4] [2 5] [3 6]]
                                 +[]  -->  []

    """
    return np.transpose(np.asarray(a))


def eval_monad_negate(a):
    """

        -a                                                      [Negate]

        Return 0-a; "a" must be a number.

        "-" is an atomic operator.

        Examples:    -1  -->  -1
                  -1.23  -->  -1.23

    """
    return vec_fn(a, lambda x: np.negative(np.asarray(x, dtype=object)))


def kg_argsort(a, descending=False):
    """
    Return the indices of the sorted array (may be nested) or a string.  Duplicate elements are disambiguated by their position in the array.

    argsort("foobar") => [4 3 0 1 2 5]
                                ^ ^
                            arbitrary ordering resolved by index position

    argsort("foobar",descending=True) => [5 2 1 0 3 4]
                                            ^ ^
                            arbitrary ordering resolved by index position

    """
    if not is_iterable(a) or len(a) == 0:
        return a
    return np.asarray(sorted(range(len(a)), key=lambda x: (np.max(a[x]),x) if is_list(a[x]) else (a[x],x), reverse=descending))


def find_context_var(ctx, k):
    if not isinstance(k, KGSym):
        raise RuntimeError(k)
    for d in ctx:
        if in_map(k, d):
            return d[k]
    raise KeyError(k)

def get_context_var(ctx, k):
    try:
        return find_context_var(ctx, k)
    except:
        return None


def set_context_var(d, name, v):
    if callable(v):
        x = KGLambda(v)
        d[KGSym(name)] = KGCall(x,args=None,arity=x.get_arity())
    else:
        d[KGSym(name)] = v


def add_builtin_globals(d):
    set_context_var(d, '.w', lambda x: print(x, end=''))
    set_context_var(d, '.p', lambda x: print(x))
    set_context_var(d, '.d', lambda x: print(x))
    set_context_var(d, '.rn', lambda: random.random())
    set_context_var(d, '.e', 0.000000000000000001)
    return d

system_globals = add_builtin_globals({})


def eval_dyad_remainder(a, b):
    """
        a!b                                                  [Remainder]

        Return the truncated division remainder of "a" and "b". Both
        "a" and "b" must be integers.

        Formally, a = (b*a:%b) + a!b .

        Dyadic "!" is an atomic operator.

        Examples:    7!5  -->  2
                    7!-5  -->  2
                  (-7)!5  --> -2
                   -7!-5  --> -2
    """
    return vec_fn2(a, b, np.fmod)


def eval_dyad_less(a, b):
    """
        a<b                                                       [Less]

        Return 1, if "a" is less than "b", otherwise return 0.

        Numbers are compared by value.
        Characters are compared by ASCII code.
        Strings and symbols are compared lexicographically.

        "<" is an atomic operator; it cannot compare lists, but only
        elements of lists.

        Examples:              1<2  -->  1
                       "bar"<"foo"  -->  1
                         :abc<:xyz  -->  1
                           0c0<0c9  -->  1
                   [1 2 3]<[1 4 3]  -->  [0 1 0]
    """
    return kg_truth(vec_fn2(a, b, lambda x,y: x < y if (isinstance(x,str) and isinstance(y,str)) else np.less(x,y)))


def eval_dyad_more(a, b):
    """
        a>b                                                       [More]

        Return 1, if "a" is greater than "b", otherwise return 0.

        See "<" (Less) for details on comparing objects.

        ">" is an atomic operator; it cannot compare lists, but only
        elements of lists.

        Examples:              2>1  -->  1
                       "foo">"bar"  -->  1
                         :xyz>:abc  -->  1
                           0c9>0c0  -->  1
                   [1 4 3]>[1 2 3]  -->  [0 1 0]
    """
    return kg_truth(vec_fn2(a, b, lambda x,y: x > y if (isinstance(x,str) and isinstance(y,str)) else np.greater(x,y)))


def eval_dyad_equal(a, b):
    """
        a=b                                                      [Equal]

        Return 1, if "a" and "b" are equal, otherwise return 0.

        Numbers are equal, if they have the same value.
        Characters are equal, if (#a)=#b.
        Strings and symbols are equal, if they contain the same
        characters in the same positions.

        "=" is an atomic operator. In particular it means that it
        cannot compare lists, but only elements of lists. Use "~"
        (Match) to compare lists.

        Real numbers should not be compared with "=". Use "~" instead.

        Examples:             1=1  -->  1
                      "foo"="foo"  -->  1
                        :foo=:foo  -->  1
                          0cx=0cx  -->  1
                  [1 2 3]=[1 4 3]  -->  [1 0 1]
    """
    return vec_fn2(a, b, lambda x, y: kg_truth(np.asarray(x,dtype=object) == np.asarray(y,dtype=object)))


def eval_dyad_power(a, b):
    """
        a^b                                                      [Power]

        Compute "a" to the power of "b" and return the result. Both "a"
        and "b" must be numbers. The result of a^b cannot be a complex
        number.

        Dyadic "^" is an atomic operator.

        Examples:   2^0  -->  1
                    2^1  -->  2
                    2^8  -->  256
                   2^-5  -->  0.03125
                  0.3^3  -->  0.027
                  2^0.5  -->  1.41421356237309504
    """
    return vec_fn2(a, b, lambda x,y: np.power(float(x) if is_integer(x) else x, y))


def eval_dyad_index_in_depth(a, b):
    """
        a:@b                                            [Index-in-Depth]

        :@ is like "@" but, when applied to an array, extracts a single
        element from a multi-dimensional array. The indices in "b" are
        used to locate the element. The number of indices must match
        the rank of the array.

        If "a" is a function, :@ is equal to "@".

        Examples: [[1 2] [3 4]]:@[0 1]  -->  2
                      [[[1]]]:@[0 0 0]  -->  1
                        {y+x*x}:@[2 3]  -->  7
    """
    return np.asarray(a)[tuple(b) if is_list(b) else b] if not is_empty(b) else b


def eval_dyad_integer_divide(a, b):
    """
        a:%b                                            [Integer-Divide]

        Return the integer part of the quotient of "a" and "b". Both "a"
        and "b" must be integers. The result is always an integer.

        Formally, a = (b*a:%b) + a!b .

        ":%" is an atomic operator.

        Examples: 10:%2  -->  5
                  10:%8  -->  1
    """
    return vec_fn2(a, b, lambda x,y: np.trunc(np.divide(x, y)))


def eval_dyad_divide(a, b):
    """
        a%b                                                     [Divide]

        Return the quotient of "a" and "b". The result is always a real
        number, even if the result has a fractional part of 0.

        "%" is an atomic operator.

        Examples: 10%2  -->  5.0
                  10%8  -->  1.25
    """
    return vec_fn2(a, b, np.divide)


def eval_dyad_minimum(a, b):
    """
        a&b                                                    [Min/And]

        Return the smaller one of two numbers.

        When both "a" and "b" are in the set {0,1} (booleans), then "&"
        acts as an "and" operator, as you can easily prove using a truth
        table:

        a  b  min/and
        0  0     0
        0  1     0
        1  0     0
        1  1     1

        Dyadic "&" is an atomic operator.

        Examples:       0&1  -->  0
                   123&-123  -->  -123
                    1.0&1.1  -->  1.0
    """
    return vec_fn2(a, b, np.minimum)


def eval_dyad_maximum(a, b):
    """
        a|b                                                     [Max/Or]

        Return the larger one of two numbers.

        When both "a" and "b" are in the set {0,1} (booleans), then "|"
        acts as an "or" operator, as you can easily prove using a truth
        table:

        a  b  max/or
        0  0    0
        0  1    1
        1  0    1
        1  1    1

        Dyadic "|" is an atomic operator.

        Examples:       0|1  -->  1
                   123|-123  -->  123
                    1.0|1.1  -->  1.1
    """
    return vec_fn2(a, b, np.maximum)


def eval_dyad_multiply(a, b):
    """
        a*b                                                      [Times]

        Return "a" multiplied by "b". "a" and "b" must both be numbers.

        Dyadic "*" is an atomic operator.

        Examples:   3*4  -->  12
                   3*-4  -->  -12
                  0.3*7  -->  2.1
    """
    return vec_fn2(a, b, np.multiply)


def eval_dyad_add(a, b):
    """
        a+b                                                       [Plus]

        Add "b" to "a" and return the result. "a" and "b" must both be
        numbers.

        Dyadic "+" is an atomic operator.

        Examples:  12+3  -->  15
                  12+-3  -->  9
                  1+0.3  -->  1.3
    """
    return vec_fn2(a, b, np.add)


def eval_dyad_subtract(a, b):
    """
        a-b                                                      [Minus]

        Subtract "b" from "a" and return the result. "a" and "b" must be
        numbers.

        "-" is an atomic operator.

        Examples:  12-3  -->  9
                  12--3  -->  15
                  1-0.3  -->  0.7
    """
    return vec_fn2(a, b, np.subtract)


def create_verb_dyads(klong):
    d = {}
    d['!'] = eval_dyad_remainder
    d['#'] = eval_dyad_take
    d['$'] = eval_dyad_format2
    d['%'] = eval_dyad_divide
    d['&'] = eval_dyad_minimum
    d['*'] = eval_dyad_multiply
    d['+'] = eval_dyad_add
    d[','] = eval_dyad_join
    d['-'] = eval_dyad_subtract
    d['<'] = eval_dyad_less
    d['='] = eval_dyad_equal
    d['>'] = eval_dyad_more
    d['?'] = eval_dyad_find
    d['@'] = lambda a, b, k=klong: eval_dyad_at_index(k, a, b)
    d['^'] = eval_dyad_power
    d['_'] = eval_dyad_drop
    d['|'] = eval_dyad_maximum
    d['~'] = eval_dyad_match
    d[':@'] = eval_dyad_index_in_depth
    d[':#'] = eval_dyad_split
    d[':$'] = eval_dyad_form
    d[':%'] = eval_dyad_integer_divide
    d[':+'] = eval_dyad_rotate
    d[':-'] = eval_dyad_amend_in_depth
    d['::'] = lambda a, b, k=klong: eval_dyad_define(k, a, b)
    d[':='] = eval_dyad_amend
    d[':^'] = eval_dyad_reshape
    d[':_'] = eval_dyad_cut
    return d


def is_adverb(s):
    try:
        return s in {
            "'",
            ':\\',
            ":'",
            ':/',
            '/',
            ':~',
            ':*',
            '\\',
            '\\~',
            '\\*'
        }
    except:
        return False


def get_adverb_fn(klong, s, arity):
    if s == "'":
        return eval_adverb_each2 if arity == 2 else eval_adverb_each
    elif s == '/':
        return eval_adverb_over_neutral if arity == 2 else eval_adverb_over
    elif s == '\\':
        return eval_adverb_scan_over_neutral if arity == 2 else eval_adverb_scan_over
    elif s == '\\~':
        return (lambda f,a,b,k=klong: eval_adverb_scan_while(k,f,a,b)) if arity == 2 else eval_adverb_scan_converging
    elif s == '\\*':
        return eval_adverb_scan_iterating
    elif s == ':\\':
        return eval_adverb_each_left
    elif s == ':\'':
        return eval_adverb_each_pair
    elif s == ':/':
        return eval_adverb_each_right
    elif s == ':*':
        return eval_dyad_adverb_iterate
    elif s == ':~':
        return (lambda f,a,b,k=klong: eval_adverb_while(k,f,a,b)) if arity == 2 else eval_adverb_converge
    raise RuntimeError(f"unknown adverb: {s}")


def get_adverb_arity(s, ctx):
    if s == "'":
        return ctx
    elif s == ':\\':
        return 2
    elif s == ':\'':
        return 2
    elif s == ':/':
        return 2
    elif s == '/':
        return 2
    elif s == ':~':
        return 1
    elif s == ':*':
        return 1
    elif s == '\\':
        return 2
    elif s == '\\~':
        return 1
    elif s == '\\*':
        return 1
    raise RuntimeError(f"unknown adverb: {s}")


def eval_monad_grade_up(a):
    """
        >a                                                  [Grade-Down]
        <a                                                    [Grade-Up]

        Impose the given order ("<" = ascending, ">" = descending") onto
        the elements of "a", which must be a list or string. Return a
        list of indices reflecting the desired order. Elements of "a"
        must be comparable by dyadic "<" (Less).

        In addition, "<" and ">" will compare lists by comparing their
        elements pairwise and recursively. E.g. [1 [2] 3] is considered
        to be "less" than [1 [4] 0], because 1=1 and 2<4 (3>0 does not
        matter, because 2<4 already finishes the comparison).

        When "a" is a string, these operators will grade its characters.

        To sort a list "a", use a@<a ("a" At Grade-Up "a") or a@>a.

        Examples:     <[1 2 3 4 5]  -->  [0 1 2 3 4]
                      >[1 2 3 4 5]  -->  [4 3 2 1 0]
                   <"hello, world"  -->  [6 5 11 1 0 2 3 10 8 4 9 7]
                    >[[1] [2] [3]]  -->  [2 1 0]
    """
    return kg_argsort(str_to_chr_arr(a) if isinstance(a,str) else a)


def eval_monad_grade_down(a):
    """ see eval_monad_grade_up """
    return kg_argsort(str_to_chr_arr(a) if isinstance(a,str) else a, descending=True)


def eval_monad_range(a):
    """
        ?a                                                       [Range]

        Return a list containing unique elements from "a" in order of
        appearance. "a" may be a list or string.

        Examples:   ?[1 2 3 4]  -->  [1 2 3 4]
                  ?[1 1 1 2 2]  -->  [1 2]
                  ?"aaabbcccd"  -->  "abcd"
    """
    return ''.join(np.unique(str_to_chr_arr(a))) if isinstance(a, str) else np.unique(a)


def eval_monad_atom(a):
    """
        @a                                                        [Atom]

        @ returns 1, if "a" is an atom and otherwise 0. All objects
        except for non-empty lists and non-empty strings are atoms.

        Examples:      @""  -->  1
                       @[]  -->  1
                      @123  -->  1
                  @[1 2 3]  -->  0
    """
    return kg_truth(is_atom(a))


def eval_monad_floor(a):
    """
        _a                                                       [Floor]

        Return "a" rounded toward negative infinity. When "a" is an
        integer, this is an identity operation. If "a" can be converted
        to integer without loss of precision after rounding, it will be
        converted. Otherwise, a floored real number will be returned.

        Note: loss of precision is predicted by comparing real number
        precision to the exponent, which is a conservative guess.

        Examples:   _123  -->  123
                  _123.9  -->  123
                  _1e100  -->  1.0e+100  :"if precision < 100 digits"
    """
    return vec_fn(a, lambda x: np.floor(np.asarray(x, dtype=float)))


def eval_monad_reverse(a):
    """
        |a                                                     [Reverse]

        Return a new list/string that contains the elements of "a" in
        reverse order. When "a" is neither a list nor a string, return
        it unchanged.

        Examples:       |[1 2 3]  -->  [3 2 1]
                  |"hello world"  -->  "dlrow olleh"
                              |1  -->  1
    """
    return a[::-1]


def eval_monad_split(a):
    """
        a:#b                                                     [Split]

        Split a list or string "b" into segments of the sizes given in
        "a". If "a" is an integer, all segments will be of the same size.
        If "a" is a list of more than one element, sizes will be taken
        from that list. When there are more segments than sizes, :# will
        cycle through "a". The last segment may be shorter than
        specified.

        Examples:         2:#[1 2 3 4]  -->  [[1 2] [3 4]]
                          3:#[1 2 3 4]  -->  [[1 2 3] [4]]
                          3:#"abcdefg"  -->  ["abc" "def" "g"]
                  [1 2]:#[1 2 3 4 5 6]  -->  [[1] [2 3] [4] [5 6]]
    """
    return rec_fn(a, lambda x: KGChar(chr(x))) if is_list(a) else KGChar(chr(a))


def eval_monad_undefined(a):
    """
        :_a                                                  [Undefined]

        Return truth, if "a" is undefined, i.e. the result of an
        operation that cannot yield any meaningful result, like
        division by zero or trying to find a non-existent key in
        a dictionary. Else return 0.

        Examples:        :_1%0  -->  1
                  :_:{[1 2]}?3  -->  1
                      :_:valid  -->  0
    """
    return kg_truth(a is None or (np.isinf(a) if is_number(a) else False))


def create_verb_monads(klong):
    d = {}
    d['!'] = eval_monad_enumerate
    d['#'] = eval_monad_size
    d['$'] = eval_monad_format
    d['%'] = eval_monad_reciprocal
    d['&'] = eval_monad_expand_where
    d['*'] = eval_monad_first
    d['+'] = eval_monad_transpose
    d[','] = eval_monad_list
    d['-'] = eval_monad_negate
    d['>'] = eval_monad_grade_down
    d['='] = eval_monad_groupby
    d['<'] = eval_monad_grade_up
    d['?'] = eval_monad_range
    d['@'] = eval_monad_atom
    d['^'] = eval_monad_shape
    d['_'] = eval_monad_floor
    d['|'] = eval_monad_reverse
    d['~'] = eval_monad_not
    d[':#'] = eval_monad_split
    d[':_'] = eval_monad_undefined
    return d


def merge_projections(arr):
    if len(arr) == 0:
        return arr
    if len(arr) == 1 or not has_none(arr[0]):
        return arr[0]
    sparse_fa = np.copy(arr[0])
    i = 0
    k = 1
    while i < len(sparse_fa) and k < len(arr):
        fa = arr[k]
        j = 0
        while i < len(sparse_fa) and j < len(fa):
            if sparse_fa[i] is None:
                sparse_fa[i] = fa[j]
                j += 1
                while j < len(fa) and safe_eq(fa[j], None):
                    j += 1
            i += 1
        k += 1
    return sparse_fa


def chain_adverbs(klong, arr):
    if arr[0].arity == 1:
        f = lambda x,k=klong,a=arr[0].a: k.eval(KGCall(a, [x], arity=1))
    else:
        f = lambda x,y,k=klong,a=arr[0].a: k.eval(KGCall(a, [x,y], arity=2))
    for i in range(1,len(arr)-1):
        o = get_adverb_fn(klong, arr[i].a, arity=arr[i].arity)
        if arr[i].arity == 1:
            f = lambda x,f=f,o=o: o(f,x)
        else:
            f = lambda x,y,f=f,o=o: o(f,x,y)
    if arr[-2].arity == 1:
        f = lambda a=arr[-1],f=f,k=klong: f(k.eval(a))
    else:
        f = lambda a=arr[-1],f=f,k=klong: f(k.eval(a[0]),k.eval(a[1]))
    return f


def get_fn_arity(f, level=0):
    if isinstance(f,KGFn):
        x = get_fn_arity(f.a, level=1)
        if is_list(f.args):
            for q in f.args:
                x.update(get_fn_arity(q,level=1))
    elif is_list(f):
        x = set()
        for q in f:
            x.update(get_fn_arity(q,level=1))
    elif isinstance(f,KGSym):
        x = set([f]) if f in reserved_fn_symbols else set()
    else:
        x = set()
    return x if level else len(x)


class KlongInterpreter():

    def __init__(self):
        self._context = deque([{}, ReadonlyDict(system_globals)])
        self._vd = create_verb_dyads(self)
        self._vm = create_verb_monads(self)

    def __setitem__(self, name, v):
        self._def_var(name if isinstance(name, KGSym) else KGSym(name), v)

    def __getitem__(self, n):
        return get_context_var(self._context, KGSym(n))

    def _context_push(self, d):
        self._context.insert(0, d)

    def _context_pop(self):
        return self._context.popleft() if len(self._context) > 1 else None

    def _def_var(self, k, v):
        if not isinstance(k, KGSym):
            raise RuntimeError(k)
        if k not in reserved_fn_symbols:
            for d in self._context:
                if in_map(k, d):
                    d[k] = v
                    return
        set_context_var(self._context[0], k, v)

    def _mk_var(self, k,v=None):
        if not self._is_defined_sym(k):
            self._def_var(k, v or k)
        return k

    def _is_defined_sym(self, k):
        if isinstance(k, KGSym):
            for d in self._context:
                if in_map(k, d):
                    return True
        return False

    def _opsym(self, s, arity):
        return self._vm[s] if arity == 1 else self._vd[s]

    def _is_operator(self, s):
        return in_map(s, self._vm) or in_map(s, self._vd)

    def _apply_adverbs(self, t, i, a, aa, arity, dyad=False, dyad_value=None):
        aa_arity = get_adverb_arity(aa, arity)
        if isinstance(a,KGOp):
            a.arity = aa_arity
        a = KGAdverb(a, aa_arity)
        arr = [a, KGAdverb(aa, arity)]
        ii,aa = peek_adverb(t, i)
        while aa is not None:
            arr.append(KGAdverb(aa, 1))
            i = ii
            ii,aa = peek_adverb(t, i)
        i, aa = self._expr(t, i)
        arr.append([dyad_value,aa] if dyad else aa)
        return i,KGCall(arr,args=None,arity=2 if dyad else 1)

    def _read_fn_args(self, t, i=0):
        """

        # Arguments are delimited by parentheses and separated by
        # semicolons. There are up to three arguments.

        a := '(' ')'
           | '(' e ')'
           | '(' e ';' e ')'
           | '(' e ':' e ';' e ')'

        # Projected argument lists are like argument lists (a), but at
        # least one argument must be omitted.

        P := '(' ';' e ')'
           | '(' e ';' ')'
           | '(' ';' e ';' e ')'
           | '(' e ';' ';' e ')'
           | '(' e ';' e ';' ')'
           | '(' ';' ';' e ')'
           | '(' ';' e ';' ')'
           | '(' e ';' ';' ')'

        """
        if cmatch(t,i,'('):
            i += 1
        elif cmatch2(t,i,':', '('):
            i+= 2
        else:
            raise UnexpectedChar(t,i,t[i])
        arr = []
        if cmatch(t, i, ')'): # nilad application
            return i+1,arr
        k = i
        while True:
            ii,c = kg_token(t,i)
            if c == ';':
                i = ii
                if k == i - 1:
                    arr.append(None)
                k = i
                continue
            elif c == ')':
                if k == ii - 1:
                    arr.append(None)
                break
            i,a = self._expr(t,i)
            arr.append(a)
        i = cexpect(t,i,')')
        return i,arr


    def _factor(self, t, i=0):
        """

        # A factor is a lexeme class (C) or a variable (V) applied to
        # arguments (a) or a function (f) or a function applied to
        # arguments or a monadic operator (m) applied to an expression
        # or a parenthesized expression or a conditional expression (c)
        # or a list (L) or a dictionary (D).

        x := C
           | V a
           | f
           | f a
           | m e
           | '(' e ')'
           | c
           | L
           | D

        # A function is a program delimited by braces. Deja vu? A
        # function may be projected onto on some of its arguments,
        # giving a projection. A variable can also be used to form
        # a projection.

        f := '{' p '}'
           | '{' p '}' P
           | V P

       """
        i,a = kg_token(t, i)
        if isinstance(a,KGChar) or is_number(a):
            pass
        elif safe_eq(a, '{'): # read fn
            i,a = self.prog(t, i)
            a = a[0] if len(a) == 1 else a
            i = cexpect(t, i, '}')
            arity = get_fn_arity(a)
            if cmatch(t, i, '(') or cmatch2(t,i,':','('):
                i,fa = self._read_fn_args(t,i)
                a = KGFn(a, fa, arity) if has_none(fa) else KGCall(a, fa, arity)
            else:
                a = KGFn(a, args=None, arity=arity)
            ii, aa = peek_adverb(t, i)
            if aa:
                i,a = self._apply_adverbs(t, ii, a, aa, arity=1)
        elif isinstance(a, KGSym):
            if cmatch(t,i,'(') or cmatch2(t,i,':','('):
                i,fa = self._read_fn_args(t,i)
                a = KGFn(a, fa, arity=len(fa)) if has_none(fa) else KGCall(a, fa, arity=len(fa))
            ii, aa = peek_adverb(t, i)
            if aa:
                i,a = self._apply_adverbs(t, ii, a, aa, arity=1)
        elif self._is_operator(a):
            a = KGOp(a,1)
            ii, aa = peek_adverb(t, i)
            if aa:
                i,a = self._apply_adverbs(t, ii, a, aa, arity=1)
            else:
                i, aa = self._expr(t, i)
                a = KGFn(a, aa, arity=1)
        elif safe_eq(a, '('):
            i,a = self._expr(t, i)
            i = cexpect(t, i, ')')
        elif safe_eq(a, '['):
            return read_list(t, ']', i)
        elif safe_eq(a, ':['):
            return read_cond(self, t, i)
        elif safe_eq(a, ':{'):
            i, d = read_list(t, '}', i)
            d = list_to_dict(d)
            import copy
            return i, KGCall(KGLambda(lambda x: copy.deepcopy(x)),args=d,arity=0)
        return i, a

    def _expr(self, t, i=0):
        """

        # An expression is a factor or a dyadic operation applied to
        # a factor and an expression. I.e. dyads associate to the right.

        e := x
           | x d e

        """
        i, a = self._factor(t, i)
        ii, aa = kg_token(t, i)
        aa = KGOp(aa,2) if self._is_operator(aa) else aa
        while isinstance(aa,KGOp) or isinstance(aa,KGSym) or safe_eq(aa, "{"):
            i = ii
            if safe_eq(aa, '{'): # read fn
                i,aa = self.prog(t, i)
                aa = aa[0] if len(aa) == 1 else aa
                i = cexpect(t, i, '}')
                arity = get_fn_arity(aa)
                if cmatch(t, i, '(') or cmatch2(t,i,':','('):
                    i,fa = self._read_fn_args(t,i)
                    aa = KGFn(aa, fa, arity=arity) if has_none(fa) else KGCall(aa, fa, arity=arity)
                else:
                    aa = KGFn(aa, args=None, arity=arity)
            elif isinstance(aa,KGSym) and (cmatch(t, i, '(') or cmatch2(t,i,':','(')):
                i,fa = self._read_fn_args(t,i)
                aa = KGFn(aa, fa, arity=len(fa)) if has_none(fa) else KGCall(aa, fa, arity=len(fa))
            ii, aaa = peek_adverb(t, i)
            if aaa:
                i,a = self._apply_adverbs(t, ii, aa, aaa, arity=2, dyad=True, dyad_value=a)
            else:
                i, aaa = self._expr(t, i)
                a = KGFn(aa, [a, aaa], arity=2)
            ii, aa = kg_token(t, i)
        return i, a

    def prog(self, t, i=0):
        """

        # A program is a ';'-separated sequence of expressions.

        p := e
           | e ';' p

        """
        arr = []
        while i < len(t):
            i, q = self._expr(t,i)
            arr.append(q)
            ii, c = kg_token(t, i)
            if c != ';':
                break
            i = ii
        return i, arr

    def _eval_fn(self, x):
        f = x.a
        f_arity = x.arity
        f_args = [(x.args if isinstance(x.args, list) else [x.args]) if x.args is not None else x.args]

        if self._is_defined_sym(f) or (isinstance(f,KGFn) and self._is_defined_sym(f.a)):
            while self._is_defined_sym(f) or (isinstance(f,KGFn) and self._is_defined_sym(f.a)):
                if (isinstance(f,KGFn) and self._is_defined_sym(f.a)):
                    f_args.append(f.args)
                    f_arity = f.arity
                    f = f.a
                f = self.eval(f)
                if isinstance(f,KGFn):
                    if f.args is not None:
                        f_args.append((f.args if isinstance(f.args, list) else [f.args]))
                    f_arity = f.arity
                    f = f.a
            f_args.reverse()
        elif isinstance(f,KGFn) and not (isinstance(f.a,KGOp) or (isinstance(f.a,list) and isinstance(f.a[0],KGAdverb))):
            # TODO: should this be recursive towards convergence?
            if f.args is not None:
                f_args.append(f.args)
            f_args.reverse()
            f_arity = f.arity
            f = f.a

        f_args = merge_projections(f_args)
        if (f_args is None and f_arity > 0) or (is_list(f_args) and len(f_args) < f_arity) or has_none(f_args):
            return x

        ctx = {} if f_args is None else {KGSym(p): self.eval(q) for p,q in zip(reserved_fn_args,f_args)}

        if is_list(f) and len(f) > 1 and is_list(f[0]) and len(f[0]) > 0:
            have_locals = True
            for q in f[0]:
                if not isinstance(q, KGSym):
                    have_locals = False
                    break
            if have_locals:
                for q in f[0]:
                    ctx[q] = q
                f = f[1:]

        self._context_push(ctx)
        try:
            # TODO: more testing on whether this is actualy the correct f
            ctx[KGSym('.f')] = f
            return f(self._context) if isinstance(f, KGLambda) else self.call(f)
        except UnresolvedArgument:
            return x
        finally:
            self._context_pop()

    # TODO: differentiate between call and eval more precisely
    # TODO: remove the need for the KGOp and Adverb tests on KGFn
    #           are they their own things? KGAdverbChain?KGOpFn?
    def call(self, x):
        return self.eval(KGCall(x.a, x.args, x.arity) if isinstance(x, KGFn) else x)

    def eval(self, x):
        if isinstance(x, KGSym):
            try:
                return find_context_var(self._context, x)
            except KeyError:
                return x if x in reserved_fn_symbols else self._mk_var(x)
        elif isinstance(x, KGCond):
            q = self.call(x[0])
            p = not (q == 0 or is_empty(q))
            return self.call(x[1]) if p else self.call(x[2])
        elif isinstance(x, KGCall) and not (isinstance(x.a,KGOp) or (isinstance(x.a,list) and isinstance(x.a[0], KGAdverb))):
            return self._eval_fn(KGFn(x.a,x.args,x.arity))
        elif isinstance(x, KGFn) and isinstance(x.a,KGOp):
            f = self._opsym(x.a.a, x.a.arity)
            fa = (x.args if isinstance(x.args, list) else [x.args]) if x.args is not None else x.args
            _x = fa[0] if x.a.a == '::' else self.eval(fa[0])
            _y = self.eval(fa[1]) if x.a.arity == 2 else None
            return f(_x) if x.a.arity == 1 else f(_x, _y)
        elif isinstance(x, KGFn) and (isinstance(x.a,list) and isinstance(x.a[0], KGAdverb)):
            return chain_adverbs(self, x.a)()
        elif isinstance(x,list) and len(x) > 0:
            return [self.call(y) for y in x][-1]
        return x

    def exec(self, x):
        return [self.call(y) for y in self.prog(x)[1]]
