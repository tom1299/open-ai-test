import inspect
import pydoc


def getclass_signatures(clazz) -> list:
    class_definition = inspect.getsource(clazz)

    # Get the methods and constructors
    methods_and_constructors = inspect.getmembers(clazz, predicate=inspect.isfunction)

    # Extract method signatures
    method_signatures = []
    for name, member in methods_and_constructors:
        source = inspect.signature(member)
        method_signatures.append(source)

    # Print the method signatures
    for signature in method_signatures:
        print(signature)

    return method_signatures


def getclass_help(clazz) -> str:
    return pydoc.render_doc(clazz, "Help on %s")