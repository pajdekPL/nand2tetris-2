
// Command(cmd_type='C_PUSH', arg_1='constant', arg_2=7)
@7
D=A
@SP
A=M
M=D
@SP
M=M+1
// Command(cmd_type='C_PUSH', arg_1='constant', arg_2=8)
@8
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