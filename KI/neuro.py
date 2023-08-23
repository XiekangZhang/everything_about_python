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
            """for _ in range(10):
                with open("text.txt", "a") as f:
                    print("bsljdfaslkfjlsjfdsklajfslf", file=f)"""
    return -100.0


def neural_network(
    input_values: list,
    hidden_layers_with_neuro_number: list,  # ! first focus on 1 hidden layer --> [3] --> 1 hidden layer + 3 neuros
    # ! [3, 2] --> 2 hidden layers --> 3 neuros, 2 neuros
    neuro_output_layer: int = 1,  # ! based on problem
    weight_split_method: str = "evenly", # ! Sepration of the weights
    **kwargs # ! unlimted parameters (key = value)
) -> list[float]:
    number_of_neuro_in_input_layer = len(input_values)
    weights = []
    # * define weights based on each neuro
    for _ in range(number_of_neuro_in_input_layer):
        weight = []
        for hidden_layers_input in hidden_layers_with_neuro_number:
            if weight_split_method == "evenly":
                weight = [1 / hidden_layers_input] * hidden_layers_input
            elif weight_split_method == "randomly":
                weight = [random.random() for _ in range(hidden_layers_input)]
                s = sum(weight)
                weight = [w / s for w in weight]
            else:
                raise RuntimeError("no support weight split method!")
        weights.append(weight)

    # * matrix multiple
    hidden_layers_input_values = []
    for index in range(len(weights[0])):
        hidden_layers_input_value = []
        for w in weights:
            hidden_layers_input_value.append(w[index])
        hidden_layers_input_values.append(
            sum([i * w for i, w in zip(input_values, hidden_layers_input_value)])
        )

    # * output
    hidden_layers_output_values = []
    for value in hidden_layers_input_values:
        hidden_layers_output_values.append(neuro(value))
    return hidden_layers_output_values


if __name__ == "__main__":
    """print(neuro(0.5))
    print(neuro(0.5, "binary"))
    print(neuro(0.5, "sigmoid"))
    print(neuro(0.5, "tanh"))
    print(neuro(0.5, "arctan"))
    print(neuro(0.5, "relu"))
    print(neuro(0.5, "prelu", 0.3))
    print(neuro(0.5, "elu", 0.12))
    print(neuro(0.5, "softplus"))
    print(neuro(0.03, parameter=0.78, activation_function="bbbbb"))"""
    # print(neuro(0.5, "bbbbbbbb"))
    # print(sys.float_info)
    print(neural_network([0.5, 0.5], [2], weight_split_method="randomly"))
