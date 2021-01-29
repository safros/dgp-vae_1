"""
Classifier for downstream proxy task of hirid representations.
"""

import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score

from absl import flags, app

FLAGS = flags.FLAGS

flags.DEFINE_integer('seed', 42, 'Random seed')
flags.DEFINE_string('labels_path', '/cluster/work/grlab/projects/projects2020_disentangled_gpvae/data/hirid/mort_labels_test.npy', 'Hirid classification labels')
flags.DEFINE_string('representation_path', '/cluster/home/bings/dgpvae/models/hirid/comp/base/dim_8/len_25/scaled/n_scales_4/210126_n_1', 'Path to latent representation that are used as input features.')

def main(argv):
    del argv # Unused

    # Load labels and representations
    labels_full = np.load(FLAGS.labels_path)
    reps_path = os.path.join(FLAGS.representation_path, 'z_mean.npy')
    reps_full = np.load(reps_path)
    # Reshape representations
    reps_full_re = np.reshape(reps_full, (labels_full.shape[0], reps_full.shape[1], -1))
    # Flatten latent time series
    reps_full_flat = np.reshape(reps_full_re, (reps_full_re.shape[0], -1))

    # Filter out samples without label
    rm_idxs = np.where(labels_full == -1.0)[0]
    labels = np.delete(labels_full, rm_idxs, axis=0)
    reps = np.delete(reps_full_flat, rm_idxs, axis=0)

    print(labels.shape)
    print(reps.shape)

    # Create train and test set
    reps_train, reps_test, labels_train, labels_test = train_test_split(reps, labels, test_size=0.25, random_state=42)

    # SVM classifier
    svm_clf = SVC(kernel='linear', random_state=FLAGS.seed)
    svm_clf.fit(reps_train, labels_train)

    svm_score = roc_auc_score(labels_test, svm_clf.decision_function(reps_test))
    print(svm_score)




if __name__ == '__main__':
    app.run(main)
