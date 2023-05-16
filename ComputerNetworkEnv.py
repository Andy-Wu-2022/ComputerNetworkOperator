from gym import spaces
import numpy as np
from ComputerNetworkSimulator import *
import random
from copy import deepcopy
from deepdiff import DeepDiff
from stable_baselines3 import DQN
from sb3_contrib import QRDQN
from stable_baselines3 import DDPG
from stable_baselines3 import TD3
from stable_baselines3 import SAC
import torch as th
from typing import Optional
from stable_baselines3.common.utils import set_random_seed

def make_env(env_vars, simulator_vars, i, seed=0):
    def _init():
        env = ComputerNetworkEnv(env_vars, simulator_vars)
        env.seed(seed + i)
        return env
    set_random_seed(seed)
    return _init

def combine_actions(action_1, action_2, action_r, expert_sampling_rate_1):
    action = []
    j = 0
    for expert_sampling_rate in expert_sampling_rate_1:
        expert_sampling_rate = expert_sampling_rate/100
        p = [expert_sampling_rate*0.5, 1-expert_sampling_rate, expert_sampling_rate*0.5]  # 0.5/0.5
        i = np.random.choice(range(3), p=p)
        if i == 0:
            action.append(action_1[j])
        elif i == 1:
            action.append(action_2[j])
        elif i == 2:
            action.append(action_r[j])
        j += 1
    action = np.array(action, dtype=np.float32)
    return action

