from .backend import np
import inspect

np.seterr(divide='ignore')

# TOOO:
# add switch for cpu vs cupy
# add channel family support
# add system commands
# add debug support


class KGSym(str):
    def __repr__(self):
        return f":{super().__str__()}"
    def __eq__(self, o):
        return isinstance(o,KGSym) and self.__str__() == o.__str__()
    def __hash__(self):
        return super().__hash__()

class KGFn():
    def __init__(self, a, args, arity):
        self.a = a
        self.args = args
        self.arity = arity

    def __str__(self):
        if self.arity == 0:
            return ":nilad"
        elif self.arity == 1:
            return ":monad"
        return ":dyad"


class KGCall(KGFn):
    pass


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
    """
    KGLambda wraps a lambda and make it available to Klong, allowing for direct
    integration of python functions in Klong.

    Introspection is used to infer which parameters should be collected from the
    current context and passed to the lambda. Parameter names must be x,y, or z
    according to the klong convention.  The value for these parameters are
    extracted directly from the currentcontext.

    If a lambda requires access to klong itself, that must be the first parameter.

    Function arity is computed by examining the arguments.

    e.g.

    lambda x,y: x + y
    lambda klong, x: klong.exec(x)

    """
    def __init__(self, fn):
        self.fn = fn
        self.args = inspect.getfullargspec(self.fn)[0]
        self.provide_klong = 'klong' in self.args

    def __call__(self, klong, ctx):
        params = [ctx[reserved_fn_symbol_map[x]] for x in reserved_fn_args if x in self.args]
        return self.fn(klong, *params) if self.provide_klong else self.fn(*params)

    def get_arity(self):
        return len(self.args) - 1 if self.provide_klong else len(self.args)


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
    if is_list(x):
        return False
    return isinstance(x, (np.floating, float, int))


def is_integer(x):
    if is_list(x):
        return False
    return isinstance(x, (np.integer, int))


def is_number(a):
    return is_integer(a) or is_float(a)


def in_map(x, v):
    try:
        return x in v
    except Exception:
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
    x = t[p:i]
    return i, reserved_fn_symbol_map.get(x) or KGSym(x)


def read_shifted_comment(t, i=0):
    while i < len(t):
        c = t[i]
        if c == '"':
            i += 1
            if not cmatch(t,i,'"'):
                break
        i += 1
    return i


def read_sys_comment(t,i,a):
    """

        .comment(x)                                            [Comment]

        Read and discard lines until the current line starts with the
        string specified in "x". Also discard the line containing the
        end-of-comment marker and return "x".

        Example: .comment("end-of-comment")
                 this will be ignored
                 this, too: *%(*^#)&(#
                 end-of-comment

        NOTE: this is handled in the parsing phase and is not a runtime function

    """
    try:
        return i + t[i:].index(a) + len(a)
    except ValueError:
        return RuntimeError("end of comment not found")


def skip_space(t, i=0):
    while i < len(t) and t[i].isspace():
        i += 1
    return i


def skip(t, i=0):
    i = skip_space(t,i)
    if cmatch2(t, i, ':', '"'):
        i = read_shifted_comment(t, i+2)
        i = skip(t, i)
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


def peek_adverb(t,i=0):
    x = cpeek2(t,i)
    if is_adverb(x):
        return i+2,x
    x = cpeek(t,i)
    if is_adverb(x):
        return i+1,x
    return i,None


def is_adverb(s):
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

