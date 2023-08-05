# --------------------------------------------------------------------------
# Source file provided under Apache License, Version 2.0, January 2004,
# http://www.apache.org/licenses/
# (c) Copyright IBM Corp. 2015, 2016
# --------------------------------------------------------------------------

# coding=utf-8
# ------------------------------
from __future__ import print_function
import sys

import six
from six import iteritems

# gendoc: ignore


class _NumPrinter(object):
    """
    INTERNAL.
    """

    def __init__(self, nb_digits_for_floats, num_infinity=1e+20, pinf="+inf", ninf="-inf"):
        assert (nb_digits_for_floats >= 0)
        assert (isinstance(pinf, str))
        assert (isinstance(ninf, str))
        self.true_infinity = num_infinity
        self.__precision = nb_digits_for_floats
        self.__positive_infinity = pinf
        self.__negative_infinity = ninf
        # coin the format from the nb of digits
        # 2 -> %.2f
        self._double_format = "%." + ('%df' % nb_digits_for_floats)

    @property
    def precision(self):
        return self.__precision

    def to_string(self, num):
        if num >= self.true_infinity:
            return self.__positive_infinity
        elif num <= - self.true_infinity:
            return self.__negative_infinity
        else:
            try:
                if num.is_integer():    # the is_integer() function is faster than testing: num == int(num)
                    return '%d' % num
                else:
                    return self._double_format % num
            except AttributeError:
                return '%d' % num

    def to_stringio(self, oss, num):
        int_num = int(num)
        if num == int_num:
            oss.write('%d' % int_num)
        else:
            raw = self._double_format % num
            oss.write(raw)

    def __call__(self, num):
        return self.to_string(num)


