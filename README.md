# mmacro

sudo pip3 install keyboard

sudo apt-get install xdotool

sudo chmod a+rwx master_macro.config

No .bashrc:

alias mmacrof='cd MMACRO_PATH'

alias mmacro='cd MMACRO_PATH && sudo python3 master_macro_main.py'

Onde MMACRO_PATH é a pasta onde mmacro foi clonado


Para usar:

Em algum local onde é possível escrever, digite \\\\macro\\, onde macro == os comandos da coluna esquerda do arquivo master_macro.config.

Assim, se digitar: \\\\wpp\\, ele irá apagar esses dígitos e digitar: web.whatsapp.com no lugar.

\\\\for 40\\==for(int i = 0; i < 40; i++), onde o 40 pode ser qualquer valor/variável



To do:
- A princípio, como o master_macro.config possui poucos macros, é feita uma busca sequencial no arquivo para encontrar o comando referente. Vai ficar lento de acordo com a quantidade de linhas, logo é necessário programar um método que organiza o arquivo e outro que realiza uma busca binária.
- Se apertar backspace em meio a um macro, o programa ainda assim vai compreender o resultado final. Mas isso não acontece se mover o cursor com as setas do teclado (muito menos clicando). Para resolver o problema da seta, pode haver uma condição que detecta que a seta foi pressionada e um contador para saber quantas vezes a tecla foi pressionada para uma direção. Isso vai permitir que um novo caractere seja inserido no meio da lista
- Expr dos macros de calcular não funcionam com número decimal.
- Acentos não funcionam, da mesma forma que alguns caractéres específicos provavelmente não funcionarão por causa do módulo keyboard.
- É necessário um caractere de escape para que seja possível digitar uma contrabarra no uso da variável de um comando sem enviar o comando para o programa.
