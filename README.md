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
1. we are using 4 devices, named Device-G, Device-A, Device-I, Device-H respectively.
2. Connection 1 is from device Device-G port Port-3 IP IP-Address-60/24 to device Device-A port Port-7 IP IP-Address-8/24, using subnet: IP-Subnet-13. Connection 2 is from device Device-G port Port-2 IP IP-Address-33/24 to device Device-H port Port-2 IP IP-Address-20/24, using subnet: IP-Subnet-4. Connection 3 is from device Device-A port Port-1 IP IP-Address-11/24 to device Device-I port Port-7 IP IP-Address-45/24, using subnet: IP-Subnet-18.
3. we use the routing protocol eigrp and the AS number 1, and the auto-summary is disabled. 

Network_Status: 
Here are the status information of the network:
Device-G # show ip interface Port-3,
Port-3 is administratively down,
  Internet address is IP-Address-54 /24,
Device-G # show ip interface Port-2,
Port-2 is administratively down,
  Internet address is IP-Address-33 /24,
Device-G # show ip protocols,
Routing Protocol is eigrp 1,
  Automatic Summarization: enabled,
  Routing for Networks : ,
    IP-Subnet-6 /24,
    IP-Subnet-29 /24,
Device-A # show ip interface Port-7,
Port-7 is administratively down,
  Internet address is IP-Address-59 /24,
Device-A # show ip interface Port-1,
Port-1 is administratively down,
  Internet address is IP-Address-52 /24,
Device-A # show ip protocols,
Routing Protocol is eigrp 1,
  Automatic Summarization: enabled,
  Routing for Networks : ,
    IP-Subnet-6 /24,
    IP-Subnet-17 /24,
    IP-Subnet-18 /24,
Device-I # show ip interface Port-7,
Port-7 is up,
  Internet address is IP-Address-40 /24,
Device-I # show ip protocols,
Routing Protocol is eigrp 1,
  Automatic Summarization: enabled,
  Routing for Networks : ,
Device-H # show ip interface Port-2,
Port-2 is administratively down,
  Internet address is IP-Address-53 /24,
Device-H # show ip protocols,
Routing Protocol is eigrp 1,
  Automatic Summarization: enabled,
  Routing for Networks : ,
    IP-Subnet-29 /24,
that is all,
please help on fixing the issues. Thanks.

Correct_Commands: 
Here are the recommended commands to fix the network issues:
On device: Device-G, Port-3, use command: no shutdown.
On device: Device-G, Port-3, use command: ip address IP-Address-60 255.255.255.0.
On device: Device-G, router eigrp 1, use command: no network IP-Subnet-6 0.0.0.255.
On device: Device-G, router eigrp 1, use command: network IP-Subnet-13 0.0.0.255.
On device: Device-G, Port-2, use command: no shutdown.
On device: Device-G, router eigrp 1, use command: no network IP-Subnet-29 0.0.0.255.
On device: Device-G, router eigrp 1, use command: network IP-Subnet-4 0.0.0.255.
On device: Device-G, router eigrp 1, use command: no auto-summary.
On device: Device-A, Port-7, use command: no shutdown.
On device: Device-A, Port-7, use command: ip address IP-Address-8 255.255.255.0.
On device: Device-A, router eigrp 1, use command: no network IP-Subnet-6 0.0.0.255.
On device: Device-A, router eigrp 1, use command: network IP-Subnet-13 0.0.0.255.
On device: Device-A, Port-1, use command: no shutdown.
On device: Device-A, Port-1, use command: ip address IP-Address-11 255.255.255.0.
On device: Device-A, router eigrp 1, use command: no network IP-Subnet-17 0.0.0.255.
On device: Device-A, router eigrp 1, use command: no auto-summary.
On device: Device-I, Port-7, use command: ip address IP-Address-45 255.255.255.0.
On device: Device-I, router eigrp 1, use command: network IP-Subnet-18 0.0.0.255.
On device: Device-I, router eigrp 1, use command: no auto-summary.
On device: Device-H, Port-2, use command: no shutdown.
On device: Device-H, Port-2, use command: ip address IP-Address-20 255.255.255.0.
On device: Device-H, router eigrp 1, use command: no network IP-Subnet-29 0.0.0.255.
On device: Device-H, router eigrp 1, use command: network IP-Subnet-4 0.0.0.255.
On device: Device-H, router eigrp 1, use command: no auto-summary.
That is all that I can find, hope it helps.
Thanks.
 ################################################## 

