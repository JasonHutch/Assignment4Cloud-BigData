import os
import string
import re

class Helper:
    def __init__(self):
        pass
    
    def write_to_file(self,directory:str, filename:str, content:str) -> None:
        file_path = os.path.join(directory,f'{filename}.txt')
        with open(file_path, 'a') as file:
            file.write(content)