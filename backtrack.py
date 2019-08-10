
class Problem(object):
    """问题对象基类"""

class BackTrack:
    """
    回溯法解决问题的框架
    """
    def __init__(self,problem,choices=None,solution_size=None):
        self.problem = problem # Problem 的实例
        self.solution_size = solution_size 
        self.choices = choices

        self.solutions = [] # 解集
        self._solution = [] # 解


    def conflict(self,k):
        """
        检测元素k是否与当前状态冲突
        """
        return False


    def dfs(self,k=0):
        """
        深度优先搜索解
        """
        if k >= self.solution_size:    # 结束条件
            self.solutions.append(self._solution[:]) # 保存（一个解的备份）
        else:
            for choice in self.choices:  # 遍历元素 a[k] 的所有选择状态
                self._solution.append(choice)

                if not self.conflict(k): # 剪枝
                    self.dfs(k+1)

                self._solution.pop()     # 回溯


    def solve(self):
        self.dfs()
        return self.solutions