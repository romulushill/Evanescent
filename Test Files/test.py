def decorator_function(original_function):
    def wrapper_function(*args, **kwargs):
        # Code to be executed before the original function
        print("Executing before {} function.".format(original_function.__name__))
        
        # Call the original function
        result = original_function(*args, **kwargs)
        
        # Code to be executed after the original function
        print("Executing after {} function.".format(original_function.__name__))
        
        # Return the result of the original function
        return result
    
    # Return the wrapper function
    return wrapper_function

# Decorate a function using the decorator
@decorator_function
def greet(name):
    print("Hello, {}!".format(name))

# Call the decorated function
greet("John")
