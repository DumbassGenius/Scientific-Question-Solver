def root(x,y):
    return x**(1/y)


operators = {'+':add,'-':sub,'*':mul,'/':truediv,'**':pow,'//':root}



class Expression(object):
    """docstring for Equation."""

    def __init__(self,term=None):
        if term:
            self.eList=[('+',term)]
            self.variables = {term}
        else:
            self.eList=[]
            self.variables = set()

    def ApplyOperator(self,operator,operand):
        exp = self.eList
        if not (operator in list(operators.keys())):
            raise Exception("Invalid operator")
        if isinstance(operand,str):
            self.variables.add(operand)
        elif isinstance(operand,Expression):
            self.variables.add(operand.variables)
        else:
            operand = float(operand)
        exp.append((operator,operand))
        return self

    def Equate(self,**values):
        if not self.variables.issubset(set(values.keys())):
            raise Exception("Not all variables contained in values")
        result = 0
        for op in self.eList:
            if isinstance(op[1],str):
                operand = values[op[1]]
            elif isinstance(op[1],Expression):
                operand = op[1].Equate(**values)
            elif isinstance(op[1],int):
                operand = op[1]



    def __add__(self,operand):
        return self.ApplyOperator('+',operand)
    def __sub__(self,operand):
        return self.ApplyOperator('-',operand)
    def __mul__(self,operand):
        return self.ApplyOperator('*',operand)
    def __div__(self,operand):
        return self.ApplyOperator('/',operand)
    def __pow__(self,operand):
        return self.ApplyOperator('**',operand)
    def __truediv__(self,operand):
        return self.ApplyOperator('//',operand)



# ax^3-bx^2 +cx-6

a = Expression('x')+'y'
print({'x', 'y'}=={'x', 'y'})

print(a.Equate(x=1,y=2))
