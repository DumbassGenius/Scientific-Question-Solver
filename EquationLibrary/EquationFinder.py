from EquationScripts.Expression_Class import Expression



def FindX(x,lib,knowns):
    print(x,lib)
    assignedVars = {}
    found = True
    while found:
        print('once')
        found = False

        for i in range(len(lib)):
            print(lib[i])
            exp = lib[i]
            vars = exp.variables
            if vars.symmetric_difference(x).issubset(knowns):
                return exp.substitudeVars(**assignedVars).SolveforX(x)
            else:
                for var in vars.symmetric_difference(x):
                    newKnown = FindX(var,lib[i+1:],knowns)
                    if newKnown:
                        print('Found',var)
                        found = True
                        knowns.append(var)
                        assignedVars[var] = newKnown


    return False



testLib = []

testLib.append(Expression('x')-'b'-'c')
testLib.append(Expression('c')-'b'-'d')

print(FindX('x',testLib,['b','z']))
