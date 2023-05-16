# Information on using / testing it

## Quick start

1. clone this github repository: `git clone https://github.com/Andy-Wu-2022/ComputerNetworkOperator.git`
2. install `python3` and `pip install stable-baselines3 sb3-contrib deepdiff`
3. `cd ComputerNetworkOperator` and run it: `python3 RunOperator.py`

Here is an example output:

```
 ################################################## 
        Network Information for Human only
 ################################################## 
Topology_Description: 
We are now implementing a computer network as follows: 
1. we are using 4 devices, named Device-B, Device-G, Device-L, Device-I respectively. 
2. Connection 1 is from device Device-B port Port-6 IP IP-Address-39/24 to device Device-G port Port-2 IP IP-Address-15/24, using subnet: IP-Subnet-28.
 Connection 2 is from device Device-B port Port-7 IP IP-Address-34/24 to device Device-I port Port-9 IP IP-Address-7/24, using subnet: IP-Subnet-3.
 Connection 3 is from device Device-G port Port-8 IP IP-Address-45/24 to device Device-L port Port-3 IP IP-Address-18/24, using subnet: IP-Subnet-17. 
3. we use the routing protocol eigrp and the AS number 1, and the auto-summary is disabled. 

Network_Status: 
Here are the status information of the network: 
Device-B # show ip interface Port-6,
 Port-6 is administratively down,  
 Internet address is IP-Address-19 /24, 
Device-B # show ip interface Port-7,
 Port-7 is administratively down,  
 Internet address is IP-Address-43 /24, 
Device-B # show ip protocols,
 Routing Protocol is eigrp 1,  
 Automatic Summarization: enabled,  
 Routing for Networks : ,   
  IP-Subnet-30 /24,   
  IP-Subnet-18 /24, 
Device-G # show ip interface Port-2,
 Port-2 is administratively down,  
 Internet address is IP-Address-41 /24, 
Device-G # show ip interface Port-8,
 Port-8 is administratively down,  
 Internet address is IP-Address-42 /24, 
Device-G # show ip protocols,
 Routing Protocol is eigrp 1,  
 Automatic Summarization: enabled,  
 Routing for Networks : , 
Device-L # show ip interface Port-3,
 Port-3 is administratively down,  
 Internet address is IP-Address-49 /24, 
Device-L # show ip protocols,
 Routing Protocol is eigrp 1,  
 Automatic Summarization: enabled,  
 Routing for Networks : ,   
  IP-Subnet-26 /24,   
  IP-Subnet-17 /24, 
Device-I # show ip interface Port-9,
 Port-9 is administratively down,  
 Internet address is IP-Address-58 /24, 
Device-I # show ip protocols,
 Routing Protocol is eigrp 1,  
 Automatic Summarization: enabled,  
 Routing for Networks : ,   
  IP-Subnet-18 /24,   
  IP-Subnet-3 /24, 
that is all, please help on fixing the issues. Thanks.

Correct_Commands: 
Here are the recommended commands to fix the network issues: 
On device: Device-B, Port-6, use command: no shutdown. 
On device: Device-B, Port-6, use command: ip address IP-Address-39 255.255.255.0. 
On device: Device-B, router eigrp 1, use command: no network IP-Subnet-30 0.0.0.255. 
On device: Device-B, router eigrp 1, use command: network IP-Subnet-28 0.0.0.255. 
On device: Device-B, Port-7, use command: no shutdown. 
On device: Device-B, Port-7, use command: ip address IP-Address-34 255.255.255.0. 
On device: Device-B, router eigrp 1, use command: no network IP-Subnet-18 0.0.0.255. 
On device: Device-B, router eigrp 1, use command: network IP-Subnet-3 0.0.0.255. 
On device: Device-B, router eigrp 1, use command: no auto-summary. 
On device: Device-G, Port-2, use command: no shutdown. 
On device: Device-G, Port-2, use command: ip address IP-Address-15 255.255.255.0. 
On device: Device-G, router eigrp 1, use command: network IP-Subnet-28 0.0.0.255. 
On device: Device-G, Port-8, use command: no shutdown. 
On device: Device-G, Port-8, use command: ip address IP-Address-45 255.255.255.0. 
On device: Device-G, router eigrp 1, use command: network IP-Subnet-17 0.0.0.255. 
On device: Device-G, router eigrp 1, use command: no auto-summary. 
On device: Device-L, Port-3, use command: no shutdown. 
On device: Device-L, Port-3, use command: ip address IP-Address-18 255.255.255.0. 
On device: Device-L, router eigrp 1, use command: no network IP-Subnet-26 0.0.0.255. 
On device: Device-L, router eigrp 1, use command: no auto-summary. 
On device: Device-I, Port-9, use command: no shutdown. 
On device: Device-I, Port-9, use command: ip address IP-Address-7 255.255.255.0. 
On device: Device-I, router eigrp 1, use command: no network IP-Subnet-18 0.0.0.255. 
On device: Device-I, router eigrp 1, use command: no auto-summary. 
That is all that I can find, hope it helps. Thanks.
 ################################################## 

---> Work start here:

Step 1: Configure on device: Device-B, Port-6. 
Step 2: Configure on device: Device-B, Port-6. Use command: no shutdown. 
Step 3: NA.
Step 4: Checking on device: Device-B, Port-6.
Step 5: Configure on device: Device-B, Port-6. 
Step 6: Configure on device: Device-B, Port-6. Use command: ip address. 
Step 7: Configure on device: Device-B, Port-6. Use command: ip address. Use IP-Address-39.
Step 8: Checking on device: Device-G, Port-2.
Step 9: Configure on device: Device-G, Port-2. 
Step 10: Configure on device: Device-G, Port-2. Use command: no shutdown. 
Step 11: NA.
Step 12: Checking on device: Device-G, Port-2.
Step 13: Configure on device: Device-G, Port-2. 
Step 14: Configure on device: Device-G, Port-2. Use command: ip address. 
Step 15: Configure on device: Device-G, Port-2. Use command: ip address. Use IP-Address-15.
Step 16: Checking on device: Device-B, Port-7.
Step 17: Configure on device: Device-B, Port-7. 
Step 18: Configure on device: Device-B, Port-7. Use command: no shutdown. 
Step 19: NA.
Step 20: Checking on device: Device-B, Port-7.
Step 21: Configure on device: Device-B, Port-7. 
Step 22: Configure on device: Device-B, Port-7. Use command: ip address. 
Step 23: Configure on device: Device-B, Port-7. Use command: ip address. Use IP-Address-34.
Step 24: Checking on device: Device-I, Port-9.
Step 25: Configure on device: Device-I, Port-9. 
Step 26: Configure on device: Device-I, Port-9. Use command: no shutdown. 
Step 27: NA.
Step 28: Checking on device: Device-I, Port-9.
Step 29: Configure on device: Device-I, Port-9. 
Step 30: Configure on device: Device-I, Port-9. Use command: ip address. 
Step 31: Configure on device: Device-I, Port-9. Use command: ip address. Use IP-Address-7.
Step 32: Checking on device: Device-G, Port-8.
Step 33: Configure on device: Device-G, Port-8. 
Step 34: Configure on device: Device-G, Port-8. Use command: no shutdown. 
Step 35: NA.
Step 36: Checking on device: Device-G, Port-8.
Step 37: Configure on device: Device-G, Port-8. 
Step 38: Configure on device: Device-G, Port-8. Use command: ip address. 
Step 39: Configure on device: Device-G, Port-8. Use command: ip address. Use IP-Address-45.
Step 40: Checking on device: Device-L, Port-3.
Step 41: Configure on device: Device-L, Port-3. 
Step 42: Configure on device: Device-L, Port-3. Use command: no shutdown. 
Step 43: NA.
Step 44: Checking on device: Device-L, Port-3.
Step 45: Configure on device: Device-L, Port-3. 
Step 46: Configure on device: Device-L, Port-3. Use command: ip address. 
Step 47: Configure on device: Device-L, Port-3. Use command: ip address. Use IP-Address-18.
Step 48: Checking on device: Device-B, eigrp 1.
Step 49: Checking on device: Device-B, eigrp 1.
Step 50: Checking on device: Device-B, eigrp 1.
Step 51: Checking on device: Device-B, eigrp 1.
Step 52: Checking on device: Device-B, eigrp 1.
Step 53: Configure on device: Device-B, eigrp 1. 
Step 54: Configure on device: Device-B, eigrp 1. Use command: network. 
Step 55: Configure on device: Device-B, eigrp 1. Use command: network. Use IP-Subnet-28.
Step 56: Checking on device: Device-B, eigrp 1.
Step 57: Configure on device: Device-B, eigrp 1. 
Step 58: Configure on device: Device-B, eigrp 1. Use command: no network. 
Step 59: Configure on device: Device-B, eigrp 1. Use command: no network. Use IP-Subnet-30.
Step 60: Checking on device: Device-B, eigrp 1.
Step 61: Checking on device: Device-B, eigrp 1.
Step 62: Checking on device: Device-B, eigrp 1.
Step 63: Checking on device: Device-B, eigrp 1.
Step 64: Configure on device: Device-B, eigrp 1. 
Step 65: Configure on device: Device-B, eigrp 1. Use command: network. 
Step 66: Configure on device: Device-B, eigrp 1. Use command: network. Use IP-Subnet-3.
Step 67: Checking on device: Device-B, eigrp 1.
Step 68: Checking on device: Device-B, eigrp 1.
Step 69: Checking on device: Device-B, eigrp 1.
Step 70: Checking on device: Device-B, eigrp 1.
Step 71: Checking on device: Device-B, eigrp 1.
Step 72: Checking on device: Device-B, eigrp 1.
Step 73: Checking on device: Device-B, eigrp 1.
Step 74: Checking on device: Device-B, eigrp 1.
Step 75: Configure on device: Device-B, eigrp 1. 
Step 76: Configure on device: Device-B, eigrp 1. Use command: no network. 
Step 77: Configure on device: Device-B, eigrp 1. Use command: no network. Use IP-Subnet-18.
Step 78: Checking on device: Device-B, eigrp 1.
Step 79: Configure on device: Device-B, eigrp 1. 
Step 80: Configure on device: Device-B, eigrp 1. Use command: no auto-summary. 
Step 81: NA.
Step 82: Checking on device: Device-B, eigrp 1.
Step 83: Checking on device: Device-G, eigrp 1.
Step 84: Checking on device: Device-G, eigrp 1.
Step 85: Checking on device: Device-G, eigrp 1.
Step 86: Checking on device: Device-G, eigrp 1.
Step 87: Checking on device: Device-G, eigrp 1.
Step 88: Configure on device: Device-G, eigrp 1. 
Step 89: Configure on device: Device-G, eigrp 1. Use command: network. 
Step 90: Configure on device: Device-G, eigrp 1. Use command: network. Use IP-Subnet-17.
Step 91: Checking on device: Device-G, eigrp 1.
Step 92: Checking on device: Device-G, eigrp 1.
Step 93: Configure on device: Device-G, eigrp 1. 
Step 94: Configure on device: Device-G, eigrp 1. Use command: network. 
Step 95: Configure on device: Device-G, eigrp 1. Use command: network. Use IP-Subnet-28.
Step 96: Checking on device: Device-G, eigrp 1.
Step 97: Checking on device: Device-G, eigrp 1.
Step 98: Checking on device: Device-G, eigrp 1.
Step 99: Checking on device: Device-G, eigrp 1.
Step 100: Checking on device: Device-G, eigrp 1.
Step 101: Checking on device: Device-G, eigrp 1.
Step 102: Checking on device: Device-G, eigrp 1.
Step 103: Checking on device: Device-G, eigrp 1.
Step 104: Checking on device: Device-G, eigrp 1.
Step 105: Checking on device: Device-G, eigrp 1.
Step 106: Checking on device: Device-G, eigrp 1.
Step 107: Checking on device: Device-G, eigrp 1.
Step 108: Configure on device: Device-G, eigrp 1. 
Step 109: Configure on device: Device-G, eigrp 1. Use command: no auto-summary. 
Step 110: NA.
Step 111: Checking on device: Device-G, eigrp 1.
Step 112: Checking on device: Device-L, eigrp 1.
Step 113: Checking on device: Device-L, eigrp 1.
Step 114: Checking on device: Device-L, eigrp 1.
Step 115: Checking on device: Device-L, eigrp 1.
Step 116: Checking on device: Device-L, eigrp 1.
Step 117: Checking on device: Device-L, eigrp 1.
Step 118: Checking on device: Device-L, eigrp 1.
Step 119: Checking on device: Device-L, eigrp 1.
Step 120: Configure on device: Device-L, eigrp 1. 
Step 121: Configure on device: Device-L, eigrp 1. Use command: no network. 
Step 122: Configure on device: Device-L, eigrp 1. Use command: no network. Use IP-Subnet-26.
Step 123: Checking on device: Device-L, eigrp 1.
Step 124: Checking on device: Device-L, eigrp 1.
Step 125: Checking on device: Device-L, eigrp 1.
Step 126: Checking on device: Device-L, eigrp 1.
Step 127: Checking on device: Device-L, eigrp 1.
Step 128: Checking on device: Device-L, eigrp 1.
Step 129: Checking on device: Device-L, eigrp 1.
Step 130: Checking on device: Device-L, eigrp 1.
Step 131: Checking on device: Device-L, eigrp 1.
Step 132: Checking on device: Device-L, eigrp 1.
Step 133: Checking on device: Device-L, eigrp 1.
Step 134: Configure on device: Device-L, eigrp 1. 
Step 135: Configure on device: Device-L, eigrp 1. Use command: no auto-summary. 
Step 136: NA.
Step 137: Checking on device: Device-L, eigrp 1.
Step 138: Checking on device: Device-I, eigrp 1.
Step 139: Checking on device: Device-I, eigrp 1.
Step 140: Checking on device: Device-I, eigrp 1.
Step 141: Checking on device: Device-I, eigrp 1.
Step 142: Checking on device: Device-I, eigrp 1.
Step 143: Checking on device: Device-I, eigrp 1.
Step 144: Checking on device: Device-I, eigrp 1.
Step 145: Checking on device: Device-I, eigrp 1.
Step 146: Checking on device: Device-I, eigrp 1.
Step 147: Checking on device: Device-I, eigrp 1.
Step 148: Checking on device: Device-I, eigrp 1.
Step 149: Configure on device: Device-I, eigrp 1. 
Step 150: Configure on device: Device-I, eigrp 1. Use command: no network. 
Step 151: Configure on device: Device-I, eigrp 1. Use command: no network. Use IP-Subnet-18.
Step 152: Checking on device: Device-I, eigrp 1.
Step 153: Checking on device: Device-I, eigrp 1.
Step 154: Checking on device: Device-I, eigrp 1.
Step 155: Checking on device: Device-I, eigrp 1.
Step 156: Checking on device: Device-I, eigrp 1.
Step 157: Checking on device: Device-I, eigrp 1.
Step 158: Checking on device: Device-I, eigrp 1.
Step 159: Checking on device: Device-I, eigrp 1.
Step 160: Configure on device: Device-I, eigrp 1. 
Step 161: Configure on device: Device-I, eigrp 1. Use command: no auto-summary. 
Episode: 0, Correct-Steps: 162/162, 100, M-S: 3, Reward: 32, Done: True, T-Rewards: 1090, Correct-Actions: 24, Remaining-F: 0, Fixed-F: 24.
Step 162: NA.
```

