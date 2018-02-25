class NoFileDir(Exception):
    """Exception for missing local file directory"""
    def __str___(self):
        return "ERROR: No local file directory `files/`"
