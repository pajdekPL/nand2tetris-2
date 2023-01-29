// ASM FILE created by VMTranslator created by pajdek.
// Compilation date: 2023-01-19 21:46:39.956365
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=0)
@0
D=A
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_POP', arg_1='local', arg_2=0)
@0
D=A
@LCL
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//Command(cmd_type='C_LABEL', arg_1='LOOP_START', arg_2=None)
(LOOP_START)
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
//Command(cmd_type='C_PUSH', arg_1='local', arg_2=0)
@0
D=A
@LCL
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
//Command(cmd_type='C_POP', arg_1='local', arg_2=0)
@0
D=A
@LCL
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
//Command(cmd_type='C_IF', arg_1='LOOP_START', arg_2=None)
@SP
AM=M-1
D=M
@LOOP_START
D;JNE
//Command(cmd_type='C_PUSH', arg_1='local', arg_2=0)
@0
D=A
@LCL
A=M+D
D=M
@SP
A=M
M=D
@SP
M=M+1