## Files

1. RunOperator.py: run it using one of the "trained_models" and see all the printed details.
2. TrainOperator.py: to create a new model to train, or load/train a saved model.
3. ComputerNetworkSimulator.py: randomly generate a computer network and maintain/update its information in real time.
4. ComputerNetworkEnv.py: encapsulate the network as an Reinforcement Learning Environment used to train a model.
5. 01_GenerateActionsList.py: update the base information related to create a computer network.
6. 02_pip_install.sh: to install all the needed python libs.

## trained_models

There are 4 QRDQN trained_models inside the folder: trained_models.

For all the 4 models: n_quantiles=7.

1. trained_model.zip.q7.512-10: it uses 10 hidden layers, each layer has 512 units.
2. trained_model.zip.q7.512-15: it uses 15 hidden layers, each layer has 512 units.
3. trained_model.zip.q7.768-10: it uses 10 hidden layers, each layer has 768 units.
4. trained_model.zip.q7.768-7: it uses 7 hidden layers, each layer has 768 units.

## How was it trained

It was trained using a GPU of A4000 on the cloud: paperspace. Each model took about 8 ~ 10 hours.

Parameters for training:

1. number of envs for multiprocessing: 128
2. use parameters: train_freq=1024, target_update_interval=350000, max_grad_norm=5, learning_rate=1e-5, tau=1, gamma=0, batch_size=512*2, gradient_steps=128*6, buffer_size=4000000
3. use: model.learn(total_timesteps=int(4e6)) to train and collect data, and also use: model.train(4000*30, 512*2) to continue training using the same data. save the model
4. loop step 3 until the loss value could not be better(smaller)
5. change: max_grad_norm=3, learning_rate=1e-6. continue training as step 3 and 4

FineTune:

1. backup the model
2. change: max_grad_norm=1, learning_rate=1e-7
3. train the model for 8000 (or less) gradient_steps totally (batch_size=512*2), save and test
4. if not OK, continue step 3 until the model can work perfectly
5. if stuck, copy the backup-model and try again
