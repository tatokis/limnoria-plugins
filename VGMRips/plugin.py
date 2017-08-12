###
# Copyright (c) 2017, Tasos Sahanidis
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
import urllib.request
import urllib.parse
import json

try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('VGMRips')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class VGMRips(callbacks.Plugin):
    """Searches VGMRips.net for VGM packs."""
    pass

    def vgm(self, irc, msg, args, text):
        """<query>"""
        
        url = "http://vgmrips.net/packs/json/suggestions.json?q=" + urllib.parse.quote_plus(text)
        try:
            reply = urllib.request.urlopen(url).read()
        except Exception as urlerror:
            irc.reply(str("Urllib error: " + str(urlerror)))
            return
        #convert bytes to a string properly and then have json parse it
        jason = json.loads(reply.decode("utf-8"))

        cnt = len(jason[1])
        if cnt == 0:
            irc.reply("No results for " + jason[0])
            return

        reply = ""

        for i in list(range(cnt)):
            reply += "#" + str(i+1) + " " + jason[1][i] + " - " + jason[2][i] + " - " + jason[3][i].replace("http:/vgmrips", "http://vgmrips") + " "
        irc.reply(reply)

    vgm = wrap(vgm, ['text'])



Class = VGMRips


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
