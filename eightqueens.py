from backtrack import Problem,BackTrack

"""
背景 
    8×8格的国际象棋上
    // 建立8*8的空棋盘
    board = Board(8,8)
步骤
    摆放八个皇后
    // 分成8步摆放
    solution_size = 8

单步可选状态
    // 每行的8个格子
    choices = range(8)
约束
    使其不能互相攻击，即任意两个皇后都不能处于同一行、同一列或同一斜线上
    constraints = [
    check_rows,
    check_cols,
    check_diag,
    ]
问题类型
    问有多少种摆法？ 
    qtype = ALL_SOLUTIONS
    """

# 棋盘是问题实体
class Board(Problem):
    """棋盘对象这里是问题本身"""
    def __init__(self,w,h): 
        self.w = w
        self.h = h
        self.status = [[0 for c in range(w)] for r in range(h)]

class Solution(BackTrack):
    def conflict(self,k):
        """检测第k步 解集与问题域的冲突"""
        for i in range(k): # 遍历前 x[0~k-1]
            if self._solution[i]==self._solution[k] or abs(self._solution[i]-self._solution[k])==abs(i-k):  # 判断是否与 x[k] 冲突
                return True
        return False

    def show(self):
        for s in self.solutions:
            print("-"*20)
            for i in range(self.solution_size):
                print('. ' * (s[i]) + 'X ' + '. '*(self.solution_size-s[i]-1))


if __name__ == '__main__':
    b = Board(5,5)
    s = Solution(b,range(5),5)
    s.dfs()
    s.show()