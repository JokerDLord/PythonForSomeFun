for a in range(1,10):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                for e in range(10):
                    if int("{}{}{}{}{}".format(a,b,c,d,e))*4 == int("{}{}{}{}{}".format(e,d,c,b,a)):
                        print("{}{}{}{}{}".format(a,b,c,d,e))
