from mceqveto import *
from matplotlib import pyplot as plt


def test_pr(cos_theta=1., kind='numu', pmods=(), hadr='SIBYLL2.3c', accuracy=20, **kwargs):
    ens = np.logspace(2,9, 100)
    prs = plt.plot(ens, [passing_rate(en, cos_theta, kind, pmods,
                                      hadr, accuracy) for en in ens],
                   **kwargs)
    plt.xlim(10**3, 10**7)
    plt.ylim(0, 1)
    plt.xscale('log')
    return prs[0]


def test_brackets(cos_theta=1., kind='numu', hadr='SIBYLL2.3c',
                  params='g h1 h2 i w6 y1 y2 z ch_a ch_b ch_e'):
    params = params.split(' ')
    uppers = [BARR[param].error for param in params]
    lowers = [-BARR[param].error for param in params]
    all_pmods = [tuple(zip(params, uppers)), tuple(zip(params, lowers))]
    pr = test_pr(cos_theta, kind, hadr=hadr, label='{} cth={}'.format(kind, cos_theta))
    for pmods in all_pmods:
        test_pr(cos_theta, kind, pmods, hadr, color=pr.get_color(), alpha=1-abs(pmods[0][-1]))


def test_samples(cos_theta=1, kind='numu', hadr='SIBYLL2.3c',
                 seed=88, nsamples=10, params='g h1 h2 i w6 y1 y2 z ch_a ch_b ch_e'):
    params = params.split(' ')
    pr = test_pr(cos_theta, kind, hadr=hadr, label='{} cth={}'.format(kind, cos_theta))
    np.random.seed(seed)
    for i in xrange(nsamples-1):
        # max(-1, throw) prevents throws that dip below -100%
        errors = [max(-1, np.random.normal(scale=BARR[param].error)) for param in params]
        pmods = tuple(zip(params, errors))
        test_pr(cos_theta, kind, pmods, hadr, color=pr.get_color(), alpha=1-min(np.mean(np.abs(errors)), 0.9))


def test_hadrs(cos_theta=1, kind='numu'):
    hadrs=['SIBYLL2.1', 'QGSJET-II-04', 'EPOS-LHC', 'SIBYLL2.3', 'SIBYLL2.3c']
    for hadr in hadrs:
        pr = test_pr(cos_theta, kind, hadr=hadr, label='{} {} cth={}'.format(hadr, kind, cos_theta))
