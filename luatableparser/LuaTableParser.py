''' Basic Implementation of Lua Table Parser

    William Cheung, 12/20/2015

    The parser interprets Lua tables that have the following syntax form:

        table ::= '{' [fieldlist] '}'
        fieldlist ::= field {fieldsep field} [fieldsep]
        field ::= '[' index ']' '=' expr | Name '=' expr | expr
        index ::= luastring | number
        expr  ::= 'nil' | boolean | number | luastring | table
        fieldsep  ::= ',' | ';'

    There are 3 class definitions in this file:
        Utils :          include utility methods used by other two classes
        LuaTableReader : read tables form a string;
                         do syntax checking and preliminary parsing
        LuaTableParser : include interfaces for clients of this parser;
                         the generic load() method loads and parses a lua table
                         from a string, the dump() method dumps a lua table from
                         the internal representation to a string
'''


class Utils:
    @staticmethod
    # convert a string to an integer or a floating point number
    def str_to_num(s):
        err_msg = '\"' + s + '\" cannot be converted to a number'
        try:
            i = int(s)
        except:
            try:
                f = float(s)
            except:
                raise Exception(err_msg)
            else:
                return f
        else:
            return i


class LuaTableReader:
    def __init__(self, s):
        self.__text = s
        self.__length = len(s)
        self.__index = 0
        self.__prevp = -1

    # get the next char in the string
    def __next(self):
        ret = None
        if self.__index < self.__length:
            ret = self.__text[self.__index]
            self.__index += 1
        return ret

    def __backward(self):
        self.__index -= 1

    def __forward(self):
        self.__index += 1

    # get the next char in the string, skipping whitespaces and comments
    def next_clean(self):
        self.__swallow_spaces()
        prevp = self.__index
        while self.__try_swallow_comments():
            self.__swallow_spaces()
            prevp = self.__index
        self.__prevp = prevp
        return self.__next()

    # back up one char
    def back(self):
        if self.__prevp != -1:
            self.__index = self.__prevp
        else:
            raise Exception('next_clean() should be called before back()')

    # get the next Lua table
    def next_table(self):
        table, fields = '{', []
        c = self.next_clean()
        if c != '{':
            raise Exception('a table must start with \'{\'')
        while True:
            c = self.next_clean()
            if c is None:
                raise Exception('a table must end with \'}\'')
            elif c == '}':
                break
            else:
                self.back()
                text, field = self.__next_field()
                table += text
                fields.append(field)
            c = self.next_clean()
            if c in ',;':
                if self.next_clean() == '}':
                    break
                self.back()
            elif c == '}':
                break
            else:
                raise Exception('expected a \',\' \';\' or \'}\'')
            table += ','
        table += '}'
        return table, fields

    # get the next field, where
    #     field ::= '[' expr1 ']' '=' expr2 | expr1 '=' expr2 | expr2
    # @return field : a string, the text representation of the field
    #         [expr1, expr2] : a list
    def __next_field(self):
        field, expr1, expr2 = '', None, ''
        c = self.next_clean()  # assert c != '\0'
        if c == '[':
            self.__backward()
            xstr, ok = self.__try_read_xstring()
            if ok:  # we get a xstring
                expr2 += xstr
                field = expr2
            else:
                self.__forward()
                index = self.__next_expr()
                x = self.next_clean()
                if x == ']':
                    if not self.__test_validity_of_index(index):
                        raise Exception('invalid table index : ' + index)
                    expr1 = index
                    if self.next_clean() != '=':
                        raise Exception('invalid table field')
                    expr2 = self.__next_expr()
                    field = '[' + expr1 + ']' + '= ' + expr2
                else:
                    raise Exception('invalid table field')
        else:
            self.back()
            expr1 = self.__next_expr()
            x = self.next_clean()
            if x == '=':
                if not self.__test_validity_of_name(expr1):
                    raise Exception('invalid variable name : ' + expr1)
                expr2 = self.__next_expr()
                field = expr1 + '= ' + expr2
            elif x is not None:
                self.back()
                expr1, expr2 = None, expr1
                field = expr2
            else:
                raise Exception('invalid table field')

        c = self.next_clean()
        if c not in ',;}':
            raise Exception('syntax error near \"' + expr2 + '\"')
        else:
            self.back()
        return field, [expr1, expr2]

    def __next_expr(self):
        c = self.next_clean()
        if c == '{':
            self.__backward()
            table, _ = self.next_table()
            return table
        elif c in '\'\"':
            self.__backward()
            return self.__next_string()
        elif c.isdigit() or c in '+-.':
            self.__backward()
            return self.__next_number()
        elif c.isalpha() or c == '_':
            self.__backward()
            return self.__next_token()
        elif c == '[':
            self.__backward()
            xstr, ok = self.__try_read_xstring()
            if ok:
                return xstr
            else:
                raise Exception('syntax error near \'[\'')
        elif c is None:
            raise Exception('an expression cannot be empty')
        else:
            raise Exception('syntax error near \'' + c + '\'')

    def __next_string(self):
        ret = '"'
        mark = self.next_clean()
        while True:
            c = self.__next()
            if c is None:
                raise Exception('a string must end with \' or \"')
            elif c == mark:
                break
            elif c in '\'\"':
                ret += '\\' + c
            else: # TODO if c is '\n', what should we do ?
                if c == '\\':  # handle escape sequences
                    ret += '\\' + self.__next()
                else:
                    ret += c
        ret += '"'
        return ret

    # try to read a xstring, where
    #     xstring ::= [[...]] | [=[...]=] | ...
    # this method has the 'commit or rollback' semantics
    # if ok, return a normal string delimited by '"'
    def __try_read_xstring(self):
        prevp, index = self.__prevp, self.__index
        c = self.__next() # assert c == '['
        if c != '[':
            raise Exception('assertion failed')

        c = self.__next()
        cnt = 0
        while c == '=':
            cnt += 1
            c = self.__next()
            if c is None:
                break
        if c == '[':
            # if we are not a xstring, then a exception will be raised
            text = self.__read_xstring_aux(cnt)
            return '"' + text + '"', True

        self.__prevp, self.__index = prevp, index
        return '', False

    def __read_xstring_aux(self, n):
        ret = ''
        c = self.__next()
        while True:
            if c is None:
                raise Exception('invalid lua xstring')
            elif c == ']':
                coll, i = ']', n
                x = self.__next()
                while x is not None:
                    if i == 0:
                        break
                    if x != '=':
                        break
                    i -= 1
                    coll += x
                    x = self.__next()
                if i == 0 and x == ']':
                    break
                elif x is None:
                    raise Exception('invalid lua xstring')
                else:
                    ret += coll
                    c = x
                    continue
            if c == '\\':
                c += '\\'
            ret += c
            c = self.__next()
        return ret

    # get the next number, using C-like syntax
    def __next_number(self):
        ret = ''
        c = self.__next()  # we have ensured that c is a digit, '.', '+', or '-'
        if c.isdigit():
            self.__backward()
            ret += self.__read_digits()
        elif c in '+-':
            ret += c + self.__read_digits()

        if c != '.':
            c = self.__next()

        if c == '.':
            digits = self.__read_digits()
            if ret == '' or ret == '-':
                if digits == '':
                    raise Exception('syntax error near \'.\'')
            ret += '.' + digits
            c = self.__next()

        if c in 'eE':
            x = self.__next()
            if x.isdigit():
                self.__backward()
                ret += c + self.__read_digits()
            elif x in '+-':
                digits = self.__read_digits()
                if digits == '':
                    raise Exception('syntax error near \"' + c + '-\"')
                ret += c + x + digits
            else:
                raise Exception('syntax error near \'' + c + '\'')
        elif c is not None:
            self.__backward()
        return ret

    def __read_digits(self):
        ret = ''
        c = self.__next()
        while c.isdigit():
            ret += c
            c = self.__next()
        if c is not None:
            self.__backward()
        return ret

    # get the next token (name, or identifier)
    def __next_token(self):
        ret = self.__next() # assert ret.isalpha() or ret == '_'
        c = self.__next()
        while c.isalnum() or c == '_':
            ret += c
            c = self.__next()
        if c is not None:
            self.__backward()
        return ret

    # try to swallow comments following the current position of the text
    # this method has the 'commit or rollback' semantics
    def __try_swallow_comments(self):
        c = self.__next()
        if c == '-':
            x = self.__next()
            if x == '-':
                self.__do_swallow_comments()
                return True
            elif x is not None:
                self.__backward() # unget x
            self.__backward() # unget c
        elif c is not None:
            self.__backward() # unget c
        return False

    def __do_swallow_comments(self):
        c = self.__next()
        if c != '[':
            self.__swallow_line()
        else:
            c = self.__next()
            cnt = 0
            while c == '=':
                cnt += 1
                c = self.__next()
                if c is None:
                    break
            if c != '[':
                self.__swallow_line()
            else:
                self.__swallow_comments_aux(cnt)

    def __swallow_line(self):
        c = self.__next()
        while c is not None and c != '\n':
            c = self.__next()

    def __swallow_spaces(self):
        c = self.__next()
        while c is not None and c.isspace():
            c = self.__next()
        if c is not None:
            self.__backward()

    def __swallow_comments_aux(self, n):
        c = self.__next()
        while c is not None:
            if c in '\'\"':
                self.__backward()
                self.__next_string()
            elif c == ']':
                x = self.__next()
                i = n
                while x is not None:
                    if i == 0:
                        break
                    if x != '=':
                        break
                    i -= 1
                    x = self.__next()
                if x is None or (i == 0 and x == ']'):
                    break
                elif x == ']':
                    c = x
                    continue
            c = self.__next()

    # names in lua can be any string of letters, digits, and underscores,
    # not beginning with a digit
    def __test_validity_of_name(self, name):
        n = len(name)
        if n == 0:
            return False
        if not name[0].isalpha() and name[0] != '_':
            return False
        if n > 1 and not self.__test_validity_aux(name[1:]):
            return False
        return True

    def __test_validity_aux(self, s):
        for c in s:
            if not c.isalnum() and c != '_':
                return False
        return True

    # the table index must be a string or a number in our convention
    def __test_validity_of_index(self, index):
        n = len(index)
        if n > 1 and index.startswith('"') and index.endswith('"'):
            return True
        elif n > 1 and index.startswith('\'') and index.endswith('\''):
            return True
        else:
            try:
                Utils.str_to_num(index)
            except:
                return False
            else:
                return True