class ModelPrinter(object):
    ''' Generic Printer code.
    '''

    def __init__(self):
        pass

    def get_format(self):
        """
        returns the Format object
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    def extension(self):
        """
        :return: the extension of the format
        """
        return self.get_format().extension

    def printModel(self, mdl, out=None):
        """ Generic method.
            If passed with a string, uses it as a file name
            if None is passed, uses standard output.
            else assume a stream is passed and try it
        """
        if out is None:
            # prints on standard output
            self.print_model_to_stream(sys.stdout, mdl)
        elif isinstance(out, six.string_types):
            # a string is interpreted as a path name
            ext = self.extension()
            path = out if out.endswith(ext) else out + ext
            # SAv format requires binary mode!
            write_mode = "wb" if self.get_format().is_binary else "w"
            with open(path, write_mode) as of:
                self.print_model_to_stream(of, mdl)
                # print("* file: %s overwritten" % path)
        else:
            try:
                self.print_model_to_stream(out, mdl)
            except AttributeError as ea:  # pragma: no cover
                pass  # pragma: no cover
                # stringio will raise an attribute error here, due to with
                # print("Cannot use this an output: %s" % str(out))

    def print_model_to_stream(self, out, mdl):
        raise NotImplementedError  # pragma: no cover

    def get_var_name_encoding(self):
        return None  # default is no encoding


# noinspection PyAbstractClass
class TextModelPrinter(ModelPrinter):
    DEFAULT_ENCODING = "ENCODING=ISO-8859-1"



    def __init__(self, comment_start, indent=1,
                 hide_user_names=False,
                 nb_digits_for_floats=3,
                 encoding=DEFAULT_ENCODING):
        ModelPrinter.__init__(self)
        # should be elsewhere
        self.true_infinity = float('inf')

        self.line_width = 79
        # noinspection PyArgumentEqualDefault

        self._comment_start = comment_start
        self._hide_user_names = hide_user_names
        self._encoding = encoding  # None is a valid value, in which case no encoding is printed
        # -----------------------
        # TODO: refactor these maps as scope objects...
        self._var_name_map = {}
        self._linct_name_map = {}  # linear constraints
        self._ic_name_map = {}  # indicators have a seperate index space.
        self._qc_name_map = {}

        # created on demand if model is not fully indexed
        self._local_var_indices = None
        self._local_linear_ct_indices = None
        self._local_indicator_ct_indices = None
        self._local_qct_indices = None
        # ------------------------

        self._rangeData = {}
        self._num_printer = _NumPrinter(nb_digits_for_floats)
        self._indent_level = indent
        self._indent_space = ' ' * indent
        self._indent_map = {1: ' '}

        # which translate_method to use
        try:
            type(unicode)
            # unciode is a type: we are in py2
            self._translate_chars = self._translate_chars2
        except NameError:
            self._translate_chars = self._translate_chars3

    def _get_indent_from_level(self, level):
        cached_indent = self._indent_map.get(level)
        if cached_indent is None:
            indent = ' ' * level
            self._indent_map[level] = indent
            return indent
        else:
            return cached_indent

    @property
    def nb_digits_for_floats(self):
        return self._num_printer.precision

    def _get_hide_user_names(self):
        """
        returns true if user names for variables and constraints should be forgotten.
        If yes, generic names (e.g. x1,x3, c45.. are generated and used everywhere).
        This is done on purpose to obfuscate the file.
        :return:
        """
        return self._hide_user_names

    def _set_hide_user_names(self, hide):
        self._hide_user_names = hide

    forget_user_names = property(_get_hide_user_names, _set_hide_user_names)

    def encrypt_user_names(self):
        """
        Actually used to decide whether to encryupt or noyt
        :return:
        """
        return self._hide_user_names

    def _print_line_comment(self, out, comment_text):
        out.write("%s %s\n" % (self._comment_start, comment_text))

    def _print_encoding(self, out):
        """
        prints the file encoding
        :return:
        """
        if self._encoding:
            self._print_line_comment(out, self._encoding)

    def _print_model_name(self, out, mdl):
        """ Redefine this method to print the model name, if necessary
        :param mdl: the model to be printed
        :return:
        """
        raise NotImplementedError  # pragma: no cover

    def _print_signature(self, out):
        """
        Prints a signature message denoting this file comes from Python Modeling Layer
        :return:
        """
        self._print_line_comment(out, "This file has been generated by DOcplex")

    def _newline(self, out, nb_lines=1):
        for _ in range(nb_lines):
            out.write("\n")

    def _precompute_name_dict(self, mobj_seq, local_index_map, prefix):
        ''' Returns a name dictionary from a sequence of modeling objects.
        '''
        fixed_name_dir = {}
        all_names = set()
        hide_names = self.encrypt_user_names()
        for mobj in mobj_seq:
            fixed_name = self.fix_name(mobj, prefix, local_index_map, hide_names)
            if fixed_name:
                if fixed_name in all_names:
                    mobj.trace("duplicated name {0} obj is {0!s}".format(fixed_name, mobj))
                # fixed_name_dir[mobj] = fixed_name
                fixed_name_dir[mobj._index] = fixed_name    # Use _index attribute as key, which improves performance
                all_names.add(fixed_name)
            else:
                pass
                # sys.__stdout__.write("\n-- object has no name: {0!s}".format(mobj))

        # prefix if not unique
        global_name_set = set(fixed_name_dir.values())
        k = 1
        if len(global_name_set) < len(fixed_name_dir):
            sys.__stdout__.write("\n--suffixing names")
            for (mobj, lp_name_pass1) in iteritems(fixed_name_dir):
                # fixed_name_dir[mobj] = "%s#%d" % (lp_name_pass1, k)
                fixed_name_dir[mobj._index] = "%s#%d" % (lp_name_pass1, k)
                k += 1
        return fixed_name_dir

    def _num_to_string(self, num):
        # INTERNAL
        return self._num_printer.to_string(num)

    def _num_to_stringio(self, oss, num):
        return self._num_printer.to_stringio(oss, num)

    def prepare(self, model):
        """
        :param model: the model being printed
        """
        # use printer local indexing for name generation.
        self._local_var_indices = {dv: k for k, dv in enumerate(model.iter_variables())}
        self._local_linear_ct_indices = {ct: k for k, ct in enumerate(model.iter_linear_constraints())}
        self._local_indicator_ct_indices = {ct: k for k, ct in enumerate(model.iter_indicator_constraints())}
        self._local_qct_indices = {qct: k for k, qct in enumerate(model.iter_quadratic_constraints())}

        self._var_name_map = self._precompute_name_dict(model.iter_variables(), self._local_var_indices, prefix='x')
        self._linct_name_map = self._precompute_name_dict(model.iter_linear_constraints(), self._local_linear_ct_indices, prefix='c')
        self._ic_name_map = self._precompute_name_dict(model.iter_indicator_constraints(), self._local_indicator_ct_indices, prefix='ic')
        self._qc_name_map = self._precompute_name_dict(model.iter_quadratic_constraints(), self._local_qct_indices, prefix='qc')

        self._rangeData = {}
        for rng in model.iter_range_constraints():
            # precompute data for ranges
            # 1 name ?
            # 2 rhs is lb - constant
            # 3 bounds are (0, ub-lb)
            varname = 'Rg%s' % self.ct_print_name(rng)
            rhs = rng.rhs()
            ub = rng.ub - rng.lb
            self._rangeData[rng] = (varname, rhs, ub)

    @staticmethod
    def fix_whitespace(name):
        """
        Swaps white spaces by underscores. Names with no blanks are not copied.
        :param name:
        :return:
        """
        return name.replace(" ", "_")

    def _var_print_name(self, dvar):
        # INTERNAL
        return self._var_name_map[dvar._index]

    def get_name_to_var_map(self, model):
        # INTERNAL
        name_to_var_map = {}
        for v in model.iter_variables():
            name_to_var_map[self._var_name_map[v._index]] = v
        return name_to_var_map

    def ct_print_name(self, ct):
        return self._linct_name_map.get(ct._index)

    def ic_print_name(self, indicator):
        return self._ic_name_map.get(indicator._index)

    def qc_print_name(self, quad_constraint):
        return self._qc_name_map.get(quad_constraint._index)

    def max_var_name_len(self):
        """
        :return: the maximum length of variable names
        """
        return max([len(vn) for vn in self._var_name_map.values()]) if self._var_name_map else 0

    def max_ct_name_len(self):
        """
        :return: the maximum length of constraint names
        """
        return max([len(cn) for cn in self._linct_name_map.values()]) if self._linct_name_map else 0

    def get_extra_var_name(self, model, pattern='x%d'):
        # UNUSED
        # """
        # :param pattern: a format string with one %d
        # :return: a variable name f the form pattern %k
        # where k is an integer, starting at max variable index+2
        # we loop until a free name is found.
        # """
        if model.number_of_variables:
            safe_index = max([dv.index for dv in model.iter_variables()]) + 2  # add1 for next, add 1 for start at 1
        else:
            safe_index = 1
        model_var_names = {dv.name for dv in model.iter_variables() if dv.name is not None}

        safe_name = pattern % safe_index
        nb_tries = 0
        while safe_name in model_var_names and nb_tries <= 1000:
            safe_index += 1
            safe_name = pattern % safe_index
            nb_tries += 1
        if nb_tries == 1000:
            return "_zorglub"
        else:
            return safe_name

    @staticmethod
    def _make_prefix_name(mobj, prefix, local_index_map, offset=1):
        index = local_index_map[mobj] if local_index_map is not None else mobj.unchecked_index
        prefixed_name = "{0:s}{1:d}".format(prefix, index + offset)
        return prefixed_name

    from docplex.mp.compat23 import mktrans

    __raw = " -+/\\<>"
    __cooked = "_mpd___"

    _str_translate_table = mktrans(__raw, __cooked)
    _unicode_translate_table = {}
    for c in range(len(__raw)):
        _unicode_translate_table[ord(__raw[c])] = ord(__cooked[c])

    @staticmethod
    def _translate_chars2(raw_name):
        if isinstance(raw_name, unicode):
            char_mapping = TextModelPrinter._unicode_translate_table
        else:
            char_mapping = TextModelPrinter._str_translate_table
        return raw_name.translate(char_mapping)
        # INTERNAL
        # return raw_name
        # from docplex.mp.utils import mktrans
        # table = mktrans(" -+/\\<>", "_mpd___")
        # return raw_name.translate(table)

    @staticmethod
    def _translate_chars3(raw_name):
        return raw_name.translate(TextModelPrinter._unicode_translate_table)

    def fix_name(self, mobj, prefix, local_index_map, hide_names):
        """
        default implementation does nothing but return the raw name
        :param mobj: a modeling object
        :param prefix: a naming pattern with a slot for a counter
        :return: the new modified name if necessary, here does nothing/
        """
        raw_name = mobj.name
        if hide_names or mobj.has_automatic_name() or mobj.is_generated() or not raw_name:
            return self._make_prefix_name(mobj, prefix, local_index_map, offset=1)
        else:
            return self._translate_chars(raw_name)

    def _expr_to_stringio(self, oss, expr):
        # nb digits
        # product symbol is '*'
        # no spaces
        expr.to_stringio(oss, self.nb_digits_for_floats, prod_symbol='*', use_space=True,
                         var_namer=lambda v: self._var_name_map[v._index])


    def _print_expr(self, wrapper, num_printer, var_name_map, expr, print_constant=False, allow_empty=False, force_first_plus=False):
        # prints an expr to a stream
        term_iter = expr.iter_terms()
        k = expr.get_constant() if print_constant else None
        self._print_expr_iter(wrapper, num_printer, var_name_map, term_iter, constant=k, allow_empty=allow_empty,
                              force_first_plus=force_first_plus)

    def _print_expr_iter(self, wrapper, num_printer, var_name_map,
                         expr_iter,
                         allow_empty=False,
                         force_first_plus=False,
                         constant=None):
        num2string_fn = num_printer.to_string
        c = 0
        for (v, coeff) in expr_iter:
            curr_token = ''
            if 0 == coeff:
                continue  # pragma: no cover

            if coeff < 0:
                curr_token += '-'
                wrote_sign = True
                coeff = - coeff
            elif c > 0 or force_first_plus:
                # here coeff is positive, we write the '+' only if term is non-first
                curr_token += '+'
                wrote_sign = True
            else:
                wrote_sign = False

            if 1 != coeff:
                if wrote_sign:
                    curr_token += ' '
                curr_token += num2string_fn(coeff)
            if wrote_sign or 1 != coeff:
                curr_token += ' '
            curr_token += var_name_map[v._index]

            wrapper.write(curr_token)
            c += 1

        if constant is not None:
            # here constant is a number
            if 0 != constant:
                if constant > 0:
                    if c > 0 or force_first_plus:
                        wrapper.write('+')
                wrapper.write(num2string_fn(constant))
            elif 0 == c and not allow_empty:
                wrapper.write('0')

        else:
            # constant is none here
            if not c and not allow_empty:
                # expr is empty, if we must print something, print 0
                wrapper.write('0')

    def _print_qexpr_obj(self, wrapper, num_printer, var_name_map, quad_expr, force_initial_plus):
        # writes a quadratic expression
        # in the form [ 2a_ij a_i.a_j ] / 2
        # Note that all coefficients must be doubled due to the tQXQ formulation

        if force_initial_plus:
            wrapper.write('+')

        return self._print_qexpr_iter(wrapper, num_printer, var_name_map, quad_expr.iter_quads(), use_double=True)


    def _print_qexpr_iter(self, wrapper, num_printer, var_name_map, iter_quads, use_double=False):
        q = 0
        wrapper.write('[')
        varname_getter = self._var_print_name
        for qvp, qk in iter_quads:
            curr_token = ''
            if 0 == qk:
                continue  # pragma: no cover
            abs_qk = qk
            if qk < 0:
                curr_token += '-'
                abs_qk = - qk
                wrote_sign = True
            elif q > 0:
                curr_token += '+'
                wrote_sign = True
            else:
                wrote_sign = False
            if wrote_sign:
                curr_token += ' '

            # all coefficients must be doubled because of the []/2 pattern.
            abs_qk2 = 2 * abs_qk if use_double else abs_qk
            if abs_qk2 != 1:

                curr_token += num_printer.to_string(abs_qk2)
                curr_token += ' '

            if qvp.is_square():
                qv_name = varname_getter(qvp[0])
                curr_token += "%s^2" % qv_name
            else:
                qv1 = qvp[0]
                qv2 = qvp[1]
                curr_token += "%s*%s" % (varname_getter(qv1), varname_getter(qv2))

            wrapper.write(curr_token)

            q += 1
        closer = ']/2' if use_double else ']'
        wrapper.write(closer)
        return q



