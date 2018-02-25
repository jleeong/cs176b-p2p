class NoHostFile(Exception):
    """Exception for missing local file directory"""
    def __str___(self):
        return "ERROR: No host file `hosts`"
