import numpy as np

from digital_logic.alg.P3code.p3_selectquestion import prepare_question_params, \
    update
from digital_logic.experiment.models import SparfaTrace


def test_mr_lan_algorithm(db):

    mastery = [0, 0, 0, 3, 3, 3]
    # Get the data from the db
    training_set = db.session.query(SparfaTrace).first()
    H = np.fromstring(training_set.H, dtype='float64').reshape((29, 4))
    d = np.fromstring(training_set.d, dtype='float64').reshape((4, 29))
    wmu = np.fromstring(training_set.wmu, dtype='float64').reshape(
        (5, 29))
    Gamma = np.fromstring(training_set.Gamma, dtype=np.float64).reshape(
        (4, 4, 29))
    mastery = np.array(mastery, dtype=np.float64)
    K, Q = d.shape
    question_ids = np.fromstring(training_set.question_ids, dtype="<U7")

    question_params_all = prepare_question_params(Q, H, d, wmu, Gamma)

    m0 = np.zeros((K,))
    V0 = 3.0 * np.ones((K,))

    mastery = np.hstack((m0, V0))

    avail = np.ones((Q,))

    qid = np.random.randint(Q)

    y = 1
    mp, Vp = update(y, question_params_all[qid], mastery)
    k = np.where(H[qid,] > 0)[0][0]
    mastery[k] = mp
    mastery[K + k] = Vp
    avail[qid] = 0.0
    q = question_ids[qid]
    assert q
