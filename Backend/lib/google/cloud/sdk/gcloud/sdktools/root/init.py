# Copyright 2013 Google Inc. All Rights Reserved.

"""Initialize a gcloud workspace.

Creates a .gcloud folder. When gcloud starts, it looks for this .gcloud folder
in the cwd or one of the cwd's ancestors.
"""

import os

from google.cloud.sdk.calliope import base
from google.cloud.sdk.calliope import exceptions as c_exc
from google.cloud.sdk.core import config
from google.cloud.sdk.core import log
from google.cloud.sdk.core import properties
from google.cloud.sdk.core import workspaces
from google.cloud.sdk.core.credentials import store as c_store
from google.cloud.sdk.core.util import files


class Init(base.Command):
  """Initialize a gcloud workspace in the current directory."""

  @staticmethod
  def Args(parser):
    parser.add_argument(
        'project',
        help='The Google Cloud project to tie the workspace to.')

  @c_exc.RaiseToolExceptionInsteadOf(workspaces.Error, c_store.Error)
  def Run(self, args):
    """Create the .gcloud folder, if possible.

    Args:
      args: argparse.Namespace, the arguments this command is run with.

    Returns:
      The path to the new gcloud workspace.
    """
    # Ensure that we're logged in.
    c_store.Load()

    is_new_directory = False

    try:
      workspace = workspaces.FromCWD()
      # Cannot re-init when in a workspace.
      current_project = workspace.GetProperty(properties.VALUES.core.project)
      if current_project != args.project:
        message = (
            'Directory [{root_directory}] is already initialized to project'
            ' [{project}].'
        ).format(
            root_directory=workspace.root_directory,
            project=current_project)
      else:
        message = (
            'Directory [{root_directory}] is already initialized.'
        ).format(root_directory=workspace.root_directory)
      raise c_exc.ToolException(message)
    except workspaces.NoContainingWorkspaceException:
      workspace_dir = os.path.join(os.getcwd(), args.project)
      message = (
          'Directory [{root_directory}] is not empty.'
      ).format(root_directory=workspace_dir)
      if os.path.exists(workspace_dir) and os.listdir(workspace_dir):
        raise c_exc.ToolException(message)
      else:
        files.MakeDir(workspace_dir)
        is_new_directory = True
        workspace = workspaces.Create(workspace_dir)

    workspace.SetProperty(properties.VALUES.core.project, args.project)

    # Everything that can fail should happen within this next try: block.
    # If something fails, and the result is an empty directory that we just
    # created, we clean it up.
    try:
      # TODO(user): We need an API to get the other aliases.
      workspace.CloneProjectRepository(
          args.project,
          workspaces.DEFAULT_REPOSITORY_ALIAS)
    finally:
      cleared_files = False
      if is_new_directory:
        dir_files = os.listdir(workspace_dir)
        if not dir_files or dir_files == [
            config.Paths().CLOUDSDK_WORKSPACE_CONFIG_DIR_NAME]:
          log.error(('Unable to initialize project [{project}], cleaning up'
                     ' [{path}].').format(
                         project=args.project, path=workspace_dir))
          files.RmTree(workspace_dir)
          cleared_files = True
    if cleared_files:
      raise c_exc.ToolException(
          'Unable to initialize project [{project}].'.format(
              project=args.project))

    return workspace

  def Display(self, args, workspace):
    log.Print('Project [{project}] was initialized in [{path}].'.format(
        path=workspace.root_directory,
        project=args.project))
