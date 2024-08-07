#!/usr/bin/python3

import sys
import monkey
import yaml
import importlib

if len(sys.argv) <= 1:
    print('Please provide a package name!')
    sys.exit(1)

onStart = ''
if len(sys.argv) > 2:
    onStart = sys.argv[2]

sys.path.append(sys.argv[1])

m = importlib.import_module('src')


game = monkey.engine()
game.start(m, on_start=onStart)
game.run()
game.shutdown()

