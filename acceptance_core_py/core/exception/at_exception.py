class ATException(Exception):
    def __init__(self, *args, **kwargs):
        default_message = 'Exception in Acceptance Selenium framework'

        # if any arguments are passed...
        if args or kwargs:
            super().__init__(*args, **kwargs)
        else:
            super().__init__(default_message)