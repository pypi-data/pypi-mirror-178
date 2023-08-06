from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

console = Console()
log = Console().print
MARKDOWN = """
# Gauss Elimination CLI

gauss elimination CLI Tool :  

1. Solve equation (matrix) type of n*n 
2. Show steps of solving
"""

md = Markdown(MARKDOWN)


class Log():
    def __init__(self , l1 = None , l2 = None , matrix = None):
        self.l1 = l1
        self.l2 = l2
        self.matrix = matrix

    def printMatrix(self , matrix):
        for i in range(len(matrix)):
            console.print('| ' , end="")
            for j in range(len(matrix)):
                console.print(f"[white]{matrix[i][j]}[/] " , end="")
                if j == len(matrix)-1:
                    console.print(f'[blue]| {matrix[i][j+1]}[/] |' , end="\n")

    # print swiper
    def swiperPrinter(self):
        log(f"Swipe [blue]L{self.l1}[/] with [blue]L{self.l2}[/]" , style="green bold u" , end="\n\n")
        
        self.printMatrix(self.matrix)
    # print pivot operation
    def pivotPrinter(self , pivot):
        console.print("\n")
        log(f"[blue]L{self.l1}[/] = [blue]L{self.l1}[/]/{pivot}[yellow] (divide the {self.l1} row by {pivot}) [/]" , style="green bold u" , end="\n\n")
        self.printMatrix(self.matrix)


    # print elimination
    def factorPrinter(self , factore):
        console.print("\n")
        log(f"[blue]L{self.l2}[/] = [blue]L{self.l1}*{factore}[/]-[blue]L{self.l2}[/] [yellow]( multiply {self.l1} row by {factore} and substract it from {self.l2} row )[/]" , style="green bold u" , end="\n\n")
        
        self.printMatrix(self.matrix)

    def printResult(self , matrix_result):
        print('\n')
        resultText = ''
        for i in range(len(matrix_result)):
            resultText += f'\n[blue]X{i}[/] [green]=[/] {str(matrix_result[i])}'

        console.print(Panel(f" {resultText}" , title="[green bold]Result !!![/]"))
        