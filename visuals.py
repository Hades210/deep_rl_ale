import numpy as np
import matplotlib
matplotlib.use('TKAgg')
from matplotlib import pyplot as plt
import seaborn as sns

class Visuals:

	def __init__(self, actions):

		print("initializing visuals")

		all_action_names = ['no-op', 'fire', 'up', 'right', 'left', 'down', 'up_right', 'up_left', 'down-right', 'down-left', 
			'up-fire', 'right-fire', 'left-fire', 'down-fire', 'up-right-fire', 'up-left-fire', 'down-right-fire', 'down-left-fire']

		action_names = [all_action_names[i] for i in actions]
		self.num_actions = len(actions)
		self.max_q = 1
		# self.max_avg_q = 1

		xlocations = np.linspace(0.5, self.num_actions - 0.5, num=self.num_actions)
		xlocations = np.append(xlocations, self.num_actions + 0.05)
		self.fig = plt.figure()
		self.bars = plt.bar(np.arange(self.num_actions), np.zeros(self.num_actions), 0.9)
		plt.xticks(xlocations, action_names + [''])
		plt.ylabel('Expected Future Reward')
		plt.xlabel('Action')
		plt.title("State-Action Values")
		color_palette = sns.color_palette(n_colors=self.num_actions)
		for bar, color in zip(self.bars, color_palette):
			bar.set_color(color)
		self.fig.show()


	def update(self, q_values):

		for bar, q_value in zip(self.bars, q_values):
			bar.set_height(q_value)
		step_max = np.amax(q_values)
		if step_max > self.max_q:
			self.max_q = step_max
			plt.gca().set_ylim([0, self.max_q])
		self.fig.canvas.draw()