# LuaTableParser instances can be used by clients to parse or dump lua tables
class LuaTableParser:
    def __init__(self):
        self.__table = {}

    # load a lua table from a string
    def load(self, s):
        self.__table = self.__parse(s)

    # dump the contents of the instance as lua table to a string
    def dump(self):
        return self.__dump(self.__table)

    # load a table form a file. p is a path points to a text file
    def loadLuaTable(self, p):
        f = open(p, 'r')
        self.load(f.read())
        f.close()

    # dump a table to a file
    def dumpLuaTable(self, p):
        f = open(p, 'w')
        f.write(self.dump())
        f.close()

    # load a dict to the instance, which represents a lua table
    def loadDict(self, d):
        for k in d.keys():
            if not isinstance(k, (int, float, str)):
                del d[k]
        s = self.__dump(d)
        self.load(s)

    # dump the internal data to a dict
    def dumpDict(self):
        tmp = self.__parse(self.dump())
        if isinstance(tmp, list):
            ret = {}
            n = len(tmp)
            for i in range(n):
                if tmp[i] is not None:
                    ret[i+1] = tmp[i]
            return ret
        return tmp

    def __getitem__(self, item):
        if isinstance(self.__table, list):
            n = len(self.__table)
            if item < 1 or item > n:
                raise IndexError('table index out of range')
            else:
                return self.__table[item-1]
        else:
            return self.__table[item]

    # parse a string to a table
    def __parse(self, s):
        reader = LuaTableReader(s)
        lst, dct = [], {}
        _, fields = reader.next_table()  # read the 1st table in s
        # print 'fields : ' + str(fields)
        for field in fields:
            # print '__parse_field : ' + str(field)
            k, v = self.__parse_field(field)
            if k is not None:
                if v is not None:
                    dct[k] = v
            else:
                lst.append(v)
        return self.__merge_result(lst, dct)

    def __merge_result(self, lst, dct):
        if len(dct) == 0:
            return lst
        elif len(lst) == 0:
            return dct
        else:
            l = len(lst)
            for i in range(l):
                if lst[i] is not None:
                    dct[i+1] = lst[i]
            return dct

    def __parse_field(self, field):
        expr_k, expr_v = field[0], field[1]
        if expr_k is None:
            return None, self.__eval_expr(expr_v)
        else:
            return self.__eval_index(expr_k), self.__eval_expr(expr_v)

    def __eval_index(self, index):
        # the table index must be a string or a number
        n = len(index)
        if n > 1 and index.startswith('"') and index.endswith('"'):
            return self.__eval_string(index[1:n-1])
        elif n > 1 and index.startswith('\'') and index.endswith('\''):
            return self.__eval_string(index[1:n-1])
        else:
            try:
                x = Utils.str_to_num(index)
            except:
                return index
            else:
                return x

    def __eval_expr(self, expr):
        if expr == 'nil':
            return None
        if expr == 'true':
            return True
        elif expr == 'false':
            return False

        n = len(expr)
        if n > 0 and expr[0] == '{':  # table
            return self.__parse(expr)
        elif n > 1 and expr[0] in '\'\"' and expr[n-1] in '\'\"' \
            and expr[0] == expr[n-1]: # string
            return self.__eval_string(expr[1:n - 1])
        try:
            x = Utils.str_to_num(expr)
        except: # nil
            return None
        else:   # number
            return x

    def __eval_string(self, s):
        ret = ''
        n, i = len(s), 0
        while i < n:
            if s[i] == '\\':
                i += 1
                if i < n:
                    t, j = self.__eval_string_aux(s, i, n)
                    i = j
                    ret += t
                else:
                    ret += '\\'
                    break
            else:
                ret += s[i]
                i += 1
        return ret

    def __eval_string_aux(self, s, i, n):
        c = s[i]
        if c.isdigit():
            x, m = '', 3
            while c.isdigit():
                x += c
                i += 1
                if i < n:
                    c = s[i]
                else:
                    break
                m -= 1
                if m == 0:
                    break
            y = int(x)
            if y > 255:
                raise Exception('invalid escape sequence \"\\'+ x \
                                + '\", only ASCII code is allowed')
            return chr(y), i
        else:
            return self.__eval_esc_seq(c), i+1

    def __eval_esc_seq(self, c):
        esc_seq_table = {'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n',
                         'r': '\r', 't': '\t', 'v': '\v'}
        if esc_seq_table.has_key(c):
            return esc_seq_table[c]
        elif c in '\\\'\"[]':
            return c
        return '\\' + c

    def __dump_char(self, c):
        esc_seq_table = {'\a': 'a', '\b': 'b', '\f': 'f', '\n': 'n',
                         '\r': 'r', '\t': 't', '\v': 'v'}
        if esc_seq_table.has_key(c):
            return '\\' + esc_seq_table[c]
        elif c in '\\\'\"[]':
            return '\\' + c
        return c

    def __dump(self, table):
        if isinstance(table, list):
            return self.__dump_list(table)
        return self.__dump_aux(table, 4, 0)

    def __dump_aux(self, d, indent_factor, indent):
        commanate = False
        length = len(d)
        keys = d.keys()
        ret = '{'
        if length == 1:
            key = keys[0]
            ret += self.__dump_index(key)
            ret += '='
            if indent_factor > 0:
                ret += ' '
            ret += self.__dump_value(d[key], indent_factor, indent)
        elif length != 0:
            new_indent = indent + indent_factor
            for key in keys:
                if commanate:
                    ret += ','
                if indent_factor > 0:
                    ret += '\n'
                ret += self.__indent(new_indent)
                ret += self.__dump_index(key)
                ret += '='
                if indent_factor > 0:
                    ret += ' '
                ret += self.__dump_value(d[key], indent_factor, new_indent)
                commanate = True
            if indent_factor > 0:
                ret += '\n'
            ret += self.__indent(indent)
        ret += '}'
        return ret

    def __indent(self, indent):
        ret = ''
        for i in range(indent):
            ret += ' '
        return ret

    def __dump_index(self, index):
        if isinstance(index, (int, float)):
            return '[' + str(index) + ']'
        elif isinstance(index, str):
            return '[' + self.__dump_string(index) + ']'
        else:
            return Exception('the table index must be a string or a number')

    def __dump_value(self, v, indent_factor, indent):
        if isinstance(v, bool):
            if v:
                return 'true'
            else:
                return 'false'
        elif isinstance(v, (int, float)):
            return str(v)
        elif isinstance(v, str):
            return self.__dump_string(v)
        elif isinstance(v, list):
            return self.__dump_list(v)
        elif isinstance(v, dict):
            return self.__dump_aux(v, indent_factor, indent)
        return 'nil'

    def __dump_string(self, s):
        ret = ''
        for c in s:
            ret += self.__dump_char(c)
        return '\"' + ret + '\"'

    def __dump_list(self, lst):
        commanate = False
        ret = '{'
        for elem in lst:
            if commanate:
                ret += ','
            ret += self.__dump_value(elem, 0, 0)
            commanate = True
        ret += '}'
        return ret
