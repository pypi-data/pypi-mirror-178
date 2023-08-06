class IterableProcessor:

    @staticmethod
    def can(obj, **kwarg):
        from collections.abc import Iterable
        return isinstance(obj, Iterable)
    
    @staticmethod
    def describe(obj, **kwarg):
        import pandas as pd
        x = pd.Series(obj)
        return x

class DoubleIterableProcessor:

    @staticmethod
    def can(obj, **kwarg):
        return IterableProcessor.can(obj) and IterableProcessor.can(next(iter(obj)))
    
    @staticmethod
    def describe(obj, **kwarg):
        import pandas as pd
        x = pd.DataFrame(obj)
        return x


class PytorchModuleProcessor:

    @staticmethod
    def can(obj, **kwargs):
        import torch.nn as nn
        return issubclass(type(obj), nn.Module)
    
    @staticmethod
    def describe(obj, **kwargs):
        import torch
        print("Warn: Using simple Pytorch processor, please use kwarg 'input_size' for rich information")
        print(obj)


class PyTorchRichModuleProcessor:
    
    @staticmethod
    def can(obj, **kwargs):
        import torch.nn as nn
        return issubclass(type(obj), nn.Module) and "input_size" in kwargs
    
    @staticmethod
    def describe(obj, **kwargs):
        from torchinfo import summary
        summary(model, **kwargs)


PROCESSORS = [
    PyTorchRichModuleProcessor,
    PytorchModuleProcessor,
    DoubleIterableProcessor,
    IterableProcessor
]


def what(obj, *args, **kwarg):

    print(f"Processing type {type(obj)}")
    for processor in PROCESSORS:
        if processor.can(obj):
            return(processor.describe(obj, *args, **kwarg))
            break
    else:
        print(f"Couldn't figure out what {obj} is")
        return obj.__repr__()


if __name__ == "__main__":
    print(what([1, 2, 3]))
    print(what([[1, 2, 3], [4, 7, 8]]))
