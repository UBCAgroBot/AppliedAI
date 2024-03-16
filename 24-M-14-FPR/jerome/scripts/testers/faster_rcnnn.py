import sys
PROJECT_ROOT = '/Users/jeromecho/Library/CloudStorage/OneDrive-Personal/ML/AppliedAI/24-M-14-FPR/jerome/'
sys.path.append(PROJECT_ROOT)

from scripts.helpers.engine import train_one_epoch, evaluate
from scripts.data.augmentations import get_transform
from scripts.data.xml_dataset import XMLDatasetPyTorch
from scripts.models import frcnn
from scripts.helpers import utils
from scripts.config.config import TEST_DIR, NUM_CORES
import torch

ACCURACY_THRESHOLD = 0.5
MODEL_NAME = 'saved_models/model_frcnn_32.pth'
device = torch.device('cpu')
num_classes = 3

def evaluate_frcnn():
  model = frcnn.get_model(num_classes)
  model.to(device)
  model.load_state_dict(torch.load(MODEL_NAME, map_location=torch.device('cpu')))
  model.eval()

  RANDOM_SEED = 42
  torch.manual_seed(RANDOM_SEED)

  dataset_test = XMLDatasetPyTorch(TEST_DIR, get_transform(train=False))

  data_loader_test = torch.utils.data.DataLoader(
  dataset_test,
  batch_size=1,
  shuffle=False,
  num_workers=NUM_CORES, 
  collate_fn=utils.collate_fn
  )

  evaluate(model, data_loader_test, device=device)
