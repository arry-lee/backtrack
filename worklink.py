
# 欧拉路关系，要使得一个图形可以一笔画完，必须满足如下两个条件：

# 图形必须是连通的不能有孤立的点。
# 图中拥有奇数连接边的点必须是0或2。

from collections import defaultdict
from backtrack import Problem,BackTrack

def circle(wordlist):
	"""建立邻接表"""
	worddict = defaultdict(list)
	worddict1 = defaultdict(list)
	for word in wordlist:
		worddict[word[0]].append(word)
		worddict[word].append(word[-1])

	for word in wordlist:
		worddict1[word] = worddict[word[-1]]
	return worddict1

# 有向有环带权图
class GraphBackTrack(BackTrack):
	"""
	回溯法作图
	"""
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
			self.best_solution = self._solution[:]

		else:
			for node in self.problem.graph[self._solution[-1]]:
				self._solution.append(node)
				if not self.conflict(k):
					self.dfs(k+1)
				self._solution.pop()

wordlist = ['abc','cde','efg','ghi','ija']
worddict = circle(wordlist)
print(worddict)

p = Problem()
p.graph = worddict
p.start = wordlist[0]
n = len(wordlist)

bt = GraphBackTrack(problem=p,solution_size=n)
bt.dfs()
print(bt.best_solution)