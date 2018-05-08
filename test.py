try:
    f()
    g()
except TypeError as e:
    print(e)
except IndexError as e:
    pass

