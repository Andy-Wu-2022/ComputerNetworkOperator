import gym
import random
from copy import deepcopy

def create_actions_list(gym_env_actions_list_file, gym_env_actions_numbers_list_file, gym_env_device_names_simple_file, gym_env_device_ports_simple_file, gym_env_port_commands_list_file, gym_env_routing_protocols_list_file, gym_env_routing_commands_list_file, gym_env_ip_subnets_file, gym_env_ip_addresses_file):
    with open(gym_env_device_names_simple_file, "r") as f:
        device_names_simple = [line.strip() for line in f]
    with open(gym_env_device_ports_simple_file, "r") as f:
        device_ports_simple = [line.strip() for line in f]
    with open(gym_env_port_commands_list_file, "r") as f:
        port_commands_list = [line.strip() for line in f]
    with open(gym_env_routing_protocols_list_file, "r") as f:
        routing_protocols_list = [line.strip() for line in f]
    with open(gym_env_routing_commands_list_file, "r") as f:
        routing_commands_list = [line.strip() for line in f]
    with open(gym_env_ip_subnets_file, "r") as f:
        ip_subnets = [line.strip() for line in f]
    with open(gym_env_ip_addresses_file, "r") as f:
        ip_addresses = [line.strip() for line in f]
    with open(gym_env_actions_list_file, 'w') as file, open(gym_env_actions_numbers_list_file, 'w') as f_num:
        i = 0
        for device in device_names_simple:
            j = 0
            for port in device_ports_simple:
                k = 1
                for command in port_commands_list:
                    if command == 'ip address':
                        l = 1
                        for ip in ip_addresses:
                            text = command_to_text(device, port, command)
                            file.write(text + ' ' + ip + '\n')
                            f_num.write(str([i, j, k, l]) + '\n')
                            l += 1
                    else:
                        text = command_to_text(device, port, command)
                        file.write(text + '\n')
                        f_num.write(str([i, j, k, 0]) + '\n')
                    k += 1
                j += 1
            i += 1
        j_pre = j
        k_pre = k
        l_pre = l
        i = 0
        for device in device_names_simple:
            j = j_pre
            for protocol in routing_protocols_list:
                k = k_pre
                for command in routing_commands_list:
                    if 'network' in command:
                        l = l_pre
                        for subnet in ip_subnets:
                            text = command_to_text(device, protocol, command)
                            file.write(text + ' ' + subnet + '\n')
                            f_num.write(str([i, j, k, l]) + '\n')
                            l += 1
                    else:
                        if 'rip' in protocol:
                            text = command_to_text(device, protocol, command)
                            file.write(text + '\n')
                            f_num.write(str([i, j, k, 0]) + '\n')
                        elif 'eigrp' in protocol and 'version' not in command:
                            text = command_to_text(device, protocol, command)
                            file.write(text + '\n')
                            f_num.write(str([i, j, k, 0]) + '\n')
                    k += 1
                j += 1
            i += 1

def command_to_text(device, feature, command):
    text = device + ', ' + feature + ', ' + command
    return text

def create_vocabulary_text_file(file_path):
    with open(file_path, 'w') as file:
        file.write('[UNK]\n')
        file.write('[SEP]\n')
        file.write('NA\n')

def update_vocabulary(vocabulary_file, text_file):
    with open(vocabulary_file, 'a+') as f_vocab, open(text_file, 'r') as f_text:
        # read the existing vocabulary into a set
        existing_words = set(line.strip() for line in f_vocab)
        # iterate over each word in the text file and add it to the vocabulary file if it's not already there
        for line in f_text:
            words = line2words(line)
            for word in words:
                word = word.strip()
                if word not in existing_words:
                    f_vocab.write(word + '\n')
                    existing_words.add(word)

def line2words(line):
    words = line.replace('[UNK]', ' [UNK] ').replace('[SEP]', ' [SEP] ').replace('#', ' # ').replace('/', ' / ').replace(',', ' , ').replace('.', ' . ').replace(':', ' : ').strip().split()
    return words

def count_words(line):
    words = line2words(line)
    return len(words)

