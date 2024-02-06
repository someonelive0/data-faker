from mimesis import Field, Locale


# 使用用户名来产生一个单词，以后应该考虑使用一个名称字典来随机产生
# mktablename() 产生一个单词
def mktablename():
    field = Field(Locale.EN)
    tablename = field("username", mask="U_d", key=str.lower, drange=(100, 10000))
    return tablename

# mktablenames(nums) 一次产生nums个单词，同时需要判断是否重复，故使用一个临时字典判断是否重复
def mktablenames(nums):
    tablenames = {}
    while len(tablenames) < nums:
        tablename = mktablename()
        if tablenames.get(tablename) is None:
            tablenames[tablename] = 1
    return list(tablenames.keys())


if __name__ == '__main__':
    print('test make tablename from mimesis')
    print('random make tablename for 5 times')
    for i in range(5):
        tablename = mktablename()
        print(len(tablename), tablename)

    print('random make tablenames in one time')
    tablenames = mktablenames(9)
    print(len(tablenames), tablenames)
