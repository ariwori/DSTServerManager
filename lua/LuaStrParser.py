# def load(self, s):
# 读取Lua table数据，输入s为一个符合Lua table定义的字符串，无返回值
# 遇到Lua table格式错误则抛出异常

# def dump(self):
# 根据类中数据返回Lua table字符串

# def loadLuaTable(self, f):
# 从文件中读取Lua table字符串，f为文件路径，遇到Lua Table的格式错误则抛出异常，文件操作失败抛出异常

# def dumpLuaTable(self, f):
# 将类中的内容以Lua table格式存入文件，f为文件路径，文件若存在则覆盖，文件操作失败抛出异常

# def loadDict(self, d):
# 读取dict中的数据，存入类中，只处理数字和字符串两种类型的key，其他类型的key直接忽略

# def dumpDict(self):
# 返回一个dict，包含类中的数据

# def update(self, d):
# 用字典d更新类中的数据，类似于字典的update

# PyLuaTblParser类支持用[]进行赋值、读写数据的操作，类似字典
import json


class LuaStrParser:
    __spaceChars = [' ', '\t', '\n', '\r']
    __stopChars = [' ', '\t', '\n', '\r', '=', ',', ';', '}', ']']
    keyTypes = [int, float, str]

    __specialChars = {
        'a': '\a', 'b': '\b', 'f': '\f', 'n': '\n', 'r': '\r', 't': '\t', 'v': '\v',
        '\\': '\\', '"': '"', "'": "'",
    }

    __reverseSpecialChars = {
        '\a': '\\a', '\b': '\\b', '\f': '\\f', '\n': '\\n', '\r': '\\r', '\t': '\\t', '\v': '\\v',
        '\\': '\\\\', '"': '\\"', "'": "\\'"
    }

    def __init__(self):
        self.__lua_object = None
        self.__lua_str = None

    def __jumpSpace(self, string, loc):
        while loc < len(string) and string[loc] in self.__spaceChars:
            loc += 1
        return loc

    def __getBackSlashNum(self, lua_str, loc):
        backslash_num = 0
        while loc >= 0 and lua_str[loc] == '\\':
            loc -= 1
            backslash_num += 1
        return backslash_num

    def __getStringEnd(self, lua_str, loc, quote):
        result = loc + 1
        if lua_str[loc] == quote:
            end = lua_str.find(quote, loc + 1)
            if end != loc + 1:
                at_end = False
                while not at_end:
                    if self.__getBackSlashNum(lua_str, end - 1) % 2 == 0:
                        at_end = True
                    if not at_end:
                        end = lua_str.find(quote, end + 1)
            if end < 0:
                raise Exception("wrong quotes!")
            result = end
        return result

    def __getStringConent(self, lua_str, loc):
        """
        return the string in the  @para lua_str
        thee result contain the quotes"""
        loc = self.__jumpSpace(lua_str, loc)
        result = None
        if lua_str[loc] == '"' or lua_str[loc] == "'":
            end = self.__getStringEnd(lua_str, loc, lua_str[loc])
            result = lua_str[loc: end + 1]
            loc = end + 1
        return result, loc

    def __removeComment(self, lua_str):
        result = ""
        loc = 0
        while loc < len(lua_str):
            # string should be add in result directly
            if lua_str[loc] == '"' or lua_str[loc] == "'":
                string, loc = self.__getStringConent(lua_str, loc)
                result += string
            # remove comment
            elif lua_str[loc] == '-':
                if loc + 1 < len(lua_str) and lua_str[loc + 1] == '-':
                    loc += 2
                    # multi line comments
                    if loc + 1 < len(lua_str) and lua_str[loc:loc + 2] == '[[':
                        loc = lua_str.find(']]', loc + 1) + 2
                    # single line comment
                    else:
                        loc = lua_str.find('\n', loc + 1) + 1
                    # add a space after remove the comment
                    result += ' '
                else:
                    result += lua_str[loc]
                    loc += 1
            # remove '\r'
            elif lua_str[loc] == '\r':
                loc += 1
                continue
            else:
                result += lua_str[loc]
                loc += 1
        return result

    def __getRightBrace(self, lua_str, loc):
        loc = lua_str.find('{', loc) + 1
        left_barce_num = 0
        while loc < len(lua_str):
            if lua_str[loc] == '"' or lua_str[loc] == "'":
                loc = self.__getStringEnd(lua_str, loc, lua_str[loc]) + 1
            elif lua_str[loc] == '{':
                left_barce_num -= 1
                loc += 1
            elif lua_str[loc] == '}':
                left_barce_num += 1
                if left_barce_num >= 1:
                    break
                loc += 1
            else:
                loc += 1
        if loc == len(lua_str):
            raise Exception("wrong number of brace")
        return loc

    def __getRightBracket(self, lua_str, loc):
        loc = lua_str.find('[', loc) + 1
        while loc < len(lua_str):
            if lua_str[loc] == '"' or lua_str[loc] == "'":
                loc = self.__getStringEnd(lua_str, loc, lua_str[loc]) + 1
            elif lua_str[loc] == ']':
                break
            else:
                loc += 1
        if loc == len(lua_str):
            raise Exception("wrong number of bracket")
        return loc

    def __getLastBrace(self, lua_str):
        end = len(lua_str) - 1
        while end >= 0 and lua_str[end] != '}':
            end -= 1
        if end < 0:
            raise Exception("wrong number of brace")
        return end

    def __readNum(self, number_str):
        try:
            num = eval(number_str)
        except Exception:
            return None
        else:
            return num

    def __getRealStr(self, s):
        result = ""
        i = 0
        while i < len(s):
            if s[i] == '\\':
                if i + 1 < len(s) and s[i + 1] in self.__specialChars.keys():
                    result += self.__specialChars[s[i+1]]
                    i += 2
                else:
                    result += s[i]
                    i += 1
            else:
                result += s[i]
                i += 1
        # print s, ">>" , result
        return result

    def __readValue(self, value):
        value = value.strip()
        if len(value) > 0:
            if value[0] == '"' or value[0] == "'":
                return self.__getRealStr(value[1:len(value) - 1]), str
            elif value == 'nil':
                return None, "nil"
            elif value == 'false':
                return False, bool
            elif value == 'true':
                return True, bool
            else:
                number = self.__readNum(value)
                if isinstance(number, int):
                    return number, int
                elif isinstance(number, float):
                    return number, float
        else:
            return None, None
        return value, str

    def __readStatement(self, lua_str, loc):
        loc = self.__jumpSpace(lua_str, loc)

        if lua_str[loc] == '{':
            end = self.__getRightBrace(lua_str, loc)
            stat = self.__parserLuaStr(lua_str[loc: end + 1])
            stat_type = type(stat)
            loc = end + 1
        elif lua_str[loc] == '[':
            end = self.__getRightBracket(lua_str, loc)
            stat, stat_type = self.__readValue(lua_str[loc + 1: end])
            loc = end + 1
        elif lua_str[loc] == '"' or lua_str[loc] == "'":
            end = self.__getStringEnd(lua_str, loc, lua_str[loc])
            stat = lua_str[loc + 1: end]
            stat = self.__getRealStr(stat)
            stat_type = str
            loc = end + 1
        else:
            end = loc
            while end < len(lua_str) and lua_str[end] not in self.__stopChars:
                end += 1
            stat, stat_type = self.__readValue(lua_str[loc: end])
            loc = end
        return stat, stat_type, loc

    def __parserLuaStr(self, lua_str):
        loc = lua_str.find('{') + 1
        end = self.__getLastBrace(lua_str)
        has_equal = False
        keys = []
        values = []
        while 0 <= loc < end:
            key, key_type, loc = self.__readStatement(lua_str, loc)
            value, value_type = None, None
            has_value = False
            loc = self.__jumpSpace(lua_str, loc)
            if lua_str[loc] == '=':
                has_value = has_equal = True
                loc += 1
                value, value_type, loc = self.__readStatement(lua_str, loc)
                loc = self.__jumpSpace(lua_str, loc)

            loc += 1

            if has_value:
                if key is not None:
                    keys.append((key, key_type))
                    values.append((value, value_type))
                else:
                    raise Exception("the key is nil")
            else:
                keys.append((key, key_type))
                values.append((None, None))
        number = 1
        if has_equal:
            result = {}
            for key_tuple, value_tuple in zip(keys, values):
                if value_tuple[1] is not None:
                    result[key_tuple[0]] = value_tuple[0]
                else:
                    if key_tuple[1] != 'nil' and key_tuple[0] is not None:
                        result[number] = key_tuple[0]
                    number += 1
            result = {k: v for k, v in result.items() if v is not None}
        else:
            result = []
            for key_tuple in keys:
                if key_tuple[1] is not None:
                    result.append(key_tuple[0])
        return result

    def readStr(self, lua_str):
        lua_str = self.__removeComment(lua_str.strip())
        self.__lua_object = self.__parserLuaStr(lua_str)

    def getLuaObject(self):
        return self.__lua_object

    def __generateKeyStr(self, lua_object):
        result = ""
        if lua_object is not None:
            if type(lua_object) is str:
                result = '["' + self.__getOriginStr(lua_object) + '"]'
            elif type(lua_object) is int or type(lua_object) is float:
                result = '[' + str(lua_object) + ']'
            elif type(lua_object) is bool:
                if lua_object:
                    result = '[true]'
                else:
                    result = '[false]'
            else:
                raise Exception("Wrong type of key: " + str(lua_object))
        return result

    def __getOriginStr(self, s):
        result = ""
        for c in s:
            if c in self.__reverseSpecialChars.keys():
                result += self.__reverseSpecialChars[c]
            else:
                result += c
        return result

    def __generateValueStr(self, lua_object):
        result = ""
        object_type = type(lua_object)
        if lua_object is None:
            result = 'nil'
        elif object_type is list or object_type is dict:
            result = self.generateLuaStr(lua_object)
        elif object_type is str:
            result = '"' + self.__getOriginStr(lua_object) + '"'
        elif object_type is int or object_type is float:
            result = str(lua_object)
        elif object_type is bool:
            if lua_object:
                result = 'true'
            else:
                result = 'false'
        return result

    def generateLuaStr(self, lua_object):
        result = ""
        if lua_object is not None:
            result += '{'
            if type(lua_object) is dict:
                for key, value in lua_object.items():
                    result += self.__generateKeyStr(key) + ' = ' + self.__generateValueStr(value) + ', '
            elif type(lua_object) is list:
                for value in lua_object:
                    result += self.__generateValueStr(value) + ', '
            result += '}'
        self.__lua_str = result
        return result


