def fooFun():
    print ("empty param")


def fooIntFun(int_param):
    print ("input", int_param)


def multiParamFun(name, age):
    print ("name", name)
    print ("age", age)


if __name__ == '__main__':
    print ("hello python")
    fooFun()
    fooIntFun(100)
    multiParamFun("jack", 29)
