"""
零一背包问题
"""

# 给定N个物品和一个背包。
# 物品i的重量是Wi,其价值位Vi,背包的容量为C。
# 问应该如何选择装入背包的物品，使得放入背包的物品的总价值为最大

# 显然，放入背包的物品，是N个物品的所有子集的其中之一。
# N个物品中每一个物品，都有选择、不选择两种状态。因此，只需要对每一个物品的这两种状态进行遍历

from backtrack import Problem,BackTrack

p = Problem()
p.n = 3 # 物品数
p.c = 30 #背包容量
p.w = [20,15,15] # 物品重量
p.v = [45,25,25] # 物品价值


solution_size = 3
META_CHOICES = (0,1)
class BagBackTrack(BackTrack):
	"""docstring for BagBackTrack"""
	def __init__(self, **kwarg):
		super(BagBackTrack, self).__init__(**kwarg)
		# self._solution = [0]*self.solution_size
		self.best_solution = None
		self.maxv = 0
		self.maxw = 0


	def conflict(self,k):
		# 目前所有物品超载 zip 是左对齐的
		if sum( x*y for x,y in zip(self.problem.w,self._solution)) > self.problem.c:
			return True
		return False

	def dfs(self,k=0):
		if k==self.solution_size:
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

bt = BagBackTrack(problem=p,solution_size=p.n,choices=META_CHOICES)
bt.dfs()
print(bt.best_solution,bt.maxv,bt.maxw)