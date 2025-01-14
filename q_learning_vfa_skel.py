import torch
import torch.nn as nn
import numpy as np
import gymnasium as gym
import json
import tqdm

import random

class CosineActivation(nn.Module):
    def __init__(self):
        super().__init__()

    def forward(self, x):
        return torch.cos(x)

class Estimator(object):
    def __init__(self, state_dim = 4, action_dim = 2, hidden_dim = 100, lr = 0.0001, activation = 'cos'):

        if activation == 'cos':
            activation = CosineActivation()
        elif activation == 'sigmoid':
            activation = torch.nn.Sigmoid()
        elif activation == 'tanh':
            activation = torch.nn.Tanh()

        ## TODO 1: Implement the estimator
        self.criterion = torch.nn.MSELoss()
        self.model = None
        # self.model = ...
        ## END TODO
        
        self._initialize_weights_and_bias(state_dim, hidden_dim)

        self.optimizer = torch.optim.Adam(self.model.parameters(), lr = lr)

    def _initialize_weights_and_bias(self, state_dim = 4, hidden_dim = 100):
        # TODO 2: Initialize the weights and biases of the first layer
        # the first weight is a state_dim x hidden_dim matrix. 
        # Initialize each row with a normal distribution with mean 0 and standard deviation sqrt((i+1) * 0.5), where i is the row index.
        # the bias is uniformly distributed between 0 and 2 pi
        pass
        
    def update(self, state, y):
        y_pred = self.model(torch.Tensor(state))
        loss = self.criterion(y_pred, torch.Tensor(y))
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        return loss.item()

    def predict(self, state):
            with torch.no_grad():
                if self.model is None:
                    return np.zeros((2,))
                return self.model(torch.Tensor(state))

def select_action(state, epsilon, model):
    ## TODO 3: Implement the epsilon-greedy policy
    action = env.action_space.sample()
    # action = ...
    ## END TODO
    return action
            


def q_learning(
    env,
    model,
    episodes,
    decay = False,
    gamma = 0.9,
    epsilon = 0.1,
    eps_decay = 0.9,
):

    total_reward = []
    total_loss = []

    for episode in tqdm.tqdm(range(episodes)):
        state, _ = env.reset()

        done = False
        episode_reward = 0

        while not done:
            action = select_action(state, epsilon, model)
            
            step_res = env.step(action)
            next_state, reward, done, _, _ = step_res
            episode_reward += reward

            # TODO 4: Implement the Q-learning update rule, using the model.predict and model.update functions
            # predict the q values for the current state
            # q_values = ...

            # If the episode is done, the q value for the action taken should be the reward
            if done:
                # q_values = ...
                
                # compute the loss using the model.update() method which also updates the model
                # loss = ...
                total_loss.append(loss)
                break
            
            # otherwise, predict the q values for the next state and use them as the TD target for the update
            # q_values_next = ...
            
            # Set the q value for the action taken to the TD target
            # q_values[action] = reward + gamma * torch.max(q_values_next).item()
            
            # compute the loss using the model.update() which also updates the model
            # loss = ...
            total_loss.append(loss)

            state = next_state

        # Update epsilon
        if decay:
            epsilon = max(epsilon * eps_decay, 0.01)

        total_reward.append(episode_reward)

    return total_reward, total_loss


spec = {
    'activation': 'sigmoid',
    'epsilon': 0.1,
    'gamma': 1.0,
    'alpha': 0.01,
    'episodes': 2000,
    'decay': True
}

if __name__ == '__main__':

    env = gym.make("CartPole-v1")

    estimator = Estimator(
        state_dim = env.observation_space.shape[0],
        action_dim = env.action_space.n,
        hidden_dim = 100,
        lr = spec['alpha']
    )
    reward, total_loss = q_learning(
        env,
        estimator,
        spec['episodes'],
        gamma = spec['gamma'],
        epsilon = spec['epsilon'],
        decay = spec['decay']
    )

    # dump the spec dict into a key value string
    spec_str = '_'.join([f'{k}={v}' for k, v in spec.items()])

    with open(f'dumps/experiment_{spec_str}.json', 'wt') as f:
        json.dump({
            'reward': reward,
            'total_loss': total_loss,
            'spec': spec
            }, f)