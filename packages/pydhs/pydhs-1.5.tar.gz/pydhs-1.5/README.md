# This package is created by Jiangshan(Tonny) Ma in his Ph.D. work in Tokyo Institute of Technology
## Tutorial
    import numpy as np
    import pydhs
    arr = np.array(pydhs.sample.get_bell2009())
    sarr =arr[:,:3].astype('int').astype('str')
    w_min, w_max = arr[:,-2], arr[:,-1]
    n, m = pydhs.describe(sarr)
    g = pydhs.make_graph(sarr, n, m)
    alg = pydhs.Ma2013(g)
    h = np.zeros(m)
    alg.run('1','37', w_min, w_max, h)

    print '------------------------------------'
    print 'eid\tvid pair\tpossibility'
    print '------------------------------------'
    for i in alg.hyperpath:
        edge = g.get_edge(i[0])
        eid, p = i
        print eid, '\t', edge.get_fv().id,'-->', edge.get_tv().id, '\t', round(p, 2)
    print '------------------------------------'
