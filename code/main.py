import random
import time
import os
import sys
import subprocess

def fileArg():

 lang = pipen()
 if len(sys.argv) != 2:
   print("Usage: python pipen.py <file name>.pipen")
   return

 file = sys.argv[1]
 lang.file(file)

class pipen: 
 def __init__(self):
     self.returned = False
     self.vars = {}
     self.instructions = {
         'POUT': lambda *args: sys.stdout.write(str(args[0])),
         'PIN': lambda *args: (
          self.vars[args[0]] if args[0] in self.vars else (
              (lambda: (
                  setattr(self, f'_{args[0]}_prompted', True),
                  self.vars.update({args[0]: input(args[1])}),
                  self.vars[args[0]]
              ))()
          ) if not getattr(self, f'_{args[0]}_prompted', False) else self.vars[args[0]]
      ),
         'VAR': lambda *args: self.vars.update({args[0]: args[1]}),
         'IF': lambda arg1, arg2, arg3, arg4, arg5, arg6 = None, arg7 = None, arg8 = None: self.if_statement(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8),
         'RETURN': lambda *args: self.returns(args[0]),
         'SLEEP': lambda *args: time.sleep(int(args[0])),
         'RANDINT': lambda *args: self.vars.update({args[0]: random.randint(int(args[1]), int(args[2]))}),
         'EVAL': lambda *args: self.vars.update({args[0]: eval(args[1])}),
     }

 def clear(self, v):
  if v == 'TRUE':
   subprocess.call('clear', shell=True)

 def returns(self, v):
  if v == '0':
   self.returned = True
  elif v == '1':
   self.returned = False,

 def rawexec(self, instruction):
  if not instruction:
      print("Empty instruction provided.")
      return

  for key, value in self.vars.items():
   instruction = instruction.replace("<<" + key + ">>", str(value))
  to_exec = instruction.split('|')
  if to_exec[0] in self.instructions:
      try: 
          self.instructions[to_exec[0]](*to_exec[1:])
      except Exception as e:
          print('Error:', e)
  else:
      print("Invalid instruction:", instruction)

 def file(self, name):
  while self.returned is False:
   try: 
    with open(name, 'r') as f:
     lines = f.readlines()
     ext = os.path.splitext(f.name)[1]
     if ext == '.pipen':
      for line in lines:
       self.rawexec(line)
     else:
      print("Invalid file extension.")
   except FileNotFoundError:
    print("File not found:", name + '.pipen')


 def if_statement(self, v1, op, v2, rs, func, arg1, arg2, arg3):
     if arg1 is not None:
      func += '|' + arg1
     if arg2 is not None:
       func += '|' + arg2
     if arg3 is not None:
        func += '|' +  arg3
     try:
         v1 = int(v1) if v1.isdigit() else int(self.vars.get(v1, 0))
         v2 = int(v2) if v2.isdigit() else int(self.vars.get(v2, 0))
         rs = int(rs) if rs.isdigit() else print('Not an int, sorry')

         if op == '<':
             if v1 < v2:
                 self.rawexec(func)
         elif op == '>':
          if v1 > v2:
              self.rawexec(func)
         elif op == '+':
          if v1 + v2 == rs:
              self.rawexec(func)
         elif op == '-':
          if v1 - v2 == rs:
             self.rawexec(func)
         elif op == '/':
           if v1 / v2 == rs:
             self.rawexec(func)
         elif op == '*':
           if v1 * v2 == rs:
             self.rawexec(func)
     except Exception as e:
         print('ErrorIF:', e)

if __name__ == '__main__':
 fileArg()