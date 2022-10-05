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
import random
from os.path import join

import requests
from ovos_plugin_manager.templates.tts import TTS, TTSValidator, RemoteTTSException
from ovos_utils.log import LOG


class LarynxServerTTSPlugin(TTS):
    """Interface to Larynx TTS."""
    PUBLIC_SERVERS = ["https://larynx.2022.us",
                      "https://larynx.jarbasai.online",
                      "https://larynx.ziggyai.online"]
    voice2id = {
        'default': 'en-us/mary_ann-glow_tts',
        'bart_de_leeuw': 'nl/bart_de_leeuw-glow_tts',
        'biblia_takatifu': 'sw/biblia_takatifu-glow_tts',
        'blizzard_fls': 'en-us/blizzard_fls-glow_tts',
        'blizzard_lessac': 'en-us/blizzard_lessac-glow_tts',
        'carlfm': 'es-es/carlfm-glow_tts',
        "glados": "en-us/glados-glow_tts",
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
        self.url = config.get("host")
        self.vocoder = config.get("vocoder", "hifi_gan/vctk_small")
        self.noise = config.get("noise", 0.333)
        self.length = config.get("length", 1.0)
        self.denoiser = config.get("denoiser", 0.002)
        voice = config.get("voice", 'mary_ann')
        self.voice = self.validate_voice(voice)

    def validate_voice(self, voice):
        if voice in self.voice2id:
            voice = self.voice2id[self.voice]
        assert voice in {v for k, v in self.voice2id.items()}
        return voice

    def get_voices(self):
        url = self.url or random.choice(self.PUBLIC_SERVERS)
        url = join(url, "api", "voices")
        return requests.get(url).json()

    def get_vocoders(self):
        url = self.url or random.choice(self.PUBLIC_SERVERS)
        url = join(url, "api", "vocoders")
        return requests.get(url).json()

    def get_tts(self, sentence, wav_file, voice=None):
        """Fetch tts audio using ResponsiveVoice endpoint.

        Arguments:
            sentence (str): Sentence to generate audio for
            wav_file (str): output file path
            voice (str): voice to be used (optional, not used in mycroft-core)
        Returns:
            Tuple ((str) written file, None)
        """
        voice = voice or self.voice
        if sentence:
            urls = [self.url] if self.url else self.PUBLIC_SERVERS
            for url in urls:
                try:
                    r = requests.get(join(url, "api", "tts"),
                                     params={"text": sentence,
                                             "voice": self.validate_voice(voice),
                                             "vocoder": self.vocoder,
                                             "lengthScale": self.length,
                                             "noiseScale": self.noise,
                                             "inlinePronunciations": False,
                                             "denoiserStrength": self.denoiser})
                    if r.ok:
                        with open(wav_file, "wb") as f:
                            f.write(r.content)
                    return wav_file, None  # No phonemes
                except Exception as e:
                    LOG.error(f"failed to get TTS from {url}")

            raise RemoteTTSException("Larynx server error")

        return wav_file, None  # No phonemes

    @property
    def available_languages(self) -> set:
        """Return languages supported by this TTS implementation in this state
        This property should be overridden by the derived class to advertise
        what languages that engine supports.
        Returns:
            set: supported languages
        """
        return set(LarynxServerTTSPluginConfig.keys())


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


# TODO manually check gender of each voice and add below
LarynxServerTTSPluginConfig = {
    "de-de": [
        {'voice': 'de-de/thorsten-glow_tts', 'display_name': 'thorsten', 'gender': '', "offline": False},
        {'voice': 'de-de/karlsson-glow_tts', 'display_name': 'karlsson', 'gender': '', "offline": False},
        {'voice': 'de-de/rebecca_braunert_plunkett-glow_tts', 'display_name': 'rebecca braunert plunkett', 'gender': '', "offline": False},
        {'voice': 'de-de/eva_k-glow_tts', 'display_name': 'eva k', 'gender': '', "offline": False},
        {'voice': 'de-de/hokuspokus-glow_tts', 'display_name': 'hokuspokus', 'gender': '', "offline": False},
        {'voice': 'de-de/kerstin-glow_tts', 'display_name': 'kerstin', 'gender': '', "offline": False},
        {'voice': 'de-de/pavoque-glow_tts', 'display_name': 'pavoque', 'gender': '', "offline": False}
    ],
    "en-us": [
        {"voice": "en-us/cmu_aew-glow_tts", "speaker": "aew", "gender": "male", "offline": False},
        {"voice": "en-us/cmu_ahw-glow_tts", "speaker": "ahw", "gender": "", "offline": False},
        {"voice": "en-us/cmu_aup-glow_tts", "speaker": "aup", "gender": "", "offline": False},
        {"voice": "en-us/cmu_bdl-glow_tts", "speaker": "bdl", "gender": "male", "offline": False},
        {"voice": "en-us/cmu_clb-glow_tts", "speaker": "clb", "gender": "female", "offline": False},
        {"voice": "en-us/cmu_eey-glow_tts", "speaker": "eey", "gender": "", "offline": False},
        {"voice": "en-us/cmu_fem-glow_tts", "speaker": "fem", "gender": "", "offline": False},
        {"voice": "en-us/cmu_jmk-glow_tts", "speaker": "jmk", "gender": "", "offline": False},
        {"voice": "en-us/cmu_ksp-glow_tts", "speaker": "ksp", "gender": "male", "offline": False},
        {"voice": "en-us/cmu_ljm-glow_tts", "speaker": "ljm", "gender": "", "offline": False},
        {"voice": "en-us/cmu_lnh-glow_tts", "speaker": "lnh", "gender": "female", "offline": False},
        {"voice": "en-us/cmu_rms-glow_tts", "speaker": "rms", "gender": "male", "offline": False},
        {"voice": "en-us/cmu_rxr-glow_tts", "speaker": "rxr", "gender": "", "offline": False},
        {"voice": "en-us/cmu_slp-glow_tts", "speaker": "slp", "gender": "", "offline": False},
        {"voice": "en-us/cmu_slt-glow_tts", "speaker": "slt", "gender": "female", "offline": False},
        {"voice": "en-us/ljspeech-glow_tts", "speaker": "ljspeech", "gender": "female", "offline": False},
        {"voice": "en-us/glados-glow_tts", "speaker": "glados", "gender": "female", "offline": False},
        {"voice": "en-us/judy_bieber-glow_tts", "speaker": "judy bieber", "gender": "female", "offline": False},
        {"voice": "en-us/mary_ann-glow_tts", "speaker": "mary ann", "gender": "female", "offline": False},
        {"voice": "en-us/blizzard_fls-glow_tts", "speaker": "blizzard fls", "gender": "", "offline": False},
        {"voice": "en-us/blizzard_lessac-glow_tts", "speaker": "blizzard lessac", "gender": "", "offline": False},
        {"voice": "en-us/ek-glow_tts", "speaker": "ek", "gender": "", "offline": False},
        {"voice": "en-us/harvard-glow_tts", "speaker": "harvard", "gender": "", "offline": False},
        {"voice": "en-us/kathleen-glow_tts", "speaker": "kathleen", "gender": "", "offline": False},
        {"voice": "en-us/northern_english_male-glow_tts", "speaker": "northern english male", "gender": "male", "offline": False},
        {"voice": "en-us/southern_english_male-glow_tts", "speaker": "southern english male", "gender": "male", "offline": False},
        {"voice": "en-us/southern_english_female-glow_tts", "speaker": "southern english female", "gender": "female", "offline": False},
        {"voice": "en-us/scottish_english_male-glow_tts", "speaker": "scottish english male", "gender": "male", "offline": False}
    ],
    "es-es": [
        {"voice": "es-es/carlfm-glow_tts", "speaker": "carlfm", "gender": "", "offline": False},
        {'voice': 'es-es/karen_savage-glow_tts', 'display_name': 'karen savage', 'gender': '', "offline": False}
    ],
    "fr-fr": [
        {'voice': 'fr-fr/gilles_le_blanc-glow_tts', 'display_name': 'gilles le blanc', 'gender': '', "offline": False},
        {'voice': 'fr_fr/siwis-glow_tts', 'display_name': 'siwis', 'gender': '', "offline": False},
        {'voice': 'fr_fr/tom-glow_tts', 'display_name': 'tom', 'gender': '', "offline": False}
    ],
    "it-it": [
        {'voice': 'it-it/riccardo_fasol-glow_tts', 'display_name': 'riccardo_fasol', 'gender': '', "offline": False},
        {'voice': 'it-it/lisa-glow_tts', 'display_name': 'lisa', 'gender': '', "offline": False}
    ],
    "nl": [
        {'voice': 'nl/bart_de_leeuw-glow_tts', 'display_name': 'bart de leeuw', 'gender': '', "offline": False},
        {'voice': 'nl/flemishguy-glow_tts', 'display_name': 'flemishguy', 'gender': '', "offline": False},
        {'voice': 'nl/nathalie-glow_tts', 'display_name': 'nathalie', 'gender': '', "offline": False},
        {'voice': 'nl/rdh-glow_tts', 'display_name': 'rdh', 'gender': '', "offline": False}
    ],
    "ru-ru": [
        {'voice': 'ru-ru/hajdurova-glow_tts', 'display_name': 'hajdurova', 'gender': '', "offline": False},
        {'voice': 'ru-ru/minaev-glow_tts', 'display_name': 'minaev', 'gender': '', "offline": False},
        {'voice': 'ru-ru/nikolaev-glow_tts', 'display_name': 'nikolaev', 'gender': '', "offline": False}
    ],
    "sw": [
        {'voice': 'sw/biblia_takatifu-glow_tts', 'display_name': 'biblia takatifu', 'gender': '', "offline": False}
    ]
}