class ComputerNetworkEnv(RandomTopo):
    def __init__(self, env_vars, simulator_vars):
        super().__init__(simulator_vars)
        self.env_hyperparameter_replay_enabled, env_hyperparameter_expert_sampling, gym_env_port_01_list_file, gym_env_autosummary_04_list_file, gym_env_version_05_list_file = env_vars
        if env_hyperparameter_expert_sampling == None:
            self.subnets_18_enabled = False  # True: for learn, False: for predict
            self.env_hyperparameter_expert_sampling = [{"episodes": 1, "percentage": 0}]
        else:
            self.subnets_18_enabled = True  # True: for learn, False: for predict
            self.env_hyperparameter_expert_sampling = env_hyperparameter_expert_sampling
        #
        self.num_replay = 0
        self.expert_sampling_list = []
        for d in self.env_hyperparameter_expert_sampling:
            num_1 = d["episodes"]
            num_2 = d["percentage"]
            self.num_replay += num_1
            for i in range(num_1):
                self.expert_sampling_list.append(num_2)
        #
        with open(gym_env_port_01_list_file, "r") as f:
            self.link_status_list = [line.strip() for line in f]
        with open(gym_env_autosummary_04_list_file, "r") as f:
            self.autosummary_status_list = [line.strip() for line in f]
        with open(gym_env_version_05_list_file, "r") as f:
            self.version_status_list = [line.strip() for line in f]
        self.len_link_status_list = len(self.link_status_list)
        self.len_autosummary_status_list = len(self.autosummary_status_list)
        self.len_version_status_list = len(self.version_status_list)
        # gym info
        self.gym_episodes = -2  # training starts at episodes 0
        self.min_gym_devices = 4
        self.max_gym_devices = 10
        self.max_device_properties = 10  # max 9 cables + 1 routing-feature
        self.max_steps = 550
        if self.subnets_18_enabled:
            self.max_steps = 5500
        #
        self.num_1st_actions = 2  # 0: "move" to next position, 1: "configure" using a command
        self.dim_action_space = self.num_1st_actions + self.len_port_commands_list+self.len_routing_commands_list + self.len_ip_addresses_simple+self.len_ip_subnets_simple+1
        self.action_space = spaces.Discrete(self.dim_action_space)
        #self.action_space = spaces.Box(low=0, high=self.dim_action_space-1, shape=(1,), dtype=np.float32)  # for DDPG/TD3/SAC
        #
        self.status_dict = spaces.Dict(
            {
            '01_local_link_status': spaces.Box(low=0, high=self.len_link_status_list-1, shape=(1,), dtype=np.int8),
            '02_local_port_ip': spaces.Box(low=1, high=self.len_ip_addresses_simple, shape=(1,), dtype=np.int8),
            '03_routing_subnets': spaces.Box(low=0, high=self.len_ip_addresses_simple+self.len_ip_subnets_simple, shape=(self.max_num_subnets*2,), dtype=np.int8),
            '04_autosummary_status': spaces.Box(low=0, high=self.len_autosummary_status_list-1, shape=(1,), dtype=np.int8),
            '05_version_status': spaces.Box(low=0, high=self.len_version_status_list-1, shape=(1,), dtype=np.int8)
            }
        )
        self.observation_space = spaces.Dict(
            {
            '01_designed_info': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32),
            '02_current_info': spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)
            }
        )
        self.reset()

    def get_zeros_status_dict(self):
        zeros_status_dict = {}
        for k, v in self.status_dict.items():
            zeros_status_dict[k] = np.zeros(v.shape, dtype=v.dtype)
        return zeros_status_dict

    def text_obs_dict_to_gym_status_dict(self, obs_d):
        gym_status_dict = self.get_zeros_status_dict()
        p = self.gym_positions_list[self.gym_position]
        device_id = p[2]
        cable_name = p[6]
        y = p[1]
        if y == self.num_devices:  # routing features
            subnets = obs_d[device_id]['routing']['subnets']
            subnets_i = [self.to_subnet_index(subnet) for subnet in subnets]
            subnets_i.sort()
            for i, subnet_i in enumerate(subnets_i):
                gym_status_dict['03_routing_subnets'][i] = subnet_i
            if self.num_routing_features >= 2:
                auto_summary = obs_d[device_id]['routing']['auto_summary']
                gym_status_dict['04_autosummary_status'][0] = self.autosummary_status_list.index(auto_summary)
            if self.num_routing_features >= 3:
                version = obs_d[device_id]['routing']['version']
                gym_status_dict['05_version_status'][0] = self.version_status_list.index(version)
        else:  # cable features
            link_status = obs_d[device_id]['cables'][cable_name]['local_port_link_status']
            ip = obs_d[device_id]['cables'][cable_name]['local_port_ip']
            gym_status_dict['01_local_link_status'][0] = self.link_status_list.index(link_status)
            gym_status_dict['02_local_port_ip'][0] = self.to_ip_index(ip)
        return gym_status_dict

    def reset(self):
        self.gym_episodes += 1
        i_replay = self.gym_episodes % self.num_replay
        self.expert_sampling = self.expert_sampling_list[i_replay]
        self.used_actions = []
        self.true_steps = 0  # count all steps
        self.steps = 0  # ignore steps for "move"
        self.substep = self.steps % 3  # substep inside an action
        self.substeps_actions = []
        self.rewards = 0
        self.fixed_faults = 0
        self.steps_on_single_fault = 0  # steps after previous reward
        self.max_steps_on_single_fault = 0
        if self.env_hyperparameter_replay_enabled == False:
            need_topo_init = True
        elif i_replay == 0:
            need_topo_init = True
        else:
            need_topo_init = False
            # revert to initial
            self.current_observation, self.current_correct_actions, self.current_observation_small, self.current_correct_actions_small, self.current_observation_simple, self.current_correct_actions_simple, self.current_correct_actions_simple_indexes, self.faults_list, self.faults_extra_info, self.current_text_obs_dict, self.all_correct_actions_indexes, self.all_wrong_actions_indexes = self.generate_text_observation(deepcopy(self.initial_faults_list), deepcopy(self.initial_faults_extra_info))
            self.current_correct_actions_numbers = [self.actions_numbers_list[i] for i in self.current_correct_actions_simple_indexes]
        while need_topo_init:
            self.subnets_18 = False
            if self.env_hyperparameter_replay_enabled == False:
                if self.subnets_18_enabled:
                    self.subnets_18 = True
            else:
                if self.subnets_18_enabled:
                    self.subnets_18 = True
            #
            self.topo_init()
            need_topo_init = False
        #
        self.data_augmentation = False
        self.data_augmentation_value = 0
        self.gym_moves = 0  # number of steps for "move"
        self.gym_moves_2 = 0
        self.gym_moves_2_done = False
        self.gym_position = self.gym_moves % self.len_gym_positions_list
        self.gym_position_info = self.gym_positions_list[self.gym_position]
        sub_pos = self.gym_position_info[10]
        if sub_pos == 0:
            self.subnets_position_info = {}
        self.re_calculate = True
        self.action_info_12 = 0
        self.reward_multiplier = 1  # not really used, not matter
        self.observation = self._get_observation()
        self.merge_nested_dicts(self.observation)
        self.action_mode = 'all'
        self.actions_list_lock = False
        #
        self.list_ori_actions = []
        self.list_ori_actions_100 = []
        self.expert_sampling_actions_list, self.expert_sampling_actions_list_2 = self.get_expert_sampling_actions_list()  # updated in time
        return self.merge_nested_dicts(self.observation)

    def action_masks(self):  # for maskable PPO only, self.expert_sampling means to get Correct-Actions
        ori_masks, self.masks = self.get_masks(self.substep, self.substeps_actions, self.action_mode, self.expert_sampling)
        return self.masks

    def get_expert_sampling_actions_list(self):
        masks, masks_2 = self.get_masks(self.substep, self.substeps_actions, self.action_mode, 100)
        list_1 = []
        for i in range(self.len_ip_addresses_simple+self.len_ip_subnets_simple+1):
            if masks[i] == True:
                list_1.append(i)
        #
        list_2 = []
        for i in range(self.dim_action_space):
            if masks_2[i] == True:
                list_2.append(i)
        return list_1, list_2

    def get_expert_sampling_action(self):  # for DQN/QRDQN/DDPG/TD3/SAC
        return random.choice(self.expert_sampling_actions_list_2)

    def get_masks(self, substep, substeps_actions, mode, p1):
        if substeps_actions == []:
            substeps_actions = [self.gym_position_info[2], self.gym_position_info[3], 0]
        #
        masks = [[], [], []]
        for i in range(self.num_1st_actions):
            masks[0].append(False)
        for k in range(self.len_port_commands_list+self.len_routing_commands_list+1):
            masks[1].append(False)
        for l in range(self.len_ip_addresses_simple+self.len_ip_subnets_simple+1):
            masks[2].append(False)
        #
        i = -1
        if p1 < 100:
            p1 = p1/100
            p2 = 1-p1
            p = [p1, p2]
            actions_lists_all = [self.current_correct_actions_numbers, self.actions_numbers_list]
            i = np.random.choice(range(len(actions_lists_all)), p=p)
            self.selected_actions_list = actions_lists_all[i]
            self.actions_list_lock = str(i)
        #
        if (i == 0 or p1 == 100) and self.substep == 0:  # expert sampling mode for substep 0
            self.reward_multiplier = 1
            if DeepDiff(self.merged_obs0['01_designed_info'], self.merged_obs0['02_current_info']) == {}:  # move
                masks[0][0] = True
                masks[1][0] = True
                masks[2][0] = True
            else:  # configure
                masks[0][1] = True
                masks[1][0] = True
                masks[2][0] = True
        elif mode == 'all':  # substep 0  # i == 1
            for i in range(self.num_1st_actions):
                masks[0][i] = True
            masks[1][0] = True
            masks[2][0] = True
        elif mode == 'configure':  # substep 1 and 2  # i == -1
            masks[0][1] = True
            if p1 < 100 and self.actions_list_lock != '0':
                masks[1], masks[2] = self.get_last_2_masks(substep+1, substeps_actions, p1)
            else:
                y = self.gym_position_info[1]
                sub_pos = self.gym_position_info[10]
                self.reward_multiplier = 18
                if substep == 1:  # command
                    if y != self.num_devices:  # not routing features
                        if sub_pos == 0:
                            command = 'no shutdown'
                        elif sub_pos == 1:
                            command = 'ip address'
                        command_i = self.to_port_command_index(command)
                    else:  # routing features
                        if sub_pos < 18:
                            if self.merged_obs0['01_designed_info'][0] == 0:
                                command = 'no network'
                            else:
                                command = 'network'
                        elif sub_pos == 18:
                            command = 'no auto-summary'
                            self.reward_multiplier = 32
                        elif sub_pos == 19:
                            command = 'version 2'
                            self.reward_multiplier = 32
                        command_i = self.to_routing_command_index(command)
                    masks[1][command_i] = True
                    masks[2][0] = True
                elif substep == 2:  # var
                    masks[1][substeps_actions[2]] = True
                    if y != self.num_devices:  # not routing features
                        if sub_pos == 0:
                            var = 0
                        elif sub_pos == 1:
                            var = self.observation['01_designed_info']['02_local_port_ip'][0]
                    else:  # routing features
                        if sub_pos < 18:
                            if self.merged_obs0['01_designed_info'][0] == 0:
                                var = self.merged_obs0['02_current_info'][0]
                            else:
                                var = self.merged_obs0['01_designed_info'][0]
                        elif sub_pos == 18:
                            var = 0
                            self.reward_multiplier = 32
                        elif sub_pos == 19:
                            var = 0
                            self.reward_multiplier = 32
                    var = int(round(var))
                    masks[2][var] = True
        #
        masks_1d = []
        for l in range(self.len_ip_addresses_simple+self.len_ip_subnets_simple+1):
            masks_1d.append(False)
        #
        masks_1d_2 = []
        for l in range(self.dim_action_space):
            masks_1d_2.append(False)
        ori_i = []
        i = 0
        for m in masks[substep]:
            if m == True:
                masks_1d[i] = True
                masks_1d_2[self.command_to_action_index(i)] = True
                ori_i.append(i)
            i += 1
        if p1 < 100:
            self.list_ori_actions = ori_i
        else:
            self.list_ori_actions_100 = ori_i
        return np.array(masks_1d), np.array(masks_1d_2)

    def get_last_2_masks(self, substep, substeps_actions, p1):
        if substep > len(substeps_actions):
            print('Error: substep > len(substeps_actions)')
        masks = [[], [], [], []]
        for i in range(self.len_device_names_simple):
            masks[0].append(False)
        for j in range(self.len_device_ports_simple+self.len_routing_protocols_list):
            masks[1].append(False)
        for k in range(self.len_port_commands_list+self.len_routing_commands_list+1):
            masks[2].append(False)
        for l in range(self.len_ip_addresses_simple+self.len_ip_subnets_simple+1):
            masks[3].append(False)
        #
        if p1 == 100:
            list_1 = self.current_correct_actions_numbers
        else:
            list_1 = self.selected_actions_list
        if substep == 2:
            masks[0][substeps_actions[0]] = True
            masks[1][substeps_actions[1]] = True
            valid = False
            for act in list_1:
                if act[0] == substeps_actions[0] and act[1] == substeps_actions[1]:
                    masks[2][act[2]] = True
                    valid = True
            if valid == False:
                masks[2][0] = True
                print('Error: no command to fix this issue in self.current_correct_actions_numbers')
            masks[3][0] = True
        elif substep == 3:
            masks[0][substeps_actions[0]] = True
            masks[1][substeps_actions[1]] = True
            masks[2][substeps_actions[2]] = True
            valid = False
            for act in list_1:
                if act[0] == substeps_actions[0] and act[1] == substeps_actions[1] and act[2] == substeps_actions[2]:
                    masks[3][act[3]] = True
                    valid = True
            if valid == False:
                masks[3][0] = True
                print('Error: no command to fix this issue in self.current_correct_actions_numbers')
        #
        return masks[2], masks[3]

    def get_expert_sampling_rate(self):
        return self.expert_sampling

    def command_to_action_index(self, command):
        if self.substep == 0:
            i = command + self.len_ip_addresses_simple+1 + self.len_port_commands_list+self.len_routing_commands_list
        elif self.substep == 1:
            if command == 0:
                i = 0
            else:
                i = command + self.len_ip_addresses_simple
        elif self.substep == 2:
            if command == 0:
                i = 0
            elif command > self.len_ip_addresses_simple:
                i = command + self.len_port_commands_list+self.len_routing_commands_list+self.num_1st_actions
            else:
                i = command
        return i

    def action_to_command_index(self, action):
        i = -1
        if self.substep == 0:
            i = action - (self.len_ip_addresses_simple+1 + self.len_port_commands_list+self.len_routing_commands_list)
        elif self.substep == 1:
            if action == 0:
                i = 0
            elif action > self.len_ip_addresses_simple:
                i = action-self.len_ip_addresses_simple
        elif self.substep == 2:
            if action == 0:
                i = 0
            elif action > self.len_ip_addresses_simple+self.num_1st_actions + self.len_port_commands_list+self.len_routing_commands_list:
                i = action-(self.num_1st_actions + self.len_port_commands_list+self.len_routing_commands_list)
            elif action > 0 and action <= self.len_ip_addresses_simple:
                i = action
        return i

    def step(self, action):
        action0 = action
        action = self.action_to_command_index(int(round(action, 0)))
        actor_info = 'Checking device: {}, {}.'.format(self.gym_position_info[4], self.gym_position_info[5])
        done = False
        append_action = False
        self.true_steps += 1
        self.steps_on_single_fault += 1
        #
        if action in self.expert_sampling_actions_list:
            reward = 1*self.reward_multiplier
            #
            if self.substep == 0:
                action = [action, 0, 0]
            elif self.substep == 1:
                self.action_info_12 = action
                action = [1, action, 0]
            elif self.substep == 2:
                action = [1, self.action_info_12, action]
            #
            if action[0] == 0:  # move
                self.actions_list_lock = False
                self.action_mode = 'all'
                if not self.data_augmentation or self.data_augmentation_value >= self.len_ip_addresses_simple:
                    self.gym_moves += 1
                    self.data_augmentation = False
                    self.data_augmentation_value = 0
                    self.gym_position = self.gym_moves % self.len_gym_positions_list
                    self.gym_position_info = self.gym_positions_list[self.gym_position]
                    y = self.gym_position_info[1]
                    sub_pos = self.gym_position_info[10]
                    '''# data_augmentation disabled here
                    if self.subnets_18_enabled and y != self.num_devices and sub_pos == 1:
                        self.data_augmentation = True
                        self.data_augmentation_value += 1
                        self.gym_moves_2_done = False
                    '''
                    if self.gym_position_info[10] == 0:
                        self.subnets_position_info = {}
                else:
                    self.gym_moves_2 += 1
                    self.data_augmentation_value += 1
                    self.gym_moves_2_done = False
                self.re_calculate = True
                #
                self.steps_on_single_fault = 0
                actor_info = 'Checking on device: {}, {}.'.format(self.gym_position_info[4], self.gym_position_info[5])
            else:
                actor_info = 'Configure on device: {}, {}. '.format(self.gym_position_info[4], self.gym_position_info[5])
                if self.substep >= 1 and action[1] > 0:
                    actor_info += 'Use command: {}. '.format(self.index_to_command(action[1]))
                if self.substep == 2 and action[2] > 0:
                    actor_info += 'Use {}.'.format(self.index_to_ip_subnet(action[2]))
                elif self.substep == 2 and action[2] == 0:
                    actor_info = 'NA.'
                #
                self.action_mode = 'configure'
                action = [self.gym_position_info[2], self.gym_position_info[3], action[1], action[2]]  # translated configure-action
                self.steps += 1
                self.substep = self.steps % 3
                self.re_calculate = True
                if self.substep == 0:
                    self.action_info_12 = 0
                    self.actions_list_lock = False
                    self.action_mode = 'all'
                    if not self.data_augmentation or self.data_augmentation_value >= self.len_ip_addresses_simple:
                        if action not in self.used_actions:
                            append_action = True
                    if action in self.current_correct_actions_numbers:
                        if self.max_steps_on_single_fault < self.steps_on_single_fault:
                            self.max_steps_on_single_fault = self.steps_on_single_fault
                        self.steps_on_single_fault = 0
                        #
                        self.gym_moves_2_done = True
                        if not self.data_augmentation or self.data_augmentation_value >= self.len_ip_addresses_simple:
                            self.fixed_faults += 1
                            index_1 = self.current_correct_actions_numbers.index(action)
                            del self.faults_list[index_1]
                            del self.faults_extra_info[index_1]
                            self.current_observation, self.current_correct_actions, self.current_observation_small, self.current_correct_actions_small, self.current_observation_simple, self.current_correct_actions_simple, self.current_correct_actions_simple_indexes, self.faults_list, self.faults_extra_info, self.current_text_obs_dict, self.all_correct_actions_indexes, self.all_wrong_actions_indexes = self.generate_text_observation(self.faults_list, self.faults_extra_info)
                            self.re_calculate = True
                            self.current_correct_actions_numbers = [self.actions_numbers_list[i] for i in self.current_correct_actions_simple_indexes]
                    else:
                        print('>>>>>>>> Error: action not in current_correct_actions_numbers:', action)
            self.substeps_actions = action
            self.observation = self._get_observation()
            self.merge_nested_dicts(self.observation)
            self.expert_sampling_actions_list, self.expert_sampling_actions_list_2 = self.get_expert_sampling_actions_list()
        else:
            reward = -1*self.reward_multiplier
            # force move on stuck when self.subnets_18_enabled == False (not for training)
            if self.subnets_18_enabled == False and self.steps_on_single_fault > 10:
                if self.gym_moves <= 235:
                    print(self.merged_obs0)
                    print(self.true_steps, self.steps_on_single_fault, ' | ', self.substep, action, self.expert_sampling_actions_list, action0, ' | ', self.gym_position_info[4], self.gym_position_info[5], '----------->>> Wrong Action Found.')
                #
                self.actions_list_lock = False
                self.action_mode = 'all'
                self.gym_moves += 1
                self.gym_position = self.gym_moves % self.len_gym_positions_list
                self.gym_position_info = self.gym_positions_list[self.gym_position]
                if self.gym_position_info[10] == 0:
                    self.subnets_position_info = {}
                self.re_calculate = True
                #
                if self.max_steps_on_single_fault < self.steps_on_single_fault:
                    self.max_steps_on_single_fault = self.steps_on_single_fault
                self.steps_on_single_fault = 0
                actor_info = 'Force moved on. Checking device: {}, {}.'.format(self.gym_position_info[4], self.gym_position_info[5])
                #
                while self.substep != 0:
                    self.steps -= 1
                    self.substep = self.steps % 3
                    self.rewards -= 1
                self.action_info_12 = 0
                self.observation = self._get_observation()
                self.merge_nested_dicts(self.observation)
                self.expert_sampling_actions_list, self.expert_sampling_actions_list_2 = self.get_expert_sampling_actions_list()
        self.rewards += reward
        if append_action:
            self.used_actions.append(action)
        num_used_actions = len(self.used_actions)
        num_faults = len(self.faults_list)
        if num_faults == 0:
            done = True
        elif self.true_steps >= self.max_steps:
            done = True
        self.gym_info = 'Episode: {}, Correct-Steps: {}/{}, {}, M-S: {}, Reward: {}, Done: {}, T-Rewards: {}, Correct-Actions: {}, Remaining-F: {}, Fixed-F: {}.'.format(self.gym_episodes, self.steps+self.gym_moves+self.gym_moves_2, self.true_steps, int((self.steps+self.gym_moves+self.gym_moves_2)*100/self.true_steps), self.max_steps_on_single_fault, reward, done, int(self.rewards), num_used_actions, num_faults, self.fixed_faults)
        if done:
            print(self.gym_info)
        if self.subnets_18_enabled:
            info_1 = {}
        elif self.true_steps == 1:
            info_1 = {'actor_info': actor_info, 'gym_info': self.gym_info, 'topology_description': self.topo_description_simple, 'network_status': self.initial_observation_simple, 'correct_commands': self.initial_correct_actions_simple}
        else:
            info_1 = {'actor_info': actor_info, 'gym_info': self.gym_info}
        return self.merge_nested_dicts(self._get_observation()), reward, done, info_1

    def render(self, mode='human'):
        print(self.gym_info)

    def to_bits(self, list_numbers, num_bits):  # not in use
        a = []
        for n in list_numbers:
            a.append(1)
            bin_n = bin(n)[2:]
            for _ in range(num_bits - len(bin_n)):
                a.append(0)
            for bn in bin_n:
                a.append(bn)
        return np.array(a, dtype=np.int8)

    def get_subnets_random_seq(self):
        y = self.gym_position_info[1]
        if y != self.num_devices:  # not routing features
            return self.observation['01_designed_info']['03_routing_subnets'], self.observation['02_current_info']['03_routing_subnets']
        subnets_designed = np.trim_zeros(deepcopy(self.observation['01_designed_info']['03_routing_subnets']))
        subnets_current = np.trim_zeros(deepcopy(self.observation['02_current_info']['03_routing_subnets']))
        s_d_random_seq = np.zeros(shape=(self.max_num_subnets*2,), dtype=np.int8)
        s_c_random_seq = np.zeros(shape=(self.max_num_subnets*2,), dtype=np.int8)
        #
        if len(self.subnets_position_info) == 0:
            s_all = deepcopy(subnets_designed)
            for n in subnets_current:
                if n not in s_all:
                    s_all = np.append(s_all, n)
            #
            len_s_all = len(s_all)
            list_1 = random.sample(range(self.max_num_subnets*2), len_s_all)
            for k, v in zip(s_all, list_1):
                self.subnets_position_info[k] = v
        #
        for n in subnets_designed:
            s_d_random_seq[self.subnets_position_info[n]] = n
        for n in subnets_current:
            s_c_random_seq[self.subnets_position_info[n]] = n
        return s_d_random_seq, s_c_random_seq

    def encode_num(self, num1, num2):
        max_substeps = 3
        SEP = 100
        d = 1
        total_numbers = SEP*5 + d*self.len_link_status_list + SEP + d*self.len_ip_addresses_simple + SEP + d*1 + SEP + d*self.len_ip_subnets_simple + SEP + d*self.len_autosummary_status_list + SEP + d*self.len_version_status_list + SEP*5
        y = self.gym_position_info[1]
        sub_pos = self.gym_position_info[10]
        #
        if y != self.num_devices:  # not routing features
            if sub_pos == 0:
                base_num = SEP
            elif sub_pos == 1:
                base_num = SEP + d*self.len_link_status_list + SEP
                num1 -= 1
                num2 -= 1
        else:  # routing features
            if sub_pos < 18:
                base_num = SEP + d*self.len_link_status_list + SEP + d*self.len_ip_addresses_simple + SEP + d*1 + SEP
                if num1 == 0:
                    num1 -= (d*1 + SEP)/d
                    num2 -= 1+self.len_ip_addresses_simple
                elif num2 == 0:
                    num1 -= 1+self.len_ip_addresses_simple
                    num2 -= (d*1 + SEP)/d
            elif sub_pos == 18:
                base_num = SEP + d*self.len_link_status_list + SEP + d*self.len_ip_addresses_simple + SEP + d*1 + SEP + d*self.len_ip_subnets_simple + SEP
            elif sub_pos == 19:
                base_num = SEP + d*self.len_link_status_list + SEP + d*self.len_ip_addresses_simple + SEP + d*1 + SEP + d*self.len_ip_subnets_simple + SEP + d*self.len_autosummary_status_list + SEP
        num1 = base_num + d*num1
        num2 = base_num + d*num2
        e_num1 = np.float32((num1+total_numbers*self.substep)/total_numbers*max_substeps)
        e_num2 = np.float32((num2+total_numbers*self.substep)/total_numbers*max_substeps)
        return e_num1, e_num2

    def merge_nested_dicts(self, obs):
        if self.re_calculate:
            subnets_random_seq_designed, subnets_random_seq_current = self.get_subnets_random_seq()
            d0 = {}
            d = {}
            y = self.gym_position_info[1]
            sub_pos = self.gym_position_info[10]
            if y != self.num_devices:  # not routing features
                if sub_pos == 0:
                    num1 = obs['01_designed_info']['01_local_link_status'][0]
                    num2 = obs['02_current_info']['01_local_link_status'][0]
                elif sub_pos == 1:
                    num1 = obs['01_designed_info']['02_local_port_ip'][0]
                    num2 = obs['02_current_info']['02_local_port_ip'][0]
            else:  # routing features
                if sub_pos < 18:
                    num1 = subnets_random_seq_designed[sub_pos]
                    num2 = subnets_random_seq_current[sub_pos]
                elif sub_pos == 18:
                    num1 = obs['01_designed_info']['04_autosummary_status'][0]
                    num2 = obs['02_current_info']['04_autosummary_status'][0]
                elif sub_pos == 19:
                    num1 = obs['01_designed_info']['05_version_status'][0]
                    num2 = obs['02_current_info']['05_version_status'][0]
            d0['01_designed_info'] = np.array([num1], dtype=np.float32)
            d0['02_current_info'] = np.array([num2], dtype=np.float32)
            d0['11_actions_substep'] = np.array(obs['11_actions_substep'], dtype=np.float32)
            num1, num2 = self.encode_num(num1, num2)
            d['01_designed_info'] = np.array([num1], dtype=np.float32)
            d['02_current_info'] = np.array([num2], dtype=np.float32)
            self.merged_obs0 = d0
            self.merged_obs = d
            self.re_calculate = False
        return self.merged_obs

    def _get_observation(self):
        if self.re_calculate:
            designed_info = self.text_obs_dict_to_gym_status_dict(self.initial_text_obs_dict)
            current_info = self.text_obs_dict_to_gym_status_dict(self.current_text_obs_dict)
            if self.data_augmentation:
                if self.gym_moves_2_done:
                    current_info['02_local_port_ip'][0] = designed_info['02_local_port_ip'][0]
                elif self.data_augmentation_value != designed_info['02_local_port_ip'][0]:
                    current_info['02_local_port_ip'][0] = self.data_augmentation_value
            self.observation = {
            '01_designed_info': designed_info,
            '02_current_info': current_info,
            '11_actions_substep': np.array([self.substep+1], dtype=np.int8),
            '12_configure_using_command': np.array([self.action_info_12], dtype=np.int8)
            }
        return self.observation

