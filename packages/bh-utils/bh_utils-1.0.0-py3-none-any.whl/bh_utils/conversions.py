"""
Some basic conversion functions.
"""

def str_to_bool( str_val: str, exception_msg=None ) -> bool:
    """
    Converts a string to Boolean.

    Main reference: 
    https://stackoverflow.com/questions/715417/converting-from-a-string-to-boolean-in-python

    If str_val can be converted to Boolean, then returns the Boolean value.
    Otherwise: 1. returns None if exception_msg is None. 2. Raises exception otherwise.

    Return:

    Four ( 4 ) possibilities: True, False, None or raise an exception.
    """
    res = None

    if str_val.lower() in [ 'true', '1', 't', 'yes', 'y', 'on' ]: 
        res = True
    elif str_val.lower() in [ 'false', '0', 'f', 'no', 'n', 'off' ]: 
        res = False

    # Succeeds.
    if ( res != None ): return res

    # Not succeeded. No exception required. Returns None.
    if ( exception_msg == None ): return res

    # Not succeeded. Exception required: raise exception.
    if ( res == None ): raise Exception( exception_msg )
	
def is_integer( value ) -> bool:
    """
    Checks whether the value of a variable is an integer.

    Main reference: 	
    https://stackoverflow.com/questions/3501382/checking-whether-a-variable-is-an-integer-or-not
    """	
    if ( isinstance(value, int) ): return True
    if ( isinstance(value, str) ):
        if value.isnumeric(): return True
    return False