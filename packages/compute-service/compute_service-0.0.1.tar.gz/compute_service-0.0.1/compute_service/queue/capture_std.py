from contextlib import redirect_stderr, redirect_stdout, contextmanager
from io import StringIO


@contextmanager
def capture_std():
    stdout = StringIO()
    stderr = StringIO()

    try:
        with redirect_stderr(stderr), redirect_stdout(stdout):
            yield stdout, stderr
    finally:
        if stdout.getvalue():
            print('[Task stdout]:', stdout.getvalue().strip())
        if stderr.getvalue():
            print('[Task stderr]:', stderr.getvalue().strip())
