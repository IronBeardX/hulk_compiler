from hulk_definitions.ast import *
from tools.semantic import Context, SemanticError, Type
from tools import visitor
from tools.semantic import Scope, ScopeInterpreter
from typing import Callable
import math, random

class Interpreter(object):
    def __init__(self, context: Context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        

    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(Program)
    def visit(self, node):
        scope = ScopeInterpreter()
        scope.define_function('print', print)
        scope.define_function('sqrt', math.sqrt)
        scope.define_function('sin', math.sin)
        scope.define_function('cos', math.cos)
        scope.define_function('exp', math.exp)
        scope.define_function('log', math.log)
        scope.define_function('rand', random)
        scope.define_function('range', range)
        scope.define_protocol('Iterable', self.context.get_protocol('Iterable'))
        
        for child in node.statements:
           return_last_statement = self.visit(child, scope )
        return return_last_statement
    
    @visitor.when(Statement)
    def visit(self, node, scope: ScopeInterpreter):
        pass

    @visitor.when(Let)
    def visit(self, node: Let, scope: ScopeInterpreter):
        child_scope = scope.create_child_scope()
        value_exp = self.visit(node.expr,scope)
        child_scope.define_variable(node.name, value_exp, node.type)
        
        value_body = self.visit( node.scope, child_scope ) 
        return value_body
        
    @visitor.when(LetList)
    def visit(self, node: LetList, scope: ScopeInterpreter):
        return self.visit( node.child, scope)

    @visitor.when(Block)
    def visit(self, node, scope: ScopeInterpreter):
        body = None
        for statement in node.body:
            body = self.visit( statement, scope)
        return body
    
    @visitor.when(Function)
    def visit(self, node: Function, scope: ScopeInterpreter):
        body_scope = scope.create_child_scope()

        def fun (*args):
            for i in range(len(node.params)):
                x = node.params[i][0]
                body_scope.define_variable(x, args[i], node.params[i][1])
                
            function_body: Callable = self.visit(node.body , body_scope)
            
            return function_body
        
        scope.define_function(node.name, fun)
        return fun

    @visitor.when(Conditional)
    def visit(self, node: Conditional, scope: ScopeInterpreter):
        body_scope = scope.create_child_scope()
        
        if_expr_value = self.visit(node.if_expr, scope)

        if if_expr_value:
            return self.visit(node.if_body, body_scope)
        else:
            return self.visit(node.else_body, body_scope)

    @visitor.when(Branch)
    def visit(self, node, scope: ScopeInterpreter):
        condition_value = self.visit( node.condition, scope)
        if condition_value:
            return self.visit(node.body)
        else:
             pass

    @visitor.when(Expression)
    def visit(self, node, scope: ScopeInterpreter):
        pass

    @visitor.when(Unary)
    def visit(self, node, scope: ScopeInterpreter):
        right_value = self.visit(node.right, scope)
        return right_value

    @visitor.when(Number)
    def visit(self, node, scope: ScopeInterpreter):
        return float(node.lex)
    
    @visitor.when(Pi)
    def visit(self, node, scope: ScopeInterpreter):
        return math.pi
    
    @visitor.when(E)
    def visit(self, node, scope: ScopeInterpreter):
        return math.e
    
    
    @visitor.when(Print)
    def visit(self, node: Print, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        print(*args)
        
    @visitor.when(Plus)
    def visit(self, node: Plus, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value + right_value

    @visitor.when(BinaryMinus)
    def visit(self, node: BinaryMinus, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value - right_value

    @visitor.when(Star)
    def visit(self, node: Star, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value * right_value

    @visitor.when(Pow)
    def visit(self, node: Pow, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value ** right_value

    @visitor.when(Div)
    def visit(self, node: Div, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value / right_value

    @visitor.when(Mod)
    def visit(self, node: Mod, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value % right_value
    
    @visitor.when(Is)
    def visit(self, node: Is, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value is right_value

    @visitor.when(As)
    def visit(self, node: As, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value == right_value

    @visitor.when(At)
    def visit(self, node: At, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return str(left_value) + ' @ ' + str(right_value)

    @visitor.when(DoubleAt)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value @ right_value

    @visitor.when(Or)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value or right_value

    @visitor.when(And)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value and right_value

    @visitor.when(GreaterThan)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value > right_value

    @visitor.when(LessThan)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value < right_value

    @visitor.when(GreaterEqual)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value >= right_value

    @visitor.when(LessEqual)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value <= right_value

    @visitor.when(NotEqual)
    def visit(self, node, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value != right_value

    @visitor.when(CompareEqual)
    def visit(self, node: CompareEqual, scope: ScopeInterpreter):
        left_value = self.visit(node.left, scope)
        right_value = self.visit(node.right, scope)
        return left_value == right_value

    @visitor.when(Not)
    def visit(self, node, scope: ScopeInterpreter):
        value = self.visit(node.right, scope)
        return not value

    @visitor.when(UnaryMinus)
    def visit(self, node, scope: ScopeInterpreter):
        value = self.visit(node.right, scope)
        return -value

    @visitor.when(Atom)
    def visit(self, node: Atom, scope: ScopeInterpreter):
        return node.lex

    @visitor.when(Call)
    def visit(self, node: Call, scope: ScopeInterpreter):
        # Evaluar los argumentos de la llamada
        args = [self.visit(arg, scope) for arg in node.args]
        func = scope.get_local_function(node.idx)
        return func(*args)

    @visitor.when(Str)
    def visit(self, node: Str, scope: ScopeInterpreter):
        return str(node.lex)

    @visitor.when(Bool)
    def visit(self, node: Bool, scope: ScopeInterpreter):
        return bool(node.lex)

    @visitor.when(Invoke)# TODO: malllllllllllllll
    def visit(self, node: Invoke, scope: ScopeInterpreter):
        child_scope = scope.create_child_scope()
        container_type = self.visit(node.container, scope)
        a = container_type.call(node.lex.lex)
        container_value = self.visit(a, scope)
        # container_type = scope.get_local_type(scope.get_local_variable(node.container.lex)[1])
       
                                               
        child_scope.define_variable(node.container.lex, container_value, container_type)
        var_type = self.context.get_protocol(scope.get_local_variable(node.container.lex)[1])
        
        for i in range(len(var_type.methods_def)):
            metodo = var_type.methods_def[i].name
            if metodo == node.lex.lex:
                a = getattr(container_type, metodo)
                return a
        # property = self.visit(node.lex, scope)
        # Devolver el resultado de la invocación
        # return getattr(container, property)

    @visitor.when(Vector)
    def visit(self, node: Vector, scope: ScopeInterpreter):
        values = [self.visit(value, scope) for value in node.lex]
        return values

    @visitor.when(VectorComprehension)
    def visit(self, node: VectorComprehension, scope: ScopeInterpreter):
        
        a = self.visit(node.lex, scope)
        values = []
        for value in a:
            scope_body = scope.create_child_scope()
            scope_body.define_variable(node.operation[0], value, type(value))
            operation = self.visit(node.operation[1], scope_body)
            values.append(operation)
        
        return values

    @visitor.when(Var)
    def visit(self, node: Var, scope: ScopeInterpreter):
        var = scope.get_local_variable(node.lex)
        return var[0] if var else None

    @visitor.when(TypeDef)
    def visit(self, node: TypeDef, scope: ScopeInterpreter):
        # body_scope = scope.create_child_scope()
        visitor = self
        
        class NewType:
            def __init__(self, params = None):
                typeScope = scope.create_child_scope()
                
                for i in range(params if params else 0):
                    typeScope.define_variable(node.args[i][0], params[i])
                 
                   
                for x in [x for x in node.body if type(x) is Property]:
                    if not typeScope.get_local_variable(x):
                        b = visitor.visit(x, typeScope)
                   
                for x in [x for x in node.body if type(x) is Function]:
                    if scope.get_local_function(x.name):
                        continue
                    a = visitor.visit(x, scope)
                   
            def call(self, name):
                return scope.get_local_function(name) 
            
            def create_new_instance(params):
                return NewType(params)       
                    
        scope.define_type(node.name, NewType)
        NewType()
        return NewType
    
    @visitor.when(Protocol)
    def visit(self, node, scope: ScopeInterpreter):
         pass
    
    @visitor.when(Assign)
    def visit(self, node: Assign, scope: ScopeInterpreter):
        value = self.visit(node.body, scope)
        scope.define_variable(node.lex.lex, value, None) 
        return value

    @visitor.when(Indexing)
    def visit(self, node: Indexing, scope: ScopeInterpreter):
        name_value = self.visit(node.lex, scope)
        index_value = int(self.visit(node.index, scope))
        return name_value[index_value]

    @visitor.when(Sin)
    def visit(self, node: Sin, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.sin(*args)

    @visitor.when(Cos)
    def visit(self, node: Cos, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.cos(*args)

    @visitor.when(Rand)
    def visit(self, node: Rand, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        return random.random(*args)

    @visitor.when(Exp)
    def visit(self, node: Exp, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.exp(*args)

    @visitor.when(Log)
    def visit(self, node: Log, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.log(*args)

    @visitor.when(Sqrt)
    def visit(self, node: Sqrt, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        return math.sqrt(*args)

    @visitor.when(Range)
    def visit(self, node: Range, scope: ScopeInterpreter):
        args = [self.visit(arg, scope) for arg in node.args]
        args_int = []
        for i in range(len(args)):
            args_int.append(int(args[i]))
        # Devolver el resultado de la función range
        return list(range(*args_int))

    @visitor.when(While)
    def visit(self, node: While, scope: ScopeInterpreter):
        while self.visit(node.stop, scope):
            return self.visit(node.body, scope)

    @visitor.when(For)
    def visit(self, node: For, scope: ScopeInterpreter):
        if node.collection.lex == 'range':
            x = int(self.visit(node.collection.args[0],scope))
            y = int(self.visit(node.collection.args[1],scope))
            for item in range(x, y):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item.name, item, node.item.type)
                value = self.visit(node.body, body_scope)
        else:
            for item in self.visit(node.collection, scope):
                body_scope = scope.create_child_scope()
                body_scope.define_variable(node.item.name, item, node.item.type)
                value = self.visit(node.body, body_scope)
        return value    
        
    @visitor.when(Self)
    def visit(self, node: Self, scope: ScopeInterpreter):
        return self.current_object

    @visitor.when(Property)
    def visit(self, node: Property, scope: ScopeInterpreter):
        name = node.name
        body_value = self.visit(node.body, scope)
        scope.define_variable(name, body_value, node.type)
        return body_value

    @visitor.when(CreateInstance)
    def visit(self, node: CreateInstance, scope: ScopeInterpreter):
        params_value = [self.visit(param) for param in node.params]
        type_value = scope.get_local_type(node.type)
        return type_value.create_new_instance(params_value)