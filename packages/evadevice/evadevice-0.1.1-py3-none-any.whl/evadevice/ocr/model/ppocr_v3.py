#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
try:
    import fastdeploy as fd
except ModuleNotFoundError as e:
    raise Exception(f"{e.args[0]}, Please run pip install fastdeploy-python -f "
                    "https://www.paddlepaddle.org.cn/whl/fastdeploy.html")


this_path = os.path.dirname(os.path.realpath(__file__))

# Detection模型, 检测文字框
det_model_file = os.path.join(this_path,
                              "ch_PP-OCRv3_det_infer", "inference.pdmodel")
det_params_file = os.path.join(this_path,
                               "ch_PP-OCRv3_det_infer", "inference.pdiparams")
# Classification模型，方向分类，可选
cls_model_file = os.path.join(this_path,
                              "ch_ppocr_mobile_v2.0_cls_infer", "inference.pdmodel")
cls_params_file = os.path.join(this_path,
                               "ch_ppocr_mobile_v2.0_cls_infer", "inference.pdiparams")
# Recognition模型，文字识别模型
rec_model_file = os.path.join(this_path,
                              "ch_PP-OCRv3_rec_infer", "inference.pdmodel")
rec_params_file = os.path.join(this_path,
                               "ch_PP-OCRv3_rec_infer", "inference.pdiparams")
rec_label_file = os.path.join(this_path, "ppocr_keys_v1.txt")


def build_option(device: str, cpu_thread_num: int, backend: str):
    """Build RuntimeOption for FastDeploy Runtime.

    :param device: Inference with CPU/Nvidia GPU.
    :param cpu_thread_num: Set number of threads if inference with CPU.
    :param backend: Use Paddle Inference backend, support inference Paddle model on CPU/Nvidia GPU.
    :return RuntimeOption.
    """

    option = fd.RuntimeOption()
    if device.lower() == "gpu":
        option.use_gpu(0)

    option.set_cpu_thread_num(cpu_thread_num)

    if backend.lower() == "trt":
        assert device.lower() == "gpu", "TensorRT backend require inference on device GPU."
        option.use_trt_backend()
    elif backend.lower() == "pptrt":
        assert device.lower() == "gpu", "Paddle-TensorRT backend require inference on device GPU."
        option.use_trt_backend()
        option.enable_paddle_trt_collect_shape()
        option.enable_paddle_to_trt()
    elif backend.lower() == "ort":
        option.use_ort_backend()
    elif backend.lower() == "paddle":
        option.use_paddle_backend()
    elif backend.lower() == "openvino":
        assert device.lower() == "cpu", "OpenVINO backend require inference on device CPU."
        option.use_openvino_backend()
    return option


runtime_option = build_option('cpu', 9, 'openvino')

det_option = runtime_option
det_option.set_trt_input_shape("x", [1, 3, 64, 64], [1, 3, 640, 640],
                               [1, 3, 960, 960])

det_model = fd.vision.ocr.DBDetector(det_model_file, det_params_file,
                                     runtime_option=det_option)

cls_option = runtime_option
cls_option.set_trt_input_shape("x", [1, 3, 48, 10], [10, 3, 48, 320],
                               [64, 3, 48, 1024])

cls_model = fd.vision.ocr.Classifier(cls_model_file, cls_params_file,
                                     runtime_option=cls_option)

rec_option = runtime_option
rec_option.set_trt_input_shape("x", [1, 3, 48, 10], [10, 3, 48, 320],
                               [64, 3, 48, 2304])

rec_model = fd.vision.ocr.Recognizer(rec_model_file, rec_params_file, rec_label_file,
                                     runtime_option=rec_option)

ppocr_v3 = fd.vision.ocr.PPOCRv3(det_model=det_model, cls_model=cls_model,
                                 rec_model=rec_model)
