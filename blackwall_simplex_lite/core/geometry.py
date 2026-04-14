import math


class Simplex4D:
    @staticmethod
    def _dot(a, b):
        return sum(x * y for x, y in zip(a, b))

    @staticmethod
    def _norm(v):
        return math.sqrt(Simplex4D._dot(v, v))

    @staticmethod
    def _sub(a, b):
        return [x - y for x, y in zip(a, b)]

    @staticmethod
    def _mul(v, s):
        return [x * s for x in v]

    @staticmethod
    def _proj(u, v):
        denom = Simplex4D._dot(v, v)
        if abs(denom) < 1e-12:
            return [0.0] * len(u)
        return Simplex4D._mul(v, Simplex4D._dot(u, v) / denom)

    @staticmethod
    def _gram_schmidt(vectors):
        basis = []
        for v in vectors:
            w = v[:]
            for b in basis:
                p = Simplex4D._proj(w, b)
                w = [w[i] - p[i] for i in range(len(w))]
            n = Simplex4D._norm(w)
            if n > 1e-9:
                basis.append([w[i] / n for i in range(len(w))])
        return basis

    @staticmethod
    def generate_simplex(size=1.0):
        e = [[1.0 if i == j else 0.0 for i in range(5)] for j in range(5)]
        c = [1.0 / 5.0] * 5
        u = [[e_i[k] - c[k] for k in range(5)] for e_i in e]

        seed = [Simplex4D._sub(u[i], u[4]) for i in range(4)]
        basis5 = Simplex4D._gram_schmidt(seed)

        vertices = []
        for vi in u:
            coords4 = [Simplex4D._dot(vi, b) for b in basis5]
            vertices.append(coords4)

        edges = []
        for i in range(5):
            for j in range(i + 1, 5):
                edges.append((i, j))

        if edges:
            i, j = edges[0]
            d = math.sqrt(sum((vertices[i][k] - vertices[j][k]) ** 2 for k in range(4)))
            if d > 1e-12:
                s = (2.0 * size) / d
                vertices = [[v[k] * s for k in range(4)] for v in vertices]

        return vertices, edges
