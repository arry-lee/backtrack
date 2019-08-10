# 从图中的一个节点出发，不重复的经过其他所有节点后回到出发节点，
# 称为一条路径，请找出所有可能的路径


# 用邻接表表示图
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

from backtrack import Problem,BackTrack

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
		if k < self.solution_size and self._solution[k] in self._solution[:k]:
			return True

		# 回到出发点
		if k == self.solution_size and self._solution[k] != self._solution[0]:
			return True

		return False

	def dfs(self,k=1):
		if k > self.solution_size:
			print(self._solution)

		else:
			for node in self.problem.graph[self._solution[-1]]:
				self._solution.append(node)
				if not self.conflict(k):
					self.dfs(k+1)
				self._solution.pop()

bt = GraphBackTrack(problem=p,solution_size=n)
bt.dfs()