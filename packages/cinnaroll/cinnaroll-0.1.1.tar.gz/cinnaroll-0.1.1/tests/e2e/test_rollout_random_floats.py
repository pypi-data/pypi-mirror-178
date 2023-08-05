import json
from pathlib import Path
from unittest import mock
from unittest.mock import MagicMock

import numpy as np
import pytest
import torch
from typing import Any, Dict, Union

from cinnaroll_internal.constants import KERAS, PYTORCH
from cinnaroll_internal.rollout_config import RolloutConfig
from cinnaroll_internal.rollout import rollout
from cinnaroll_internal.utils import clean_path

from tests.unit.model_utils import generate_random_data
from tests.unit.tf_model_utils import create_keras_model_object
from tests.unit.pytorch_model_utils import create_pytorch_model_object


INPUT_DIM = np.random.randint(5, 10)
NUM_SAMPLES = 13


class MyRolloutConfigKeras(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> Dict[str, float]:
        X, Y = generate_random_data(NUM_SAMPLES, INPUT_DIM)
        model_object.fit(X, Y, epochs=5, verbose=2)

        accuracy = model_object.evaluate(X, Y, verbose=2)
        metrics = {"dataset": "random_floats", "accuracy": accuracy}
        return metrics

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        X = np.array(json.loads(input_data)).reshape(1, -1)
        Y = model_object.predict(X, verbose=2)
        output = {"output": Y.item()}

        return json.dumps(output)


class MyRolloutConfigKerasInferOnly(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> Dict[str, float]:
        pass

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        X = np.array(json.loads(input_data)).reshape(1, -1)
        Y = model_object.predict(X, verbose=2)
        output = {"output": Y.item()}

        return json.dumps(output)


class MyRolloutConfigPyTorch(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> Dict[str, Union[str, float]]:
        X, Y = generate_random_data(NUM_SAMPLES, INPUT_DIM)
        model_object.perform_training(torch.Tensor(X), torch.Tensor(Y), num_epochs=5)

        loss = model_object.compute_loss(torch.Tensor(X), torch.Tensor(Y))
        metrics = {"dataset": "random_floats", "loss": loss.item()}
        return metrics

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        X = torch.Tensor(np.array(json.loads(input_data)).reshape(1, -1))
        Y = model_object(X)
        output = {"output": Y.item()}

        return json.dumps(output)


class MyRolloutConfigPyTorchInferOnly(RolloutConfig):
    @staticmethod
    def train_eval(model_object: Any) -> Dict[str, Union[str, float]]:
        pass

    @staticmethod
    def infer(model_object: Any, input_data: str) -> str:
        X = torch.Tensor(np.array(json.loads(input_data)).reshape(1, -1))
        Y = model_object(X)
        output = {"output": Y.item()}

        return json.dumps(output)


def get_rollout_config(framework: str, infer_only: bool) -> RolloutConfig:
    # generate random input to the model
    model_input_sample = generate_random_data(1, INPUT_DIM)[0]
    infer_func_input_sample = json.dumps(model_input_sample.tolist())

    dense_layers = (8, 1)

    if framework == KERAS:
        model_object = create_keras_model_object(INPUT_DIM, dense_layers)
    elif framework == PYTORCH:
        model_object = create_pytorch_model_object(INPUT_DIM, dense_layers)
    else:
        raise RuntimeError(f"Unsupported framework: {framework}")

    kwargs_template = {
        "project_id": "my_project_id",
        "model_object": model_object,
        "infer_func_input_format": "json",
        "infer_func_output_format": "json",
        "infer_func_input_sample": infer_func_input_sample,
    }

    if framework == KERAS:
        kwargs = {**kwargs_template, **{"model_input_sample": model_input_sample}}
        if infer_only:
            return MyRolloutConfigKerasInferOnly(**kwargs)
        else:
            return MyRolloutConfigKeras(**kwargs)
    elif framework == PYTORCH:
        kwargs = {
            **kwargs_template,
            **{"model_input_sample": torch.Tensor(model_input_sample)},
        }
        if infer_only:
            return MyRolloutConfigPyTorchInferOnly(**kwargs)
        else:
            return MyRolloutConfigPyTorch(**kwargs)
    else:
        raise RuntimeError(f"Unsupported framework: {framework}")


class TestRandomFloats:
    @staticmethod
    @pytest.mark.parametrize("framework", (KERAS, PYTORCH))
    @pytest.mark.parametrize("infer_only", (True, False))
    @mock.patch("cinnaroll_internal.rollout.get_cache_dir_path")
    def test_rollout_config(
        mock_get_cache_dir_path: MagicMock, framework: str, infer_only: bool
    ) -> None:
        cache_dir_path = Path(__file__).parent / "tmp"
        clean_path(cache_dir_path, True)
        mock_get_cache_dir_path.return_value = cache_dir_path

        rollout_config = get_rollout_config(framework, infer_only)
        rollout(rollout_config)
