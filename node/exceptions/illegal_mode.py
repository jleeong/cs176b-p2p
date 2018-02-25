class IllegalMode(Exception):
    """Exception for missing local file directory"""
    def __str___(self,mode):
        return "ERROR: Illegal Mode " + str(mode) +". Must be [g|d|s]"
