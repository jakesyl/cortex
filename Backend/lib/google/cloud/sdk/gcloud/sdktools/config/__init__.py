# Copyright 2013 Google Inc. All Rights Reserved.

"""config command group."""

from google.cloud.sdk.calliope import base
from google.cloud.sdk.calliope import exceptions as c_exc
from google.cloud.sdk.core import config
from google.cloud.sdk.core import properties


class Config(base.Group):
  """View and edit Google Cloud SDK properties."""

  @staticmethod
  def PropertiesCompleter(prefix, parsed_args, **kwargs):
    section = parsed_args.section or properties.VALUES.default_section.name
    if section in properties.VALUES.AllSections():
      props = properties.VALUES.Section(section).AllProperties()
      return [p for p in props if p.startswith(prefix)]
