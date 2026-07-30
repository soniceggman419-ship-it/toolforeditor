try:

    from Numeric import add, subtract, maximum

except ImportError:

    import operator

    def add(x, y):
        return tuple(map(operator.add, x, y))

    def subtract(x, y):
        return tuple(map(operator.sub, x, y))

    def maximum(*args):
        result = args[0]
        for x in args[1:]:
            result = tuple(map(max, result, x))
        return result
