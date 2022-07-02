//import * as be from '../threejs/node_modules/three/build/three.module.js';

function a(e) {
    return yt(e);
    /*for (var n = e.faces.length, a = 0; a < n;) {
        var r = e.faces[a];
        a += 1;
        var i = {
            isQuad: Ct(r, 0),
            hasMaterial: Ct(r, 1),
            hasFaceVertexUv: Ct(r, 3),
            hasFaceNormal: Ct(r, 4),
            hasFaceVertexNormal: Ct(r, 5),
            hasFaceColor: Ct(r, 6),
            hasFaceVertexColor: Ct(r, 7)
        };
        a = i.isQuad ? gt(t, a, e, i) : xt(t, a, e, i)
    }*/
}

function has_algo(e, t) {
    return function (e) {
        if (Array.isArray(e)) return e
    }(e) || function (e, t) {
        var n = null == e ? null : "undefined" !== typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
        if (null != n) {
            var r, o, a = [], i = !0, s = !1;
            try {
                for (n = n.call(e); !(i = (r = n.next()).done) && (a.push(r.value), !t || a.length !== t); i = !0) ;
            } catch (c) {
                s = !0, o = c
            } finally {
                try {
                    i || null == n.return || n.return()
                } finally {
                    if (s) throw o
                }
            }
            return a
        }
    }(e, t) || (0, r.Z)(e, t) || function () {
        throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
    }()
}

var f80318 = function (e, t, n) {
    "use strict";
    n.d(t, {
        Z: function () {
            return o
        }
    });
    var r = f16988;

    function o(e, t) {
        return function (e) {
            if (Array.isArray(e)) return e
        }(e) || function (e, t) {
            var n = null == e ? null : "undefined" !== typeof Symbol && e[Symbol.iterator] || e["@@iterator"];
            if (null != n) {
                var r, o, a = [], i = !0, s = !1;
                try {
                    for (n = n.call(e); !(i = (r = n.next()).done) && (a.push(r.value), !t || a.length !== t); i = !0) ;
                } catch (c) {
                    s = !0, o = c
                } finally {
                    try {
                        i || null == n.return || n.return()
                    } finally {
                        if (s) throw o
                    }
                }
                return a
            }
        }(e, t) || (0, r.Z)(e, t) || function () {
            throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")
        }()
    }
}

var f16988 = function (e, t, n) {
    "use strict";
    n.d(t, {
        Z: function () {
            return o
        }
    });
    var r = f56586;

    function o(e, t) {
        if (e) {
            if ("string" === typeof e) return (0, r.Z)(e, t);
            var n = Object.prototype.toString.call(e).slice(8, -1);
            return "Object" === n && e.constructor && (n = e.constructor.name), "Map" === n || "Set" === n ? Array.from(e) : "Arguments" === n || /^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n) ? (0, r.Z)(e, t) : void 0
        }
    }
}

