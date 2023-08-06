from typing import Callable, Optional, Union
from importlib.resources import open_binary
from zipfile import ZipFile
import torch
from torchvision.datasets import CIFAR10, CIFAR100
from .utils import random_noisify, transition_matrix


__all__ = ['NoisyCIFAR10', 'NoisyCIFAR100']


def _load_cifar_n(dataset: str, noise_level: str):
    key = {
        'CIFAR-10': {
            'clean': 'clean_label',
            'aggregate': 'aggre_label',
            'random1': 'random_label1',
            'random2': 'random_label2',
            'random3': 'random_label3',
            'worst': 'worse_label',
        },
        'CIFAR-100': {
            'clean': 'clean_label',
            'noisy': 'noisy_label',
        }
    }[dataset][noise_level]

    with ZipFile(open_binary(__package__, 'CIFAR-N.zip')) as zipfile:
        with zipfile.open(f'CIFAR-N/{dataset}_human.pt') as file:
            return torch.load(file)[key]


class NoisyCIFAR10(CIFAR10):
    def __init__(
        self,
        root: str,
        noise_type: str,
        noise_level: Union[float, str],
        random_seed: int = 0,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        download: bool = False,
    ):
        super().__init__(
            root,
            train=True,
            transform=transform,
            target_transform=target_transform,
            download=download
        )
        self.noise_type = noise_type
        self.noise_level = noise_level
        self.random_seed = random_seed

        if noise_type == 'human':
            self.targets = _load_cifar_n('CIFAR-10', noise_level)
        else:
            T = transition_matrix('CIFAR10', noise_type, noise_level)
            self.targets = random_noisify(self.targets, T, random_seed)


class NoisyCIFAR100(CIFAR100):
    def __init__(
        self,
        root: str,
        noise_type: str,
        noise_level: Union[float, str],
        random_seed: int = 0,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        download: bool = False,
    ):
        super().__init__(
            root,
            train=True,
            transform=transform,
            target_transform=target_transform,
            download=download
        )
        self.noise_type = noise_type
        self.noise_ratio = noise_level
        self.random_seed = random_seed

        if noise_type == 'human':
            self.targets = _load_cifar_n('CIFAR-100', noise_level)
        else:
            T = transition_matrix('CIFAR100', noise_type, noise_level)
            self.targets = random_noisify(self.targets, T, random_seed)
