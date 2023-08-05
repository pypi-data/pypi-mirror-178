__version__ = '0.1.0'

class Link:
  def init():
   x = input("Do you have a nlcky id? Y or N if Y, enter your id number instead.")
   if x == "N" or x == "n":
    print("Ok! Loading repl...")
   else:
    print(x + " is your id number. Loading repl...")