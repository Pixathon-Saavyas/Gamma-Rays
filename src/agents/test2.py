def read_file_as_string(filename):
  
#   try:
#     with open(filename, "r") as file:
#       return file.read()
#   except FileNotFoundError:
#     # File not found, return empty string
#     return ""
    with open(filename, "r") as file:
        return file.read()
  
print(read_file_as_string("msgs.txt"))
