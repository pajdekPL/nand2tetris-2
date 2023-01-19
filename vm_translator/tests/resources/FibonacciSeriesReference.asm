// ASM FILE created by VMTranslator created by pajdek.
// Compilation date: 2023-01-17 17:05:03.561633
//Command(cmd_type='C_PUSH', arg_1='argument', arg_2=1)
@1
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_POP', arg_1='pointer', arg_2=1)
@SP
AM=M-1
D=M
@THAT
M=D
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=0)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_POP', arg_1='that', arg_2=0)
@0
D=A
@THAT
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=1)
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_POP', arg_1='that', arg_2=1)
@1
D=A
@THAT
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//Command(cmd_type='C_PUSH', arg_1='argument', arg_2=0)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=2)
@2
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
//Command(cmd_type='C_POP', arg_1='argument', arg_2=0)
@0
D=A
@ARG
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//Command(cmd_type='C_LABEL', arg_1='MAIN_LOOP_START', arg_2=None)
(MAIN_LOOP_START)
//Command(cmd_type='C_PUSH', arg_1='argument', arg_2=0)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_IF', arg_1='COMPUTE_ELEMENT', arg_2=None)
@SP
AM=M-1
D=M
@COMPUTE_ELEMENT
D;JNE
//Command(cmd_type='C_GOTO', arg_1='END_PROGRAM', arg_2=None)
@END_PROGRAM
0;JMP
//Command(cmd_type='C_LABEL', arg_1='COMPUTE_ELEMENT', arg_2=None)
(COMPUTE_ELEMENT)
//Command(cmd_type='C_PUSH', arg_1='that', arg_2=0)
@0
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_PUSH', arg_1='that', arg_2=1)
@1
D=A
@THAT
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
//Command(cmd_type='C_POP', arg_1='that', arg_2=2)
@2
D=A
@THAT
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//Command(cmd_type='C_PUSH', arg_1='pointer', arg_2=1)
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=1)
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
//Command(cmd_type='C_POP', arg_1='pointer', arg_2=1)
@SP
AM=M-1
D=M
@THAT
M=D
//Command(cmd_type='C_PUSH', arg_1='argument', arg_2=0)
@0
D=A
@ARG
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=1)
@1
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
//Command(cmd_type='C_POP', arg_1='argument', arg_2=0)
@0
D=A
@ARG
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//Command(cmd_type='C_GOTO', arg_1='MAIN_LOOP_START', arg_2=None)
@MAIN_LOOP_START
0;JMP
//Command(cmd_type='C_LABEL', arg_1='END_PROGRAM', arg_2=None)
(END_PROGRAM)