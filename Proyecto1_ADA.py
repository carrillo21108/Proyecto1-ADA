import yaml

#Referencia: https://python-course.eu/applications-python/turing-machine.php
#Clase para Cinta
class Tape(object):
    
    blank_symbol = ' '
    
    def __init__(self,tape_string = '',blank_symbol = ' '):
        self.tape = dict((enumerate(tape_string)))
        Tape.blank_symbol = blank_symbol
    
    #Se especifica la generacion de la cinta como string desde el min hasta el max index
    def __str__(self):
        str_tape = ''
        min_index = min(self.tape.keys()) 
        max_index = max(self.tape.keys())
        
        for i in range(min_index, max_index+1):
            str_tape += self.tape[i]
            
        return str_tape
    
    #Generacion de descripcion instantanea (en amarillo el estado)
    def get_id(self,head_position,current_control):
        str_tape = ''
        
        if head_position not in self.tape:
            self.tape[head_position] = Tape.blank_symbol
            
        min_index = min(self.tape.keys()) 
        max_index = max(self.tape.keys())
        
        for i in range(min_index, max_index+1):
            if i==head_position:
                str_tape += '\033[1;33m' + current_control + '\033[0m'
            
            str_tape += self.tape[i]
                
            
        return str_tape
    
    #Al obtener un item, en caso el indice no este en la cinta, se retorna blank
    def __getitem__(self,index):
        if index in self.tape:
            return self.tape[index]
        else:
            return Tape.blank_symbol

    def __setitem__(self, pos, char):
        self.tape[pos] = char 


#Clase Maquina de Turing        
class TuringMachine(object):
    
    def __init__(self, tape = '', alphabet = set(), tape_alphabet=set(), states=set(), blank_symbol = ' ', initial_control = '', final_states = set(), transition_function = dict()):
        self.tape = Tape(tape,blank_symbol)
        self.head_position = 0
        self.current_control = initial_control
        self.transition_function = transition_function
        self.final_states = final_states
        self.alphabet = alphabet
        self.tape_alphabet = tape_alphabet
        self.states = states
        
    #Obtener la cinta como string        
    def get_tape(self):
        return str(self.tape)
                

    #Paso en la maquina
    def step(self):
        char_under_head = self.tape[self.head_position]
        control = (self.current_control, char_under_head)
        
        #Validacion de caracter y estado validos
        if control[1] in self.tape_alphabet and control[0] in self.states:
            
            #Validacion de control valido
            if control in self.transition_function:
                __id = self.tape.get_id(self.head_position,self.current_control)
            
                item = self.transition_function[control]
                self.current_control = item[0]
                self.tape[self.head_position] = item[1]
            
                if item[2] == "R":
                    self.head_position += 1
                elif item[2] == "L":
                    self.head_position -= 1

                #Impresion de descripcion instantanea
                __id += '\t⊢\t' + self.tape.get_id(self.head_position,self.current_control)
                print(__id)
                return True
            
            else:
                return False
        else:
            return False
            
    #Verificacion de estado final
    def final(self):      
        if self.current_control in self.final_states:
            __id = self.tape.get_id(self.head_position,self.current_control)
            __id += '\t⊢\t' + self.get_tape().replace(Tape.blank_symbol,'')
            print(__id)
            print('Cadena aceptada')
            return True
        else:
            return False

#Obtencion de la data en yaml        
def get_data():
   with open('mt-fibonacci.yaml', 'r') as f:
       data = yaml.safe_load(f)
   
   return data

def get_TuringMachine(tape,data):
    
    transition_function = dict()
    for item in data['delta']:
        #Conversion de None a blank
        if item['params']['tape_input']==None:
            item['params']['tape_input'] = 'B'
            
        if item['output']['tape_output']==None:
            item['output']['tape_output'] = 'B'
            
        transition_function[(item['params']['initial_state'],item['params']['tape_input'])] = (item['output']['final_state'], item['output']['tape_output'],item['output']['tape_displacement'])
    
    if data['tape_alphabet'][-1]==None:
        data['tape_alphabet'][-1] = 'B'
        
    return TuringMachine(tape = tape,
                      alphabet = set(data['alphabet']),
                      tape_alphabet = set(data['tape_alphabet']).union(set(data['alphabet'])),
                      states = set(data['q_states']['q_list']),
                      blank_symbol = data['tape_alphabet'][-1],
                      initial_control = data['q_states']['initial'],
                      final_states = {data['q_states']['final']},
                      transition_function = transition_function)

#Simulacion por cada string
data = get_data()
for tape in data['simulation_strings']:
    t = get_TuringMachine(tape,data)
    
    print('\nInput:\n' + t.get_tape())
    
    while not t.final():
        if not t.step():
            print('ERROR: Cadena rechazada')
            break