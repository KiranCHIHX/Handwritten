#####################################################################
# Copyright(C), 2022 IHX Private Limited. All Rights Reserved
# Unauthorized copying of this file, via any medium is
# strictly prohibited
#
# Proprietary and confidential
# email: care@ihx.in
#####################################################################

import time
from datetime import datetime

import numpy as np


from PIL import Image
import torch
from torch import nn
from efficientnet_pytorch import EfficientNet
import torch.nn.functional as F
from albumentations.pytorch import ToTensorV2
from albumentations import Compose, Resize, ToFloat


from app.core import logger
from app.core.config import cfg
from app.utils import utilities as U
from app.utils import constants as C

int_to_class = {0: "Handwritten", 1: "printed"}

# from app.controllers.AI.LMLayout import preprocess as MP
# from app.controllers.AI.LMLayout import postprocess as MPO

_response = {"prob": 0.0, "is_hw": False, "Model_Version": "1.0.0"}


class HWClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = EfficientNet.from_pretrained("efficientnet-b2")
        # 1280 is the number of neurons in last layer. is diff for diff. architecture
        self.dense_output = nn.Linear(1408, 2)

    def forward(self, x):
        feat = self.model.extract_features(x)
        feat = F.avg_pool2d(feat, feat.size()[2:]).reshape(-1, 1408)
        return self.dense_output(feat)


class HWClassifierModel:
    def __init__(self):
        self.model = self.load_model()
        self.img_size = 512
        self.AUGMENTATIONS = Compose(
            [
                Resize(self.img_size, self.img_size, p=1),
                ToFloat(max_value=255),
                ToTensorV2(),
            ],
            p=1,
        )

    def load_model(self):
        model = HWClassifier()

        model_dict = torch.load(
            cfg.models.Classifier.model_path,
            map_location="cpu",
        )["model_state_dict"]
        model.load_state_dict(model_dict)
        model.to(C.DEVICE)
        model.eval()
        return model

    def predict(self, trxId: str, image_path: str):
        print("retreiving predictions...")
        start_ts = datetime.now()
        start_time = time.time()
        logger.info(f"{U.set_log_prefix(trxid = trxId)} - Begin prediction -> {start_ts}")

        im = np.array(Image.open(image_path))
        img_tensor = self.AUGMENTATIONS(image=im)

        out = self.model(
            img_tensor["image"].unsqueeze(0).to(C.DEVICE),
        )
        out = torch.nn.functional.softmax(out, dim=1)
        out = out.cpu().detach().numpy()

        prob = np.max(out)

        img_typ = int_to_class[np.argmax(out)]

        resp = _response.copy()
        resp["prob"] = prob

        if img_typ == "Handwritten":
            resp["is_hw"] = True
        else:
            resp["is_hw"] = False

        resp["Model_Version"] = cfg.models.Classifier.model_version

        print("retrieved predictions!", resp)
        logger.info(f"{U.set_log_prefix(trxid = trxId)} - Prediction -> {resp}")
        logger.info(
            f"{U.set_log_prefix(trxid = trxId)} - Completed prediction -> {datetime.now()} -> Time Take {time.time() - start_time}"
        )
        return resp
