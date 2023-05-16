#!/usr/bin/env python3

from ComputerNetworkSimulator import *

if __name__ == '__main__':
    gym_env_device_names_simple_file = 'gym_env_text_files/device_names_simple.txt'
    gym_env_device_ports_simple_file = 'gym_env_text_files/device_ports_simple.txt'
    #
    gym_env_port_commands_list_file = 'gym_env_text_files/port_commands_list.txt'
    gym_env_routing_protocols_list_file = 'gym_env_text_files/routing_protocols_list.txt'
    gym_env_routing_commands_list_file = 'gym_env_text_files/routing_commands_list.txt'
    #
    gym_env_ip_subnets_file = 'gym_env_text_files/ip_subnets.txt'
    gym_env_ip_addresses_file = 'gym_env_text_files/ip_addresses.txt'
    # Actions
    gym_env_actions_list_file = 'gym_env_text_files/actions_list.txt'
    gym_env_actions_numbers_list_file = 'gym_env_text_files/actions_numbers_list.txt'
    create_actions_list(gym_env_actions_list_file, gym_env_actions_numbers_list_file, gym_env_device_names_simple_file, gym_env_device_ports_simple_file, gym_env_port_commands_list_file, gym_env_routing_protocols_list_file, gym_env_routing_commands_list_file, gym_env_ip_subnets_file, gym_env_ip_addresses_file)
