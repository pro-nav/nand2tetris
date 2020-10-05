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

// Solution by @pro-nav


    @i
    M=0

    @8192
    D=A
    @n
    M=D

(LOOP)
    @i
    M=0
    @KBD
    D=M
    @NOFILL
    D;JEQ
    @FILL
    0;JMP


(FILL)
    @i
    D=M
    @n
    D=D-M
    @LOOP
    D;JEQ

    @SCREEN
    D=A
    @i
    A=D+M
    M=-1

    @i
    M=M+1

    @FILL
    0;JMP

(NOFILL)
    @i
    D=M
    @n
    D=D-M
    @LOOP
    D;JEQ

    @SCREEN
    D=A
    @i
    A=D+M
    M=0

    @i
    M=M+1

    @NOFILL
    0;JMP