 

import re

END_WITH_SEMICOLON = ";$"
START_WITH_CHARACTER = "^[a-zA-Z]"
HAS_ASSIGNMENT_SIGNAL = "^[a-zA-Z]=.+;$"
IS_VARIABLE = "[a-zA-Z]"
IS_VALUE = "[0-9]"
ASSIGNMENT_CORRECT = "^[a-zA-Z][=]([a-zA-Z]|[0-9]+[+,*][a-zA-Z]|[0-9]+)([+,*]([a-zA-Z]|[0-9]+))*;"
CONSOLE_REGEX = "^[a-zA-Z];"


class Interp:
    def __init__(self):
        self.env = {}
        self.stack = []
        self.pos = 0
        self.addPending = False
        
    
    def pushValue(self, line):
        valueToPush = 0
        if self.pos >= len(line): raise Exception('Fim de entrada inesoperada.')
        if re.findall(IS_VARIABLE, line[self.pos]):
            valueOfVariable = self.env.get(line[self.pos])

            if not valueOfVariable: 
                expMessage = "{} is not defined at '{}' column {}" 
                raise Exception(expMessage.format(line[self.pos], line ,self.pos))
        
            self.stack.append(valueOfVariable)
            self.pos += 1
            return
        if re.findall(IS_VALUE, line[self.pos]):
            while self.pos < len(line) and re.findall(IS_VALUE, line[self.pos]):
                valueToPush = valueToPush*10 + int(line[self.pos])
                self.pos +=1
            self.stack.append(valueToPush)

            return 
        raise Exception('Valor inesperado em {}:{}'.format(line,self.pos))
    
    def evalExp(self, line):
        v1 = 0
        v2 = 0

        while self.pos < len(line):
            if line[self.pos] == '+':

                self.pos +=1

                self.pushValue(line)
                if self.pos < len(line) and line[self.pos] == '*':
                    self.addPending = True
                else:
                    v1 = self.stack.pop()
                    v2 = self.stack.pop()
                    
                    self.stack.append(v1 + v2)
            elif line[self.pos] == '*':
                self.pos +=1
                self.pushValue(line)
                v1 = self.stack.pop()
                v2 = self.stack.pop()
                self.stack.append(v1 * v2)
                if self.pos < len(line) and self.addPending and line[self.pos] != '*':
                    v1 = self.stack.pop()
                    v2 = self.stack.pop()
                    self.stack.append(v1 + v2)
                    self.addPending = false
            else:
                self.pos +=1

    
    def interp(self, code):
        for line in code:
            self.addPending = False
            if(line[1] == '='):
                self.pos = 2
                self.pushValue(line)
                self.evalExp(line)

                self.env[line[0]] = self.stack.pop()

            else:
                self.pos = 0
                print(self.env[line[self.pos]])
            self.stack.clear()


        