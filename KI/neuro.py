# this script is about creating neuro from scratch
# @author: Xiekang
import math
import sys
import random

# ! placeholder -> do it later
Matrix = str
ActivationFunction = str


def neuro(
    neuro_input: float, activation_function: str = "linear", parameter: float = 0.0
) -> float:
    match activation_function.lower():
        case "linear":
            return neuro_input
        case "binary":
            return 0 if neuro_input < 0 else 1
        case "sigmoid":
            return 1 / (1 + math.exp(-neuro_input))
        case "tanh":
            return math.tanh(neuro_input)
        case "arctan":
            return 1 / math.tan(neuro_input)
        case "relu":
            return 0 if neuro_input < 0 else neuro_input
        case "prelu":
            prelu = lambda p, x: p * x
            return prelu(parameter, neuro_input) if neuro_input < 0 else neuro_input
        case "elu":
            elu = lambda p, x: p * (math.exp(x) - 1)
            return elu(parameter, neuro_input) if neuro_input < 0 else neuro_input
        case "softplus":
            return math.log1p(1 + math.exp(neuro_input))
        case _:
            print("Does not support given activation function", file=sys.stderr)
    return -100.0


def neural_network(
    input_values: list,
    hidden_layers_with_neuro_number: list,
    neuro_output_layer: int = 1,
    weight_split_method: str = "evenly",
) -> list[float]:
    number_of_neuro_in_input_layer = len(input_values)
    weights = []
    for _ in range(number_of_neuro_in_input_layer):
        weight = []
        for hidden_layers_input in hidden_layers_with_neuro_number:
            if weight_split_method == "evenly":
                weight = [1 / hidden_layers_input] * hidden_layers_input
            elif weight_split_method == "randomly":
                weight = [random.random() for _ in range(hidden_layers_input)]
                s = sum(weight)
                weight = [w/s for w in weight]
            else:
                raise RuntimeError("no support weight split method!")
        weights.append(weight)
    return weights


if __name__ == "__main__":
    """print(neuro(0.5, "linear"))
    print(neuro(0.5, "binary"))
    print(neuro(0.5, "sigmoid"))
    print(neuro(0.5, "tanh"))
    print(neuro(0.5, "arctan"))
    print(neuro(0.5, "relu"))
    print(neuro(0.5, "prelu", 0.3))
    print(neuro(0.5, "elu", 0.12))
    print(neuro(0.5, "softplus"))
    print(neuro(0.5, "bbbbbbbb"))"""
    print(sys.float_info)
    print(neural_network([0.5, 0.5], [3], weight_split_method="bbbbb"))
