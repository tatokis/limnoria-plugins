###
# Copyright (c) 2018, Tasos Sahanidis
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import collections
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('SilenceErrors')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class SilenceErrors(callbacks.Plugin):
    """Provides a command to silence any errors that might arise from executing a subcommand"""
    pass

    # Mostly taken from the cerror conditional plugin from Limnoria
    def silence(self, irc, msg, args, command):
        """<command>
        Runs <command> and returns its output, if any, suppressing any errors
        """
        tokens = callbacks.tokenize(command)
        InvalidCommand = collections.namedtuple('InvalidCommand',
                'command')
        # Don't have a use for storing the errors now
        errors = []
        class ErrorReportingProxy(self.Proxy):
            def error(self2, s, Raise=False, *args, **kwargs):
                errors.append(s)
                if Raise:
                    raise ArgumentError
            def _callInvalidCommands(self2):
                errors.append(InvalidCommand(self2.args))
            def evalArgs(self2):
                # We don't want the replies in the nested command to
                # be stored here.
                super(ErrorReportingProxy, self2).evalArgs(withClass=self.Proxy)

        try:
            ErrorReportingProxy(irc.irc, msg, tokens)
        except callbacks.ArgumentError as e:
            pass

        # This is probably not needed
        if errors:
            return

    silence = wrap(silence, ['text'])

Class = SilenceErrors


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
