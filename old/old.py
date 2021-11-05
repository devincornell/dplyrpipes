

from typing import List, Callable, Any

class Comp:
	'''Component for a pipeline.
	'''
	def __init__(self, func: Callable, *args, **kwargs):
		self.func = func
		self.args = args
		self.kwargs = kwargs

	def __call__(self, input: Any):
		return self.func(input, *self.args, **self.kwargs)


class Pipeline:
	def __init__(self, components: List[Comp]):
		self.components = components

	def __call__(self, input: Any):
		x = input
		for comp in self.components:
			x = comp(x)
		return x


pipeline = Pipeline([
	Comp(filter, lambda x: x == 1),
	Comp(map, lambda x: x * 2),
])

mylist = [1, 2, 3]
newlist = list(map(pipeline, mylist))