class ExpertSamplingDQN(DQN):
    def _sample_action(
        self,
        learning_starts: int,
        action_noise = None,
        n_envs: int = 1,
    ):
        action_1 = np.stack(self.env.env_method("get_expert_sampling_action"))
        action_2, _ = self.predict(self._last_obs, deterministic=True)
        action_r = np.array([self.action_space.sample() for _ in range(n_envs)])
        expert_sampling_rate_1 = np.stack(self.env.env_method("get_expert_sampling_rate"))
        #
        action = combine_actions(action_1, action_2, action_r, expert_sampling_rate_1)
        buffer_action = action
        return action, buffer_action

def quantile_huber_loss_2(
    current_quantiles: th.Tensor,
    target_quantiles: th.Tensor,
    cum_prob: Optional[th.Tensor] = None,
    sum_over_quantiles: bool = True,
) -> th.Tensor:  # modified, use 0.7 and 0.3 as the midpoint for positive and negative rewards (the target_q)
    """
    The quantile-regression loss, as described in the QR-DQN and TQC papers.
    Partially taken from https://github.com/bayesgroup/tqc_pytorch.
    :param current_quantiles: current estimate of quantiles, must be either
        (batch_size, n_quantiles) or (batch_size, n_critics, n_quantiles)
    :param target_quantiles: target of quantiles, must be either (batch_size, n_target_quantiles),
        (batch_size, 1, n_target_quantiles), or (batch_size, n_critics, n_target_quantiles)
    :param cum_prob: cumulative probabilities to calculate quantiles (also called midpoints in QR-DQN paper),
        must be either (batch_size, n_quantiles), (batch_size, 1, n_quantiles), or (batch_size, n_critics, n_quantiles).
        (if None, calculating unit quantiles)
    :param sum_over_quantiles: if summing over the quantile dimension or not
    :return: the loss
    """
    if current_quantiles.ndim != target_quantiles.ndim:
        raise ValueError(
            f"Error: The dimension of curremt_quantile ({current_quantiles.ndim}) needs to match "
            f"the dimension of target_quantiles ({target_quantiles.ndim})."
        )
    if current_quantiles.shape[0] != target_quantiles.shape[0]:
        raise ValueError(
            f"Error: The batch size of curremt_quantile ({current_quantiles.shape[0]}) needs to match "
            f"the batch size of target_quantiles ({target_quantiles.shape[0]})."
        )
    if current_quantiles.ndim not in (2, 3):
        raise ValueError(f"Error: The dimension of current_quantiles ({current_quantiles.ndim}) needs to be either 2 or 3.")

    if cum_prob is None:  # cum_prob not used
        n_quantiles = current_quantiles.shape[-1]
        # Cumulative probabilities to calculate quantiles.
        cum_prob = (th.arange(n_quantiles, device=current_quantiles.device, dtype=th.float) + 0.5) / n_quantiles
        if current_quantiles.ndim == 2:
            # For QR-DQN, current_quantiles have a shape (batch_size, n_quantiles), and make cum_prob
            # broadcastable to (batch_size, n_quantiles, n_target_quantiles)
            cum_prob = cum_prob.view(1, -1, 1)
        elif current_quantiles.ndim == 3:
            # For TQC, current_quantiles have a shape (batch_size, n_critics, n_quantiles), and make cum_prob
            # broadcastable to (batch_size, n_critics, n_quantiles, n_target_quantiles)
            cum_prob = cum_prob.view(1, 1, -1, 1)

    # QR-DQN
    # target_quantiles: (batch_size, n_target_quantiles) -> (batch_size, 1, n_target_quantiles)
    # current_quantiles: (batch_size, n_quantiles) -> (batch_size, n_quantiles, 1)
    # pairwise_delta: (batch_size, n_target_quantiles, n_quantiles)
    # TQC
    # target_quantiles: (batch_size, 1, n_target_quantiles) -> (batch_size, 1, 1, n_target_quantiles)
    # current_quantiles: (batch_size, n_critics, n_quantiles) -> (batch_size, n_critics, n_quantiles, 1)
    # pairwise_delta: (batch_size, n_critics, n_quantiles, n_target_quantiles)
    # Note: in both cases, the loss has the same shape as pairwise_delta

    big_n = 0.9995
    small_n = 0.0005
    high_n = 0.7
    low_n = 0.3
    safe_range = (high_n-low_n)/2*0.7
    target_quantiles = th.where(target_quantiles > 0, high_n, low_n)

    big_or_small_n = target_quantiles.unsqueeze(2).expand(-1, -1, n_quantiles)
    safe_n = th.where(big_or_small_n == high_n, safe_range, -safe_range)
    big_or_small_n = th.where(big_or_small_n == high_n, big_n, small_n)

    pairwise_delta = target_quantiles.unsqueeze(-2) - current_quantiles.unsqueeze(-1)
    pairwise_delta_d = pairwise_delta.detach()
    abs_pairwise_delta = th.abs(pairwise_delta)
    huber_loss = th.where(abs_pairwise_delta > 1, abs_pairwise_delta - 0.5, pairwise_delta**2 * 0.5)
    loss = th.abs(big_or_small_n - (pairwise_delta_d < 0).float()) * huber_loss
    #
    pairwise_delta_safe = (pairwise_delta_d - safe_n).sum(dim=-2).unsqueeze(-1).expand(-1, -1, n_quantiles)
    loss = th.abs(big_or_small_n - (pairwise_delta_safe < 0).float()) * loss
    #
    if sum_over_quantiles:
        loss = loss.sum(dim=-2).mean()
    else:
        loss = loss.mean()
    return loss

