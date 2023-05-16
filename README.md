# Information on using / testing it

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
