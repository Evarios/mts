operators = ["AND", "&", "∧", "OR", "|", "∨", "IMPLIES", "→", "IFF", "↔", "XOR", "⊕"]
negations = ["NOT", "~", "¬"]
quantifiers = ["FORALL", "∀", "EXISTS", "∃"]
functionsAndPreds = ["f", "g", "h", "i", "j", "k", "l", "m",
                     "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
def onp_to_infix(s):
    exp = s.split()
    stack = []
    for i in range(len(exp)):
        if exp[i] in operators:
            a = stack.pop()
            b = stack.pop()
            stack.append("(" + b + " " + exp[i] + " " + a + ")")
        elif exp[i][0] in functionsAndPreds:
            substr = exp[i].split("/")
            res = substr[0] + "("
            parameters = []
            for j in range(int(substr[1])):
                parameters.append(stack.pop())
            for j in range(int(substr[1])):
                res += parameters.pop() + ", "
            res = res[:-2]
            res += ")"
            stack.append(res)
        elif exp[i] in quantifiers:
            second = stack.pop()
            first = stack.pop()
            res = "(" + exp[i] + " " + first + " " + second + ")"
            stack.append(res)
        elif exp[i] in negations:
            res = "(" + exp[i] + " " + stack.pop() + ")"
            stack.append(res)
        else:
            stack.append(exp[i])
    return stack.pop()


while True:
    s = input("Podaj polecenie\n")
    exp = onp_to_infix(s)
