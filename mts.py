operators = ["AND", "&", "∧", "OR", "|", "∨", "IMPLIES", "→", "IFF", "↔", "XOR", "⊕"]
negations = ["NOT", "~", "¬"]
ands = ["AND", "&", "∧"]
ors = ["OR", "|", "∨"]
quantifiers = ["FORALL", "∀", "EXISTS", "∃"]
functionsAndPreds = ["f", "g", "h", "i", "j", "k", "l", "m",
                     "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
res = []


def is_satisfable(clauses):
    clauses = clauses.split("AND")
    for i in range(len(clauses)):
        clauses[i] = clauses[i].split("OR")
        for j in range(len(clauses[i])):
            clauses[i][j] = clauses[i][j].strip()
    if len(clauses) < 2:
        print("SPEŁNIALNA")
    else:
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if type(resolvent(clauses[i], clauses[j])) != list:
                    continue
                elif resolvent(clauses[i], clauses[j]) is not None:
                    res2 = resolvent(clauses[i], clauses[j])
                    if len(resolvent(clauses[i], clauses[j])) == 0:
                        return False
                    else:
                        clauses.append(resolvent(clauses[i], clauses[j]))
    return True


def resolvent(c1, c2):
    for i in range(len(c1)):
        for j in range(len(c2)):
            if is_complementary(c1[i], c2[j]):
                c11 = c1[:]
                c22 = c2[:]
                c11.pop(i)
                c22.pop(j)
                res = c11 + c22
                return c11 + c22
    return False


def is_complementary(l1, l2):
    if "NOT " + l1 == l2:
        return True
    elif l1 == "NOT " + l2:
        return True
    else:
        return False


def clause_to_literals_main(clause):
    res = []

    def clause_to_literals(clause):
        # nonlocal res
        for i in clause:
            if type(i) == list:
                clause_to_literals(i)
            else:
                res.append(i)

    clause_to_literals(clause)
    return res


def onp_to_infix_clause(s):
    exp = s.split()
    stack = []
    for i in range(len(exp)):
        if exp[i] in operators:
            a = stack.pop()
            b = stack.pop()
            if exp[i] in ands:
                exp[i] = "AND"
            if exp[i] in ors:
                exp[i] = "OR"
            stack.append(b + " " + exp[i] + " " + a)

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
        elif exp[i] in quantifiers:  # Usuwa kwantyfikatory
            second = stack.pop()
            res = second
            stack.append(res)
        elif exp[i] in negations:
            exp[i] = "NOT"
            res = exp[i] + " " + stack.pop()
            stack.append(res)
        else:
            stack.append(exp[i])
    return stack.pop()


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
    clauses = onp_to_infix_clause(s)
    if is_satisfable(clauses):
        print("SPEŁNIALNA")
    else:
        print("NIESPEŁNIALNA")
    print(exp)
