###############################################################################
##
##  Copyright (C) 2014 Tavendo GmbH
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.
##
###############################################################################

import datetime

from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks

from autobahn.wamp.protocol import WampAppSession



class TimeServiceBackend(WampAppSession):
   """
   A simple time service application component.
   """

   def onSessionOpen(self, details):

      def utcnow():
         now = datetime.datetime.utcnow()
         return now.strftime("%Y-%m-%dT%H:%M:%SZ")

      self.register(utcnow, 'com.timeservice.now')



class TimeServiceFrontend(WampAppSession):
   """
   An application component using the time service.
   """

   @inlineCallbacks
   def onSessionOpen(self, details):

      try:
         now = yield self.call('com.timeservice.now')
      except Exception as e:
         print("Error: {}".format(e))
      else:
         print("Current time from time service: {}".format(now))

      self.closeSession()


   def onSessionClose(self, details):
      reactor.stop()
