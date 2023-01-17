// ASM FILE created by VMTranslator created by pajdek.
// Compilation date: 2023-01-17 17:05:03.561633
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=3030)
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_POP', arg_1='pointer', arg_2=0)
@SP
AM=M-1
D=M
@THIS
M=D
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=3040)
@3040
D=A
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
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=32)
@32
D=A
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_POP', arg_1='this', arg_2=2)
@2
D=A
@THIS
D=M+D
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
//Command(cmd_type='C_PUSH', arg_1='constant', arg_2=46)
@46
D=A
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_POP', arg_1='that', arg_2=6)
@6
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
//Command(cmd_type='C_PUSH', arg_1='pointer', arg_2=0)
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
//Command(cmd_type='C_PUSH', arg_1='pointer', arg_2=1)
@THAT
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
//Command(cmd_type='C_PUSH', arg_1='this', arg_2=2)
@2
D=A
@THIS
A=M+D
D=M
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
//Command(cmd_type='C_PUSH', arg_1='that', arg_2=6)
@6
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