class ExpertSamplingQRDQN(QRDQN):
    def _sample_action(
        self,
        learning_starts: int,
        action_noise = None,
        n_envs: int = 1,
    ):
        action_1 = np.stack(self.env.env_method("get_expert_sampling_action"))
        action_2, _ = self.predict(self._last_obs, deterministic=True)
        action_r = np.array([self.action_space.sample() for _ in range(n_envs)])
        expert_sampling_rate_1 = np.stack(self.env.env_method("get_expert_sampling_rate"))
        #
        action = combine_actions(action_1, action_2, action_r, expert_sampling_rate_1)
        buffer_action = action
        return action, buffer_action

    def train(self, gradient_steps: int, batch_size: int = 100) -> None:
        # Switch to train mode (this affects batch norm / dropout)
        self.policy.set_training_mode(True)
        # Update learning rate according to schedule
        self._update_learning_rate(self.policy.optimizer)

        losses = []
        for _ in range(gradient_steps):
            # Sample replay buffer
            replay_data = self.replay_buffer.sample(batch_size, env=self._vec_normalize_env)  # type: ignore[union-attr]

            # Get current quantile estimates
            current_quantiles = self.quantile_net(replay_data.observations)

            # Make "n_quantiles" copies of actions, and reshape to (batch_size, n_quantiles, 1).
            actions = replay_data.actions[..., None].long().expand(batch_size, self.n_quantiles, 1)
            # Retrieve the quantiles for the actions from the replay buffer
            current_quantiles = th.gather(current_quantiles, dim=2, index=actions).squeeze(dim=2)

            with th.no_grad():  # not using target NN, force gamma == 0
                target_quantiles = replay_data.rewards + 0 * current_quantiles  # original reward

            # Compute Quantile Huber loss, summing over a quantile dimension as in the paper.
            loss = quantile_huber_loss_2(current_quantiles, target_quantiles, sum_over_quantiles=True)
            losses.append(loss.item())

            # Optimize the policy
            self.policy.optimizer.zero_grad()
            loss.backward()
            # Clip gradient norm
            if self.max_grad_norm is not None:
                th.nn.utils.clip_grad_norm_(self.policy.parameters(), self.max_grad_norm)
            self.policy.optimizer.step()

        # Increase update counter
        self._n_updates += gradient_steps

        self.logger.record("train/n_updates", self._n_updates, exclude="tensorboard")
        self.logger.record("train/loss", np.mean(losses))

