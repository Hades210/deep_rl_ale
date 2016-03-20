import sys
import argparse
from atari_environment import AtariEnvironment
from experience_memory import ExperienceMemory
from q_network import QNetwork
from dqn_agent import DQNAgent
from record_stats import RecordStats
import experiment

if len(sys.argv) < 2:
  print ("Usage: {0} rom_file".format(sys.argv[0]))
  sys.exit()

ROM = str.encode(sys.argv[1])

def main():

	# name type default help choices

	parser = argparse.ArgumentParser()
	parser.add_argument("--epochs", type=int, help="number of epochs", default=200)
	parser.add_argument("--epoch_length", type=int, help="number of steps in an epoch", default=250000)
	parser.add_argument("--test_steps", type=int, help="max number of steps per test", default=125000)
	parser.add_argument("--test_episodes", type=int, help="max number of episodes per test", default=30)
	parser.add_argument("--history_length", type=int, help="number of frames in a state", default=4)
	parser.add_argument("--training_frequency", type=int, help="number of steps run before training", default=4)
	parser.add_argument("--random_exploration_length", type=int, 
		help="number of randomly-generated experiences to initially fill experience memory", default=50000)
	parser.add_argument("--initial_exploration_rate", type=float, help="initial exploration rate", default=1.0)
	parser.add_argument("--final_exploration_rate", type=float, help="final exploration rate from linear annealing", default=0.1)
	parser.add_argument("--final_exploration_frame", type=int, 
		help="frame at which the final exploration rate is reached", default=1000000)
	parser.add_argument("--test_exploration_rate", type=float, help="exploration rate while testing", default=0.05)
	parser.add_argument("--epochs", type=int, help="Number of epochs", default=200)
	parser.add_argument("--epochs", type=int, help="Number of epochs", default=200)
	parser.add_argument("--epochs", type=int, help="Number of epochs", default=200)
	parser.add_argument("--epochs", type=int, help="Number of epochs", default=200)
	parser.add_argument("--epochs", type=int, help="Number of epochs", default=200)
	parser.add_argument("--epochs", type=int, help="Number of epochs", default=200)
	parser.add_argument("--epochs", type=int, help="Number of epochs", default=200)
	args = parser.parse_args()

	# Experiment parameters

	EPOCHS = 200
	EPOCH_LENGTH = 250000
	TEST_STEPS = 125000
	TEST_GAMES = 30

	'''
	EPOCHS = 100
	EPOCH_LENGTH = 50000
	TEST_STEPS = 10000
	TEST_GAMES = 10
	RANDOM_EXPLORATION_LENGTH = 100
	'''

	# Agent parameters
	OBSERVATION_LENGTH = 4
	TRAINING_FREQUENCY = 4
	RANDOM_EXPLORATION_LENGTH = 50000

	INITIAL_EXPLORATION_RATE = 1.0
	FINAL_EXPLORATION_RATE = 0.1
	FINAL_EXPLORATION_FRAME = 1000000
	TEST_EXPLORATION_RATE = 0.05


	# Environment parameters
	FRAME_SKIP = 4
	SCREEN_HEIGHT = 84
	SCREEN_WIDTH = 84
	MAX_START_WAIT = 30
	BUFFER_LENGTH = 2
	BLEND_METHOD = "max"
	REWARD_PROCESSING = "clip"
	SHOW_SCREEN = False


	# Network parameters

	CONV_KERNAL_SHAPES = [
		[8,8,4,32],
		[4,4,32,64],
		[3,3,64,64]]
	CONV_STRIDES = [
		[1,4,4,1],
		[1,2,2,1],
		[1,1,1,1]]
	DENSE_LAYER_SHAPES = [[3136, 512]]
	'''
	CONV_KERNAL_SHAPES = [
		[8,8,4,16],
		[4,4,16,32]]
	CONV_STRIDES = [
		[1,4,4,1],
		[1,2,2,1]]
	DENSE_LAYER_SHAPES = [[2592, 256]]
	'''

	DISCOUNT_FACTOR = 0.99
	LEARNING_RATE = 0.00025
	RMSPROP_DECAY = 0.95
	RMSPROP_CONSTANT = 0.01
	TARGET_UPDATE_FREQUENCY = 10000
	LOAD_MODEL = False


	# Memory parameters

	MEMORY_CAPACITY = 1000000
	BATCH_SIZE = 32

	NAME = 'breakout_test3'
	record_stats = RecordStats(NAME)

	training_emulator = AtariEnvironment(ROM, FRAME_SKIP, OBSERVATION_LENGTH, SCREEN_HEIGHT, SCREEN_WIDTH, 
		BUFFER_LENGTH, BLEND_METHOD, REWARD_PROCESSING, MAX_START_WAIT, record_stats, SHOW_SCREEN)

	testing_emulator = AtariEnvironment(ROM, FRAME_SKIP, OBSERVATION_LENGTH, SCREEN_HEIGHT, SCREEN_WIDTH, 
		BUFFER_LENGTH, BLEND_METHOD, "none", MAX_START_WAIT, None, SHOW_SCREEN)

	NUM_ACTIONS = len(training_emulator.get_possible_actions())

	experience_memory = ExperienceMemory(MEMORY_CAPACITY, OBSERVATION_LENGTH, BATCH_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH, NUM_ACTIONS)

	q_network = QNetwork(CONV_KERNAL_SHAPES, CONV_STRIDES, DENSE_LAYER_SHAPES, NUM_ACTIONS, OBSERVATION_LENGTH, SCREEN_HEIGHT, SCREEN_WIDTH, 
		DISCOUNT_FACTOR, LEARNING_RATE, RMSPROP_DECAY, RMSPROP_CONSTANT, record_stats, LOAD_MODEL, NAME)

	agent = DQNAgent(q_network, training_emulator, experience_memory, OBSERVATION_LENGTH, NUM_ACTIONS, TRAINING_FREQUENCY, RANDOM_EXPLORATION_LENGTH, 
		INITIAL_EXPLORATION_RATE, FINAL_EXPLORATION_RATE, FINAL_EXPLORATION_FRAME, TEST_EXPLORATION_RATE, TARGET_UPDATE_FREQUENCY)

	experiment.run_experiment(agent, EPOCHS, EPOCH_LENGTH, testing_emulator, TEST_STEPS, TEST_GAMES)


if __name__ == "__main__":
    main()