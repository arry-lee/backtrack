# 回溯法解题框架

## 引言
任何算法题都可以用暴力法解决，也就是遍历所有情况，而回溯法就是增加了剪枝的暴力美学。
所以回溯法有普适性，脑海里要记住这个解题框架。


## 用法
特此写了一个 BackTrack 算法框架类；和一个辅助类 Problem 用于针对性的传递问题的相关参数。

用法：

1. 实例化一个 p = Problem()
2. 将问题相关的参数传递给 p
3. 针对具体问题继承 BackTrack 类，重写其 dfs 方法 和 conflict 方法。
4. 实例化你的子类 使用三个参数 `problem,choices=None,solution_length=None`
    1. `problem` 代表具体问题
    2. `choices` 代表每个选项，与状态无关的可以赋值，否则要重写 dfs 的 状态空间
    3. `solution_length` 单个解的长度，若为 None 则解长度可变。要重写 dfs 的结束条件
    4. 如果是最优解 则增加 `self.best_solution` 属性和 `self.best_value` 属性

5. 最重要的是分析问题，知道解的形状，以及每个选择的状态空间。

## 源码

```python
class Problem:
    """
    用来传递问题相关参数
    """
    pass
    
        
class BackTrack:
    """
    回溯法解决问题的框架
    """
    def __init__(self,problem,choices=None,solution_length=None):
        self.problem = problem # Problem 的实例或字典
        self.solution_length = solution_length 
        self.choices = choices

        self.solutions = [] # 解集
        self._solution = [] # 解


    def conflict(self,k):
        """
        检测元素k是否与当前状态冲突
        """
        pass
        return False


    def dfs(self,k=0):
        """
        深度优先搜索解
        """
        if k >= self.solution_length:  # 结束条件
            self.solutions.append(self._solution[:]) # 保存（一个解的备份）
        else:
            for i in self.choices: # 遍历元素 a[k] 的两种选择状态:1-选择，0-不选
                self._solution.append(i)
                if not self.conflict(k): # 剪枝
                    self.dfs(k+1)
                self._solution.pop()              # 回溯

    def decode(self):
        """
        对解集进行解码操作
        """
        pass

    def show(self):
        """
        对解集进行可视化操作
        """
        pass
```

## 实例

### 实例一：八皇后问题
8×8格的国际象棋上摆放八个皇后，使其不能互相攻击，即任意两个皇后都不能处于同一行、同一列或同一斜线上，问有多少种摆法？

#### 题解



```python
from backtrack import Problem,BackTrack

P = [[0 for c in range(8)] for r in range(8)] # 没有用到 problem
solution_length = 8 # 解长度
META_CHOICES = [0,1,2,3,4,5,6,7] # 每行位置的状态空间



class EightQueensBackTrack(BackTrack):
    def conflict(self,k):
        for i in range(k):                              # 遍历前 x[0~k-1]
            if self._solution[i]==self._solution[k] or abs(self._solution[i]-self._solution[k])==abs(i-k):  # 判断是否与 x[k] 冲突
                return True
        return False

    def show(self):
        for s in self.solutions:
            print("-"*20)
            for i in range(self.solution_length):
                print('. ' * (s[i]) + 'X ' + '. '*(self.solution_length-s[i]-1))

bt = EightQueensBackTrack(problem=P,solution_length=solution_length,choices=META_CHOICES)

bt.dfs()
bt.show()
```

#### 结果如下

```
. . . . . . . X 
. . . X . . . . 
X . . . . . . . 
. . X . . . . . 
. . . . . X . . 
. X . . . . . . 
. . . . . . X . 
. . . . X . . . 
```

### 实例二：01背包问题
给定N个物品和一个背包。
物品i的重量是Wi,其价值位Vi,背包的容量为C。
问应该如何选择装入背包的物品，使得放入背包的物品的总价值为最大
显然，放入背包的物品，是N个物品的所有子集的其中之一。
N个物品中每一个物品，都有选择、不选择两种状态。因此，只需要对每一个物品的这两种状态进行遍历

