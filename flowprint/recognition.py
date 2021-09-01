import argparse
import os
import numpy as np

from preprocessor  import Preprocessor
from flowprint     import FlowPrint
from sklearn.metrics         import classification_report
from sklearn.model_selection import train_test_split

import collections

if __name__ == "__main__":
    ########################################################################
    #                             Handle input                             #
    ########################################################################
    # Parse input
    parser = argparse.ArgumentParser("FlowPrint recognition example")
    parser.add_argument('--files' , nargs='+', help='files to use as input')
    parser.add_argument('--dir'   , help='directory containing files to use as input')
    parser.add_argument('--ratio' , type=float, default=0.5, help='train ratio of data (default=0.5)')
    parser.add_argument('--random', action='store_true', help='split randomly instead of sequentially')
    args = parser.parse_args()

    # Check if arguments were given
    # if (args.files is None and args.dir is None) or\
    #    (args.files is not None and args.dir is not None):
    #     raise ValueError("Please specify either --files or --dir but not both.")

    # Get file names
    # files = args.files or [args.dir+x for x in os.listdir(args.dir)]
    # files = ['data\\amongus\\amongus1.pcap', 'data\\amongus\\amongus2.pcap', 'data\\amongus\\amongus3.pcap', 
    # 'data\\amongus\\amongus4.pcap', 'data\\amongus\\amongus5.pcap', 'data\\daifm\\daifm.pcap', 
    # 'data\\diijam\\diijam.pcap', 'data\\fptplay\\fptplay1.pcap', 'data\\fptplay\\fptplay2.pcap',
    #  'data\\freefire\\freefire.pcap', 'data\\lienquan\\lienquan1.pcap', 'data\\lienquan\\lienquan2.pcap',
    #   'data\\nhaccuatui\\nhaccuatui.pcap', 'data\\nhacvang\\nhacvang.pcap', 'data\\phim247\\phim247_1.pcap',
    #    'data\\phim247\\phim247_2.pcap', 'data\\pinterest\\pinterest1.pcap', 'data\\pinterest\\pinterest2.pcap', 
    #    'data\\pubg\\pubg1.pcap', 'data\\pubg\\pubg2.pcap', 'data\\pubg\\pubg3.pcap', 'data\\pubg\\pubg4.pcap', 
    #    'data\\pubg\\pubg5.pcap', 'data\\sachnoiapp\\sachnoiapp.pcap', 'data\\soundcloud\\soundcloud.pcap',
    #     'data\\spotify\\spotify.pcap', 'data\\truyenaudiosachnoiviet\\truyenaudiosachnoiviet1.pcap', 
    #     'data\\truyenaudiosachnoiviet\\truyenaudiosachnoiviet2.pcap', 'data\\tunefm\\tunefm1.pcap',
    #      'data\\tunefm\\tunefm2.pcap', 'data\\voizfm\\voizfm.pcap', 'data\\vtvgo\\vtvgo1.pcap',
    #       'data\\vtvgo\\vtvgo2.pcap', 'data\\youtube\\youtube1.pcap', 'data\\youtube\\youtube2.pcap',
    #        'data\\zingmp3\\zingmp3.pcap']
    
    # labels = ['amongus']*5 + ['daifm', 'diijam', 'fptplay', 'fptplay', 'freefire'] + ['lienquan']*2 +\
    # ['nhaccuatui', 'nhacvang'] + ['phim247']*2 + ['pinterest']*2 + ['pubg']*5 + ['sachnoiapp', 'soundclound'] +\
    # ['spotify'] + ['truyenaudiosachnoiviet']*2 + ['tunefm']*2 + ['voizfm'] + ['vtvgo']*2 + ['youtube']*2 + ['zingmp3']

    def get_files(folder):
        files = []
        labels = []
        for app in os.listdir(folder):
            app_path = os.path.join(folder, app)
            for filename in os.listdir(app_path):
                path = os.path.join(app_path, filename)
                files.append(path)
                labels.append(app)
        return files, labels

    train_files, train_labels = get_files('dataset')
    test_files, test_labels = get_files('test_dataset')

    preprocessor = Preprocessor(verbose=True)
    X_train, y_train = preprocessor.process(train_files, train_labels)
    print('Count flows: ', collections.Counter(y_train))
    X_test, y_test = preprocessor.process(test_files, test_labels)

     # Create FlowPrint example
    flowprint = FlowPrint(
        batch       = 300,
        window      = 30,
        correlation = 0.1,
        similarity  = 0.9
    )

    # Fit FlowPrint with training data
    flowprint.fit(X_train, y_train)
    # Create test fingerprints
    fp_test = flowprint.fingerprinter.fit_predict(X_test)
    # Create prediction
    y_pred = flowprint.recognize(fp_test)

    ########################################################################
    #                           Print evaluation                           #
    ########################################################################
    print(classification_report(y_test, y_pred, digits=4))



    

    # ########################################################################
    # #                              Read data                               #
    # ########################################################################
    # # Create preprocessor
    # preprocessor = Preprocessor(verbose=True)
    # # Process all files
    # # X, y = preprocessor.process(files, files)
    # X, y = preprocessor.process(files, labels)

    # ########################################################################
    # #                              Split data                              #
    # ########################################################################
    # if args.random:
    #     # Perform random split
    #     X_train, X_test, y_train, y_test = train_test_split(
    #         X, y, test_size=args.ratio, random_state=42)

    # # Perform temporal split split
    # else:
    #     # Initialise training and testing data
    #     X_train = list()
    #     y_train = list()
    #     X_test  = list()
    #     y_test  = list()

    #     # Loop over each different app
    #     for app in np.unique(y):
    #         # Extract flows relevant for selected app
    #         X_app = X[y == app]
    #         y_app = y[y == app]

    #         # Create train and test instances by split
    #         X_app_train = X_app[:int(X_app.shape[0]*args.ratio) ]
    #         y_app_train = y_app[:int(X_app.shape[0]*args.ratio) ]
    #         X_app_test  = X_app[ int(X_app.shape[0]*args.ratio):]
    #         y_app_test  = y_app[ int(X_app.shape[0]*args.ratio):]

    #         # Append to training/testing data
    #         X_train.append(X_app_train)
    #         y_train.append(y_app_train)
    #         X_test.append(X_app_test)
    #         y_test.append(y_app_test)

    #         # Print how we split the data
    #         print("Split {:40} into {} train and {} test flows".format(
    #             app, X_app_train.shape[0], X_app_test.shape[0]))

    #     # Concatenate
    #     X_train = np.concatenate(X_train)
    #     y_train = np.concatenate(y_train)
    #     X_test  = np.concatenate(X_test )
    #     y_test  = np.concatenate(y_test )

    # ########################################################################
    # #                              Flowprint                               #
    # ########################################################################
    # # Create FlowPrint example
    # flowprint = FlowPrint(
    #     batch       = 300,
    #     window      = 30,
    #     correlation = 0.1,
    #     similarity  = 0.9
    # )

    # # Fit FlowPrint with training data
    # flowprint.fit(X_train, y_train)
    # # Create test fingerprints
    # fp_test = flowprint.fingerprinter.fit_predict(X_test)
    # # Create prediction
    # y_pred = flowprint.recognize(fp_test)

    # ########################################################################
    # #                           Print evaluation                           #
    # ########################################################################
    # print(classification_report(y_test, y_pred, digits=4))
