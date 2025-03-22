def matching_dict_to_set(matching):
    """Converts matching dict format to matching set format."""
    edges = set()
    for edge in matching.items():
        u, v = edge
        if (v, u) in edges or edge in edges:
            continue
        if u == v:
            raise ValueError(f"Selfloops cannot appear in matchings {edge}")
        edges.add(edge)
    return edges

def max_weight_matching(G, weight="weight"):
    """Compute a maximum-weighted matching of G represented as an adjacency dict."""
    class NoNode:
        pass

    class Blossom:
        __slots__ = ["childs", "edges", "mybestedges"]

        def __init__(self):
            self.childs = []
            self.edges = []
            self.mybestedges = None

        def leaves(self):
            stack = [*self.childs]
            while stack:
                t = stack.pop()
                if isinstance(t, Blossom):
                    stack.extend(t.childs)
                else:
                    yield t

    gnodes = list(G)
    if not gnodes:
        return set()

    maxweight = 0
    for u in G:
        for v in G[u]:
            if u == v:
                continue
            edge_data = G[u][v]
            if isinstance(edge_data, dict):
                wt = edge_data.get(weight, 1)
            else:
                wt = edge_data
            if wt > maxweight:
                maxweight = wt

    mate = {}
    label = {}
    labeledge = {}
    inblossom = dict(zip(gnodes, gnodes))
    blossomparent = dict(zip(gnodes, [None] * len(gnodes)))
    blossombase = dict(zip(gnodes, gnodes))
    bestedge = {}
    dualvar = dict(zip(gnodes, [maxweight] * len(gnodes)))
    blossomdual = {}
    allowedge = {}
    queue = []

    def slack(v, w):
        edge_data = G[v][w]
        if isinstance(edge_data, dict):
            wt = edge_data.get(weight, 1)
        else:
            wt = edge_data
        return dualvar[v] + dualvar[w] - 2 * wt

    def assignLabel(w, t, v):
        b = inblossom[w]
        assert label.get(w) is None and label.get(b) is None
        label[w] = label[b] = t
        if v is not None:
            labeledge[w] = labeledge[b] = (v, w)
        else:
            labeledge[w] = labeledge[b] = None
        bestedge[w] = bestedge[b] = None
        if t == 1:
            if isinstance(b, Blossom):
                queue.extend(b.leaves())
            else:
                queue.append(b)
        elif t == 2:
            base = blossombase[b]
            assignLabel(mate[base], 1, base)

    def scanBlossom(v, w):
        path = []
        base = NoNode
        while v is not NoNode:
            b = inblossom[v]
            if label[b] & 4:
                base = blossombase[b]
                break
            assert label[b] == 1
            path.append(b)
            label[b] = 5
            if labeledge[b] is None:
                v = NoNode
            else:
                v = labeledge[b][0]
                b = inblossom[v]
                assert label[b] == 2
                v = labeledge[b][0]
            if w is not NoNode:
                v, w = w, v
        for b in path:
            label[b] = 1
        return base

    def addBlossom(base, v, w):
        bb = inblossom[base]
        bv = inblossom[v]
        bw = inblossom[w]
        b = Blossom()
        blossombase[b] = base
        blossomparent[b] = None
        blossomparent[bb] = b
        b.childs = path = []
        b.edges = edgs = [(v, w)]
        while bv != bb:
            blossomparent[bv] = b
            path.append(bv)
            edgs.append(labeledge[bv])
            v = labeledge[bv][0]
            bv = inblossom[v]
        path.append(bb)
        path.reverse()
        edgs.reverse()
        while bw != bb:
            blossomparent[bw] = b
            path.append(bw)
            edgs.append((labeledge[bw][1], labeledge[bw][0]))
            w = labeledge[bw][0]
            bw = inblossom[w]
        label[b] = 1
        labeledge[b] = labeledge[bb]
        blossomdual[b] = 0
        for v in b.leaves():
            if label[inblossom[v]] == 2:
                queue.append(v)
            inblossom[v] = b
        bestedgeto = {}
        for bv in path:
            if isinstance(bv, Blossom):
                if bv.mybestedges is not None:
                    nblist = bv.mybestedges
                    bv.mybestedges = None
                else:
                    nblist = [
                        (v, w) for v in bv.leaves() for w in G[v] if v != w
                    ]
            else:
                nblist = [(bv, w) for w in G[bv] if bv != w]
            for k in nblist:
                (i, j) = k
                if inblossom[j] == b:
                    i, j = j, i
                bj = inblossom[j]
                if (
                    bj != b
                    and label.get(bj) == 1
                    and ((bj not in bestedgeto) or slack(i, j) < slack(*bestedgeto[bj]))
                ):
                    bestedgeto[bj] = k
            bestedge[bv] = None
        b.mybestedges = list(bestedgeto.values())
        mybestedge = None
        bestedge[b] = None
        for k in b.mybestedges:
            kslack = slack(*k)
            if mybestedge is None or kslack < mybestslack:
                mybestedge = k
                mybestslack = kslack
        bestedge[b] = mybestedge

    def expandBlossom(b, endstage):
        def _recurse(b, endstage):
            for s in b.childs:
                blossomparent[s] = None
                if isinstance(s, Blossom):
                    if endstage and blossomdual[s] == 0:
                        yield s
                else:
                    inblossom[s] = s
            if (not endstage) and label.get(b) == 2:
                entrychild = inblossom[labeledge[b][1]]
                j = b.childs.index(entrychild)
                if j & 1:
                    j -= len(b.childs)
                    jstep = 1
                else:
                    jstep = -1
                v, w = labeledge[b]
                while j != 0:
                    if jstep == 1:
                        p, q = b.edges[j]
                    else:
                        q, p = b.edges[j - 1]
                    label[w] = None
                    label[q] = None
                    assignLabel(w, 2, v)
                    allowedge[(p, q)] = allowedge[(q, p)] = True
                    j += jstep
                    if jstep == 1:
                        v, w = b.edges[j]
                    else:
                        w, v = b.edges[j - 1]
                    allowedge[(v, w)] = allowedge[(w, v)] = True
                    j += jstep
                bw = b.childs[j]
                label[w] = label[bw] = 2
                labeledge[w] = labeledge[bw] = (v, w)
                bestedge[bw] = None
                j += jstep
                while b.childs[j] != entrychild:
                    bv = b.childs[j]
                    if label.get(bv) == 1:
                        j += jstep
                        continue
                    if isinstance(bv, Blossom):
                        for v in bv.leaves():
                            if label.get(v):
                                break
                    else:
                        v = bv
                    if label.get(v):
                        assert label[v] == 2
                        assert inblossom[v] == bv
                        label[v] = None
                        label[mate[blossombase[bv]]] = None
                        assignLabel(v, 2, labeledge[v][0])
                    j += jstep
            label.pop(b, None)
            labeledge.pop(b, None)
            bestedge.pop(b, None)
            del blossomparent[b]
            del blossombase[b]
            del blossomdual[b]

        stack = [_recurse(b, endstage)]
        while stack:
            top = stack[-1]
            for s in top:
                stack.append(_recurse(s, endstage))
                break
            else:
                stack.pop()

    def augmentBlossom(b, v):
        def _recurse(b, v):
            t = v
            while blossomparent[t] != b:
                t = blossomparent[t]
            i = j = b.childs.index(t)
            if i & 1:
                j -= len(b.childs)
                jstep = 1
            else:
                jstep = -1
            while j != 0:
                j += jstep
                t = b.childs[j]
                if jstep == 1:
                    w, x = b.edges[j]
                else:
                    x, w = b.edges[j - 1]
                if isinstance(t, Blossom):
                    yield (t, w)
                j += jstep
                t = b.childs[j]
                if isinstance(t, Blossom):
                    yield (t, x)
                mate[w] = x
                mate[x] = w
            b.childs = b.childs[i:] + b.childs[:i]
            b.edges = b.edges[i:] + b.edges[:i]
            blossombase[b] = blossombase[b.childs[0]]
            assert blossombase[b] == v

        stack = [_recurse(b, v)]
        while stack:
            top = stack[-1]
            for args in top:
                stack.append(_recurse(*args))
                break
            else:
                stack.pop()

    def augmentMatching(v, w):
        for s, j in ((v, w), (w, v)):
            while 1:
                bs = inblossom[s]
                assert label[bs] == 1
                assert (labeledge[bs] is None and blossombase[bs] not in mate) or (
                    labeledge[bs][0] == mate[blossombase[bs]]
                )
                if isinstance(bs, Blossom):
                    augmentBlossom(bs, s)
                mate[s] = j
                if labeledge[bs] is None:
                    break
                t = labeledge[bs][0]
                bt = inblossom[t]
                assert label[bt] == 2
                s, j = labeledge[bt]
                assert blossombase[bt] == t
                if isinstance(bt, Blossom):
                    augmentBlossom(bt, j)
                mate[j] = s

    def verifyOptimum():
        vdualoffset = 0
        assert min(dualvar.values()) + vdualoffset >= 0
        assert len(blossomdual) == 0 or min(blossomdual.values()) >= 0
        for i in G:
            for j in G[i]:
                if i == j:
                    continue
                edge_data = G[i][j]
                if isinstance(edge_data, dict):
                    wt = edge_data.get(weight, 1)
                else:
                    wt = edge_data
                s = dualvar[i] + dualvar[j] - 2 * wt
                iblossoms = [i]
                jblossoms = [j]
                while blossomparent[iblossoms[-1]] is not None:
                    iblossoms.append(blossomparent[iblossoms[-1]])
                while blossomparent[jblossoms[-1]] is not None:
                    jblossoms.append(blossomparent[jblossoms[-1]])
                iblossoms.reverse()
                jblossoms.reverse()
                for bi, bj in zip(iblossoms, jblossoms):
                    if bi != bj:
                        break
                    s += 2 * blossomdual[bi]
                assert s >= 0, f"Edge {i}-{j} has negative slack {s}"
                if mate.get(i) == j or mate.get(j) == i:
                    assert mate[i] == j and mate[j] == i
                    assert s == 0, f"Matched edge {i}-{j} has slack {s}"
        for v in gnodes:
            if v not in mate:
                assert dualvar[v] + vdualoffset == 0, f"Exposed node {v} has dualvar {dualvar[v]}"
        for b in blossomdual:
            if blossomdual[b] > 0:
                assert len(b.edges) % 2 == 1, f"Blossom {b} has even number of edges"
                for i, j in b.edges[1::2]:
                    assert mate[i] == j and mate[j] == i, f"Edge {i}-{j} not matched in blossom {b}"

    while 1:
        label.clear()
        labeledge.clear()
        bestedge.clear()
        for b in blossomdual:
            b.mybestedges = None
        allowedge.clear()
        queue[:] = []
        for v in gnodes:
            if (v not in mate) and label.get(inblossom[v]) is None:
                assignLabel(v, 1, None)
        augmented = 0
        while 1:
            while queue and not augmented:
                v = queue.pop()
                assert label[inblossom[v]] == 1
                for w in G[v]:
                    if w == v:
                        continue
                    bv = inblossom[v]
                    bw = inblossom[w]
                    if bv == bw:
                        continue
                    if (v, w) not in allowedge:
                        kslack = slack(v, w)
                        if kslack <= 0:
                            allowedge[(v, w)] = allowedge[(w, v)] = True
                    if (v, w) in allowedge:
                        if label.get(bw) is None:
                            assignLabel(w, 2, v)
                        elif label.get(bw) == 1:
                            base = scanBlossom(v, w)
                            if base is not NoNode:
                                addBlossom(base, v, w)
                            else:
                                augmentMatching(v, w)
                                augmented = 1
                                break
                        elif label.get(w) is None:
                            assert label[bw] == 2
                            label[w] = 2
                            labeledge[w] = (v, w)
                    elif label.get(bw) == 1:
                        if bestedge.get(bv) is None or kslack < slack(*bestedge[bv]):
                            bestedge[bv] = (v, w)
                    elif label.get(w) is None:
                        if bestedge.get(w) is None or kslack < slack(*bestedge[w]):
                            bestedge[w] = (v, w)
            if augmented:
                break
            deltatype = -1
            delta = deltaedge = deltablossom = None
            deltatype = 1
            delta = min(dualvar.values())
            for v in gnodes:
                if label.get(inblossom[v]) is None and bestedge.get(v) is not None:
                    d = slack(*bestedge[v])
                    if deltatype == -1 or d < delta:
                        delta = d
                        deltatype = 2
                        deltaedge = bestedge[v]
            for b in blossomparent:
                if (
                    blossomparent[b] is None
                    and label.get(b) == 1
                    and bestedge.get(b) is not None
                ):
                    kslack = slack(*bestedge[b])
                    d = kslack // 2  # Use integer division
                    if deltatype == -1 or d < delta:
                        delta = d
                        deltatype = 3
                        deltaedge = bestedge[b]
            for b in blossomdual:
                if (
                    blossomparent[b] is None
                    and label.get(b) == 2
                    and (deltatype == -1 or blossomdual[b] < delta)
                ):
                    delta = blossomdual[b]
                    deltatype = 4
                    deltablossom = b
            if deltatype == -1:
                deltatype = 1
                delta = max(0, min(dualvar.values()))
            for v in gnodes:
                if label.get(inblossom[v]) == 1:
                    dualvar[v] -= delta
                elif label.get(inblossom[v]) == 2:
                    dualvar[v] += delta
            for b in blossomdual:
                if blossomparent[b] is None:
                    if label.get(b) == 1:
                        blossomdual[b] += delta
                    elif label.get(b) == 2:
                        blossomdual[b] -= delta
            if deltatype == 1:
                break
            elif deltatype == 2:
                (v, w) = deltaedge
                allowedge[(v, w)] = allowedge[(w, v)] = True
                queue.append(v)
            elif deltatype == 3:
                (v, w) = deltaedge
                allowedge[(v, w)] = allowedge[(w, v)] = True
                queue.append(v)
            elif deltatype == 4:
                expandBlossom(deltablossom, False)
        if not augmented:
            break
        for b in list(blossomdual.keys()):
            if b not in blossomdual:
                continue
            if blossomparent[b] is None and label.get(b) == 1 and blossomdual[b] == 0:
                expandBlossom(b, True)
    verifyOptimum()
    return matching_dict_to_set(mate)
