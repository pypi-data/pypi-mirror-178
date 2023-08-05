#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   tflite_detection.py
@Time    :   2022/11/23 16:34:58
@Author  :   Moyan 
'''
import sys
sys.path.insert(0, "D:\Code\AI-in-air\moyan\test")


import numpy as np
from abc import abstractmethod
from TFLite import TFLiteModel

class DetectModel(TFLiteModel):
    def __init__(self, model_path: str) -> None:
        super().__init__(model_path)
        pass
    
    @abstractmethod
    def preprocess(self):
        pass

    @abstractmethod
    def postprocess(self):
        pass
    
    def run(self, x:np.ndarray):
        input_tensor = self.preprocess(x)
        output_tensor = self.forward(input_tensor)
        return self.postprocess(output_tensor)

