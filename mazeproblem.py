from backtrack import Problem,BackTrack
# 给定一个迷宫，入口已知。问是否有路径从入口到出口，若有则输出一条这样的路径。
# 注意移动可以从上、下、左、右、上左、上右、下左、下右八个方向进行。
# 迷宫输入0表示可走，输入1表示墙。为方便起见，用1将迷宫围起来避免边界问题。

# 解的长度是不固定
# solution = []
maze = [[1,1,1,1,1,1,1,1,1,1],
        [0,0,1,0,1,1,1,1,0,1],
        [1,1,0,1,0,1,1,0,1,1],
        [1,0,1,1,1,0,0,1,1,1],
        [1,1,1,0,0,1,1,0,1,1],
        [1,1,0,1,1,1,1,1,0,1],
        [1,0,1,0,0,1,1,1,1,0],
        [1,1,1,1,1,0,1,1,1,1]]

entry = (1,0)

# 如果一个问题的条件太多，就实例化一个Problem的类
p = Problem()
p.maze = maze
p.entry = entry
p.m = len(maze)
p.n = len(maze[0])

META_CHOICES = [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)] # 八个方向


class MazeBackTrack(BackTrack):

    def __init__(self,**kwargs):
        super(MazeBackTrack, self).__init__(**kwargs)
        self._solution.append(self.problem.entry)

    def conflict(self,k):
        x = self._solution[-1][0]
        y = self._solution[-1][1]

        if 0 <= x < self.problem.m and 0 <= y < self.problem.n and self.problem.maze[x][y]==0:
            return False
        return True


    def dfs(self,k=0):
        if (self._solution[k] != self.problem.entry
            and (self._solution[k][0]%(self.problem.m-1)==0 
            or self._solution[k][1]%(self.problem.n-1)==0)):# 出口
            self.solutions.append(self._solution[:])
        else:
            for i in self.choices:
                cur = (self._solution[-1][0]+i[0],self._solution[-1][1]+i[1])
                self._solution.append(cur)
                if not self.conflict(k): # 剪枝
                    self.problem.maze[cur[0]][cur[1]]=2 # 一定要标记来过
                    self.dfs(k+1)
                    self.problem.maze[cur[0]][cur[1]]=0 # 回溯恢复现场

                self._solution.pop()              # 回溯

    def show(self):
        import copy
        from pprint import pprint
        for s in self.solutions:
            print('-'*20)
            maze = copy.deepcopy(self.problem.maze)

            for p in s:
                maze[p[0]][p[1]] = 2

            pprint(maze)


bt = MazeBackTrack(problem=p,choices=META_CHOICES)

bt.dfs()
print(bt.solutions)
bt.show()