class PyLuaTblParser:
    def __init__(self):
        self.str_praser = LuaStrParser()
        self.lua_table = None

    def load(self, s):
        self.str_praser.readStr(s)
        self.lua_table = self.str_praser.getLuaObject()

    def dump(self):
        return self.str_praser.generateLuaStr(self.lua_table)

    def loadLuaTable(self, f):
        with open(f, 'r') as lua_str_file:
            lua_str = lua_str_file.read()
            self.load(lua_str)

    def dumpLuaTable(self, f):
        with open(f, 'w') as out_file:
            out_file.write(self.str_praser.generateLuaStr(self.lua_table))

    def deleteOtherKey(self, d):
        result = None
        if type(d) is dict:
            result = {}
            for key, value in d.iteritems():
                if type(key) in LuaStrParser.keyTypes:
                    if type(value) is list or type(value) is dict:
                        result[key] = self.deleteOtherKey(value)
                    else:
                        result[key] = value
        elif type(d) is list:
            result = []
            for value in d:
                if type(value) is list or type(value) is dict:
                    result.append(self.deleteOtherKey(value))
                else:
                    result.append(value)
        return result

    def loadDict(self, d):
        if type(d) is dict:
            self.lua_table = self.deleteOtherKey(d)

    def dumpDict(self):
        if type(self.lua_table) is dict:
            return self.lua_table.copy()
        elif type(self.lua_table) is list:
            return [v for v in self.lua_table]

    def update(self, d):
        if self.lua_table is None:
            self.lua_table = d
        else:
            if type(self.lua_table) is list:
                new_table = {}
                for k, v in zip(range(1, len(self.lua_table) + 1), self.lua_table):
                    if v is not None:
                        new_table[k] = v
                self.lua_table = new_table
            new_table = self.deleteOtherKey(d)
            for k, v in new_table.iteritems():
                self.lua_table[k] = v

    def __getitem__(self, item):
        try:
            return self.lua_table[item]
        except:
            return None

    def __setitem__(self, key, value):
        if self.lua_table is None:
            self.lua_table = {}
            self.lua_table[key] = value
        elif type(self.lua_table) is dict:
            self.lua_table[key] = value
        elif type(self.lua_table) is list:
            new_table = {}
            for k, v in zip(range(1,len(self.lua_table) + 1), self.lua_table):
                if v is not None:
                    new_table[k] = v
            new_table[key] = value
            self.lua_table = new_table


if __name__ == '__main__':
    pyluatblparser = PyLuaTblParser()
    f = open("modinfo.lua", "r", encoding="utf-8")
    data = f.read()
    f.close()
    pyluatblparser.load(data)
    a = pyluatblparser.dumpDict()
    with open("aa.json", 'w', encoding="utf-8") as f:
        json.dump(a, f)
