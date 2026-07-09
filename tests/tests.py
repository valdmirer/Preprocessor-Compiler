from tests.Register import *
import math

def __ASSERT__(condition, message):
    if (not condition):
        print("\033[31m", message.split('|')[0], "\033[0m")
        return
    print("\033[32m", message.split('|')[1], "\033[0m")

#@register('clstest1')
#def CLS(*args, **kwargs) -> None:
#    message = "Comments Found while Tests.       | Clear of all Comments while Tests."
#    message2 = "An empty Line Found While Tests. | Clear of all empty flagged lines."
#    
#    t1,t2,t3 = args
#    
#    comments = ['//', '/*', '*/']
#    test2 = t2.split('\    u200c')
#
#    __ASSERT__(math.prod([(_ not in t1) for _ in comments]), f"{message}")
#    __ASSERT__(math.prod([len(_.split("\u200B")[1]) >= 1 for _ in test2[1:len(test2)-1]]), f"{message2}")
#    
#    return None
#@register('testingtest1')
#def testing(*args) -> int: pass
#@register('testagaintest1')
#def testagain(*args) -> int: pass

