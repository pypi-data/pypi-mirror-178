"""
Contains all models used in test and demonstration. Note that they could be written as one module, but for clarity all
 three are defined explicitly.
"""
import logging
from abc import ABC
from typing import Any, Callable, List, Optional, Tuple, Union

import numpy as np

try:
    import torch
    import torch.nn as nn
    from torch.nn import Softmax, Tanh
    from torch.optim import Optimizer
    from torch.optim.lr_scheduler import _LRScheduler
    from torch.utils.data import DataLoader, Dataset

    _TORCH_INSTALLED = True
except ImportError:
    _TORCH_INSTALLED = False

__all__ = [
    "TorchLinearRegression",
    "TorchBinaryLogisticRegression",
    "TorchNeuralNetwork",
]

logger = logging.getLogger(__name__)


class InternalDataset(Dataset):
    """
    Simple class wrapper for the data loader.
    TODO: remove it once dataset is compatible with data loaders
    """

    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def __len__(self):
        return len(self.x)

    def __getitem__(self, idx):
        return self.x[idx], self.y[idx]


class TorchModel(ABC):
    def __init__(self):
        if not _TORCH_INSTALLED:
            raise RuntimeWarning("This function requires PyTorch.")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        pass

    def fit(
        self,
        x_train: Union[np.ndarray, torch.tensor],
        y_train: Union[np.ndarray, torch.tensor],
        x_val: Union[np.ndarray, torch.tensor],
        y_val: Union[np.ndarray, torch.tensor],
        loss: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
        optimizer: Optimizer,
        scheduler: Optional[_LRScheduler] = None,
        num_epochs: int = 1,
        batch_size: int = 64,
    ):
        """
        Wrapper of pytorch fit method. It fits the model to the supplied data.
        It represents a simple machine learning loop, iterating over a number of
        epochs, sampling data with a certain batch size, calculating gradients and updating the parameters through a
        loss function.
        :param x: Matrix of shape [NxD] representing the features x_i.
        :param y: Matrix of shape [NxK] representing the prediction targets y_i.
        :param optimizer: Select either ADAM or ADAM_W.
        :param scheduler: A pytorch scheduler. If None, no scheduler is used.
        :param num_epochs: Number of epochs to repeat training.
        :param batch_size: Batch size to use in training.
        :param tensor_type: accuracy of tensors. Typically 'float' or 'long'
        """
        x_train = torch.as_tensor(x_train).clone()
        y_train = torch.as_tensor(y_train).clone()
        x_val = torch.as_tensor(x_val).clone()
        y_val = torch.as_tensor(y_val).clone()

        dataset = InternalDataset(x_train, y_train)
        dataloader = DataLoader(dataset, batch_size=batch_size)
        train_loss = []
        val_loss = []

        for epoch in range(num_epochs):
            batch_loss = []
            for train_batch in dataloader:
                batch_x, batch_y = train_batch
                pred_y = self.forward(batch_x)
                loss_value = loss(torch.squeeze(pred_y), torch.squeeze(batch_y))
                batch_loss.append(loss_value.item())

                logger.debug(f"Epoch: {epoch} ---> Training loss: {loss_value.item()}")
                loss_value.backward()
                optimizer.step()
                optimizer.zero_grad()

                if scheduler:
                    scheduler.step()
            pred_val = self.forward(x_val)
            val_loss.append(loss(torch.squeeze(pred_val), torch.squeeze(y_val)).item())
            train_loss.append(np.mean(batch_loss))
        return train_loss, val_loss

    def predict(self, x: torch.Tensor) -> np.ndarray:
        """
        Use internal model to deliver prediction in numpy.
        :param x: A np.ndarray [NxD] representing the features x_i.
        :returns: A np.ndarray [NxK] representing the predicted values.
        """
        return self.forward(x).detach().numpy()  # type: ignore

    def score(
        self,
        x: torch.Tensor,
        y: torch.Tensor,
        score: Callable[[torch.Tensor, torch.Tensor, Any], torch.Tensor],
    ) -> float:
        """
        Use internal model to measure how good is prediction through a loss function.
        :param x: A np.ndarray [NxD] representing the features x_i.
        :param y: A np.ndarray [NxK] representing the predicted target values y_i.
        :returns: The aggregated value over all samples N.
        """
        return score(self.forward(x), y).detach().numpy()  # type: ignore