#### 题解
```python
from backtrack import Problem,BackTrack

p = Problem()
p.n = 3 # 物品数
p.c = 30 #背包容量
p.w = [20,15,15] # 物品重量
p.v = [45,25,25] # 物品价值


solution_length = 3
META_CHOICES = (0,1)
class BagBackTrack(BackTrack):
	"""docstring for BagBackTrack"""
	def __init__(self, **kwarg):
		super(BagBackTrack, self).__init__(**kwarg)
		# self._solution = [0]*self.solution_length
		self.best_solution = None
		self.maxv = 0
		self.maxw = 0


	def conflict(self,k):
		# 目前所有物品超载 zip 是左对齐的
		if sum( x*y for x,y in zip(self.problem.w,self._solution)) > self.problem.c:
			return True
		return False

	def dfs(self,k=0):
		if k==self.solution_length:
			# 此处检查是否是最优的
			cv = sum( x*y for x,y in zip(self.problem.v,self._solution))
			cw = sum( x*y for x,y in zip(self.problem.w,self._solution))

			if cv > self.maxv: # 价值高的优先
				self.maxv = cv
				self.maxw = cw
				self.best_solution = self._solution[:]

			if cv == self.maxv and cw < self.maxw: # 价值相同重量轻的优先
				self.maxw = cw
				self.best_solution = self._solution[:]

		else:
			for i in self.choices:
				self._solution.append(i) # 选择
				if not self.conflict(k):
					self.dfs(k+1)
				self._solution.pop()     # 撤销选择

bt = BagBackTrack(problem=p,solution_length=p.n,choices=META_CHOICES)
bt.dfs()
print(bt.best_solution,bt.maxv,bt.maxw)
```

#### 结果
输出 `[0, 1, 1] 50 30`

### 迷宫问题
给定一个迷宫，入口已知。问是否有路径从入口到出口，若有则输出一条这样的路径。
注意移动可以从上、下、左、右、上左、上右、下左、下右八个方向进行。
迷宫输入0表示可走，输入1表示墙。为方便起见，用1将迷宫围起来避免边界问题。
解的长度是不固定


#### 题解
```python
from backtrack import Problem,BackTrack

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

```

#### 结果
```
[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
 [2, 2, 1, 2, 1, 1, 1, 1, 0, 1],
 [1, 1, 2, 1, 2, 1, 1, 0, 1, 1],
 [1, 0, 1, 1, 1, 2, 2, 1, 1, 1],
 [1, 1, 1, 0, 0, 1, 1, 2, 1, 1],
 [1, 1, 0, 1, 1, 1, 1, 1, 2, 1],
 [1, 0, 1, 0, 0, 1, 1, 1, 1, 2],
 [1, 1, 1, 1, 1, 0, 1, 1, 1, 1]]
```


### 实例四：有向图的遍历通路
从图中的一个节点出发，不重复的经过其他所有节点后回到出发节点，
称为一条路径，请找出所有可能的路径

```python
# 用邻接表表示图
from backtrack import Problem,BackTrack

n = 6
a,b,c,d,e,f = range(n)
graph = [
	{b,c},
	{c,d,e},
	{a,d},
	{c},
	{f},
	{c,d},
]

p = Problem()
p.graph = graph
p.start = e


class GraphBackTrack(BackTrack):
	"""docstring for GraphBackTrack"""
	def __init__(self, **kwargs):
		super(GraphBackTrack, self).__init__(**kwargs)
		self._solution.append(self.problem.start)

	def conflict(self,k):
		# 第k个节点，是否前面已经走过
		if k < self.solution_length and self._solution[k] in self._solution[:k]:
			return True

		# 回到出发点
		if k == self.solution_length and self._solution[k] != self._solution[0]:
			return True

		return False

	def dfs(self,k=1):
		if k > self.solution_length:
			print(self._solution)

		else:
			for node in self.problem.graph[self._solution[-1]]:
				self._solution.append(node)
				if not self.conflict(k):
					self.dfs(k+1)
				self._solution.pop()

bt = GraphBackTrack(problem=p,solution_length=n)
bt.dfs()
```

#### 结果
输出` [4, 5, 3, 2, 0, 1, 4]`