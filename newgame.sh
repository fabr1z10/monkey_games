if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

mkdir $1
mkdir $1/src
mkdir $1/assets
cat > $1/src/__init__.py << EOF
from .factory import *
EOF

cat > $1/main.py << EOF
#!/usr/bin/python3

import monkey2

game = monkey2.game()
game.start()
game.run()
EOF
 
#cat > $1/factory.py << EOF
#def create_room(room):
#    pass
#EOF

cat > $1/settings.py << EOF
import monkey2

device_size = monkey2.IVec2(256, 240)
title = 'New game'
EOF

cat > $1/src/factory.py << EOF
import monkey2

def create_room():
    room = monkey2.Room()
    return room
EOF



chmod 755 $1/main.py
