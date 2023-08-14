# this script is about creating neuro from scratch
# @author: Xiekang
import math
import sys
# ! placeholder -> do it later
Matrix = str
ActivationFunction = str

def neuro(neuro_input: float, activation_function: str, parameter: float = 0.0) -> float:
    match activation_function.lower():
        case "linear": return neuro_input
        case "binary": return 0 if neuro_input < 0 else 1
        case "sigmoid": return 1/(1+math.exp(-neuro_input))
        case "tanh": return math.tanh(neuro_input)
        case "arctan": return 1/math.tan(neuro_input)
        case "relu": return 0 if neuro_input < 0 else neuro_input
        case "prelu": 
            prelu = lambda p, x: p*x  
            return prelu(parameter, neuro_input) if neuro_input < 0 else neuro_input
        case "elu":
            elu = lambda p, x: p * (math.exp(x) - 1)
            return elu(parameter, neuro_input) if neuro_input < 0 else neuro_input
        case "softplus": return math.log1p(1+math.exp(neuro_input))
        case _:
            print("Does not support given activation function", file=sys.stderr)
    return 0.0