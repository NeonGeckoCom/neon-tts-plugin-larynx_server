#!/usr/bin/env python3
from setuptools import setup

PLUGIN_ENTRY_POINT = 'neon-tts-plugin-larynx-server = ' \
                     'neon_tts_plugin_larynx_server:LarynxServerTTSPlugin'
setup(
    name='neon-tts-plugin-larynx-server',
    version='0.0.1',
    description='Larynx tts plugin for OVOS / Neon / Mycroft',
    url='https://github.com/NeonJarbas/neon-tts-plugin-larynx-server',
    author='JarbasAi',
    author_email='jarbasai@mailfence.com',
    license='Apache-2.0',
    packages=['neon_tts_plugin_larynx_server'],
    install_requires=["requests",
                      'ovos-plugin-manager>=0.0.1a7'],
    zip_safe=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='mycroft ovos neon plugin tts',
    entry_points={'mycroft.plugin.tts': PLUGIN_ENTRY_POINT}
)
