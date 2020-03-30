from LuaTableParser import *


def test1():
    print '.................... Test1 load and dump :'

    p = LuaTableParser()

    s0 = '{}'
    print '... load s0'
    p.load(s0)
    print '... dump'
    print p.dump()

    s1 = '{[\'array\'] = {65, 23, 5,}}'
    print '... load s1'
    p.load(s1)
    print '... dump'
    print p.dump()

    s2 = '{"Sunday", "Monday", "Tuesday", \'Wednesday\', "Thursday", "Friday", "Saturday"}'
    print '... load s2'
    p.load(s2)
    print '... dump'
    print p.dump()
    print p[1]
    # print p[0]

    s3 = '{x=0,y=1,[3]=2}'
    print '... load s3'
    p.load(s3)
    print '... dump'
    print p.dump()
    print p[3]

    s4 = '{array = {65,23,5,},dict = {mixed = {43,54.33,false,9,string = "value",},array = {3,6,4,},string = "value",},}'
    print '... load s4'
    p.load(s4)
    print '... dump'
    print p.dump()

    s5 = '{color="blue", thickness=2, npoints=4,\
                 {x=0,   y=0},\
                 {x=-10, y=0},\
                 {x=-10, y=1},\
                 {x=0,   y=1}\
          }'
    print '... load s5'
    p.load(s5)
    print '... dump'
    print p.dump()

    p = LuaTableParser()
    s6 = '{["x"]=0, ["y"]=0}'
    print '... load s6'
    p.load(s6)
    print '... dump'
    print p.dump()

    s7 = '{x=10, y=45; "one", "two", "three"}'
    print '... load s7'
    p.load(s7)
    print '... dump'
    print p.dump()

    # Test tables with 'nil'
    s8 = '{x=nil, y = 0, z=nil, nil}'
    print '... load s8'
    p.load(s8)
    print '... dump'
    print p.dump()

    # Test tables with 'nil'
    s8 = '{nil, 0, nil, 1}'
    print '... load s8'
    p.load(s8)
    print '... dump'
    print p.dump()
    print p[1], p[2], p[3], p[4]

    s9 = '{["x"]="{", ["y"]="}"}'
    print '... load s9'
    p.load(s9)
    print '... dump'
    print p.dump()

test1()


def test2():
    print '.................... Test2 loadLuaTable and dumpLuaTable'
    p = LuaTableParser()
    p.loadLuaTable('test2-load.txt')
    print p.dump()
    p.dumpLuaTable('test2-dump.txt')

test2()


def test3():
    print '.................... Test3 loadDict and dumpDict'
    info = {'name':'William', 'age':24, 'gender':'Male', 'description':''}
    print info
    p = LuaTableParser()
    p.loadDict(info)
    print p.dump()
    info['description'] = 'blabla...'
    print info
    print p.dump()

    dct = p.dumpDict()
    dct['age'] = 24.5
    print dct
    print p.dump()

test3()


def test4():
    print '.................... Test4'
    f = open('test4.txt', 'r')
    lines = f.readlines()
    p = LuaTableParser()
    count = 1
    for line in lines:
        print '----------- line ' + str(count) + ' :'
        count += 1
        if len(line) > 0 and line[0] == '#' or line.isspace():
            print '... omitted'
            continue
        p.load(line)
        print p.dump()
    f.close()

test4()




