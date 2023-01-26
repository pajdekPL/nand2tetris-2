// ASM FILE created by VMTranslator created by pajdek.
// Compilation date: 2023-01-24 14:01:49.970181
// Command(cmd_type='C_FUNCTION', arg_1='SimpleFunction.test', arg_2=2)(SimpleFunction.test)
@SP
A=M
M=0
@SP
M=M+1
@SP
A=M
M=0
@SP
M=M+1

// Command(cmd_type='C_PUSH', arg_1='local', arg_2=0)
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
// Command(cmd_type='C_PUSH', arg_1='local', arg_2=1)
@1
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
// or
@SP
A=M-1
M=!M
// Command(cmd_type='C_PUSH', arg_1='argument', arg_2=0)
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
// add
@SP
AM=M-1
D=M
A=A-1
M=D+M
// Command(cmd_type='C_PUSH', arg_1='argument', arg_2=1)
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
// sub
@SP
AM=M-1
D=M
A=A-1
M=M-D
// Command(cmd_type='C_RETURN', arg_1=None, arg_2=None)
@LCL
D=M
@endFrame
M=D
@5
D=A
@endFrame
A=M-D
D=M
@retAddr
M=D
@SP
AM=M-1
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@endFrame
A=M-1
D=M
@THAT
M=D
@endFrame
A=M-1
A=A-1
D=M
@THIS
M=D
@endFrame
A=M-1
A=A-1
A=A-1
D=M
@ARG
M=D
@endFrame
A=M-1
A=A-1
A=A-1
A=A-1
D=M
@LCL
M=D
@retAddr
A=M
0;JMP