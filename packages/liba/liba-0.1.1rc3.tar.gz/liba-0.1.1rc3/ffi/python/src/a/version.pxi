from a.version cimport *

def version() -> str:
    '''algorithm library version'''
    return a_version().decode()

def version_major() -> a_uint_t:
    '''algorithm library version major'''
    return a_version_major()

def version_minor() -> a_uint_t:
    '''algorithm library version minor'''
    return a_version_minor()

def version_patch() -> a_uint_t:
    '''algorithm library version patch'''
    return a_version_patch()
