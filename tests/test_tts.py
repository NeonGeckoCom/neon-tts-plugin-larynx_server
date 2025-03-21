# NEON AI (TM) SOFTWARE, Software Development Kit & Application Framework
# All trademark and other rights reserved by their respective owners
# Copyright 2008-2025 Neongecko.com Inc.
# Contributors: Daniel McKnight, Guy Daniels, Elon Gasper, Richard Leeds,
# Regina Bloomstine, Casimiro Ferreira, Andrii Pernatii, Kirill Hrymailo
# BSD-3 License
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from this
#    software without specific prior written permission.
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
# PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
# CONTRIBUTORS  BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS;  OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE,  EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), "res"))
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from neon_tts_plugin_larynx_server import LarynxServerTTSPlugin


class TestTTS(unittest.TestCase):
    def setUp(self) -> None:
        self.tts = LarynxServerTTSPlugin(config={'host': 'https://larynx.2022.us'})

    def doCleanups(self) -> None:
        try:
            os.remove(os.path.join(os.path.dirname(__file__), "test.wav"))
        except FileNotFoundError:
            pass
        try:
            self.tts.playback.stop()
            self.tts.playback.join()
        except AttributeError:
            pass
        except RuntimeError:
            pass

    def test_get_voices(self):
        voices = self.tts.get_voices()
        self.assertIsInstance(voices, dict)

    def test_get_vocoders(self):
        vocoders = self.tts.get_vocoders()
        self.assertIsInstance(vocoders, list)
        for vocoder in vocoders:
            self.assertIsInstance(vocoder, dict)

    def test_speak_no_params(self):
        out_file = os.path.join(os.path.dirname(__file__), "test.wav")
        file, _ = self.tts.get_tts("Hello.", out_file)
        self.assertEqual(file, out_file)

    def test_empty_speak(self):
        out_file = os.path.join(os.path.dirname(__file__), "test2.wav")
        # this is called internally as part of preprocessing via execute method
        utt = self.tts.format_speak_tags("</speak>Hello.")
        file, _ = self.tts.get_tts(utt, out_file)
        self.assertFalse(os.path.isfile(out_file))


if __name__ == '__main__':
    unittest.main()
