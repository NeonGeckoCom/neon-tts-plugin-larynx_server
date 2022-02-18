# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from os.path import join

import requests
from ovos_plugin_manager.templates.tts import TTS, TTSValidator
from neon_utils.parse_utils import format_speak_tags


class LarynxServerTTSPlugin(TTS):
    """Interface to Larynx TTS."""
    voice2id = {'bart_de_leeuw': 'nl/bart_de_leeuw-glow_tts',
                'biblia_takatifu': 'sw/biblia_takatifu-glow_tts',
                'blizzard_fls': 'en-us/blizzard_fls-glow_tts',
                'blizzard_lessac': 'en-us/blizzard_lessac-glow_tts',
                'carlfm': 'es-es/carlfm-glow_tts',
                'cmu_aew': 'en-us/cmu_aew-glow_tts',
                'cmu_ahw': 'en-us/cmu_ahw-glow_tts',
                'cmu_aup': 'en-us/cmu_aup-glow_tts',
                'cmu_bdl': 'en-us/cmu_bdl-glow_tts',
                'cmu_clb': 'en-us/cmu_clb-glow_tts',
                'cmu_eey': 'en-us/cmu_eey-glow_tts',
                'cmu_fem': 'en-us/cmu_fem-glow_tts',
                'cmu_jmk': 'en-us/cmu_jmk-glow_tts',
                'cmu_ksp': 'en-us/cmu_ksp-glow_tts',
                'cmu_ljm': 'en-us/cmu_ljm-glow_tts',
                'cmu_lnh': 'en-us/cmu_lnh-glow_tts',
                'cmu_rms': 'en-us/cmu_rms-glow_tts',
                'cmu_rxr': 'en-us/cmu_rxr-glow_tts',
                'cmu_slp': 'en-us/cmu_slp-glow_tts',
                'cmu_slt': 'en-us/cmu_slt-glow_tts',
                'ek': 'en-us/ek-glow_tts',
                'eva_k': 'de-de/eva_k-glow_tts',
                'flemishguy': 'nl/flemishguy-glow_tts',
                'gilles_le_blanc': 'fr-fr/gilles_le_blanc-glow_tts',
                'hajdurova': 'ru-ru/hajdurova-glow_tts',
                'harvard': 'en-us/harvard-glow_tts',
                'hokuspokus': 'de-de/hokuspokus-glow_tts',
                'judy_bieber': 'en-us/judy_bieber-glow_tts',
                'karen_savage': 'es-es/karen_savage-glow_tts',
                'karlsson': 'de-de/karlsson-glow_tts',
                'kathleen': 'en-us/kathleen-glow_tts',
                'kerstin': 'de-de/kerstin-glow_tts',
                'lisa': 'it-it/lisa-glow_tts',
                'ljspeech': 'en-us/ljspeech-glow_tts',
                'mary_ann': 'en-us/mary_ann-glow_tts',
                'minaev': 'ru-ru/minaev-glow_tts',
                'nathalie': 'nl/nathalie-glow_tts',
                'nikolaev': 'ru-ru/nikolaev-glow_tts',
                'northern_english_male': 'en-us/northern_english_male-glow_tts',
                'pavoque': 'de-de/pavoque-glow_tts',
                'rdh': 'nl/rdh-glow_tts',
                'rebecca_braunert_plunkett': 'de-de/rebecca_braunert_plunkett-glow_tts',
                'riccardo_fasol': 'it-it/riccardo_fasol-glow_tts',
                'scottish_english_male': 'en-us/scottish_english_male-glow_tts',
                'siwis': 'fr-fr/siwis-glow_tts',
                'southern_english_female': 'en-us/southern_english_female-glow_tts',
                'southern_english_male': 'en-us/southern_english_male-glow_tts',
                'talesyntese': 'sv-se/talesyntese-glow_tts',
                'thorsten': 'de-de/thorsten-glow_tts',
                'tom': 'fr-fr/tom-glow_tts'}

    def __init__(self, lang="en-us", config=None):
        config = config or {"lang": lang,
                            "pitch": 0.5,
                            "rate": 0.5,
                            "vol": 1}
        super(LarynxServerTTSPlugin, self).__init__(
            lang, config, LarynxServerTTSPluginValidator(self), 'wav')
        self.url = config.get("host", "http://tts.neon.ai")
        self.vocoder = config.get("vocoder", "hifi_gan/vctk_small")
        self.noise = config.get("noise", 0.333)
        self.length = config.get("length", 1.0)
        self.denoiser = config.get("denoiser", 0.002)
        self.voice = config.get("voice", 'mary_ann')
        if self.voice in self.voice2id:
            self.voice = self.voice2id[self.voice]

    def get_voices(self):
        url = join(self.url, "api", "voices")
        return requests.get(url).json()

    def get_vocoders(self):
        url = join(self.url, "api", "vocoders")
        return requests.get(url).json()

    def get_tts(self, sentence, wav_file):
        """Fetch tts audio using ResponsiveVoice endpoint.

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
        Returns:
            Tuple ((str) written file, None)
        """
        sentence = format_speak_tags(sentence, False)
        if not sentence:
            return wav_file, None
        url = join(self.url, "api", "tts")
        wav = requests.get(url,
                           params={"text": sentence,
                                   "voice": self.voice,
                                   "vocoder": self.vocoder,
                                   "lengthScale": self.length,
                                   "noiseScale": self.noise,
                                   "inlinePronunciations": False,
                                   "denoiserStrength": self.denoiser}).content
        with open(wav_file, "wb") as f:
            f.write(wav)
        return wav_file, None  # No phonemes


class LarynxServerTTSPluginValidator(TTSValidator):
    def __init__(self, tts):
        super(LarynxServerTTSPluginValidator, self).__init__(tts)

    def validate_lang(self):
        pass

    def validate_voice(self):
        pass

    def validate_connection(self):
        pass

    def get_tts_class(self):
        return LarynxServerTTSPlugin