class RandomTopo(gym.Env):
    def __init__(self, simulator_vars):
        initial_num_devices, self.ips_subnets_dataset, gym_env_actions_list_file, gym_env_actions_numbers_list_file, gym_env_port_commands_list_file, gym_env_routing_protocols_list_file, gym_env_routing_commands_list_file, gym_env_device_names_file, gym_env_device_names_simple_file, gym_env_device_ports_types_file, gym_env_device_ports_numbers_file, gym_env_device_ports_simple_file, gym_env_ip_subnets_file, gym_env_ip_addresses_file, gym_env_ip_subnets_train_file, gym_env_ip_addresses_train_file, gym_env_ip_subnets_test_file, gym_env_ip_addresses_test_file, self.faults_types_inserted = simulator_vars
        self.subnets_18 = False  # will be reset by ComputerNetworkEnv()
        #
        with open(gym_env_actions_list_file, "r") as f:
            self.actions_list = [line.strip() for line in f]
        with open(gym_env_actions_numbers_list_file, "r") as f:
            self.actions_numbers_list = [eval(line.strip()) for line in f]
        with open(gym_env_port_commands_list_file, "r") as f:
            self.port_commands_list = [line.strip() for line in f]
        with open(gym_env_routing_protocols_list_file, "r") as f:
            self.routing_protocols_list = [line.strip() for line in f]
        with open(gym_env_routing_commands_list_file, "r") as f:
            self.routing_commands_list = [line.strip() for line in f]
        with open(gym_env_device_names_file, "r") as f:
            self.device_names = [line.strip() for line in f]
        with open(gym_env_device_names_simple_file, "r") as f:
            self.device_names_simple = [line.strip() for line in f]
        with open(gym_env_device_ports_types_file, "r") as f:
            self.device_ports_types = [line.strip() for line in f]
        with open(gym_env_device_ports_numbers_file, "r") as f:
            self.device_ports_numbers = [line.strip() for line in f]
        with open(gym_env_device_ports_simple_file, "r") as f:
            self.device_ports_simple = [line.strip() for line in f]
        with open(gym_env_ip_subnets_file, "r") as f:
            self.ip_subnets_simple = [line.strip() for line in f]
        with open(gym_env_ip_addresses_file, "r") as f:
            self.ip_addresses_simple = [line.strip() for line in f]
        with open(gym_env_ip_subnets_train_file, "r") as f:
            self.ip_subnets_simple_train = [line.strip() for line in f]
        with open(gym_env_ip_addresses_train_file, "r") as f:
            self.ip_addresses_simple_train = [line.strip() for line in f]
        with open(gym_env_ip_subnets_test_file, "r") as f:
            self.ip_subnets_simple_test = [line.strip() for line in f]
        with open(gym_env_ip_addresses_test_file, "r") as f:
            self.ip_addresses_simple_test = [line.strip() for line in f]
        #
        self.ip_subnets_simple_seq = self.ip_subnets_simple
        self.ip_addresses_simple_seq = self.ip_addresses_simple
        # train on complete datesets
        self.ip_subnets_simple_train = deepcopy(self.ip_subnets_simple)
        self.ip_addresses_simple_train = deepcopy(self.ip_addresses_simple)
        #
        self.num_actions = len(self.actions_list)
        self.initial_num_devices = initial_num_devices
        #
        self.len_ip_subnets_simple = len(self.ip_subnets_simple)
        self.len_ip_addresses_simple = len(self.ip_addresses_simple)
        self.len_port_commands_list = len(self.port_commands_list)
        self.len_routing_commands_list = len(self.routing_commands_list)
        self.len_device_names_simple = len(self.device_names_simple)
        self.len_device_ports_simple = len(self.device_ports_simple)
        self.len_routing_protocols_list = len(self.routing_protocols_list)
        #
        self.topo_init()

    def topo_init(self):
        self.routing_protocol = random.choice(self.routing_protocols_list)
        if self.subnets_18 == True:
            self.initial_num_devices = 10
            self.routing_protocol = 'router rip'  # to maximize faults for training
        #
        if self.initial_num_devices == None:
            self.num_devices = random.randint(4, 10)
        else:
            if self.initial_num_devices > 10:
                self.initial_num_devices = 10
                print('Error: num_devices > 10, use 10 instead.')
            self.num_devices = self.initial_num_devices
        num_devices = self.num_devices
        num_subnets = num_devices - 1
        self.num_subnets = num_subnets
        self.max_num_subnets = 9  # 10(max num_devices)-1
        self.ids, self.names_simple = self.generate_simple_names()
        self.names = random.sample(self.device_names, self.num_devices)
        #
        if num_devices == 4:
            self.num_inserted_faults = 24
        else:
            list_1 = list(range(25, 33))
            self.num_inserted_faults = random.choice(list_1)
        self.IP_num_1 = random.sample(list(range(1, 127)), 50)  # class A IP range
        self.IP_num_2 = random.sample(list(range(1, 255)), 50)
        self.IP_num_3 = random.sample(list(range(1, 255)), 50)
        IP_num_4 = random.sample(list(range(1, 128)), 50)
        self.IP_num_4 = [x * 2 - 1 for x in IP_num_4]
        self.IP_num_1_correct = self.IP_num_1[0:num_subnets]
        self.IP_num_1_wrong = self.IP_num_1[num_subnets:num_subnets*2]
        self.IP_num_2_correct = self.IP_num_2[0:num_subnets]
        self.IP_num_2_wrong = self.IP_num_2[num_subnets:num_subnets*2]
        self.IP_num_3_correct = self.IP_num_3[0:num_subnets]
        self.IP_num_3_wrong = self.IP_num_3[num_subnets:num_subnets*2]
        self.IP_num_4_correct = self.IP_num_4[0:num_subnets]
        self.IP_num_4_wrong = self.IP_num_4[num_subnets:num_subnets*2]
        self.subnets_correct, self.subnets_wrong, self.IPs_correct, self.IPs_wrong = self.generate_subnets()
        random.shuffle(self.ip_subnets_simple_train)
        random.shuffle(self.ip_addresses_simple_train)
        random.shuffle(self.ip_subnets_simple_test)
        random.shuffle(self.ip_addresses_simple_test)
        if self.ips_subnets_dataset == 'train':
            self.subnets_simple_correct = self.ip_subnets_simple_train[0:num_subnets]
            self.subnets_simple_wrong = self.ip_subnets_simple_train[num_subnets:num_subnets*2]
            self.IPs_simple_correct = self.ip_addresses_simple_train[0:num_subnets*2]
            self.IPs_simple_wrong = self.ip_addresses_simple_train[num_subnets*2:num_subnets*4]
        elif self.ips_subnets_dataset == 'test':
            self.subnets_simple_correct = self.ip_subnets_simple_test[0:num_subnets]
            self.subnets_simple_wrong = self.ip_subnets_simple_test[num_subnets:num_subnets*2]
            self.IPs_simple_correct = self.ip_addresses_simple_test[0:num_subnets*2]
            self.IPs_simple_wrong = self.ip_addresses_simple_test[num_subnets*2:num_subnets*4]
        else:
            print('Error: ips_subnets_dataset must be (train OR test)')
        #
        self.num_routing_features = 1
        num_possible_faults = num_subnets*2*2 + num_subnets*2*2  # types of faults: int-down|ip-wrong and have-wrong-subnet|no-correct-subnet
        if 'ospf' not in self.routing_protocol:
            self.num_routing_features += 1
            num_possible_faults = num_possible_faults + num_devices  # add auto-summary-issue
            if 'rip' in self.routing_protocol:
                self.num_routing_features += 1
                num_possible_faults = num_possible_faults + num_devices  # add version-issue
        self.num_possible_faults = num_possible_faults
        if self.subnets_18 == True:
            self.num_inserted_faults = num_possible_faults  # full faults to keep total rewards similar
        self.initial_faults_list = random.sample(list(range(num_possible_faults)), self.num_inserted_faults)
        self.initial_faults_extra_info = ['' for i in self.initial_faults_list]
        #
        self.connections, self.connections_un_ordered = self.generate_connections()
        self.connections_oneway = self.get_connections_oneway()
        self.leaf_devices, self.num_leaf_devices = self.get_leaf_devices()
        self.ports_type = random.choice(self.device_ports_types)
        self.ports, self.ports_simple, self.ports_oneway, self.ports_simple_oneway = self.generate_ports()
        # topo_description: to describe the randomly generated network
        # _simple: use IP-Address-32 instead of real IP numbers
        # _small: a small/short version of text for future use
        self.mapped_subnets_correct, self.mapped_subnets_wrong, self.mapped_IPs_correct, self.mapped_IPs_wrong, self.mapped_subnets_simple_correct, self.mapped_subnets_simple_wrong, self.mapped_IPs_simple_correct, self.mapped_IPs_simple_wrong, self.topo_description, self.topo_description_small, self.topo_description_simple = self.map_devices_subnets_ips()
        self.small_actions_list = self.get_small_actions_list()
        self.num_small_actions = len(self.small_actions_list)
        # init text observation dict
        self.initial_text_obs_dict = self.generate_initial_text_obs_dict()  # the dict format network design/requirements
        for fault_type, enabled in self.faults_types_inserted.items():
            if not enabled:
                for fault in self.faults_types_lists[fault_type]:
                    if fault in self.initial_faults_list:
                        index_1 = self.initial_faults_list.index(fault)
                        del self.initial_faults_list[index_1]
                        del self.initial_faults_extra_info[index_1]
        # initial_observation: the network status of ports and routing-features
        # initial_correct_actions: commands to fix faults
        # _simple: use IP-Address-32 instead of real IP numbers
        # _small: a small/short version of text for future use
        self.initial_observation, self.initial_correct_actions, self.initial_observation_small, self.initial_correct_actions_small, self.initial_observation_simple, self.initial_correct_actions_simple, self.initial_correct_actions_simple_indexes, self.faults_list, self.faults_extra_info, self.current_text_obs_dict, self.all_correct_actions_indexes, self.all_wrong_actions_indexes = self.generate_text_observation(deepcopy(self.initial_faults_list), deepcopy(self.initial_faults_extra_info))
        self.num_inserted_faults = len(self.initial_faults_list)  # update it here after generate_text_observation()
        self.subnets_18 = False  # swith it off here
        self.current_observation_simple = deepcopy(self.initial_observation_simple)
        self.current_correct_actions_simple_indexes = deepcopy(self.initial_correct_actions_simple_indexes)
        #
        self.current_correct_actions_numbers = [self.actions_numbers_list[i] for i in self.current_correct_actions_simple_indexes]
        self.all_correct_actions_numbers = [self.actions_numbers_list[i] for i in self.all_correct_actions_indexes]
        self.all_wrong_actions_numbers = [self.actions_numbers_list[i] for i in self.all_wrong_actions_indexes]
        #
        self.len_initial_observation = count_words(self.initial_observation)
        self.len_initial_correct_actions = count_words(self.initial_correct_actions)
        self.len_initial_observation_small = count_words(self.initial_observation_small)
        self.len_initial_correct_actions_small = count_words(self.initial_correct_actions_small)
        self.len_initial_observation_simple = count_words(self.initial_observation_simple)
        self.len_initial_correct_actions_simple = count_words(self.initial_correct_actions_simple)
        self.len_topo_description = count_words(self.topo_description)
        self.len_topo_description_small = count_words(self.topo_description_small)
        self.len_topo_description_simple = count_words(self.topo_description_simple)
        self.total_gym_tokens = self.len_topo_description_simple + self.len_initial_observation_simple
        self.num_tokens = [self.len_topo_description, self.len_initial_observation, self.len_initial_correct_actions, self.len_topo_description_simple, self.len_initial_observation_simple, self.len_initial_correct_actions_simple, self.num_devices, self.len_topo_description_small, self.len_initial_observation_small, self.len_initial_correct_actions_small, self.num_actions, self.total_gym_tokens]

    def topo_info(self):
        topo = {}
        topo['topo_description'] = self.topo_description
        topo['topo_description_simple'] = self.topo_description_simple
        topo['topo_description_small'] = self.topo_description_small
        topo['num_devices'] = self.num_devices
        topo['num_leaf_devices'] = self.num_leaf_devices
        topo['ports_type'] = self.ports_type
        topo['routing_protocol'] = self.routing_protocol
        topo['num_inserted_faults'] = self.num_inserted_faults
        topo['initial_faults_list'] = self.initial_faults_list
        topo['num_actions'] = self.num_actions
        topo['devices_ids'] = self.ids
        topo['names'] = self.names
        topo['names_simple'] = self.names_simple
        topo['leaf_devices'] = self.leaf_devices
        topo['connections_un_ordered'] = self.connections_un_ordered
        topo['connections'] = self.connections
        topo['ports'] = self.ports
        topo['ports_simple'] = self.ports_simple
        topo['connections_oneway'] = self.connections_oneway
        topo['ports_oneway'] = self.ports_oneway
        topo['ports_simple_oneway'] = self.ports_simple_oneway
        topo['subnets_correct'] = self.mapped_subnets_correct
        topo['subnets_wrong'] = self.mapped_subnets_wrong
        topo['IPs_correct'] = self.mapped_IPs_correct
        topo['IPs_wrong'] = self.mapped_IPs_wrong
        topo['subnets_simple_correct'] = self.mapped_subnets_simple_correct
        topo['subnets_simple_wrong'] = self.mapped_subnets_simple_wrong
        topo['IPs_simple_correct'] = self.mapped_IPs_simple_correct
        topo['IPs_simple_wrong'] = self.mapped_IPs_simple_wrong
        topo['initial_observation'] = self.initial_observation
        topo['initial_correct_actions'] = self.initial_correct_actions
        topo['initial_observation_simple'] = self.initial_observation_simple
        topo['initial_correct_actions_simple'] = self.initial_correct_actions_simple
        topo['initial_observation_small'] = self.initial_observation_small
        topo['initial_correct_actions_small'] = self.initial_correct_actions_small
        topo['faults_list'] = self.faults_list
        topo['initial_correct_actions_simple_indexes'] = self.initial_correct_actions_simple_indexes
        topo['all_correct_actions_indexes'] = self.all_correct_actions_indexes
        topo['all_wrong_actions_indexes'] = self.all_wrong_actions_indexes
        topo['num_tokens'] = self.num_tokens
        topo['current_correct_actions_numbers'] = self.current_correct_actions_numbers
        return topo

    def to_cable_name(self, conn):
        cable_index = self.cables_conns.index(conn)
        cable_name = self.cables_names[cable_index]
        return cable_name

    def to_ip_index(self, ip):
        index = self.ip_addresses_simple_seq.index(ip)+1
        return index

    def to_subnet_index(self, subnet):
        index = self.ip_subnets_simple_seq.index(subnet)+1+self.len_ip_addresses_simple
        return index

    def index_to_ip_subnet(self, i):
        if i > self.len_ip_addresses_simple:
            return self.ip_subnets_simple_seq[i-1-self.len_ip_addresses_simple]
        else:
            return self.ip_addresses_simple_seq[i-1]

    def index_to_command(self, i):
        if i > self.len_port_commands_list:
            return self.routing_commands_list[i-1-self.len_port_commands_list]
        else:
            return self.port_commands_list[i-1]

    def to_port_command_index(self, port_command):
        index = self.port_commands_list.index(port_command)+1
        return index

    def to_routing_command_index(self, routing_command):
        index = self.routing_commands_list.index(routing_command)+1+self.len_port_commands_list
        return index

    def generate_initial_text_obs_dict(self):
        # cables seqence info
        cables_conns = []
        cables_names = []
        c = 1
        for device_conns in self.connections_oneway:
            for conn in device_conns:
                cables_conns.append(conn)
                cables_names.append('Cable-'+str(c))
                cables_conns.append([conn[1], conn[0]])
                cables_names.append('Cable-'+str(c))
                c += 1
        self.cables_conns = cables_conns
        self.cables_names = cables_names
        #
        faults_types_lists = {'port_down': [], 'wrong_ip': [], 'extra_subnet': [], 'missing_subnet': [], 'network_summary_issue': [], 'protocol_version_mismatch': []}
        #
        gym_positions_list = []
        gym_positions_list_p2 = []
        x = 1
        y = 1
        conn_used = []
        #
        obs_d = {}
        seq = 0
        for i, device_conns in enumerate(self.connections):
            device_id = self.ids[i]
            obs_d[device_id] = {}
            obs_d[device_id]['name'] = self.names_simple[i]
            obs_d[device_id]['cables'] = {}
            obs_d[device_id]['routing'] = {}
            obs_d[device_id]['routing']['subnets'] = []
            for j, conn in enumerate(device_conns):
                cable_index = cables_conns.index(conn)
                cable_name = cables_names[cable_index]
                obs_d[device_id]['cables'][cable_name] = {}
                obs_d[device_id]['cables'][cable_name]['local_device_id'] = conn[0]
                obs_d[device_id]['cables'][cable_name]['local_device_name'] = self.device_names_simple[conn[0]]
                obs_d[device_id]['cables'][cable_name]['remote_device_id'] = conn[1]
                obs_d[device_id]['cables'][cable_name]['remote_device_name'] = self.device_names_simple[conn[1]]
                obs_d[device_id]['cables'][cable_name]['local_port_name'] = self.ports_simple[i][j][0]
                obs_d[device_id]['cables'][cable_name]['remote_port_name'] = self.ports_simple[i][j][1]
                obs_d[device_id]['cables'][cable_name]['local_port_ip'] = self.mapped_IPs_simple_correct[i][j][0]
                obs_d[device_id]['cables'][cable_name]['remote_port_ip'] = self.mapped_IPs_simple_correct[i][j][1]
                obs_d[device_id]['cables'][cable_name]['local_port_link_status'] = 'up'
                obs_d[device_id]['cables'][cable_name]['remote_port_link_status'] = 'up'
                subnet = self.mapped_subnets_simple_correct[i][j]
                obs_d[device_id]['routing']['subnets'].append(subnet)
                #
                if conn not in conn_used:
                    gym_positions_list.append([1, y, device_id, self.device_ports_simple.index(self.ports_simple[i][j][0]), self.names_simple[i], self.ports_simple[i][j][0], cable_name, i, j, 0, 0])
                    gym_positions_list.append([1, y, device_id, self.device_ports_simple.index(self.ports_simple[i][j][0]), self.names_simple[i], self.ports_simple[i][j][0], cable_name, i, j, 0, 1])
                    gym_positions_list.append([2, y, conn[1], self.device_ports_simple.index(self.ports_simple[i][j][1]), self.device_names_simple[conn[1]], self.ports_simple[i][j][1], cable_name, i, j, 1, 0])
                    gym_positions_list.append([2, y, conn[1], self.device_ports_simple.index(self.ports_simple[i][j][1]), self.device_names_simple[conn[1]], self.ports_simple[i][j][1], cable_name, i, j, 1, 1])
                    y += 1
                conn_used.append(conn)
                conn_used.append([conn[1], conn[0]])
                #
                faults_types_lists['port_down'].append(seq)
                seq = seq + 1
                faults_types_lists['wrong_ip'].append(seq)
                seq = seq + 1
                faults_types_lists['extra_subnet'].append(seq)
                seq = seq + 1
                faults_types_lists['missing_subnet'].append(seq)
                seq = seq + 1
            if 'ospf' not in self.routing_protocol:
                obs_d[device_id]['routing']['auto_summary'] = 'disabled'
                faults_types_lists['network_summary_issue'].append(seq)
                seq = seq + 1
                if 'rip' in self.routing_protocol:
                    obs_d[device_id]['routing']['version'] = 'version 2'
                    faults_types_lists['protocol_version_mismatch'].append(seq)
                    seq = seq + 1
            #
            for y in range(20):
                gym_positions_list_p2.append([x, self.num_devices, device_id, self.routing_protocols_list.index(self.routing_protocol)+self.len_device_ports_simple, self.names_simple[i], self.routing_protocol.replace('router ', ''), '', i, 0, 0, y])
            x += 1
        #
        for l in gym_positions_list_p2:
            gym_positions_list.append(l)
        self.gym_positions_list = gym_positions_list
        self.len_gym_positions_list = len(gym_positions_list)
        self.faults_types_lists = faults_types_lists
        return obs_d

    def generate_text_observation(self, faults_list, faults_extra_info):
        obs_d = deepcopy(self.initial_text_obs_dict)
        #
        obs, act, obs_a, act_a, obs_s, act_s, act_s_indexes, act_c_indexes, act_w_indexes = 'Here are the status information of the network: ', 'Here are the recommended commands to fix the network issues: ', 'The network status information: ', 'Here are the recommended commands: ', 'Here are the status information of the network: ', 'Here are the recommended commands to fix the network issues: ', [], [], []
        seq = 0
        for i, device_conns in enumerate(self.connections):
            device_id = self.ids[i]
            name = self.names[i]
            name_s = self.names_simple[i]
            subnets, subnets_s = [], []
            for j, conn in enumerate(device_conns):
                cable_name = self.to_cable_name(conn)
                port = self.ports[i][j][0]
                port_s = self.ports_simple[i][j][0]
                subnet_c = self.mapped_subnets_correct[i][j]
                subnet_w = self.mapped_subnets_wrong[i][j]
                IP_c = self.mapped_IPs_correct[i][j][0]
                IP_w = self.mapped_IPs_wrong[i][j][0]
                subnet_s_c = self.mapped_subnets_simple_correct[i][j]
                subnet_s_w = self.mapped_subnets_simple_wrong[i][j]
                IP_s_c = self.mapped_IPs_simple_correct[i][j][0]
                IP_s_w = self.mapped_IPs_simple_wrong[i][j][0]
                #
                if seq in faults_list:  # port down
                    obs_d[device_id]['cables'][cable_name]['local_port_link_status'] = 'administratively down'
                    #
                    obs = obs + name+' # show ip interface {}, '.format(port) + '{} is administratively down, '.format(port)
                    obs_a = obs_a + name+' # show ip interface {}, '.format(port) + '{} is administratively down, '.format(port)
                    obs_s = obs_s + name_s+' # show ip interface {}, '.format(port_s) + '{} is administratively down, '.format(port_s)
                    act = act + 'On device: {}, {}, use command: no shutdown. '.format(name, port)
                    act_a = act_a + 'For {}, {}, command: no shutdown. '.format(name, port)
                    act_s = act_s + 'On device: {}, {}, use command: no shutdown. '.format(name_s, port_s)
                else:
                    obs = obs + name+' # show ip interface {}, '.format(port) + '{} is up, '.format(port)
                    obs_a = obs_a + name+' # show ip interface {}, '.format(port) + '{} is up, '.format(port)
                    obs_s = obs_s + name_s+' # show ip interface {}, '.format(port_s) + '{} is up, '.format(port_s)
                act_str = '{}, {}, no shutdown'.format(name_s, port_s)
                act_c_indexes.append(self.actions_list.index(act_str))
                act_str = '{}, {}, shutdown'.format(name_s, port_s)
                act_w_indexes.append(self.actions_list.index(act_str))
                seq = seq + 1
                #
                if seq in faults_list:  # ip address issue
                    obs_d[device_id]['cables'][cable_name]['local_port_ip'] = IP_s_w
                    #
                    # str_1 = '  Internet protocol processing disabled, '
                    str_2 = '  Internet address is {} /24, '.format(IP_w)
                    str_2_s = '  Internet address is {} /24, '.format(IP_s_w)
                    str_3 = random.choice([str_2])
                    str_3_s = random.choice([str_2_s])
                    obs = obs + str_3
                    obs_a = obs_a + str_3
                    obs_s = obs_s + str_3_s
                    act = act + 'On device: {}, {}, use command: ip address {} 255.255.255.0. '.format(name, port, IP_c)
                    act_a = act_a + 'For {}, {}, command: ip address {} 255.255.255.0. '.format(name, port, IP_c)
                    act_s = act_s + 'On device: {}, {}, use command: ip address {} 255.255.255.0. '.format(name_s, port_s, IP_s_c)
                else:
                    str_3 = '  Internet address is {} /24, '.format(IP_c)
                    str_3_s = '  Internet address is {} /24, '.format(IP_s_c)
                    obs = obs + str_3
                    obs_a = obs_a + str_3
                    obs_s = obs_s + str_3_s
                act_str = '{}, {}, ip address {}'.format(name_s, port_s, IP_s_c)
                act_c_indexes.append(self.actions_list.index(act_str))
                act_str = '{}, {}, no ip address'.format(name_s, port_s)
                act_w_indexes.append(self.actions_list.index(act_str))
                seq = seq + 1
                #
                if seq in faults_list:  # wrong subnet exists
                    subnets.append(subnet_w)
                    subnets_s.append(subnet_s_w)
                    act = act + 'On device: {}, {}, use command: no network {}'.format(name, self.routing_protocol, subnet_w)
                    act_a = act_a + 'For {}, {}, command: no network {}'.format(name, self.routing_protocol, subnet_w)
                    act_s = act_s + 'On device: {}, {}, use command: no network {}'.format(name_s, self.routing_protocol, subnet_s_w)
                    if 'rip' in self.routing_protocol:
                        act = act + '. '
                        act_a = act_a + '. '
                        act_s = act_s + '. '
                    elif 'eigrp' in self.routing_protocol:
                        act = act + ' 0.0.0.255. '
                        act_a = act_a + ' 0.0.0.255. '
                        act_s = act_s + ' 0.0.0.255. '
                    elif 'ospf' in self.routing_protocol:
                        act = act + ' 0.0.0.255 area 0. '
                        act_a = act_a + ' 0.0.0.255 area 0. '
                        act_s = act_s + ' 0.0.0.255 area 0. '
                act_str = '{}, {}, no network {}'.format(name_s, self.routing_protocol, subnet_s_w)
                act_c_indexes.append(self.actions_list.index(act_str))
                act_str = '{}, {}, network {}'.format(name_s, self.routing_protocol, subnet_s_w)
                act_w_indexes.append(self.actions_list.index(act_str))
                seq = seq + 1
                #
                if seq in faults_list:  # correct subnet NOT exists
                    act = act + 'On device: {}, {}, use command: network {}'.format(name, self.routing_protocol, subnet_c)
                    act_a = act_a + 'For {}, {}, command: network {}'.format(name, self.routing_protocol, subnet_c)
                    act_s = act_s + 'On device: {}, {}, use command: network {}'.format(name_s, self.routing_protocol, subnet_s_c)
                    if 'rip' in self.routing_protocol:
                        act = act + '. '
                        act_a = act_a + '. '
                        act_s = act_s + '. '
                    elif 'eigrp' in self.routing_protocol:
                        act = act + ' 0.0.0.255. '
                        act_a = act_a + ' 0.0.0.255. '
                        act_s = act_s + ' 0.0.0.255. '
                    elif 'ospf' in self.routing_protocol:
                        act = act + ' 0.0.0.255 area 0. '
                        act_a = act_a + ' 0.0.0.255 area 0. '
                        act_s = act_s + ' 0.0.0.255 area 0. '
                else:
                    subnets.append(subnet_c)
                    subnets_s.append(subnet_s_c)
                act_str = '{}, {}, network {}'.format(name_s, self.routing_protocol, subnet_s_c)
                act_c_indexes.append(self.actions_list.index(act_str))
                act_str = '{}, {}, no network {}'.format(name_s, self.routing_protocol, subnet_s_c)
                act_w_indexes.append(self.actions_list.index(act_str))
                seq = seq + 1
            #
            protocol = self.routing_protocol.replace('router ', '')
            obs = obs + name+' # show ip protocols, Routing Protocol is {}, '.format(protocol)
            obs_a = obs_a + name+' # show ip protocols, Routing Protocol is {}, '.format(protocol)
            obs_s = obs_s + name_s+' # show ip protocols, Routing Protocol is {}, '.format(protocol)
            if 'ospf' not in self.routing_protocol:  # auto-summary issue
                if seq in faults_list:
                    obs_d[device_id]['routing']['auto_summary'] = 'enabled'
                    #
                    if 'eigrp' in self.routing_protocol:
                        obs = obs + '  Automatic Summarization: enabled, '
                        obs_a = obs_a + '  Automatic Summarization: enabled, '
                        obs_s = obs_s + '  Automatic Summarization: enabled, '
                    elif 'rip' in self.routing_protocol:
                        obs = obs + '  Automatic network summarization is in effect, '
                        obs_a = obs_a + '  Automatic network summarization is in effect, '
                        obs_s = obs_s + '  Automatic network summarization is in effect, '
                    act = act + 'On device: {}, {}, use command: no auto-summary. '.format(name, self.routing_protocol)
                    act_a = act_a + 'For {}, {}, command: no auto-summary. '.format(name, self.routing_protocol)
                    act_s = act_s + 'On device: {}, {}, use command: no auto-summary. '.format(name_s, self.routing_protocol)
                else:
                    if 'eigrp' in self.routing_protocol:
                        obs = obs + '  Automatic Summarization: disabled, '
                        obs_a = obs_a + '  Automatic Summarization: disabled, '
                        obs_s = obs_s + '  Automatic Summarization: disabled, '
                    elif 'rip' in self.routing_protocol:
                        obs = obs + '  Automatic network summarization is not in effect, '
                        obs_a = obs_a + '  Automatic network summarization is not in effect, '
                        obs_s = obs_s + '  Automatic network summarization is not in effect, '
                act_str = '{}, {}, no auto-summary'.format(name_s, self.routing_protocol)
                act_c_indexes.append(self.actions_list.index(act_str))
                act_str = '{}, {}, auto-summary'.format(name_s, self.routing_protocol)
                act_w_indexes.append(self.actions_list.index(act_str))
                seq = seq + 1
            if 'rip' in self.routing_protocol:  # version 1 or 2 issue
                if seq in faults_list:
                    obs_d[device_id]['routing']['version'] = 'version 1'
                    #
                    obs = obs + '  Default version control: send version 1, receive any version, '
                    obs_a = obs_a + '  Default version control: send version 1, receive any version, '
                    obs_s = obs_s + '  Default version control: send version 1, receive any version, '
                    act = act + 'On device: {}, {}, use command: version 2. '.format(name, self.routing_protocol)
                    act_a = act_a + 'For {}, {}, command: version 2. '.format(name, self.routing_protocol)
                    act_s = act_s + 'On device: {}, {}, use command: version 2. '.format(name_s, self.routing_protocol)
                else:
                    obs = obs + '  Default version control: send version 2, receive version 2, '
                    obs_a = obs_a + '  Default version control: send version 2, receive version 2, '
                    obs_s = obs_s + '  Default version control: send version 2, receive version 2, '
                act_str = '{}, {}, version 2'.format(name_s, self.routing_protocol)
                act_c_indexes.append(self.actions_list.index(act_str))
                act_str = '{}, {}, no version 2'.format(name_s, self.routing_protocol)
                act_w_indexes.append(self.actions_list.index(act_str))
                seq = seq + 1
            #
            obs_d[device_id]['routing']['subnets'] = subnets_s
            #
            obs = obs + '  Routing for Networks : , '
            obs_a = obs_a + '  Routing for Networks : , '
            obs_s = obs_s + '  Routing for Networks : , '
            for x, subnet in enumerate(subnets):
                if 'rip' in self.routing_protocol:
                    obs = obs + '    {}.0.0.0, '.format(subnet.split('.')[0])
                    obs_a = obs_a + '    {}.0.0.0, '.format(subnet.split('.')[0])
                    obs_s = obs_s + '    {}.0.0.0, '.format(subnets_s[x].split('.')[0])
                elif 'eigrp' in self.routing_protocol:
                    obs = obs + '    {} /24, '.format(subnet)
                    obs_a = obs_a + '    {} /24, '.format(subnet)
                    obs_s = obs_s + '    {} /24, '.format(subnets_s[x])
                elif 'ospf' in self.routing_protocol:
                    obs = obs + '    {} 0.0.0.255 area 0, '.format(subnet)
                    obs_a = obs_a + '    {} 0.0.0.255 area 0, '.format(subnet)
                    obs_s = obs_s + '    {} 0.0.0.255 area 0, '.format(subnets_s[x])
        #
        str_1 = 'that is all, please help on fixing the issues. Thanks.'
        obs = obs + str_1
        obs_a = obs_a + 'that is all, please help. Thanks.'
        obs_s = obs_s + str_1
        str_2 = 'That is all that I can find, hope it helps. Thanks.'
        act = act + str_2
        act_a = act_a + str_2
        act_s = act_s + str_2
        #
        for y in faults_list:
            act_s_indexes.append(act_c_indexes[y])
        if len(act_s_indexes) == 0:
            act = 'I do not see any issue on the devices-ports or the routing protocols, the network should be working. Or the issues might be in other areas that I currently can not help. Good luck.'
            act_a = act
            act_s = act
        return obs, act, obs_a, act_a, obs_s, act_s, act_s_indexes, faults_list, faults_extra_info, obs_d, act_c_indexes, act_w_indexes

    def generate_connections_description(self, names, ports, IPs, mode, subnets):
        desc = ''
        used_conn = []
        k = 1
        for i, device_conns in enumerate(self.connections):
            for j, conn in enumerate(device_conns):
                if conn not in used_conn:
                    index_device_1 = self.ids.index(conn[0])
                    index_device_2 = self.ids.index(conn[1])
                    name_1 = names[index_device_1]
                    name_2 = names[index_device_2]
                    port_1 = ports[i][j][0]
                    port_2 = ports[i][j][1]
                    ip_1 = IPs[i][j][0]
                    ip_2 = IPs[i][j][1]
                    subnet = subnets[i][j]
                    #
                    list_1 = [k, name_1, port_1, ip_1, name_2, port_2, ip_2]
                    list_2 = [k, name_1, port_1, ip_1, name_2, port_2, ip_2, subnet]
                    if mode == 'small':
                        desc = desc + 'Connection {} is from {} {} {}/24 to {} {} {}/24. '.format(*list_1)
                    elif mode == 'simple':
                        desc = desc + 'Connection {} is from device {} port {} IP {}/24 to device {} port {} IP {}/24, using subnet: {}. '.format(*list_2)
                    else:
                        desc = desc + 'Connection {} is from device {} port {} IP {}/24 to device {} port {} IP {}/24. '.format(*list_1)
                    #
                    used_conn.append(conn)
                    used_conn.append([conn[1], conn[0]])
                    k = k + 1
        return desc

    def map_devices_subnets_ips(self):
        mapped_subnets_correct = []
        mapped_subnets_wrong = []
        mapped_IPs_correct = []
        mapped_IPs_wrong = []
        mapped_subnets_simple_correct = []
        mapped_subnets_simple_wrong = []
        mapped_IPs_simple_correct = []
        mapped_IPs_simple_wrong = []
        str_1 = 'We are now implementing a computer network as follows: 1. we are using {} devices, '.format(self.num_devices)
        desc = str_1 + 'named {} respectively. 2. '.format(", ".join(self.names))
        desc_simple = str_1 + 'named {} respectively. 2. '.format(", ".join(self.names_simple))
        str_1_small = 'For a computer network: 1. using {} devices, '.format(self.num_devices)
        desc_small = str_1_small + 'named {} respectively. 2. '.format(", ".join(self.names))
        # the mapping jobs
        used_conns, used_s_c, used_s_w, used_i_c, used_i_w, used_s_s_c, used_s_s_w, used_i_s_c, used_i_s_w = [], [], [], [], [], [], [], [], []
        k = 0  # index position of subnets
        for device_conns in self.connections:
            device_s_c, device_s_w, device_i_c, device_i_w, device_s_s_c, device_s_s_w, device_i_s_c, device_i_s_w = [], [], [], [], [], [], [], []
            for conn in device_conns:
                if conn not in used_conns:
                    device_s_c.append(self.subnets_correct[k])
                    device_s_w.append(self.subnets_wrong[k])
                    device_i_c.append([self.IPs_correct[k*2], self.IPs_correct[k*2+1]])
                    device_i_w.append([self.IPs_wrong[k*2], self.IPs_wrong[k*2+1]])
                    device_s_s_c.append(self.subnets_simple_correct[k])
                    device_s_s_w.append(self.subnets_simple_wrong[k])
                    device_i_s_c.append([self.IPs_simple_correct[k*2], self.IPs_simple_correct[k*2+1]])
                    device_i_s_w.append([self.IPs_simple_wrong[k*2], self.IPs_simple_wrong[k*2+1]])
                    #
                    used_conns.append(conn)
                    used_s_c.append(self.subnets_correct[k])
                    used_s_w.append(self.subnets_wrong[k])
                    used_i_c.append([self.IPs_correct[k*2], self.IPs_correct[k*2+1]])
                    used_i_w.append([self.IPs_wrong[k*2], self.IPs_wrong[k*2+1]])
                    used_s_s_c.append(self.subnets_simple_correct[k])
                    used_s_s_w.append(self.subnets_simple_wrong[k])
                    used_i_s_c.append([self.IPs_simple_correct[k*2], self.IPs_simple_correct[k*2+1]])
                    used_i_s_w.append([self.IPs_simple_wrong[k*2], self.IPs_simple_wrong[k*2+1]])
                    #
                    used_conns.append([conn[1], conn[0]])
                    used_s_c.append(self.subnets_correct[k])
                    used_s_w.append(self.subnets_wrong[k])
                    used_i_c.append([self.IPs_correct[k*2+1], self.IPs_correct[k*2]])
                    used_i_w.append([self.IPs_wrong[k*2+1], self.IPs_wrong[k*2]])
                    used_s_s_c.append(self.subnets_simple_correct[k])
                    used_s_s_w.append(self.subnets_simple_wrong[k])
                    used_i_s_c.append([self.IPs_simple_correct[k*2+1], self.IPs_simple_correct[k*2]])
                    used_i_s_w.append([self.IPs_simple_wrong[k*2+1], self.IPs_simple_wrong[k*2]])
                    #
                    k = k + 1
                else:
                    index_conn = used_conns.index(conn)
                    device_s_c.append(used_s_c[index_conn])
                    device_s_w.append(used_s_w[index_conn])
                    device_i_c.append(used_i_c[index_conn])
                    device_i_w.append(used_i_w[index_conn])
                    device_s_s_c.append(used_s_s_c[index_conn])
                    device_s_s_w.append(used_s_s_w[index_conn])
                    device_i_s_c.append(used_i_s_c[index_conn])
                    device_i_s_w.append(used_i_s_w[index_conn])
            mapped_subnets_correct.append(device_s_c)
            mapped_subnets_wrong.append(device_s_w)
            mapped_IPs_correct.append(device_i_c)
            mapped_IPs_wrong.append(device_i_w)
            mapped_subnets_simple_correct.append(device_s_s_c)
            mapped_subnets_simple_wrong.append(device_s_s_w)
            mapped_IPs_simple_correct.append(device_i_s_c)
            mapped_IPs_simple_wrong.append(device_i_s_w)
        # description string of connections
        str_2 = self.generate_connections_description(self.names, self.ports, mapped_IPs_correct, '', mapped_subnets_correct)
        str_2_simple = self.generate_connections_description(self.names_simple, self.ports_simple, mapped_IPs_simple_correct, 'simple', mapped_subnets_simple_correct)
        str_2_small = self.generate_connections_description(self.names, self.ports, mapped_IPs_correct, 'small', mapped_subnets_correct)
        desc = desc + str_2
        desc_simple = desc_simple + str_2_simple
        desc_small = desc_small + str_2_small
        #
        if 'ospf' in self.routing_protocol:
            str_3 = '3. we use the routing protocol ospf and the process id 1. '
        elif 'eigrp' in self.routing_protocol:
            str_3 = '3. we use the routing protocol eigrp and the AS number 1, and the auto-summary is disabled. '
        elif 'rip' in self.routing_protocol:
            str_3 = '3. we use the routing protocol rip version 2, and the auto-summary is disabled. '
        desc = desc + str_3
        desc_simple = desc_simple + str_3
        desc_small = desc_small + str_3
        return mapped_subnets_correct, mapped_subnets_wrong, mapped_IPs_correct, mapped_IPs_wrong, mapped_subnets_simple_correct, mapped_subnets_simple_wrong, mapped_IPs_simple_correct, mapped_IPs_simple_wrong, desc, desc_small, desc_simple

    def generate_subnets(self):
        subnets_correct, IPs_correct = self.generate_subnets_with_numbers(self.IP_num_1_correct, self.IP_num_2_correct, self.IP_num_3_correct, self.IP_num_4_correct)
        subnets_wrong, IPs_wrong = self.generate_subnets_with_numbers(self.IP_num_1_wrong, self.IP_num_2_wrong, self.IP_num_3_wrong, self.IP_num_4_wrong)
        return subnets_correct, subnets_wrong, IPs_correct, IPs_wrong

    def generate_subnets_with_numbers(self, num_1, num_2, num_3, num_4):
        subnets = []
        IPs = []
        for i, n1 in enumerate(num_1):
            subnet = str(n1)+'.'+str(num_2[i])+'.'+str(num_3[i])+'.0'
            IP_1 = str(n1)+'.'+str(num_2[i])+'.'+str(num_3[i])+'.'+str(num_4[i])
            IP_2 = str(n1)+'.'+str(num_2[i])+'.'+str(num_3[i])+'.'+str(num_4[i]+1)
            subnets.append(subnet)
            IPs.append(IP_1)
            IPs.append(IP_2)
        return subnets, IPs

    def get_ports_info(self, ports_in_use, env_ports_list, add_ports_type, conn_info):
        ports = []
        ports_in_use_2 = deepcopy(ports_in_use)
        #
        conn_used = []
        conn_ports_mapped = []
        for device_conn in conn_info:
            device_ports_mapped = []
            for conn in device_conn:
                if conn not in conn_used:
                    ports_mapped = []
                    for id in conn:
                        index_device = self.ids.index(id)
                        j = 0
                        for index_port in ports_in_use_2[index_device]:
                            if index_port != '':
                                port = env_ports_list[index_port]
                                if add_ports_type:
                                    port = self.ports_type + ' ' + port
                                ports_mapped.append(port)
                                ports_in_use_2[index_device][j] = ''  # removed after use
                                break
                            j = j+1
                    device_ports_mapped.append(ports_mapped)
                    #
                    conn_used.append(conn)
                    conn_ports_mapped.append(ports_mapped)
                    conn_used.append([conn[1], conn[0]])
                    conn_ports_mapped.append([ports_mapped[1], ports_mapped[0]])
                else:
                    index_1 = conn_used.index(conn)
                    device_ports_mapped.append(conn_ports_mapped[index_1])
            ports.append(device_ports_mapped)
        #
        return ports

    def generate_ports(self):
        ports_in_use = []
        l_device_ports_simple = len(self.device_ports_simple)
        list_1 = list(range(l_device_ports_simple))
        for conn in self.connections:
            index_ports = random.sample(list_1, len(conn))
            ports_in_use.append(index_ports)
        #
        ports = self.get_ports_info(ports_in_use, self.device_ports_numbers, True, self.connections)
        ports_simple = self.get_ports_info(ports_in_use, self.device_ports_simple, False, self.connections)
        ports_oneway = self.get_ports_info(ports_in_use, self.device_ports_numbers, True, self.connections_oneway)
        ports_simple_oneway = self.get_ports_info(ports_in_use, self.device_ports_simple, False, self.connections_oneway)
        #
        return ports, ports_simple, ports_oneway, ports_simple_oneway

    def get_leaf_devices(self):
        leaf_devices = []
        num_leaf_devices = 0
        for conn in self.connections:
            if len(conn) == 1:
                leaf_devices.append(1)
                num_leaf_devices = num_leaf_devices+1
            else:
                leaf_devices.append(0)
        return leaf_devices, num_leaf_devices

    def get_small_actions_list(self):
        list = []
        for i, id in enumerate(self.ids):
            for conn_ports, conn_ips_c, conn_ips_w in zip(self.ports_simple[i], self.mapped_IPs_simple_correct[i], self.mapped_IPs_simple_wrong[i]):
                j = self.device_ports_simple.index(conn_ports[0])
                l_c = self.ip_addresses_simple_seq.index(conn_ips_c[0])
                l_w = self.ip_addresses_simple_seq.index(conn_ips_w[0])
                for k, command in enumerate(self.port_commands_list):
                    if command == "ip address":
                        list.append([id, j, k+1, l_c+1])
                        list.append([id, j, k+1, l_w+1])
                    else:
                        list.append([id, j, k+1, 0])
        for i, id in enumerate(self.ids):
            for j, protocol in enumerate(self.routing_protocols_list):
                if self.routing_protocol in protocol:
                    for k, command in enumerate(self.routing_commands_list):
                        if 'network' in command:
                            for subnet_c, subnet_w in zip(self.mapped_subnets_simple_correct[i], self.mapped_subnets_simple_wrong[i]):
                                l_c = self.ip_subnets_simple_seq.index(subnet_c)
                                l_w = self.ip_subnets_simple_seq.index(subnet_w)
                                list.append([id, self.len_device_ports_simple+j, self.len_port_commands_list+k+1, self.len_ip_addresses_simple+l_c+1])
                                list.append([id, self.len_device_ports_simple+j, self.len_port_commands_list+k+1, self.len_ip_addresses_simple+l_w+1])
                        elif 'rip' in protocol:
                            list.append([id, self.len_device_ports_simple+j, self.len_port_commands_list+k+1, 0])
                        elif 'eigrp' in protocol and 'version' not in command:
                            list.append([id, self.len_device_ports_simple+j, self.len_port_commands_list+k+1, 0])
        return list

    def generate_connections(self):
        connections_un_ordered = []  # this is un_ordered connections
        # choose one device as root
        root_device = random.choice(self.ids)
        devices_in_use = [root_device]
        # generate connections_un_ordered which can connect other devices to devices_in_use
        for id in self.ids:
            if id not in devices_in_use:
                target_id = random.choice(devices_in_use)
                if self.subnets_18 == True:
                    target_id = root_device
                connections_un_ordered.append([id, target_id])
                devices_in_use.append(id)
        # order connections_un_ordered per self.ids
        # one connection is associated to 2 devices, so appears TWICE in conn_ordered
        conn_ordered = []
        for id in self.ids:
            device_conn = []
            for conn in connections_un_ordered:
                if id in conn:
                    another_id = conn[(conn.index(id) + 1) % 2]
                    device_conn.append([id, another_id])
            conn_ordered.append(device_conn)
        #
        return conn_ordered, connections_un_ordered

    def get_connections_oneway(self):
        connections_un_ordered = deepcopy(self.connections_un_ordered)
        # ONLY list one connection ONCE in conn_ordered_oneway
        conn_ordered_oneway = []
        for id in self.ids:
            device_conn = []
            j = 0
            for conn in connections_un_ordered:
                if id in conn:
                    another_id = conn[(conn.index(id) + 1) % 2]
                    device_conn.append([id, another_id])
                    connections_un_ordered[j] = []  # remove used conn
                j = j+1
            conn_ordered_oneway.append(device_conn)
        #
        return conn_ordered_oneway

    def generate_simple_names(self):
        names = []
        n = len(self.device_names_simple)
        list_1 = list(range(n))
        ids = random.sample(list_1, self.num_devices)
        for id in ids:
            names.append(self.device_names_simple[id])
        return ids, names