---> The operator starts here:

Step 1: Checking on device: Device-G, Port-3, Link-Status. -> Issue-Found.
Step 2: Configure on device: Device-G, Port-3, Link-Status. -> Use command: no shutdown. 
Step 3: Configure on device: Device-G, Port-3, Link-Status. -> Use command: no shutdown. Parameter not needed.
Step 4: Checking on device: Device-G, Port-3, Link-Status. -> Here is Good.
Step 5: Checking on device: Device-G, Port-3, IP-Info. -> Issue-Found.
Step 6: Configure on device: Device-G, Port-3, IP-Info. -> Use command: ip address. 
Step 7: Configure on device: Device-G, Port-3, IP-Info. -> Use command: ip address. Use parameter: IP-Address-60.
Step 8: Checking on device: Device-G, Port-3, IP-Info. -> Here is Good.
Step 9: Checking on device: Device-A, Port-7, Link-Status. -> Issue-Found.
Step 10: Configure on device: Device-A, Port-7, Link-Status. -> Use command: no shutdown. 
Step 11: Configure on device: Device-A, Port-7, Link-Status. -> Use command: no shutdown. Parameter not needed.
Step 12: Checking on device: Device-A, Port-7, Link-Status. -> Here is Good.
Step 13: Checking on device: Device-A, Port-7, IP-Info. -> Issue-Found.
Step 14: Configure on device: Device-A, Port-7, IP-Info. -> Use command: ip address. 
Step 15: Configure on device: Device-A, Port-7, IP-Info. -> Use command: ip address. Use parameter: IP-Address-8.
Step 16: Checking on device: Device-A, Port-7, IP-Info. -> Here is Good.
Step 17: Checking on device: Device-G, Port-2, Link-Status. -> Issue-Found.
Step 18: Configure on device: Device-G, Port-2, Link-Status. -> Use command: no shutdown. 
Step 19: Configure on device: Device-G, Port-2, Link-Status. -> Use command: no shutdown. Parameter not needed.
Step 20: Checking on device: Device-G, Port-2, Link-Status. -> Here is Good.
Step 21: Checking on device: Device-G, Port-2, IP-Info. -> Here is Good.
Step 22: Checking on device: Device-H, Port-2, Link-Status. -> Issue-Found.
Step 23: Configure on device: Device-H, Port-2, Link-Status. -> Use command: no shutdown. 
Step 24: Configure on device: Device-H, Port-2, Link-Status. -> Use command: no shutdown. Parameter not needed.
Step 25: Checking on device: Device-H, Port-2, Link-Status. -> Here is Good.
Step 26: Checking on device: Device-H, Port-2, IP-Info. -> Issue-Found.
Step 27: Configure on device: Device-H, Port-2, IP-Info. -> Use command: ip address. 
Step 28: Configure on device: Device-H, Port-2, IP-Info. -> Use command: ip address. Use parameter: IP-Address-20.
Step 29: Checking on device: Device-H, Port-2, IP-Info. -> Here is Good.
Step 30: Checking on device: Device-A, Port-1, Link-Status. -> Issue-Found.
Step 31: Configure on device: Device-A, Port-1, Link-Status. -> Use command: no shutdown. 
Step 32: Configure on device: Device-A, Port-1, Link-Status. -> Use command: no shutdown. Parameter not needed.
Step 33: Checking on device: Device-A, Port-1, Link-Status. -> Here is Good.
Step 34: Checking on device: Device-A, Port-1, IP-Info. -> Issue-Found.
Step 35: Configure on device: Device-A, Port-1, IP-Info. -> Use command: ip address. 
Step 36: Configure on device: Device-A, Port-1, IP-Info. -> Use command: ip address. Use parameter: IP-Address-11.
Step 37: Checking on device: Device-A, Port-1, IP-Info. -> Here is Good.
Step 38: Checking on device: Device-I, Port-7, Link-Status. -> Here is Good.
Step 39: Checking on device: Device-I, Port-7, IP-Info. -> Issue-Found.
Step 40: Configure on device: Device-I, Port-7, IP-Info. -> Use command: ip address. 
Step 41: Configure on device: Device-I, Port-7, IP-Info. -> Use command: ip address. Use parameter: IP-Address-45.
Step 42: Checking on device: Device-I, Port-7, IP-Info. -> Here is Good.
Step 43: Checking on device: Device-G, eigrp 1, Routing-Feature-1. -> Here is Good.
Step 44: Checking on device: Device-G, eigrp 1, Routing-Feature-2. -> Here is Good.
Step 45: Checking on device: Device-G, eigrp 1, Routing-Feature-3. -> Here is Good.
Step 46: Checking on device: Device-G, eigrp 1, Routing-Feature-4. -> Issue-Found.
Step 47: Configure on device: Device-G, eigrp 1, Routing-Feature-4. -> Use command: network. 
Step 48: Configure on device: Device-G, eigrp 1, Routing-Feature-4. -> Use command: network. Use parameter: IP-Subnet-4.
Step 49: Checking on device: Device-G, eigrp 1, Routing-Feature-4. -> Here is Good.
Step 50: Checking on device: Device-G, eigrp 1, Routing-Feature-5. -> Here is Good.
Step 51: Checking on device: Device-G, eigrp 1, Routing-Feature-6. -> Here is Good.
Step 52: Checking on device: Device-G, eigrp 1, Routing-Feature-7. -> Here is Good.
Step 53: Checking on device: Device-G, eigrp 1, Routing-Feature-8. -> Here is Good.
Step 54: Checking on device: Device-G, eigrp 1, Routing-Feature-9. -> Here is Good.
Step 55: Checking on device: Device-G, eigrp 1, Routing-Feature-10. -> Here is Good.
Step 56: Checking on device: Device-G, eigrp 1, Routing-Feature-11. -> Here is Good.
Step 57: Checking on device: Device-G, eigrp 1, Routing-Feature-12. -> Here is Good.
Step 58: Checking on device: Device-G, eigrp 1, Routing-Feature-13. -> Here is Good.
Step 59: Checking on device: Device-G, eigrp 1, Routing-Feature-14. -> Issue-Found.
Step 60: Configure on device: Device-G, eigrp 1, Routing-Feature-14. -> Use command: no network. 
Step 61: Configure on device: Device-G, eigrp 1, Routing-Feature-14. -> Use command: no network. Use parameter: IP-Subnet-6.
Step 62: Checking on device: Device-G, eigrp 1, Routing-Feature-14. -> Here is Good.
Step 63: Checking on device: Device-G, eigrp 1, Routing-Feature-15. -> Issue-Found.
Step 64: Configure on device: Device-G, eigrp 1, Routing-Feature-15. -> Use command: network. 
Step 65: Configure on device: Device-G, eigrp 1, Routing-Feature-15. -> Use command: network. Use parameter: IP-Subnet-13.
Step 66: Checking on device: Device-G, eigrp 1, Routing-Feature-15. -> Here is Good.
Step 67: Checking on device: Device-G, eigrp 1, Routing-Feature-16. -> Here is Good.
Step 68: Checking on device: Device-G, eigrp 1, Routing-Feature-17. -> Issue-Found.
Step 69: Configure on device: Device-G, eigrp 1, Routing-Feature-17. -> Use command: no network. 
Step 70: Configure on device: Device-G, eigrp 1, Routing-Feature-17. -> Use command: no network. Use parameter: IP-Subnet-29.
Step 71: Checking on device: Device-G, eigrp 1, Routing-Feature-17. -> Here is Good.
Step 72: Checking on device: Device-G, eigrp 1, Routing-Feature-18. -> Here is Good.
Step 73: Checking on device: Device-G, eigrp 1, Routing-Feature-19. -> Issue-Found.
Step 74: Configure on device: Device-G, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. 
Step 75: Configure on device: Device-G, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. Parameter not needed.
Step 76: Checking on device: Device-G, eigrp 1, Routing-Feature-19. -> Here is Good.
Step 77: Checking on device: Device-G, eigrp 1, Routing-Feature-20. -> Here is Good.
Step 78: Checking on device: Device-A, eigrp 1, Routing-Feature-1. -> Here is Good.
Step 79: Checking on device: Device-A, eigrp 1, Routing-Feature-2. -> Here is Good.
Step 80: Checking on device: Device-A, eigrp 1, Routing-Feature-3. -> Here is Good.
Step 81: Checking on device: Device-A, eigrp 1, Routing-Feature-4. -> Here is Good.
Step 82: Checking on device: Device-A, eigrp 1, Routing-Feature-5. -> Here is Good.
Step 83: Checking on device: Device-A, eigrp 1, Routing-Feature-6. -> Issue-Found.
Step 84: Configure on device: Device-A, eigrp 1, Routing-Feature-6. -> Use command: network. 
Step 85: Configure on device: Device-A, eigrp 1, Routing-Feature-6. -> Use command: network. Use parameter: IP-Subnet-13.
Step 86: Checking on device: Device-A, eigrp 1, Routing-Feature-6. -> Here is Good.
Step 87: Checking on device: Device-A, eigrp 1, Routing-Feature-7. -> Issue-Found.
Step 88: Configure on device: Device-A, eigrp 1, Routing-Feature-7. -> Use command: no network. 
Step 89: Configure on device: Device-A, eigrp 1, Routing-Feature-7. -> Use command: no network. Use parameter: IP-Subnet-6.
Step 90: Checking on device: Device-A, eigrp 1, Routing-Feature-7. -> Here is Good.
Step 91: Checking on device: Device-A, eigrp 1, Routing-Feature-8. -> Here is Good.
Step 92: Checking on device: Device-A, eigrp 1, Routing-Feature-9. -> Here is Good.
Step 93: Checking on device: Device-A, eigrp 1, Routing-Feature-10. -> Here is Good.
Step 94: Checking on device: Device-A, eigrp 1, Routing-Feature-11. -> Here is Good.
Step 95: Checking on device: Device-A, eigrp 1, Routing-Feature-12. -> Here is Good.
Step 96: Checking on device: Device-A, eigrp 1, Routing-Feature-13. -> Here is Good.
Step 97: Checking on device: Device-A, eigrp 1, Routing-Feature-14. -> Here is Good.
Step 98: Checking on device: Device-A, eigrp 1, Routing-Feature-15. -> Here is Good.
Step 99: Checking on device: Device-A, eigrp 1, Routing-Feature-16. -> Issue-Found.
Step 100: Configure on device: Device-A, eigrp 1, Routing-Feature-16. -> Use command: no network. 
Step 101: Configure on device: Device-A, eigrp 1, Routing-Feature-16. -> Use command: no network. Use parameter: IP-Subnet-17.
Step 102: Checking on device: Device-A, eigrp 1, Routing-Feature-16. -> Here is Good.
Step 103: Checking on device: Device-A, eigrp 1, Routing-Feature-17. -> Here is Good.
Step 104: Checking on device: Device-A, eigrp 1, Routing-Feature-18. -> Here is Good.
Step 105: Checking on device: Device-A, eigrp 1, Routing-Feature-19. -> Issue-Found.
Step 106: Configure on device: Device-A, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. 
Step 107: Configure on device: Device-A, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. Parameter not needed.
Step 108: Checking on device: Device-A, eigrp 1, Routing-Feature-19. -> Here is Good.
Step 109: Checking on device: Device-A, eigrp 1, Routing-Feature-20. -> Here is Good.
Step 110: Checking on device: Device-I, eigrp 1, Routing-Feature-1. -> Here is Good.
Step 111: Checking on device: Device-I, eigrp 1, Routing-Feature-2. -> Here is Good.
Step 112: Checking on device: Device-I, eigrp 1, Routing-Feature-3. -> Here is Good.
Step 113: Checking on device: Device-I, eigrp 1, Routing-Feature-4. -> Here is Good.
Step 114: Checking on device: Device-I, eigrp 1, Routing-Feature-5. -> Here is Good.
Step 115: Checking on device: Device-I, eigrp 1, Routing-Feature-6. -> Here is Good.
Step 116: Checking on device: Device-I, eigrp 1, Routing-Feature-7. -> Here is Good.
Step 117: Checking on device: Device-I, eigrp 1, Routing-Feature-8. -> Here is Good.
Step 118: Checking on device: Device-I, eigrp 1, Routing-Feature-9. -> Here is Good.
Step 119: Checking on device: Device-I, eigrp 1, Routing-Feature-10. -> Here is Good.
Step 120: Checking on device: Device-I, eigrp 1, Routing-Feature-11. -> Here is Good.
Step 121: Checking on device: Device-I, eigrp 1, Routing-Feature-12. -> Here is Good.
Step 122: Checking on device: Device-I, eigrp 1, Routing-Feature-13. -> Issue-Found.
Step 123: Configure on device: Device-I, eigrp 1, Routing-Feature-13. -> Use command: network. 
Step 124: Configure on device: Device-I, eigrp 1, Routing-Feature-13. -> Use command: network. Use parameter: IP-Subnet-18.
Step 125: Checking on device: Device-I, eigrp 1, Routing-Feature-13. -> Here is Good.
Step 126: Checking on device: Device-I, eigrp 1, Routing-Feature-14. -> Here is Good.
Step 127: Checking on device: Device-I, eigrp 1, Routing-Feature-15. -> Here is Good.
Step 128: Checking on device: Device-I, eigrp 1, Routing-Feature-16. -> Here is Good.
Step 129: Checking on device: Device-I, eigrp 1, Routing-Feature-17. -> Here is Good.
Step 130: Checking on device: Device-I, eigrp 1, Routing-Feature-18. -> Here is Good.
Step 131: Checking on device: Device-I, eigrp 1, Routing-Feature-19. -> Issue-Found.
Step 132: Configure on device: Device-I, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. 
Step 133: Configure on device: Device-I, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. Parameter not needed.
Step 134: Checking on device: Device-I, eigrp 1, Routing-Feature-19. -> Here is Good.
Step 135: Checking on device: Device-I, eigrp 1, Routing-Feature-20. -> Here is Good.
Step 136: Checking on device: Device-H, eigrp 1, Routing-Feature-1. -> Here is Good.
Step 137: Checking on device: Device-H, eigrp 1, Routing-Feature-2. -> Here is Good.
Step 138: Checking on device: Device-H, eigrp 1, Routing-Feature-3. -> Here is Good.
Step 139: Checking on device: Device-H, eigrp 1, Routing-Feature-4. -> Here is Good.
Step 140: Checking on device: Device-H, eigrp 1, Routing-Feature-5. -> Issue-Found.
Step 141: Configure on device: Device-H, eigrp 1, Routing-Feature-5. -> Use command: network. 
Step 142: Configure on device: Device-H, eigrp 1, Routing-Feature-5. -> Use command: network. Use parameter: IP-Subnet-4.
Step 143: Checking on device: Device-H, eigrp 1, Routing-Feature-5. -> Here is Good.
Step 144: Checking on device: Device-H, eigrp 1, Routing-Feature-6. -> Here is Good.
Step 145: Checking on device: Device-H, eigrp 1, Routing-Feature-7. -> Here is Good.
Step 146: Checking on device: Device-H, eigrp 1, Routing-Feature-8. -> Issue-Found.
Step 147: Configure on device: Device-H, eigrp 1, Routing-Feature-8. -> Use command: no network. 
Step 148: Configure on device: Device-H, eigrp 1, Routing-Feature-8. -> Use command: no network. Use parameter: IP-Subnet-29.
Step 149: Checking on device: Device-H, eigrp 1, Routing-Feature-8. -> Here is Good.
Step 150: Checking on device: Device-H, eigrp 1, Routing-Feature-9. -> Here is Good.
Step 151: Checking on device: Device-H, eigrp 1, Routing-Feature-10. -> Here is Good.
Step 152: Checking on device: Device-H, eigrp 1, Routing-Feature-11. -> Here is Good.
Step 153: Checking on device: Device-H, eigrp 1, Routing-Feature-12. -> Here is Good.
Step 154: Checking on device: Device-H, eigrp 1, Routing-Feature-13. -> Here is Good.
Step 155: Checking on device: Device-H, eigrp 1, Routing-Feature-14. -> Here is Good.
Step 156: Checking on device: Device-H, eigrp 1, Routing-Feature-15. -> Here is Good.
Step 157: Checking on device: Device-H, eigrp 1, Routing-Feature-16. -> Here is Good.
Step 158: Checking on device: Device-H, eigrp 1, Routing-Feature-17. -> Here is Good.
Step 159: Checking on device: Device-H, eigrp 1, Routing-Feature-18. -> Here is Good.
Step 160: Checking on device: Device-H, eigrp 1, Routing-Feature-19. -> Issue-Found.
Step 161: Configure on device: Device-H, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. 
Step 162: Configure on device: Device-H, eigrp 1, Routing-Feature-19. -> Use command: no auto-summary. Parameter not needed.
Episode: 0, Correct-Steps/Total-Steps, Percentage: 162/162, 100, Max_substeps_used_on_Single_fault: 3, Reward: 1, Done: True, Total-Rewards: 162, Correct-Commands: 24, Remaining-Faults: 0, Fixed-Faults: 24.
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
