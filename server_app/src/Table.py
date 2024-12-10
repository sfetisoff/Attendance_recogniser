class Table:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.text_array = []
        self.__table_array = [[''] * col for i in range(row)]
        self.words = []
        self.read_group_file()

    def read_group_file(self):
        file = open('surnames.txt', 'r', encoding='utf-8')
        self.words = file.readlines()

    def get_element(self, row, col):
        return self.__table_array[row][col]

    def get_table(self):
        return self.__table_array

    def fill_table(self):
        flag = False
        for i in range(self.row):
            if flag:
                break
            for j in range(self.col):
                if len(self.text_array) > self.col*i+j:
                    self.__table_array[i][j] = self.text_array[self.col*i+j]
                else:
                    flag = True
                    break

    def print_table(self):
        for i in range(self.row):
            print(self.__table_array[i])

    def correct_table(self):
        for i in range(self.row):
            for j in range(self.col):
                for k in self.words:
                    if k in self.__table_array[i][j]:
                        self.__table_array[i][j] = k
