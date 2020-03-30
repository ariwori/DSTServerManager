# -*- coding: utf-8 -*-


class LuaMaker:
    """
    lua 处理器
    """

    @staticmethod
    def makeLuaTable(table):
        """
        table 转换为 lua table 字符串
        """
        _tableMask = {}
        _keyMask = {}

        def analysisTable(_table, _indent, _parent):
            if isinstance(_table, tuple):
                _table = list(_table)
            if isinstance(_table, list):
                _table = dict(zip(range(1, len(_table) + 1), _table))
            if isinstance(_table, dict):

                if id(_table) in _tableMask:
                    print("error: LuaMaker.makeLuaTable() 成环: this = " + _parent + "  oldP = " + _tableMask[id(_table)])
                    return

                _tableMask[id(_table)] = _parent
                cell = []
                thisIndent = _indent + "    "
                for k in _table:
                    if not (isinstance(k, str) or isinstance(k, int) or isinstance(k, float)):
                        print("error: LuaMaker.makeLuaTable() key类型错误: parent = " + _parent + "  key = " + k)
                        return
                    key = isinstance(k, int) and "[" + str(k) + "]" or "[\"" + str(k) + "\"]"
                    if (_parent + key) in _keyMask:
                        print("error: LuaMaker.makeLuaTable() 重复key: key = " + _parent + key)
                        return
                    _keyMask[_parent + key] = True

                    var = None
                    v = _table[k]
                    if isinstance(v, str):
                        var = "\"" + v + "\""
                    elif isinstance(v, bool):
                        var = v and "true" or "false"
                    elif isinstance(v, int) or isinstance(v, float):
                        var = str(v)
                    else:
                        var = analysisTable(v, thisIndent, _parent + key)
                    print(type(key))
                    if isinstance(k, int):
                        cell.append(thisIndent + var)
                    else:
                        cell.append(thisIndent + key + " = " + var)
                lineJoin = ",\n"
                return "{\n" + lineJoin.join(cell) + "\n" + _indent + "}"

            else:
                print("error: LuaMaker.makeLuaTable() table类型错误: " + _parent)

        return analysisTable(table, "", "root")
