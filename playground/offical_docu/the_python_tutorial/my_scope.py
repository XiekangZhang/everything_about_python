def scope_test():
    def do_local():
        # namespace: local
        # scope: local
        spam = "local spam"

    def do_nonlocal():
        # namespace: nonlocal
        # scope: enclosing 
        nonlocal spam
        spam = "nonlocal spam"

    def do_global():
        # namespace: global (module)
        # scope: global 
        global spam
        spam = "global spam"

    # namespace: nonlocal
    # scope: enclosing 
    spam = "test spam"
    do_local() # local namespace for do_local is destroyed --> enclosing scope
    print(f"After local assignment: { spam = }")  # test spam
    do_nonlocal() # enclosing scope --> updated 
    print(f"After nonlocal assignment: { spam = }")  # nonlocal spam --> function level
    do_global() # search order --> enclosing finds spam --> stop
    print(f"After global assignment: { spam = }")  # nonlocal spam


if __name__ == "__main__": # module level
    scope_test() # local namespace destroyed --> global 
    print(f"In global scope: { spam = }") # global spam
