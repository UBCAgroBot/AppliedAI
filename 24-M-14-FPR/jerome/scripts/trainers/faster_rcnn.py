from scripts.helpers.engine import train_one_epoch, evaluate
from scripts.data.augmentations import get_transform
from scripts.data.xml_dataset import XMLDatasetPyTorch
from scripts.models.frcnn import get_model
from scripts.helpers import utils
import torch
from tqdm import tqdm

def train_and_evaluate_frcnn():
    # MPS issues
    # device = torch.device('mps') if torch.backends.mps.is_available() else torch.device('cpu')
    device = torch.device('cpu')
    RANDOM_SEED = 42
    torch.manual_seed(RANDOM_SEED)

    num_classes = 3
    dataset = XMLDatasetPyTorch('data/blueberries/all_data', get_transform(train=True))
    # TODO - make 3 folders - train, test, valid. Randomly split XML + Image pairs into those folders via 
    #        a python script 
    dataset_test = XMLDatasetPyTorch('data/blueberries/all_data', get_transform(train=False))

    data_loader_train = torch.utils.data.DataLoader(
      dataset,
      batch_size=2,
      shuffle=True,
      num_workers=0,
      collate_fn=utils.collate_fn
    )

    data_loader_test = torch.utils.data.DataLoader(
      dataset_test,
      batch_size=1,
      shuffle=False,
      num_workers=0, 
      collate_fn=utils.collate_fn
    )

    model = get_model(num_classes)

    model.to(device)

    params = [p for p in model.parameters() if p.requires_grad]

    optimizer = torch.optim.Adam(
      params,
      lr=0.005,
      betas=(0.9, 0.99),
      weight_decay=0 # e.g., the lambda term used in L1 and L2 regularization
    )

    lr_scheduler = torch.optim.lr_scheduler.StepLR(
            optimizer,
            step_size=3,
            gamma=0.1 # every 3 epochs, multiple currently learning rate by 0.1
    )

    num_epochs = 20

    print(f'--- TRAINING ALL EPOCHS ---')

    for epoch in tqdm(range(num_epochs)):
        print(f"--- TRAINING EPOCH {epoch} ---")
        train_one_epoch(model, optimizer, data_loader_train, device, epoch, print_freq=10)
        lr_scheduler.step()
        print(f'--- EVAULATING MODEL FOR EPOCH {epoch} ----')
        evaluate(model, data_loader_test, device=device)

    print(f'--- SAVING THE MODEL ---')
    torch.save(model.state_dict(), './saved_models/model_frcnn.pth')

    # TODO: 
    # 2. Finish PyTorch workflow - train quickly on local machine
    # 3. Build a Tensorflow dataset based on torch dataset

