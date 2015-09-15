from functools import wraps

from refactor.core import console
from refactor.core.config import settings


class Utility(object):
    machines = []

    def stop_on(*exceptions):
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    for error in e.errors:
                        print(error[0])
                        print(error[1])

            return wrapper

        return decorator



    @staticmethod
    def write_heading(message):
        trailer_length = 80 - (len(message) + 5)
        console.writeln('=== {message} {trailer}\n'.format(
            message=console.strong(message),
            trailer=('=' * trailer_length)))