class TorchLinearRegression(nn.Module, TorchModel):
    """
    A simple linear regression model (with bias) f(x)=Ax+b.
    """

    def __init__(
        self, n_input: int, n_output: int, init: Tuple[np.ndarray, np.ndarray] = None
    ):
        """
        :param n_input: input to the model.
        :param n_output: output of the model
        :param init A tuple with two matrices, namely A of shape [K, D] and b of shape [K]. If set to None Xavier
        uniform initialization is used.
        """
        super().__init__()
        self.n_input = n_input
        self.n_output = n_output
        if init is None:
            r = np.sqrt(6 / (n_input + n_output))
            init_A = np.random.uniform(-r, r, size=[n_output, n_input])
            init_b = np.zeros(n_output)
            init = (init_A, init_b)

        self.A = nn.Parameter(
            torch.tensor(init[0], dtype=torch.float64), requires_grad=True
        )
        self.b = nn.Parameter(
            torch.tensor(init[1], dtype=torch.float64), requires_grad=True
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Calculate A @ x + b using RAM-optimized calculation layout.
        :param x: Tensor [NxD] representing the features x_i.
        :returns A tensor [NxK] representing the outputs y_i.
        """
        return x @ self.A.T + self.b


class TorchBinaryLogisticRegression(nn.Module, TorchModel):
    """
    A simple binary logistic regression model p(y)=sigmoid(dot(a, x) + b).
    """

    def __init__(self, n_input: int, init: Tuple[np.ndarray, np.ndarray] = None):
        """
        :param n_input: Number of feature inputs to the BinaryLogisticRegressionModel.
        :param init A tuple representing the initialization for the weight matrix A and the bias b. If set to None
        sample the values uniformly using the Xavier rule.
        """
        super().__init__()
        self.n_input = n_input
        if init is None:
            init_A = np.random.normal(0, 0.02, size=(1, n_input))
            init_b = np.random.normal(0, 0.02, size=(1))
            init = (init_A, init_b)

        self.A = nn.Parameter(torch.tensor(init[0]), requires_grad=True)
        self.b = nn.Parameter(torch.tensor(init[1]), requires_grad=True)

    def forward(self, x: Union[np.ndarray, torch.Tensor]) -> torch.Tensor:
        """
        Calculate sigmoid(dot(a, x) + b) using RAM-optimized calculation layout.
        :param x: Tensor [NxD] representing the features x_i.
        :returns: A tensor [N] representing the probabilities for p(y_i).
        """
        x = torch.as_tensor(x)
        return torch.sigmoid(x @ self.A.T + self.b)


class TorchNeuralNetwork(nn.Module, TorchModel):
    """
    A simple fully-connected neural network f(x) model defined by y = v_K, v_i = o(A v_(i-1) + b), v_1 = x. It contains
    K layers and K - 2 hidden layers. It holds that K >= 2, because every network contains a input and output.
    """

    def __init__(
        self,
        n_input: int,
        n_output: int,
        n_neurons_per_layer: List[int],
        output_probabilities: bool = True,
        init: List[Tuple[np.ndarray, np.ndarray]] = None,
    ):
        """
        :param n_input: Number of feature in input.
        :param n_output: Output length.
        :param n_neurons_per_layer: Each integer represents the size of a hidden layer. Overall this list has K - 2
        :param output_probabilities: True, if the model should output probabilities. In the case of n_output 2 the
        number of outputs reduce to 1.
        :param init: A list of tuple of np.ndarray representing the internal weights.
        """
        super().__init__()
        self.n_input = n_input
        self.n_output = 1 if output_probabilities and n_output == 2 else n_output

        self.n_hidden_layers = n_neurons_per_layer
        self.output_probabilities = output_probabilities

        all_dimensions = [self.n_input] + self.n_hidden_layers + [self.n_output]
        layers = []
        num_layers = len(all_dimensions) - 1
        for num_layer, (in_features, out_features) in enumerate(
            zip(all_dimensions[:-1], all_dimensions[1:])
        ):
            linear_layer = nn.Linear(
                in_features, out_features, bias=num_layer < len(all_dimensions) - 2
            )

            if init is None:
                torch.nn.init.xavier_uniform_(linear_layer.weight)
                if num_layer < len(all_dimensions) - 2:
                    linear_layer.bias.data.fill_(0.01)

            else:
                A, b = init[num_layer]
                linear_layer.weight.data = A
                if num_layer < len(all_dimensions) - 2:
                    linear_layer.bias.data = b

            layers.append(linear_layer)
            if num_layer < num_layers - 1:
                layers.append(Tanh())
            elif self.output_probabilities:
                layers.append(Softmax(dim=-1))

        self.layers = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Perform forward-pass through the network.
        :param x: Tensor input of shape [NxD].
        :returns: Tensor output of shape[NxK].
        """
        return self.layers(x)
