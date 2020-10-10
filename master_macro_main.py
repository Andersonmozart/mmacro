#!/bin/python3
import subprocess
import os
import os.path
import time
import keyboard

CONFIG_PATH = "master_macro.config"
TEXT_EDITOR = "gedit"
VALID_KEYS = "1234567890-=qwertyuiop[asdfghjklç]zxcvbnm,.;/\\"


if not os.path.exists(CONFIG_PATH):
    os.mknod(CONFIG_PATH)

key_pressed_before = ""
key_pressed_is_listening = 0
key_pressed_cache = []


def send_temp_char(temp_char):
#    print("temp_char: ",temp_char)

    if(temp_char in VALID_KEYS):
        if(temp_char == "\\"):
            # A única forma que encontrei de fazer o programa conseguir digitar uma contrabarra
            # Você pode pensar "Uau, mas esse xdotool é muito bom. Por que não usamos ele para digitar em vez do módulo keyboard?"
            # A resposta é que a única vantagem do xdotool seria digitar letras que o módulo do python não consegue (como acentos), entretanto ,se fizer um teste do tipo: xdotool type "áááéé", vai ver que é muito lento, o que é exatamente o que eu não desejo para o programa.
            # E ele é mais lento que o módulo do keyboard, então, até o momento, o módulo é a solução mais viável.
            os.system("xdotool type \\\\")
        else:
            keyboard.send(temp_char)
    else:
        if(temp_char == ":"):
            keyboard.press('shift')
            keyboard.send(';')
            keyboard.release('shift')                                
        else:
            keyboard.press('shift')
            keyboard.send(temp_char)
            keyboard.release('shift')                                

def run_command(key_list):
    global key_pressed_before
    global key_pressed_is_listening
    global key_pressed_cache
    cache_string = ''.join(key_list)

#    Apagar os caracteres para inserir os novos. +3 por causa das contrabarras
    for i in range(len(cache_string)+3):
        keyboard.press_and_release('backspace')
        time.sleep(0.02)

#Essa parte é onde se coloca os comandos em que programação é necessária. Cuidado para não colocar os mesmos comandos do config
    if(cache_string == 'new'):
        temp_command =TEXT_EDITOR +" " + CONFIG_PATH + " &"
        os.system(temp_command)
    elif(cache_string[:5] == 'shell'):
        temp_command = cache_string[6:]
        os.system(temp_command)
#############################################
    else:
        temp_arg = []
        if(" " in cache_string):
            temp_split = cache_string.split(" ")
            cache_string = temp_split[0]
            temp_arg = temp_split[1:]
        try:
            with open(CONFIG_PATH) as search:
                for line in search:
                    line = line.rstrip().split("==")  # remove '\n' at end of line
                    if(" " in line[0]):
                        line[0] = line[0].split(" ")[0]
                    if(cache_string == line[0]):
#                        print("line[1]: ",line[1])
                        key_pressed_is_listening = 0
                        key_pressed_before = ""
                        key_pressed_cache = []
                        # system1 não retorna output para o teclado
                        # system2 retorna o output para o teclado
                        # system1 pode ser usando quando se quer desligar o pc, por exemplo
                        # system2 quando se deseja retornar algum valor para ser digitado
                        if("system1" in line[1]):
                            os.system(line[1][8:-1])
                            break
                        if("system2" in line[1]):
                            temp_command = line[1][8:-1]
                            cont_sys2 = 0
                            while("$" in temp_command):
                                temp_command = temp_command.replace("$",temp_arg[cont_sys2],1)
                                cont_sys2 +=1

                            line[1] = os.popen(temp_command).read().rstrip()

                        for j in range(len(line[1])):
                            time.sleep(0.01)
                            temp_char = line[1][j]
                            if(temp_char.isupper()):
                                temp_char = 'shift+'+temp_char.lower()

                            if(temp_char == "$"):
                                for y in range(line[1].count("$")):
                                    for z in range(len(temp_arg[y])):
                                        send_temp_char(temp_arg[y][z])
                            else:
                                send_temp_char(temp_char)

                        break



        except (IOError):
            print("Falha ao abrir o config")


def on_press_reaction(event):
    global key_pressed_before
    global key_pressed_is_listening
    global key_pressed_cache
    if(key_pressed_is_listening and (event.name != "\\")):
        if(event.name == "space"):
            key_pressed_cache.append(" ")
        elif(event.name == "backspace"):
            key_pressed_cache.pop()
        elif(event.name != "shift" and event.name != "ctrl" and event.name != "alt"):
            key_pressed_cache.append(event.name)
    
    elif(key_pressed_is_listening and (event.name == "\\")):
        key_pressed_is_listening = 0
#        print(key_pressed_cache)
        run_command(key_pressed_cache)
        key_pressed_cache = []
        #Se não tiver um return, a condição abaixo é executada
        return

    if event.name == "\\" and key_pressed_before == "\\" and key_pressed_is_listening == 0:
        key_pressed_before = ""
        key_pressed_is_listening = 1
    elif event.name:
        key_pressed_before = event.name


keyboard.on_press(on_press_reaction)

keyboard.wait()



