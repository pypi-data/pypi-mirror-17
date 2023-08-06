from functools import wraps

__version__ = '1.2.0'


def as_session(name=''):  # decorator
    """print start/title/end info before and after the function call

    Args:
        title: title will show after the start, if has any
    """
    def get_func(func):
        @wraps(func)
        def call_func(*args, **kwargs):
            start()
            if name:
                title(name)
            result = func(*args, **kwargs)
            end()
            return result
        return call_func
    return get_func


def start():
    print('*')


def end():
    print('!')


def br(count=1):
    """print 1 to N blank lines"""
    print('\n' * (count - 1))


def echo(msg, pre="", lvl=0):
    msg = str(msg)
    prefix = '({}) '.format(pre.capitalize()) if pre else ''
    tabs = '    ' * int(lvl) if int(lvl) else ''
    print("| {pf}{tabs}{msg}".format(pf=prefix, tabs=tabs, msg=msg))


def title(msg, **options):
    """print something like a title"""
    return echo("__{}__________________________".format(msg.upper()), **options)


def ask(msg, **options):
    return echo(msg, "?", **options)


def info(msg, **options):
    return echo(msg, "info", **options)


def warn(msg, **options):
    return echo(msg, "warning", **options)


def err(msg, **options):
    return echo(msg, "error", **options)


def pause(msg="Press Enter to Continue..."):
    """press to continue"""
    input('\n' + msg)


def bye(msg=''):
    """print msg and exit"""
    exit(msg)


def get_input(question='', prompt='> '):
    if question:
        print(question)
    return str(input(prompt)).strip()


def get_choice(choices):
    assemble_print = ""
    for index, item in enumerate(choices):
        assemble_print += '\n' if index else ''
        assemble_print += "| " + " {}) ".format(str(index + 1)) + str(item)
    user_choice = get_input(assemble_print)
    if user_choice in choices:
        return user_choice
    elif user_choice.isdigit():
        index = int(user_choice) - 1
        if index >= len(choices):
            err("Invalid Choice")
            bye()
        return choices[index]
    else:
        err("Please enter a valid choice")
        return get_choice(choices)
