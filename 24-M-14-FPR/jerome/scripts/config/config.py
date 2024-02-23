CLASSES = {
  "background": 0,
  "green": 1, 
  "unripe": 1, 
  "half": 1,   # half-ripe
  "immature": 1,
  "ripe": 2,
}

CLASS_CODES_MAP = [
  'background', # 0 => background
  'unripe',     # 1 => unripe
  'ripe',       # 2 => ripe
]

TRAIN_DIR = 'data/blueberries/train'
TEST_DIR = 'data/blueberries/test'
VALIDATE_DIR = 'data/blueberries/validate'