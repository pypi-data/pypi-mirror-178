class DriftAppConfigError(ValueError):
    """
    Raise when a value in the config is wrong
    Allows users initialize misc. arguments as any other builtin Error
    """

    def __init__(self, message, val, *args):
        self.message = message
        self.val = val
        super(DriftAppConfigError, self).__init__(message, val, *args)
