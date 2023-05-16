#!/usr/bin/env python3

from stable_baselines3.common.vec_env.subproc_vec_env import SubprocVecEnv
from ComputerNetworkEnv import *

if __name__ == '__main__':
    gym_env_device_names_file = 'gym_env_text_files/device_names.txt'
    gym_env_device_names_simple_file = 'gym_env_text_files/device_names_simple.txt'
    #
    gym_env_device_ports_types_file = 'gym_env_text_files/device_ports_types.txt'
    gym_env_device_ports_numbers_file = 'gym_env_text_files/device_ports_numbers.txt'
    gym_env_device_ports_simple_file = 'gym_env_text_files/device_ports_simple.txt'
    #
    gym_env_port_commands_list_file = 'gym_env_text_files/port_commands_list.txt'
    gym_env_routing_protocols_list_file = 'gym_env_text_files/routing_protocols_list.txt'
    gym_env_routing_commands_list_file = 'gym_env_text_files/routing_commands_list.txt'
    #
    gym_env_ip_subnets_file = 'gym_env_text_files/ip_subnets.txt'
    gym_env_ip_addresses_file = 'gym_env_text_files/ip_addresses.txt'
    gym_env_ip_subnets_train_file = 'gym_env_text_files/ip_subnets_train.txt'
    gym_env_ip_addresses_train_file = 'gym_env_text_files/ip_addresses_train.txt'
    gym_env_ip_subnets_test_file = 'gym_env_text_files/ip_subnets_test.txt'
    gym_env_ip_addresses_test_file = 'gym_env_text_files/ip_addresses_test.txt'
    #
    gym_env_port_01_list_file = 'gym_env_text_files/01_port_status_list.txt'
    gym_env_autosummary_04_list_file = 'gym_env_text_files/04_auto_summary_status_list.txt'
    gym_env_version_05_list_file = 'gym_env_text_files/05_version_status_list.txt'
    # Actions
    gym_env_actions_list_file = 'gym_env_text_files/actions_list.txt'
    gym_env_actions_numbers_list_file = 'gym_env_text_files/actions_numbers_list.txt'

    # Simulator Hyper parameters
    num_devices = 10  # if None, will generate a random number [4-10]. Can also be a fixed number of [4-10]
    faults_types_inserted = {'port_down': True, 'wrong_ip': True, 'extra_subnet': True, 'missing_subnet': True, 'network_summary_issue': True, 'protocol_version_mismatch': True}
    ips_subnets_dataset = 'train'  # use 'train' or 'test' dataset. This Feature is Disabled now, will always use full data

    # Env Hyper parameters
    env_hyperparameter_replay_enabled = False  # when True, env will re-use a certain episode multiple times (as indicated in env_hyperparameter_expert_sampling). For example: episodes 0 ~ 4 can be identical if the env re-use it for 5 times. When 'False', will generate a New episode every time to increase diversity.
    #
    # algorithms (maskablePPO/ExpertSampling-QRDQN/DQN/TD3/DDPG/SAC) support env_hyperparameter_expert_sampling. values ignored for other algorithms.
    #
    # env_hyperparameter_expert_sampling = [{"episodes": 1, "percentage": 100}, {"episodes": 2, "percentage": 70}, {"episodes": 2, "percentage": 30}, {"episodes": 2, "percentage": 3}]  # a list of Dicts, can contain any number of Dicts, such as: [{"episodes": 3, "percentage": 70}, ...], it controls how a specific network-topology is repeated (when env_hyperparameter_replay_enabled = True) and how much percentage the (expert_sampling actions) are injected. For {"episodes": 3, "percentage": 70}, it means the same network-topology is repeated 3 times with 70% expert samples. After iterate all the Dicts in this list, the next episode will be generated as a NEW random network-topology. IMPORTANT: for maskablePPO the "percentage" is used to inject Correct-Actions, for other algorithms, the injected actions are Half-correct and Half-wrong (to increase diversity)
    #
    # env_hyperparameter_expert_sampling = None  # Note: disable it when use model.predict
    #
    env_hyperparameter_expert_sampling = [{"episodes": 1, "percentage": 80}]  # For ExpertSamplingQRDQN, will inject 40% correct actions and 40% wrong actions, the remaining 20% actions will be from the QRDQN-NN

    # num_envs = 128  # multiprocessing
    num_envs = 1

    # make_env
    env_vars = [env_hyperparameter_replay_enabled, env_hyperparameter_expert_sampling, gym_env_port_01_list_file, gym_env_autosummary_04_list_file, gym_env_version_05_list_file]
    #
    simulator_vars = [num_devices, ips_subnets_dataset, gym_env_actions_list_file, gym_env_actions_numbers_list_file, gym_env_port_commands_list_file, gym_env_routing_protocols_list_file, gym_env_routing_commands_list_file, gym_env_device_names_file, gym_env_device_names_simple_file, gym_env_device_ports_types_file, gym_env_device_ports_numbers_file, gym_env_device_ports_simple_file, gym_env_ip_subnets_file, gym_env_ip_addresses_file, gym_env_ip_subnets_train_file, gym_env_ip_addresses_train_file, gym_env_ip_subnets_test_file, gym_env_ip_addresses_test_file, faults_types_inserted]
    #
    topology_envs = SubprocVecEnv([make_env(env_vars, simulator_vars, i) for i in range(num_envs)])

    # Load or Define the model
    # Note: parameters below are for demo purpose, not for real-training
    policy_kwargs = dict(net_arch=[64, 64], n_quantiles=7)
    model = ExpertSamplingQRDQN("MultiInputPolicy", topology_envs, train_freq=512, learning_rate=1e-4, tau=1, gamma=0, batch_size=9, gradient_steps=50, max_grad_norm=5, buffer_size=10000, policy_kwargs=policy_kwargs, target_update_interval=10000, verbose=1)
    # print(model.policy)
    #
    #model = ExpertSamplingQRDQN.load("trained_model", topology_envs, train_freq=512, learning_rate=1e-4, tau=1, gamma=0, batch_size=9, gradient_steps=50, max_grad_norm=5, buffer_size=10000, target_update_interval=10000, verbose=1)

    for i in range(100):
        if i >= 0:  # start from 0
            print('start '+str(i)+' ---------------------------#############################')
            model.learn(total_timesteps=int(1e6))
            #
            model.train(100000, 9)  # extra training as needed
            #
            # Save the trained model and replay_buffer
            #model.save_replay_buffer(str(i)+".pickle")
            model.save("trained_model")
