// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.
//参数的预先定义
@24575 //屏幕的最大地址
D = A 
@R0
M = D //内存R0存储屏幕的最大地址值
@SCREEN //屏幕的当前地址，初始为SCREEN
D = A
@R1
M = D //内存R1存储屏幕的当前地址值

//初始循环，读取键盘
(LOOP)
    @KBD
    D = M //D存储键盘读取值
    @BLACKLOOP
    D; JGT //键盘被按下，进入涂黑循环
    @WHITELOOP
    0; JMP //否则进入变白循环
(BLACKLOOP)
    @R0
    D = M
    @R1
    D = D - M
    @LOOP
    D; JLT //判断屏幕是否涂满，即当前地址是否已经达到最大地址
           //涂满了就回去读键盘
    @R1
    D = M //把当前地址存到D里，用于计算下个地址
    A = M //把当前地址存到A里，用于更新当前地址的颜色
    M = -1 //M[A]==M[R1]=-1
    //此时R1为当前地址，M[R1]=-1,即M[R1]=1111111111111111,全黑
    @R1
    M = D + 1 //M[R1]=M[R1]+1，计算下个地址
    @LOOP
    0; JMP //继续回去读键盘
(WHITELOOP)
    @SCREEN
    D = A 
    @R1
    D = D - M 
    @LOOP
    D; JGT //判断屏幕是否为空，即当前地址是否已经达到最小地址
            //空了就回去读键盘
    //后面的和BLACKLOOP基本一样了，只是涂黑变成涂白，地址加变成减
    //后面具体注释就不写了
    @R1
    D = M
    A = M 
    M = 0
    @R1
    M = D - 1
    @LOOP
    0; JMP
