## Description

TTS plugin for [Larynx](https://github.com/rhasspy/larynx)

## Install

`pip install neon-tts-plugin-larynx-server`

## Configuration


```json
  "tts": {
    "module": "neon-tts-plugin-larynx-server",
    "neon-tts-plugin-larynx-server": {
      "host": "http://138.68.25.242:5002",
      "voice": "mary_ann",
      "vocoder": "hifi_gan/vctk_small"
    }
 }
```

:warning: depending on where larynx is hosted different voices and vocoders 
might be available, see below for default list

- `host` - url where larynx is running
- `voice` - additional voices can be downloaded in the web interface, default `mary_ann`
- `vocoder` -  recommend using `hifi_gan/vctk_small` for performance reasons, other options are `hifi_gan/universal_medium` and `hifi_gan/universal_large`
- `noise` - Volatility of speaker (0-1, default: 0.333)
- `denoiser` - Strength of vocoder denoiser (0-1, 0 is disabled)
- `length` - Speed of speaker (default: 1.0, faster < 1 < slower)


### Voices

the config will accept either the name or voice_id

```
{'bart_de_leeuw': 'nl/bart_de_leeuw-glow_tts',
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
```