var f56586 = function (e, t, n) {
    "use strict";

    function r(e, t) {
        (null == t || t > e.length) && (t = e.length);
        for (var n = 0, r = new Array(t); n < t; n++) r[n] = e[n];
        return r
    }

    n.d(t, {
        Z: function () {
            return r
        }
    })
}
let gt;
let xt;
let Ct;
let _t;
let wt;
let yt;
let vt;
vt = f80318
gt = function (e, t, n, a) {
    try {
        var r = e.nUVLayers
            , i = n.faces[t]
            , o = n.faces[t + 1]
            , s = n.faces[t + 2]
            , c = n.faces[t + 3]
            , l = [n.vertices[3 * i], n.vertices[3 * i + 1], n.vertices[3 * i + 2]]
            , u = [n.vertices[3 * o], n.vertices[3 * o + 1], n.vertices[3 * o + 2]]
            , m = [n.vertices[3 * s], n.vertices[3 * s + 1], n.vertices[3 * s + 2]]
            , h = [n.vertices[3 * c], n.vertices[3 * c + 1], n.vertices[3 * c + 2]]
            , f = [].concat(l, u, h, u, m, h);
        if (t += 4,
        n.skinIndices && n.skinWeights) {
            var p = void 0 !== n.influencesPerVertex ? n.influencesPerVertex : 2;
            if (n.skinIndices.length > 1 && n.skinWeights.length > 1) {
                var v, g = i * p, x = o * p, C = s * p, _ = c * p,
                    w = [n.skinWeights[g], p > 1 ? n.skinWeights[g + 1] : 0, p > 2 ? n.skinWeights[g + 2] : 0, p > 3 ? n.skinWeights[g + 3] : 0],
                    y = [n.skinWeights[x], p > 1 ? n.skinWeights[x + 1] : 0, p > 2 ? n.skinWeights[x + 2] : 0, p > 3 ? n.skinWeights[x + 3] : 0],
                    j = [n.skinWeights[C], p > 1 ? n.skinWeights[C + 1] : 0, p > 2 ? n.skinWeights[C + 2] : 0, p > 3 ? n.skinWeights[C + 3] : 0],
                    b = [n.skinWeights[_], p > 1 ? n.skinWeights[_ + 1] : 0, p > 2 ? n.skinWeights[_ + 2] : 0, p > 3 ? n.skinWeights[_ + 3] : 0];
                (v = e.skinWeight).push.apply(v, w.concat(y, b, y, j, b))
            } else {
                var k, S, M = [n.skinWeights[0], 0, 0, 0];
                (k = e.skinWeight).push.apply(k, M.concat(M, M, M, M, M));
                var P = [n.skinIndices[0], 0, 0, 0];
                (S = e.skinIndex).push.apply(S, P.concat(P, P, P, P, P))
            }
        }
        if (a.hasMaterial) {
            var z = n.faces[t];
            t += 1,
                e.materialIndices.push(z, z, z, z, z, z)
        }
        if (a.hasFaceVertexUv) {
            for (var R, D = 0; D < r; D += 1) {
                var A, O = n.uvs[D], I = n.faces[t];
                t += 1;
                var F = [O[2 * I], O[2 * I + 1]]
                    , T = n.faces[t];
                t += 1;
                var L = [O[2 * T], O[2 * T + 1]]
                    , N = n.faces[t];
                t += 1;
                var V = [O[2 * N], O[2 * N + 1]]
                    , H = n.faces[t];
                t += 1;
                var B = [O[2 * H], O[2 * H + 1]];
                (A = e.uvs[D]).push.apply(A, F.concat(L, B, L, V, B))
            }
            if (a.hasFaceNormal) {
                var E = 3 * n.faces[t];
                t += 1,
                    e.faceNormals.push(n.normals[E], n.normals[E + 1], n.normals[E + 2], n.normals[E], n.normals[E + 1], n.normals[E + 2])
            }
            if (a.hasFaceVertexNormal) {
                var Z, q = 3 * n.faces[t];
                t += 1;
                var W = [n.normals[q], n.normals[q + 1], n.normals[q + 3]]
                    , G = 3 * n.faces[t];
                t += 1;
                var U = [n.normals[G], n.normals[G + 1], n.normals[G + 3]]
                    , Q = 3 * n.faces[t];
                t += 1;
                var K = [n.normals[Q], n.normals[Q + 1], n.normals[Q + 3]]
                    , X = 3 * n.faces[t];
                t += 1;
                var Y = [n.normals[X], n.normals[X + 1], n.normals[X + 3]];
                (Z = e.vertexNormals).push.apply(Z, W.concat(U, Y, U, K, Y))
            }
            a.hasFaceColor && (t += 1),
            a.hasFaceVertexColor && n.colors && (t += 4),
                (R = e.position).push.apply(R, (0,
                    d.Z)(f))
        }
        return t
    } catch ($) {
        console.log($)
    }
}
xt = function (e, t, n, a) {
    var r, i, o = e.nUVLayers, s = n.faces[t], c = n.faces[t + 1], l = n.faces[t + 2], u = [s, c, l],
        d = [n.vertices[3 * s], n.vertices[3 * s + 1], n.vertices[3 * s + 2], n.vertices[3 * c], n.vertices[3 * c + 1], n.vertices[3 * c + 2], n.vertices[3 * l], n.vertices[3 * l + 1], n.vertices[3 * l + 2]];
    if (t += 3,
    n.skinWeights && n.skinIndices) {
        var m = void 0 !== n.influencesPerVertex ? n.influencesPerVertex : 2;
        if (n.skinIndices.length > 1 && n.skinWeights.length > 1) {
            var h = s * m
                , f = c * m
                , p = l * m;
            e.skinWeight.push(n.skinWeights[h], m > 1 ? n.skinWeights[h + 1] : 0, m > 2 ? n.skinWeights[h + 2] : 0, m > 3 ? n.skinWeights[h + 3] : 0, n.skinWeights[f], m > 1 ? n.skinWeights[f + 1] : 0, m > 2 ? n.skinWeights[f + 2] : 0, m > 3 ? n.skinWeights[f + 3] : 0, n.skinWeights[p], m > 1 ? n.skinWeights[p + 1] : 0, m > 2 ? n.skinWeights[p + 2] : 0, m > 3 ? n.skinWeights[p + 3] : 0),
                e.skinIndex.push(n.skinIndices[h], m > 1 ? n.skinIndices[h + 1] : 0, m > 2 ? n.skinIndices[h + 2] : 0, m > 3 ? n.skinIndices[h + 3] : 0, n.skinIndices[f], m > 1 ? n.skinIndices[f + 1] : 0, m > 2 ? n.skinIndices[f + 2] : 0, m > 3 ? n.skinIndices[f + 3] : 0, n.skinIndices[p], m > 1 ? n.skinIndices[p + 1] : 0, m > 2 ? n.skinIndices[p + 2] : 0, m > 3 ? n.skinIndices[p + 3] : 0)
        } else {
            var v, g, x = [n.skinWeights[0], 0, 0, 0];
            (v = e.skinWeight).push.apply(v, x.concat(x, x));
            var C = [n.skinIndices[0], 0, 0, 0];
            (g = e.skinIndex).push.apply(g, C.concat(C, C))
        }
    }
    if (a.hasMaterial) {
        var _ = n.faces[t];
        t += 1,
            e.materialIndices.push(_, _, _)
    }
    if (a.hasFaceVertexUv)
        for (var w = 0; w < o; w += 1)
            for (var y = n.uvs[w], j = 0; j < 3; j += 1) {
                var b = n.faces[t];
                t += 1;
                var k = y[2 * b]
                    , S = y[2 * b + 1];
                e.uvs[w].push(k, S)
            }
    if (a.hasFaceNormal) {
        var M = 3 * n.faces[t];
        t += 1,
            e.faceNormals.push(n.normals[M], n.normals[M + 1], n.normals[M + 2])
    }
    if (a.hasFaceVertexNormal)
        for (var P = 0; P < 3; P += 1) {
            var z = 3 * n.faces[t];
            t += 1,
                e.vertexNormals.push(n.normals[z], n.normals[z + 1], n.normals[z + 2])
        }
    if (a.hasFaceColor && (t += 1),
        a.hasFaceVertexColor)
        for (var R = 0; R < 3; R += 1)
            t += 1;
    return (r = e.index).push.apply(r, u),
        (i = e.position).push.apply(i, d),
        t
}
Ct = function (e, t) {
    return e & 1 << t
}
_t = function (e, t) {
    for (var n = e.faces.length, a = 0; a < n;) {
        var r = e.faces[a];
        a += 1;
        var i = {
            isQuad: Ct(r, 0),
            hasMaterial: Ct(r, 1),
            hasFaceVertexUv: Ct(r, 3),
            hasFaceNormal: Ct(r, 4),
            hasFaceVertexNormal: Ct(r, 5),
            hasFaceColor: Ct(r, 6),
            hasFaceVertexColor: Ct(r, 7)
        };
        a = i.isQuad ? gt(t, a, e, i) : xt(t, a, e, i)
    }
}
wt = function (e) {
    if (e.uvs) {
        for (var t = 0, n = [], a = 0; a < e.uvs.length; a++)
            e.uvs[a].length && (t += 1);
        for (var r = 0; r < t; r++)
            n.push([]);
        return [t, n]
    }
    return [0, []]
}



yt = function (e) {
    var t = arguments.length > 1 && void 0 !== arguments[1] && arguments[1]
        , n = wt(e)
        , a = has_algo(n, 2)
        , r = a[0]
        , i = a[1]
        , o = {
        nUVLayers: r,
        index: [],
        position: [],
        skinWeight: [],
        skinIndex: [],
        uvs: i,
        faceNormals: [],
        vertexNormals: [],
        faceColor: [],
        vertexColor: [],
        materialIndices: []
    };
    _t(e, o);
    return {object:o,
            t:t}
}