def announce(f):
    def wrapper():
        print("Running the function...")
        f()
        print("Done with the function.")
    return wrapper

@announce
def hello():
    print("Hello world!")

hello()
