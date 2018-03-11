###
# Copyright (c) 2015, Tasos Sahanidis
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
    _ = PluginInternationalization('UrbanDictionary')
except ImportError:
    # Placeholder that allows to run the plugin on a bot
    # without the i18n module
    _ = lambda x: x


class UrbanDictionary(callbacks.Plugin):
    """Queries the Urban Dictionary API and returns the first result"""
    threaded = True

    def urban(self, irc, msg, args, opts_raw, word):
        """ [--example] [--random] [--single] [phrase]

        Queries Urban Dictionary and returns the first result.
        [--example] adds an extra reply with usage examples.
        [--random] ignores any words provided and looks up a random one.
        [--single] returns only the word, not the definiton. Implies --random."""

        opts = []
        for opt in opts_raw:
            opts.append(opt[0])

        if " --" in word:
            irc.reply("Old syntax won't work, sorry. Arguments must be passed before the search term.")
            return

        if "random" in opts or "single" in opts:
            urbanUrl = "http://api.urbandictionary.com/v0/random"
        else:
            # Check if a word was provided

            if not word:
                irc.reply("No word or phrase to look up was provided. See help urban.")
                return

            urbanUrl = "http://api.urbandictionary.com/v0/define?term=" + urllib.parse.quote_plus(word)

        try:
            reply = urllib.request.urlopen(urbanUrl).read()
        except Exception as urlex:
            irc.reply("Urllib error: " + str(urlex))
            return

        try:
            # Convert bytes to a string properly and then have json parse it
            jason = json.loads(reply.decode("utf-8"))

            # If it proceeds when we have no results, we get an exception
            # result_type does not exist in random mode, try to work around that
            try:
                jason_result = jason["result_type"]
            except:
                jason_result = "results"

            if jason_result != "no_results":
                reply = []
                if "single" in opts:
                    reply.append(jason["list"][0]["word"])
                else:
                    reply.append((jason["list"][0]["word"] + ": " + jason["list"][0]["definition"]).replace("\n", " ").replace("\r", ""))

                if "example" in opts:
                    example = jason["list"][0]["example"].replace("\n", " ").replace("\r", "")
                    if example != "":
                        reply.append("Usage Example: " + example)
                irc.replies(reply, oneToOne=False)
            else:
                irc.reply("No results were found.")

        except Exception as jasonex:
            irc.reply("JSON error: " + str(jasonex))

    urban = wrap(urban, [getopts({"single":"", "random":"", "example":""}), optional("text", "")])

Class = UrbanDictionary


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
