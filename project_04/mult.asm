// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.

@R2 // A=R2
M = 0 //M[R2]=0,输出地址置零
(LOOP)
    @R1 //A=R1
    D=M //D=M[R1]
    @END
    D, JEQ //如果M[R1]==0， 结束
    @R0 //A=R0
    D=M //D=M[R0]
    @R2 //A=R2
    M=D+M //M[R2]=M[R0]+M[R2]
    @R1 //A=R1
    M=M-1 //M[R1]=M[R1]-1
    @LOOP
    0; JMP //goto LOOP
(END)
    @END
    0; JMP 