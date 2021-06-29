from common.GlobalVariables import GlobalVariables as GV

# TODO: change the logging module to official logging module
def logging(*args, **kwargs):
    """
    A logging helper function, *arg, **kwargs are directly using by print().
    When GV.debug is set, these logs will be printed for debugging.
    """
    if GV.debug:
        print(*args, **kwargs)
