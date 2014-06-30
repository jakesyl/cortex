# Copyright 2013 Google Inc. All Rights Reserved.

"""Generate usage text for displaying to the user.
"""

import argparse


class _CommandChoiceSuggester(object):
  """Utility to suggest mistyped commands.

  """
  TEST_QUOTA = 5000
  MAX_DISTANCE = 5

  def __init__(self):
    self.cache = {}
    self.inf = float('inf')
    self._quota = self.TEST_QUOTA

  def Deletions(self, s):
    return [s[:i]+s[i+1:] for i in range(len(s))]

  def GetDistance(self, longer, shorter):
    """Get the edit distance between two words.

    They must be in the correct order, since deletions and mutations only happen
    from 'longer'.

    Args:
      longer: str, The longer of the two words.
      shorter: str, The shorter of the two words.

    Returns:
      int, The number of substitutions or deletions on longer required to get
      to shorter.
    """

    if longer == shorter:
      return 0

    try:
      return self.cache[(longer, shorter)]
    except KeyError:
      pass

    self.cache[(longer, shorter)] = self.inf
    best_distance = self.inf

    if len(longer) > len(shorter):
      if self._quota < 0:
        return self.inf
      self._quota -= 1
      for m in self.Deletions(longer):
        best_distance = min(best_distance, self.GetDistance(m, shorter)+1)

    if len(longer) == len(shorter):
      # just count how many letters differ
      best_distance = 0
      for i in range(len(longer)):
        if longer[i] != shorter[i]:
          best_distance += 1

    self.cache[(longer, shorter)] = best_distance
    return best_distance

  def SuggestCommandChoice(self, arg, choices):
    """Find the item that is closest to what was attempted.

    Args:
      arg: str, The argument provided.
      choices: [str], The list of valid arguments.

    Returns:
      str, The closest match.
    """

    min_distance = self.inf
    for choice in choices:
      self._quota = self.TEST_QUOTA
      first, second = arg, choice
      if len(first) < len(second):
        first, second = second, first
      if len(first) - len(second) > self.MAX_DISTANCE:
        # Don't bother if they're too different.
        continue
      d = self.GetDistance(first, second)
      if d < min_distance:
        min_distance = d
        bestchoice = choice
    if min_distance > self.MAX_DISTANCE:
      return None
    return bestchoice


def CheckValueAndSuggest(action, value):
  """Override's argparse.ArgumentParser's ._check_value(action, value) method.

  Args:
    action: argparse.Action, The action being checked against this value.
    value: The command line argument provided that needs to correspond to this
        action.

  Raises:
    argparse.ArgumentError: If the action and value don't work together.
  """
  if action.choices is not None and value not in action.choices:

    choices = sorted([choice for choice in action.choices])
    suggestion = _CommandChoiceSuggester().SuggestCommandChoice(value, choices)
    if suggestion:
      suggest = ' Did you mean %r?' % suggestion
    else:
      suggest = ''
    message = """\
Invalid subcommand: %r.%s
""" % (value, suggest)
    raise argparse.ArgumentError(action, message)


def PrintParserError(parser):
  """Create an error function that knows about the correct parser.

  Args:
    parser: argparse.ArgumentParser, The parser this method is going to be
        tied to.

  Returns:
    func(str): The new .error(message) method.
  """
  def PrintError(message):
    """Override's argparse.ArgumentParser's .error(message) method.

    Specifically, it avoids reprinting the program name and the string "error:".

    Args:
      message: str, The error message to print.
    """
    # pylint:disable=protected-access, Trying to mimic exactly what happens
    # in the argparse code, except for the desired change.
    parser.print_usage(argparse._sys.stderr)
    parser.exit(2, 'ERROR: ({prog}) {message}\n'.format(
        prog=parser.prog, message=message))
  return PrintError


def PositionalDisplayString(arg):
  """Create the display help string for a positional arg.

  Args:
    arg: argparse.Argument, The argument object to be displayed.

  Returns:
    str, The string representation for printing.
  """
  message = arg.metavar or arg.dest.upper()
  if arg.nargs == '+':
    message += '+'
  elif arg.nargs == '*' or arg.nargs == argparse.REMAINDER:
    message += '*'
  elif arg.nargs == '?':
    message = '[{msg}]'.format(msg=message)
  return message


def FlagDisplayString(arg, brief):
  """Create the display help string for a flag arg.

  Args:
    arg: argparse.Argument, The argument object to be displayed.
    brief: bool, If true, only display one version of a flag that has
        multiple versions, and do not display the default value.

  Returns:
    str, The string representation for printing.
  """
  if brief:
    if arg.nargs == 0:
      return arg.option_strings[0]
    return '{flag}={metavar}'.format(
        flag=arg.option_strings[0],
        metavar=arg.metavar or arg.dest.upper())
  else:
    if arg.nargs == 0:
      return ', '.join(arg.option_strings)
    else:
      display_string = ', '.join(
          ['{flag} {metavar}'.format(
              flag=option_string,
              metavar=arg.metavar or arg.dest.upper())
           for option_string in arg.option_strings])
      if not arg.required and arg.default:
        display_string += '; default="{val}"'.format(val=arg.default)
      return display_string
