# -*- encoding: utf-8 -*-

import ast
import inspect
import textwrap


def tail_recursive(function, debug=False):
    """Optimizes functions that are tail recursive

    Transforms the body of the function into a while loop where
    recursive calls are transformed into assignments against the
    function parameters. Example:

    @tail_recursive
    def factorial(n, accu=1):
        if n <= 1: return accu
        else:      return factorial(n-1, n*accu)

    becomes

    def factorial(n, accu=1):
        while True:
            if n <= 1: return accu
            else:      n, accu = n-1, n*accu
    """
    string_mode = not callable(function)

    source = function if string_mode else inspect.getsource(function)
    ast_tree = ast.parse(textwrap.dedent(source))

    # Decorator should only work on function definitions
    assert len(ast_tree.body) == 1
    assert type(ast_tree.body[0]) == ast.FunctionDef

    # exec() will need a scope -- we need to merge both caller scopes because
    # https://docs.python.org/3/library/functions.html
    # Remember that at module level, globals and locals are the same dictionary
    caller_frame = inspect.currentframe().f_back
    caller_globals = caller_frame.f_globals.copy()
    caller_locals = caller_frame.f_locals.copy()
    caller_scope = caller_globals
    caller_scope.update(caller_locals)

    def params(function_def):
        try:
            # Python 3+
            return [ast.Name(id=arg.arg, ctx=ast.Store()) for arg in function_def.args.args]
        except AttributeError:  # pragma: no cover
            # Python 2
            return [ast.Name(id=arg.id, ctx=ast.Store()) for arg in function_def.args.args]  # pragma: no cover

    function_def = ast_tree.body[0]
    function_def.decorator_list = []  # If @tail_recursive is still there, infinite recursion
    function_name = function_def.name
    function_params = params(function_def)

    class TransformRecursionCalls(ast.NodeTransformer):
        """
        Transforms recursive calls into tuple assignments
    
        return factorial(n-1, n*accu)
        becomes
        n, accu = n-1, n*accu
        """
        def visit_Return(self, node):
            if type(node.value) == ast.Call:
                call = node.value
                if is_recursion(call):
                    values = call.args
                    return ast.Assign(
                        targets=[ast.Tuple(elts=function_params, ctx=ast.Store())],
                        value=ast.Tuple(elts=values, ctx=ast.Load())
                    )
                else:
                    return node
            else:
                return node

    transformer = TransformRecursionCalls()

    def search(root, ast_type):
        for elem in ast.walk(root):
            if type(elem) == ast_type:
                yield elem

    def is_recursion(elem):
        # TODO: name only is not so precise
        return hasattr(elem, "func") and hasattr(elem.func, "id") and elem.func.id == function_name

    def is_tailrec(root):
        # TODO: better definition of what tailrec really is
        recursive_calls = 0
        for elem in list(search(root, ast.Return)):
            if elem.value is None:
                continue
            elif type(elem.value) == ast.IfExp:
                return is_tailrec(
                    ast.If(
                        test=elem.value.test,
                        body=[ast.Return(value=elem.value.body)],
                        orelse=[ast.Return(value=elem.value.orelse)]
                    )
                )
            elif type(elem.value) == ast.Call:
                if is_recursion(elem.value):
                    recursive_calls += 1
            else:
                calls = list(search(elem, ast.Call))
                recursions = sum(1 if is_recursion(e) else 0 for e in calls)
                if recursions > 0 and type(elem.value) != ast.Call:
                    return False

        return recursive_calls > 0

    def replace_recursions(function_body):
        transformer.visit(function_body)
        return function_body

    if is_tailrec(function_def):
        while_wrapper = ast.While(
            test=ast.Name(id='True', ctx=ast.Load()),
            body=function_def.body,
            orelse=[]
        )
        function_def.body = [replace_recursions(while_wrapper)]
        fixed = ast.fix_missing_locations(ast_tree)

        if debug:
            import astunparse
            print(astunparse.unparse(fixed))

        if string_mode:
            import astunparse
            return astunparse.unparse(fixed).strip()

        code_object = compile(fixed, "<string>", "exec")
        exec(code_object, caller_scope)
        wrapped_function = caller_scope[function_name]
        return wrapped_function
    else:
        raise RuntimeError("Not tail recursive")


# TODO:
# - Better recursion identification
# - Support for kwargs and varargs
