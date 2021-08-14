from operator import *
from copy import *

def root(x,y):
    return x**(1/y)

"Equates each operator to a function. // is not floor div but a root, much in the same way ** is power"
operators = {'+':add,'-':sub,'*':mul,'/':truediv,'**':pow,'//':root}
opposite = {'+':'-','-':'+','*':'/','/':'*','**':'//','//':'**'}


class Expression(object):
    """This class allows you to represent mathematical expressions as a list of tuples that contain a value and operand."""

    "The init creates the list of operands and the set of variables"
    def __init__(self,term=None):
        self.eList=[]
        self.variables = set()
        if term:
            self + term

    "This is the function to add a new operator. Using the operators merely applies this function with the operator in question as the operator input"
    "It merely appends a tuple to eList that contains the operator and operand. If the operand is a variable or expression it adds them to the variables"
    def ApplyOperator(self,operator,operand):
        exp = self.eList
        if not (operator in list(operators.keys())):
            raise Exception("Invalid operator")
        if isinstance(operand,str):
            self.variables.add(operand)
        elif isinstance(operand,Expression):
            self.variables= self.variables.union(operand.variables)
        elif isinstance(operand,float) or isinstance(operand,int):
            operand = float(operand)
        else:
            raise Exception("Invalid operand")
        exp.append((operator,operand))
        return self

    "This goes through each instance in eList, turns variables into the value given by the input, applies itself to expressions within eList,"
    "then applies the function equavalent to the given operator to the result and the value"
    def Equate(self,**values):
        if not self.variables.issubset(set(values.keys())):
            raise Exception("Not all variables contained in values")
        result = 0
        for op in self.eList:
            operator = op[0]
            operand = op[1]
            if isinstance(operand,str):
                newOperand = values[op[1]]
            elif isinstance(operand,Expression):
                newOperand = operand.Equate(**values)
                print(operand.eList)
            elif isinstance(operand,float):
                newOperand = operand
            result = operators[operator](result,newOperand)
        return result

    def SolveforX(self,x):
        if not x in self.variables:
            raise Exception('X not in Expression')
        xEx = deepcopy(self)
        yEx = Expression()
        i=0
        while xEx.eList != Expression(x).eList:
            if i==len(self.eList)*2:
                raise Exception("Can't solve")
            operation = xEx.eList.pop()
            operator = operation[0]
            operand = operation[1]
            if operand == x or (isinstance(operand,Expression) and x in operand.variables):

                if operator in ['-','/']:
                    yEx.ApplyOperator(operator,xEx)
                    yEx.ApplyOperator({'-':'*','/':'**'}[operator],-1)
                    xEx = Expression(operand)
                elif operator in ['**','//']:
                    raise Exception("Can't solve")
                else:
                    yEx.ApplyOperator(opposite[operator],xEx)
                if isinstance(operand,Expression):
                    xEx = operand
                else:
                    xEx = Expression(operand)
            else:
                yEx.ApplyOperator(opposite[operator],operand)
            i+=1

        yEx.variables = self.variables.symmetric_difference(x)
        return yEx


    def __repr__(self):
        return str(self.eList)





    """def __str__(self):
        outstring = ''
        print('layer')
        i=0
        for op in self.eList:
            if i==0 and op[0]=='+':
                outstring += str(op[1])
                i+=1
                continue
            if isinstance(op[1],Expression):
                outstring += op[0] + str(op[1])
                i+=1
                continue
            outstring = '(' + outstring
            outstring += op[0] + str(op[1])
            outstring += ')'
            print(outstring)
            i+=1
        print('exit layer')
        return outstring"""





    "Turns operators such as +,-,*,/ into the apply operator function respectively"
    def __add__(self,operand):
        return self.ApplyOperator('+',operand)
    def __sub__(self,operand):
        return self.ApplyOperator('-',operand)
    def __mul__(self,operand):
        return self.ApplyOperator('*',operand)
    def __truediv__(self,operand):
        return self.ApplyOperator('/',operand)
    def __pow__(self,operand):
        return self.ApplyOperator('**',operand)
    def __floordiv__(self,operand):
        return self.ApplyOperator('//',operand)

V = Expression('v0')**2 + Expression(2)*'a'*'d' - Expression('v')**2

print(V.SolveforX('d').variables)
