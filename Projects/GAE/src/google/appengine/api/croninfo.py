#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""CronInfo tools.

A library for working with CronInfo records, describing cron entries for an
application. Supports loading the records from yaml.
"""



import logging
import sys
import traceback

try:
  import pytz
except ImportError:
  pytz = None

from google.appengine.cron import groc
from google.appengine.api import validation
from google.appengine.api import yaml_builder
from google.appengine.api import yaml_listener
from google.appengine.api import yaml_object

_URL_REGEX = r'^/.*$'
_TIMEZONE_REGEX = r'^.{0,100}$'
_DESCRIPTION_REGEX = r'^.{0,499}$'


class GrocValidator(validation.Validator):
  """Checks that a schedule is in valid groc format."""

  def Validate(self, value):
    """Validates a schedule."""
    if value is None:
      raise validation.MissingAttribute('schedule must be specified')
    if not isinstance(value, basestring):
      raise TypeError('schedule must be a string, not \'%r\'' % type(value))
    schedule = groc.CreateParser(value)
    try:
      schedule.timespec()
    except groc.GrocException, e:
      raise validation.ValidationError('schedule \'%s\' failed to parse: %s' % (
          value, e.args[0]))
    return value


class TimezoneValidator(validation.Validator):
  """Checks that a timezone can be correctly parsed and is known."""

  def Validate(self, value):
    """Validates a timezone."""
    if value is None:
      return
    if not isinstance(value, basestring):
      raise TypeError('timezone must be a string, not \'%r\'' % type(value))
    if pytz is None:
      return value
    try:
      pytz.timezone(value)
    except pytz.UnknownTimeZoneError:
      raise validation.ValidationError('timezone \'%s\' is unknown' % value)
    except IOError:
      return value
    except:
      e, v, t = sys.exc_info()
      logging.warning("pytz raised an unexpected error: %s.\n" % (v) + 
                      "Traceback:\n" + "\n".join(traceback.format_tb(t)))
      raise
    return value


CRON = 'cron'

URL = 'url'
SCHEDULE = 'schedule'
TIMEZONE = 'timezone'
DESCRIPTION = 'description'


class MalformedCronfigurationFile(Exception):
  """Configuration file for Cron is malformed."""
  pass


class CronEntry(validation.Validated):
  """A cron entry describes a single cron job."""
  ATTRIBUTES = {
      URL: _URL_REGEX,
      SCHEDULE: GrocValidator(),
      TIMEZONE: TimezoneValidator(),
      DESCRIPTION: validation.Optional(_DESCRIPTION_REGEX)
  }


class CronInfoExternal(validation.Validated):
  """CronInfoExternal describes all cron entries for an application."""
  ATTRIBUTES = {
      CRON: validation.Optional(validation.Repeated(CronEntry))
  }


def LoadSingleCron(cron_info):
  """Load a cron.yaml file or string and return a CronInfoExternal object."""
  builder = yaml_object.ObjectBuilder(CronInfoExternal)
  handler = yaml_builder.BuilderHandler(builder)
  listener = yaml_listener.EventListener(handler)
  listener.Parse(cron_info)

  cron_info = handler.GetResults()
  if len(cron_info) < 1:
    raise MalformedCronfigurationFile('Empty cron configuration.')
  if len(cron_info) > 1:
    raise MalformedCronfigurationFile('Multiple cron sections '
                                      'in configuration.')
  return cron_info[0]