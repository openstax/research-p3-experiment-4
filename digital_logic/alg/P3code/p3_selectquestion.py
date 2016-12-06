__author__ = 'ricedspgroup'
"""
this code provides functions to perform iterative updates and
do personalized exercise recommendations
"""

import numpy as np
from scipy.stats import norm
import scipy.io as sio


def approx(m0, V0, w, mu):
    """
    Approximate Kalman Filter approximation step: a crucial step in updating
    student's state
    :param m0:
    :param V0:
    :param w:
    :param mu:
    :return:
    """
    den = np.sqrt(1 + V0 * (w ** 2))
    z = (w * m0 + mu) / den
    rat = norm.pdf(z) / np.double(norm.cdf(z))
    if z < -4:
        rat = -z
    mhat = m0 + V0 * w * rat / den
    Vhat = V0 - (w ** 2) * (V0 ** 2) * (rat * (z + rat) / den ** 2)

    return mhat, Vhat


def update(y, question_param, mastery):
    """
    this function updates a student's mastery given a new response to a question (y)
    and question_param, the parameter of this question
    :param y:
    :param question_param:
    :param mastery:
    :return:
    """
    m0 = mastery[0]
    V0 = mastery[1]
    w = question_param[0]
    mu = question_param[1]
    d = question_param[2]
    sig2 = question_param[3]

    m1, V1 = approx(m0, V0, (2 * y - 1) * w, (2 * y - 1) * mu)
    m2 = m1 + d
    V2 = V1 + sig2

    return m2, V2


def learn_effect(question_param, mastery):
    """
    this function calculates the expected immediate learning outcome for a student
    working on a question

    :param question_param:
    :param mastery:
    :return:
    """
    m0 = mastery[0]
    V0 = mastery[1]

    p1 = norm.cdf(m0 / V0)
    m0p, V0p = update(0, question_param, mastery)
    m1p, V1p = update(1, question_param, mastery)

    after_learn_cdf = p1 * norm.cdf(m1p / V1p) + (1 - p1) * norm.cdf(m0p / V0p)
    return after_learn_cdf


def question_selector(question_params_all, avail, mastery, no_questions):
    """
    this function selects the best personalized question for a student, given the current availability
    so if we want to choose among questions on a particular topic, we just manipulate the "avail" variable

    :param question_params_all:
    :param avail:
    :param mastery:
    :param no_questions:
    :return:
    """
    Q = len(question_params_all)
    K = len(mastery) / 2
    learning_gains = np.zeros((Q,))
    for ii in range(Q):
        if avail[ii] > 0:
            k = question_params_all[ii][4]
            learning_gains[ii] = learn_effect(question_params_all[ii],
                                              [mastery[k], mastery[K + k]])
        else:
            learning_gains[ii] = -np.inf

    idx = np.argsort(-learning_gains)
    return idx[0:no_questions]




if __name__ == '__main__':
    # load a data file containing pre-trained information on each question
    data = np.load('P3next.npy', encoding='latin1')
    H = data[0]
    d = data[1]
    wmu = data[2]
    Gamma = data[3]
    question_ids = data[4]

    K, Q = d.shape

    # re-format the trained info
    question_params_all = []
    for ii in range(Q):
        temp_question = []
        k = np.where(H[ii,] > 0)[0][0]
        temp_question = [wmu[k, ii], wmu[-1, ii], d[k, ii], Gamma[k, k, ii], k]
        question_params_all.append(temp_question)

    # start of time parameters
    m0 = np.zeros((K,))
    V0 = 3.0 * np.ones((K,))

    # run the test for 1 student! (for simplicy we'll use a synthetic student for demo purposes)
    T = 10
    np.random.seed(0)
    mastery = np.hstack((m0, V0))
    avail = np.ones((Q,))
    for tt in range(3):
        # for the first 3 time steps you only do the update but not select questions
        while True:
            qid = np.random.randint(Q)
            if avail[qid] > 0:
                break
        y = np.random.binomial(1, .5)
        mp, Vp = update(y, question_params_all[qid], mastery)
        k = np.where(H[qid,] > 0)[0][0]
        mastery[k] = mp
        mastery[K + k] = Vp
        avail[qid] = 0.0
        print(question_ids[qid])

    for tt in range(3, T):
        # now we choose what the student should do given their current state
        qid = question_selector(question_params_all, avail, mastery, 1)[0]

        # and then receive the answer and update the states
        y = np.random.binomial(1, .5)
        mp, Vp = update(y, question_params_all[qid], mastery)
        k = np.where(H[qid,] > 0)[0][0]
        mastery[k] = mp
        mastery[K + k] = Vp
        avail[qid] = 0.0
        print(question_ids[qid])
