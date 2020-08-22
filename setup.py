#!/usr/bin/env python

from distutils.core import setup

setup(
    name="wither",
    version="1.0",
    description="Wither",
    author="Johan du Plessis",
    author_email="johandp92@gmail.com",
    packages=["wither", "wither.open_weather_map", "wither.config",],
)