class ExpertSamplingDDPG(DDPG):
    def _sample_action(
        self,
        learning_starts: int,
        action_noise = None,
        n_envs: int = 1,
    ):
        action_1 = np.stack(self.env.env_method("get_expert_sampling_action"))
        action_2, _ = self.predict(self._last_obs, deterministic=True)
        action_r = np.array([self.action_space.sample() for _ in range(n_envs)])
        num_env = len(action_1)
        action_2 = action_2.reshape((1, num_env))[0]
        action_r = action_r.reshape((1, num_env))[0]
        expert_sampling_rate_1 = np.stack(self.env.env_method("get_expert_sampling_rate"))
        #
        action = combine_actions(action_1, action_2, action_r, expert_sampling_rate_1)
        buffer_action = action
        return action, buffer_action

class ExpertSamplingTD3(TD3):
    def _sample_action(
        self,
        learning_starts: int,
        action_noise = None,
        n_envs: int = 1,
    ):
        action_1 = np.stack(self.env.env_method("get_expert_sampling_action"))
        action_2, _ = self.predict(self._last_obs, deterministic=True)
        action_r = np.array([self.action_space.sample() for _ in range(n_envs)])
        num_env = len(action_1)
        action_2 = action_2.reshape((1, num_env))[0]
        action_r = action_r.reshape((1, num_env))[0]
        expert_sampling_rate_1 = np.stack(self.env.env_method("get_expert_sampling_rate"))
        #
        action = combine_actions(action_1, action_2, action_r, expert_sampling_rate_1)
        buffer_action = action
        return action, buffer_action

class ExpertSamplingSAC(SAC):
    def _sample_action(
        self,
        learning_starts: int,
        action_noise = None,
        n_envs: int = 1,
    ):
        action_1 = np.stack(self.env.env_method("get_expert_sampling_action"))
        action_2, _ = self.predict(self._last_obs, deterministic=True)
        action_r = np.array([self.action_space.sample() for _ in range(n_envs)])
        num_env = len(action_1)
        action_2 = action_2.reshape((1, num_env))[0]
        action_r = action_r.reshape((1, num_env))[0]
        expert_sampling_rate_1 = np.stack(self.env.env_method("get_expert_sampling_rate"))
        #
        action = combine_actions(action_1, action_2, action_r, expert_sampling_rate_1)
        buffer_action = action
        return action, buffer_action
