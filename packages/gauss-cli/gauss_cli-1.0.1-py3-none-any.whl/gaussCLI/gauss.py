import numpy as np
from .printer import Log
  
class GaussMethods:
    def __init__(self , matrix):
        self.matrix = matrix
        self.n = len(matrix)
        
    # swap lines
    def swapLines(self , k):
        for i in range(k+1 , self.n):
            if np.fabs(self.matrix[i][k]) > np.fabs(self.matrix[k][k]):
                for j in range(k , self.n):
                    self.matrix[k][j], self.matrix[i][j] = self.matrix[i][j] , self.matrix[k][j]
                self.matrix[k][j+1], self.matrix[i][j+1] = self.matrix[i][j+1] , self.matrix[k][j+1]
                # print result
                Log(k,i,self.matrix).swiperPrinter()
                break

    # divide the pivot row << convert it to ones
    def pivotDivision(self , k):
        pivot = self.matrix[k][k]
        for j in range(k , self.n):
            self.matrix[k][j] = self.matrix[k][j] / pivot
        self.matrix[k][j+1] = self.matrix[k][j+1] / pivot
        # print result
        Log(k,j,self.matrix).pivotPrinter(pivot)

    # Eliminate the othe value of matrix

    def eleminator(self , k):
        for i in range(self.n):
            if i == k or self.matrix[i][k] == 0 : continue
            factor = self.matrix[i][k]
            for j in range(k,self.n):
                self.matrix[i][j] -= factor * self.matrix[k][j]
            self.matrix[i][j+1] -= factor * self.matrix[k][j+1]
             # print result
            Log(k,i,self.matrix).factorPrinter(factor)


class Gauss(GaussMethods):
    def __init__(self , matrix):
        super().__init__(matrix)

    # calculate matrix
    def calculateMatrix(self):
        for k in range(self.n):
            if np.fabs(self.matrix[k][k]) < 1.0e-12:
                super().swapLines(k)

            # divide pivot row
            super().pivotDivision(k)
            # elimination loop
            super().eleminator(k) 
        return self.matrix

    def result(self):
        matrix_result = self.calculateMatrix()
        
        l = []
        for i in range(len(matrix_result)):
            l.append(matrix_result[i][-1])
        
        return l

        

