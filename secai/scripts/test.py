def tfunc1(tf_param):
    tfunc2(tf_param)

def tfunc2(tf_param):
    print(tf_param)
    tfunc3()



def tfunc3():
    print('bottom')

tfunc1('test')
