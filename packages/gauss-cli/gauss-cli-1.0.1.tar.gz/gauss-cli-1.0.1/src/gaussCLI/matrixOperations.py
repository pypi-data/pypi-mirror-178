from rich.console import Console
from .printer import Log
import numpy as np

console = Console()

def userDefine():
    # user input
    while(True):
        try:
            matrixSize = int(console.input("\n[bold green]matrix size[/] ? :smiley: : "))
            if(matrixSize > 0):
                break
            console.print('[red bold]:x: Please write valide size !!![/]')     
        except:
            console.print('[red bold]:x: Please write valide size !!![/]')    
    userInput = matrixSize
    matrix = np.zeros((userInput, userInput+1))

    return matrix
def fillMatrix(matrix):

    # fill matrix
    for i in range(len(matrix)):
        for j in range(len(matrix)+1):
            while(True):
                try:
                    userInput = int(console.input(f"\n[bold green]matrix[{i}][{j}][/] : "))
                    break
                except:
                    console.print('[red bold]:x: Please write valide value !!![/]')  
            matrix[i][j] = int(userInput)
            Log().printMatrix(matrix)

