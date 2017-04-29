import os
import pickle
from subprocess import run

import pandas as pd

import neural_net

if __name__ == '__main__':
    exit_ = False
    while not exit_:
        print('\nMenu\n1. Train Neural Net')
        print('2. Analyse Voice')
        print('3. Exit')
        option = input('Enter Option Number: ')

        if option == '1':
            neural_net.run()
        elif option == '2':
            if not os.path.isfile('neural_net'):  # check if neural_net file exists
                print('\nNeural net not trained. First train the neural net.')
            else:
                # sound_recorder.run()

                print('\nExtracting data from recorded voice...\n')
                run(['Rscript', 'getAttributes1.r', os.getcwd(), 'output.wav'])

                print('\nPreprocessing extracted data...')
                data = pd.read_csv('output/voiceDetails.csv')
                del data['peakf'], data['sound.files'], data['selec'], data['duration']
                dataset = pd.read_csv('voice.csv')
                dataset = dataset.iloc[:, :-1]
                data = (data - dataset.mean()) / (dataset.max() - dataset.min())  # scale

                neural_net = pickle.load(open('neural_net', 'rb'))  # load trained neural net from file
                print()
                print('Female' if neural_net.predict(data)[0] == 0 else 'Male')
        elif option == '3':
            exit_ = True
        else:
            print('Invalid option. Please try again...')
