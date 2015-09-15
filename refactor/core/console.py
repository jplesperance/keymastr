from functools import partial
import sys


class Console(object):

    _console_colors = {
        'yellow': 33, 'green': 32, 'red': 31
    }

    def format(self, text, color=None, bold=False):
        if not color and not bold:
            return text
        else:
            bold_code = ';1' if bold else ''
            color_code = self._console_colors[color] if color else ''
            return '\x1b[{0}{1}m{text}\x1b[0m'.format(
                color_code, bold_code, text=text)

    error = partial(format, color='red')
    warning = partial(format, color='yellow')
    success = partial(format, color='green')
    strong = partial(format, bold=True)

    @staticmethod
    def write(message):
        sys.stdout.write(message)
        sys.stdout.flush()

    def writeln(self, message):
        self.write(message + '\n')

    def status(self, message, details=''):
        self.write('[ {} ]'.format(message))
        if details:
            self.write(' [{}]'.format(details))
        self.write('\n')

    def status_ok(self, details=''):
        self.status(self.success('Ok'), details)

    def status_skipped(self, details=''):
        self.status(self.warning('Exists'), details)

    def status_failed(self, details=''):
        self.status(self.error('Failed'), details)

    def log(self, message):
        self.write(message + '... ')

    ok = status_ok
    skipped = status_skipped
    failed = status_failed
