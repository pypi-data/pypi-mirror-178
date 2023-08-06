
extern char const * const basic_grammar = R"(

Program <- Line*

Line <- Integer Statements NewLine

NewLine <- '\n'

Statements <- Statement (':' Statement)*

# Statement <- If / (Keyword Arguments)

# Keyword <- < [A-Z]+ >

Dim <- Id2 '(' ExpressionList ')'

Statement <- 'CLOSE'i Integer
                / 'CLR'i
                / 'CMD'i  Expression
                / 'CONT'i
                / 'DATA'i ConstantList
                / 'DEF'i FunctionId '(' IdList ')' '=' Expression
                / 'DIM'i Dim (',' Dim)*
                / 'END'i
                / 'FOR'i Id '=' Expression 'TO' Expression ('STEP'i Expression)?
                / 'GET'i Id
                / 'GET'i '#' Integer ',' Id
                / 'GOSUB'i Expression
                / 'GOTO'i Expression
                / 'IF'i Expression 'THEN'i (Integer / Statement)
                / 'INPUT'i IdList
                / 'INPUT'i '#' Integer ',' IdList
                / 'LET'i Id '=' Expression
                / 'LIST'i LineRange
            #    / 'LOAD'i ValueList
                / 'ID'i '=' Expression
                / 'NEW'i
                / 'NEXT'i IdList
                / 'ON'i Id 'GOTO'i ExpressionList
                / 'OPEN'i ExpressionList
                / 'POKE'i Expression ',' Expression
                / 'PRINT'i PrintList
                / 'READ'i IdList
                / 'RETURN'i
                / 'RESTORE'i
                / 'RUN'i
                / 'RUN'i Expression
                / 'STOP'i
                / 'SYS'i Expression
                / 'WAIT'i ExpressionList
                / 'VERIFY'i ExpressionList
                / Remark
                / Id '=' Expression

Remark <- 'REM'i .*

LineRange <- Integer? ('-' Integer)?

PrintList <- Expression (';' Expression)*

FunctionId <- 'F' 'N' Letter Letter?

Letter <- [A-Z]

ConstantList <- Constant (',' Constant)*

Constant <- Integer / Real / String

ExpressionList <- Expression (',' Expression)*

Id <- [A-Z] [A-Z0-9]* [$%]? ( '(' ExpressionList ')' )?

Id2 <- [A-Z] [A-Z0-9]* [$%]?

IdList <- Id (',' Id)*

#Arguments <- (Argument (',' Argument)*)?
#Argument <- Expression / String / Id


Expression  <- Atom (Operator Atom)* {
                         precedence
                           L 'OR'
                           L 'AND'
                           L = <> > >= < <=
                           L + -
                           L * /
                           L ^
                       }


Operator <- 'OR'i / 'AND'i / '=' / '<>' / '>' / '>=' / '<' / '<=' / '+' / '-' / '*' / '/' / '^'

Atom <- Unary / Value / '(' Expression ')'

Unary <- UnOp Atom

UnOp <- 'NOT'i / '-'

Value <- Func / Constant / Id

Func <- Symbol '(' Expression ')'

Symbol <- [A-Z]i+

Integer <- < [0-9]+ >
Real <- < ([0-9]+ '.')? [0-9]+ >

String <- ["] StringContents ["]
StringContents <- (!["] .)*

%whitespace <- [ \t]*
)";
