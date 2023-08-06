from .printer import Log , md
from .matrixOperations import userDefine , fillMatrix
from rich.console import Console
from .gauss import Gauss


console = Console()

class GaussCliMethods:
    def __init__(self):
        self.matrix = None
        self.result = None

    def markdown(self):
        console.print(md)
    # print user define
    def userMatrix(self):
        self.matrix = userDefine()
        # print zeros matrix
        Log().printMatrix(self.matrix)

    # fill matrix
    def fillMatrix(self):
        fillMatrix(self.matrix)
    
    # print progress
    def printProgress(self):
        import time
        from rich.progress import track

        print("\n")

        for i in track(range(20), description="Processing..."):
            time.sleep(0.03)
        console.rule("\n\n[bold green]Solution ")

    # print gauss operation
    def gaussCalculator(self):
        gauss = Gauss(self.matrix)
        self.result = gauss.result()
        
    # print result
    def printResult(self):
        Log().printResult(self.result)

class GaussCLI(GaussCliMethods):
    def __init__(self):
        super().markdown()
        super().userMatrix()
        super().fillMatrix()
        super().printProgress()
        super().gaussCalculator()
        super().printResult()