class _ExportWrapper(object):
    """
    INTERNAL.
    """
    __new_line_sep = '\n'


    def __init__(self, oss, indent_str, line_width=80):
        self._oss = oss
        self._indent_str = indent_str
        self._line_width = line_width
        self._curr_line = ''
        self._wrote = False

    def reset_indent(self, new_indent):
        self._indent_str = new_indent
        # reset dynamic line data
        self._curr_line = ''
        self._wrote = False

    def is_empty(self):
        return not self._wrote

    def set_indent(self, new_indent):
        self._indent_str = new_indent

    def begin_line(self, indented=False):
        # reset dynamic line data
        self._wrote = False
        self._curr_line = self._indent_str if indented else ''


    # The 'write' function is invoked intensively when exporting a model.
    # Any piece of code that can be saved here will improve performance in a visible way.
    def write(self, token, separator=True):
        try:
            if len(self._curr_line) + len(token) >= self._line_width:
                # faster to write concatenated string, slightly faster to use '\n' instead of ref to static value
                self._oss.write(self._curr_line + '\n')
                self._curr_line = self._indent_str + token
            else:
                # 1 separator
                if separator and self._wrote:
                    self._curr_line += (' ' + token)
                else:
                    self._curr_line += token
            self._wrote = True

        except TypeError:
            # An exception will occur if token is None. In that case, there is nothing to write and
            # one can safely return.
            pass

    def flush(self, print_newline=True, reset=False):
        self._oss.write(self._curr_line)
        if print_newline:
            self._oss.write('\n')
        # Reset '_wrote' flag so that no separator will be added when writing first token of next line
        self._wrote = False
        # if reset, start a new line.
        self._curr_line = '' if reset else self._indent_str

    def newline(self):
        self._oss.write('\n')
