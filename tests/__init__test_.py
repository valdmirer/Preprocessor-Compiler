from inspect import currentframe, getframeinfo

'''
def t1_sift(t1):
    message = "Not all Comments were removed. | All Comments were removed."
    comments = ['//', '/*', '*/']
    for i in comments:
        __ASSERT__(i not in t1, f"{message}")
    return message

def t2_sift(t2):
    message = "An empty Line was found | All empty flagged lines were removed"
    for i in t2:
        if i == 0: break
        __ASSERT__(len(i.split('\u200B', 1)[1]) >= 1, f"{i} {message}")
    return message

def t3_sift(t3):
    return " test not ok | test ok"

class prep_tests:
    def sift(self, func) -> None:
        def wrapper(*args, **kwargs):
            t1, t2, t3 = func(*args, **kwargs)
            t2 = t2.split('\n')
            t2.append(0)
            try:
                t2.remove('')
            except:
                return
            __ASSERT__(None, t1_sift(t1))
            __ASSERT__(None, t2_sift(t2))
            __ASSERT__(None, t3_sift(t3))
        return wrapper

def __ASSERT__(condition, message):
    if condition == None:
        dbg([-11, f"\033[1;32m[OK] {message.split('|')[1]}\033[0m\n"])
    elif not condition:
        error = f"\n\033[35m[test warning]\033[0m {__file__}:{getframeinfo(currentframe()).lineno}"
        dbg([-11, error+" "+message.split('|')[0]])
    return
'''