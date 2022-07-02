__all__ = ['utilsWeb']

# Don't look below, you will not understand this Python code :) I don't.

from js2py.pyjs import *
# setting scope
var = Scope( JS_BUILTINS )
set_global_object(var)

# Code follows:
var.registers(['yt', 'xt', 'f56586', 'gt', 'Ct', '_t', 'wt', 'vt', 'has_algo', 'f16988', 'f80318', 'a'])
@Js
def PyJsHoisted_a_(e, this, arguments, var=var):
    var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
    var.registers(['e'])
    return var.get('yt')(var.get('e'))
PyJsHoisted_a_.func_name = 'a'
var.put('a', PyJsHoisted_a_)
@Js
def PyJsHoisted_has_algo_(e, t, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
    var.registers(['t', 'e'])
    @Js
    def PyJs_anonymous_0_(e, this, arguments, var=var):
        var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
        var.registers(['e'])
        if var.get('Array').callprop('isArray', var.get('e')):
            return var.get('e')
    PyJs_anonymous_0_._set_name('anonymous')
    @Js
    def PyJs_anonymous_1_(e, t, this, arguments, var=var):
        var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
        var.registers(['e', 'n', 'i', 's', 't', 'r', 'o', 'a'])
        var.put('n', (var.get(u"null") if (var.get(u"null")==var.get('e')) else ((PyJsStrictNeq(Js('undefined'),var.get('Symbol',throw=False).typeof()) and var.get('e').get(var.get('Symbol').get('iterator'))) or var.get('e').get('@@iterator'))))
        if (var.get(u"null")!=var.get('n')):
            var.put('a', Js([]))
            var.put('i', Js(0.0).neg())
            var.put('s', Js(1.0).neg())
            try:
                #for JS loop
                var.put('n', var.get('n').callprop('call', var.get('e')))
                while (var.put('i', var.put('r', var.get('n').callprop('next')).get('done')).neg() and PyJsComma(var.get('a').callprop('push', var.get('r').get('value')),(var.get('t').neg() or PyJsStrictNeq(var.get('a').get('length'),var.get('t'))))):
                    try:
                        pass
                    finally:
                            var.put('i', Js(0.0).neg())
            except PyJsException as PyJsTempException:
                PyJsHolder_63_67166127 = var.own.get('c')
                var.force_own_put('c', PyExceptionToJs(PyJsTempException))
                try:
                    PyJsComma(var.put('s', Js(0.0).neg()),var.put('o', var.get('c')))
                finally:
                    if PyJsHolder_63_67166127 is not None:
                        var.own['c'] = PyJsHolder_63_67166127
                    else:
                        del var.own['c']
                    del PyJsHolder_63_67166127
            finally:
                try:
                    ((var.get('i') or (var.get(u"null")==var.get('n').get('return'))) or var.get('n').callprop('return'))
                finally:
                    if var.get('s'):
                        PyJsTempException = JsToPyException(var.get('o'))
                        raise PyJsTempException
            return var.get('a')
    PyJs_anonymous_1_._set_name('anonymous')
    @Js
    def PyJs_anonymous_2_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        PyJsTempException = JsToPyException(var.get('TypeError').create(Js('Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.')))
        raise PyJsTempException
    PyJs_anonymous_2_._set_name('anonymous')
    return (((PyJs_anonymous_0_(var.get('e')) or PyJs_anonymous_1_(var.get('e'), var.get('t'))) or PyJsComma(Js(0.0),var.get('r').get('Z'))(var.get('e'), var.get('t'))) or PyJs_anonymous_2_())
PyJsHoisted_has_algo_.func_name = 'has_algo'
var.put('has_algo', PyJsHoisted_has_algo_)
pass
pass
@Js
def PyJs_anonymous_3_(e, t, n, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n', 't', 'r', 'o', 'e'])
    @Js
    def PyJsHoisted_o_(e, t, this, arguments, var=var):
        var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
        var.registers(['t', 'e'])
        @Js
        def PyJs_anonymous_5_(e, this, arguments, var=var):
            var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
            var.registers(['e'])
            if var.get('Array').callprop('isArray', var.get('e')):
                return var.get('e')
        PyJs_anonymous_5_._set_name('anonymous')
        @Js
        def PyJs_anonymous_6_(e, t, this, arguments, var=var):
            var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
            var.registers(['e', 'n', 'i', 's', 't', 'r', 'o', 'a'])
            var.put('n', (var.get(u"null") if (var.get(u"null")==var.get('e')) else ((PyJsStrictNeq(Js('undefined'),var.get('Symbol',throw=False).typeof()) and var.get('e').get(var.get('Symbol').get('iterator'))) or var.get('e').get('@@iterator'))))
            if (var.get(u"null")!=var.get('n')):
                var.put('a', Js([]))
                var.put('i', Js(0.0).neg())
                var.put('s', Js(1.0).neg())
                try:
                    #for JS loop
                    var.put('n', var.get('n').callprop('call', var.get('e')))
                    while (var.put('i', var.put('r', var.get('n').callprop('next')).get('done')).neg() and PyJsComma(var.get('a').callprop('push', var.get('r').get('value')),(var.get('t').neg() or PyJsStrictNeq(var.get('a').get('length'),var.get('t'))))):
                        try:
                            pass
                        finally:
                                var.put('i', Js(0.0).neg())
                except PyJsException as PyJsTempException:
                    PyJsHolder_63_71438206 = var.own.get('c')
                    var.force_own_put('c', PyExceptionToJs(PyJsTempException))
                    try:
                        PyJsComma(var.put('s', Js(0.0).neg()),var.put('o', var.get('c')))
                    finally:
                        if PyJsHolder_63_71438206 is not None:
                            var.own['c'] = PyJsHolder_63_71438206
                        else:
                            del var.own['c']
                        del PyJsHolder_63_71438206
                finally:
                    try:
                        ((var.get('i') or (var.get(u"null")==var.get('n').get('return'))) or var.get('n').callprop('return'))
                    finally:
                        if var.get('s'):
                            PyJsTempException = JsToPyException(var.get('o'))
                            raise PyJsTempException
                return var.get('a')
        PyJs_anonymous_6_._set_name('anonymous')
        @Js
        def PyJs_anonymous_7_(this, arguments, var=var):
            var = Scope({'this':this, 'arguments':arguments}, var)
            var.registers([])
            PyJsTempException = JsToPyException(var.get('TypeError').create(Js('Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.')))
            raise PyJsTempException
        PyJs_anonymous_7_._set_name('anonymous')
        return (((PyJs_anonymous_5_(var.get('e')) or PyJs_anonymous_6_(var.get('e'), var.get('t'))) or PyJsComma(Js(0.0),var.get('r').get('Z'))(var.get('e'), var.get('t'))) or PyJs_anonymous_7_())
    PyJsHoisted_o_.func_name = 'o'
    var.put('o', PyJsHoisted_o_)
    Js('use strict')
    @Js
    def PyJs_anonymous_4_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get('o')
    PyJs_anonymous_4_._set_name('anonymous')
    var.get('n').callprop('d', var.get('t'), Js({'Z':PyJs_anonymous_4_}))
    var.put('r', var.get('f16988'))
    pass
PyJs_anonymous_3_._set_name('anonymous')
var.put('f80318', PyJs_anonymous_3_)
@Js
def PyJs_anonymous_8_(e, t, n, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['n', 't', 'r', 'o', 'e'])
    @Js
    def PyJsHoisted_o_(e, t, this, arguments, var=var):
        var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
        var.registers(['n', 't', 'e'])
        if var.get('e'):
            if PyJsStrictEq(Js('string'),var.get('e',throw=False).typeof()):
                return PyJsComma(Js(0.0),var.get('r').get('Z'))(var.get('e'), var.get('t'))
            var.put('n', var.get('Object').get('prototype').get('toString').callprop('call', var.get('e')).callprop('slice', Js(8.0), (-Js(1.0))))
            def PyJs_LONG_10_(var=var):
                return PyJsComma(((PyJsStrictEq(Js('Object'),var.get('n')) and var.get('e').get('constructor')) and var.put('n', var.get('e').get('constructor').get('name'))),(var.get('Array').callprop('from', var.get('e')) if (PyJsStrictEq(Js('Map'),var.get('n')) or PyJsStrictEq(Js('Set'),var.get('n'))) else (PyJsComma(Js(0.0),var.get('r').get('Z'))(var.get('e'), var.get('t')) if (PyJsStrictEq(Js('Arguments'),var.get('n')) or JsRegExp('/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/').callprop('test', var.get('n'))) else PyJsComma(Js(0.0), Js(None)))))
            return PyJs_LONG_10_()
    PyJsHoisted_o_.func_name = 'o'
    var.put('o', PyJsHoisted_o_)
    Js('use strict')
    @Js
    def PyJs_anonymous_9_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get('o')
    PyJs_anonymous_9_._set_name('anonymous')
    var.get('n').callprop('d', var.get('t'), Js({'Z':PyJs_anonymous_9_}))
    var.put('r', var.get('f56586'))
    pass
PyJs_anonymous_8_._set_name('anonymous')
var.put('f16988', PyJs_anonymous_8_)
@Js
def PyJs_anonymous_11_(e, t, n, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'n':n, 'this':this, 'arguments':arguments}, var)
    var.registers(['e', 'n', 't', 'r'])
    @Js
    def PyJsHoisted_r_(e, t, this, arguments, var=var):
        var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
        var.registers(['e', 'n', 't', 'r'])
        (((var.get(u"null")==var.get('t')) or (var.get('t')>var.get('e').get('length'))) and var.put('t', var.get('e').get('length')))
        #for JS loop
        var.put('n', Js(0.0))
        var.put('r', var.get('Array').create(var.get('t')))
        while (var.get('n')<var.get('t')):
            try:
                var.get('r').put(var.get('n'), var.get('e').get(var.get('n')))
            finally:
                    (var.put('n',Js(var.get('n').to_number())+Js(1))-Js(1))
        return var.get('r')
    PyJsHoisted_r_.func_name = 'r'
    var.put('r', PyJsHoisted_r_)
    Js('use strict')
    pass
    @Js
    def PyJs_anonymous_12_(this, arguments, var=var):
        var = Scope({'this':this, 'arguments':arguments}, var)
        var.registers([])
        return var.get('r')
    PyJs_anonymous_12_._set_name('anonymous')
    var.get('n').callprop('d', var.get('t'), Js({'Z':PyJs_anonymous_12_}))
PyJs_anonymous_11_._set_name('anonymous')
var.put('f56586', PyJs_anonymous_11_)
pass
pass
pass
pass
pass
pass
pass
var.put('vt', var.get('f80318'))
@Js
def PyJs_anonymous_13_(e, t, n, a, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'n':n, 'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['k', 'c', 'l', 'G', 'P', 'L', 'p', 'C', 'z', 'x', 'M', 'Q', 'w', 'g', 'e', 'm', 'i', 'f', 'E', 'h', 'Y', 'B', 'I', 'n', 'u', 'j', 'V', 'R', 'U', '_', 'K', 'N', 'A', 'X', 'S', 'W', 'v', 'q', 'T', 'Z', 'O', 's', 'D', 't', 'y', 'F', 'r', 'o', 'b', 'H', 'a'])
    try:
        var.put('r', var.get('e').get('nUVLayers'))
        var.put('i', var.get('n').get('faces').get(var.get('t')))
        var.put('o', var.get('n').get('faces').get((var.get('t')+Js(1.0))))
        var.put('s', var.get('n').get('faces').get((var.get('t')+Js(2.0))))
        var.put('c', var.get('n').get('faces').get((var.get('t')+Js(3.0))))
        var.put('l', Js([var.get('n').get('vertices').get((Js(3.0)*var.get('i'))), var.get('n').get('vertices').get(((Js(3.0)*var.get('i'))+Js(1.0))), var.get('n').get('vertices').get(((Js(3.0)*var.get('i'))+Js(2.0)))]))
        var.put('u', Js([var.get('n').get('vertices').get((Js(3.0)*var.get('o'))), var.get('n').get('vertices').get(((Js(3.0)*var.get('o'))+Js(1.0))), var.get('n').get('vertices').get(((Js(3.0)*var.get('o'))+Js(2.0)))]))
        var.put('m', Js([var.get('n').get('vertices').get((Js(3.0)*var.get('s'))), var.get('n').get('vertices').get(((Js(3.0)*var.get('s'))+Js(1.0))), var.get('n').get('vertices').get(((Js(3.0)*var.get('s'))+Js(2.0)))]))
        var.put('h', Js([var.get('n').get('vertices').get((Js(3.0)*var.get('c'))), var.get('n').get('vertices').get(((Js(3.0)*var.get('c'))+Js(1.0))), var.get('n').get('vertices').get(((Js(3.0)*var.get('c'))+Js(2.0)))]))
        var.put('f', Js([]).callprop('concat', var.get('l'), var.get('u'), var.get('h'), var.get('u'), var.get('m'), var.get('h')))
        if PyJsComma(var.put('t', Js(4.0), '+'),(var.get('n').get('skinIndices') and var.get('n').get('skinWeights'))):
            var.put('p', (var.get('n').get('influencesPerVertex') if PyJsStrictNeq(PyJsComma(Js(0.0), Js(None)),var.get('n').get('influencesPerVertex')) else Js(2.0)))
            if ((var.get('n').get('skinIndices').get('length')>Js(1.0)) and (var.get('n').get('skinWeights').get('length')>Js(1.0))):
                var.put('g', (var.get('i')*var.get('p')))
                var.put('x', (var.get('o')*var.get('p')))
                var.put('C', (var.get('s')*var.get('p')))
                var.put('_', (var.get('c')*var.get('p')))
                var.put('w', Js([var.get('n').get('skinWeights').get(var.get('g')), (var.get('n').get('skinWeights').get((var.get('g')+Js(1.0))) if (var.get('p')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('g')+Js(2.0))) if (var.get('p')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('g')+Js(3.0))) if (var.get('p')>Js(3.0)) else Js(0.0))]))
                var.put('y', Js([var.get('n').get('skinWeights').get(var.get('x')), (var.get('n').get('skinWeights').get((var.get('x')+Js(1.0))) if (var.get('p')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('x')+Js(2.0))) if (var.get('p')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('x')+Js(3.0))) if (var.get('p')>Js(3.0)) else Js(0.0))]))
                var.put('j', Js([var.get('n').get('skinWeights').get(var.get('C')), (var.get('n').get('skinWeights').get((var.get('C')+Js(1.0))) if (var.get('p')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('C')+Js(2.0))) if (var.get('p')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('C')+Js(3.0))) if (var.get('p')>Js(3.0)) else Js(0.0))]))
                var.put('b', Js([var.get('n').get('skinWeights').get(var.get('_')), (var.get('n').get('skinWeights').get((var.get('_')+Js(1.0))) if (var.get('p')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('_')+Js(2.0))) if (var.get('p')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('_')+Js(3.0))) if (var.get('p')>Js(3.0)) else Js(0.0))]))
                var.put('v', var.get('e').get('skinWeight')).get('push').callprop('apply', var.get('v'), var.get('w').callprop('concat', var.get('y'), var.get('b'), var.get('y'), var.get('j'), var.get('b')))
            else:
                var.put('M', Js([var.get('n').get('skinWeights').get('0'), Js(0.0), Js(0.0), Js(0.0)]))
                var.put('k', var.get('e').get('skinWeight')).get('push').callprop('apply', var.get('k'), var.get('M').callprop('concat', var.get('M'), var.get('M'), var.get('M'), var.get('M'), var.get('M')))
                var.put('P', Js([var.get('n').get('skinIndices').get('0'), Js(0.0), Js(0.0), Js(0.0)]))
                var.put('S', var.get('e').get('skinIndex')).get('push').callprop('apply', var.get('S'), var.get('P').callprop('concat', var.get('P'), var.get('P'), var.get('P'), var.get('P'), var.get('P')))
        if var.get('a').get('hasMaterial'):
            var.put('z', var.get('n').get('faces').get(var.get('t')))
            PyJsComma(var.put('t', Js(1.0), '+'),var.get('e').get('materialIndices').callprop('push', var.get('z'), var.get('z'), var.get('z'), var.get('z'), var.get('z'), var.get('z')))
        if var.get('a').get('hasFaceVertexUv'):
            #for JS loop
            var.put('D', Js(0.0))
            while (var.get('D')<var.get('r')):
                try:
                    var.put('O', var.get('n').get('uvs').get(var.get('D')))
                    var.put('I', var.get('n').get('faces').get(var.get('t')))
                    var.put('t', Js(1.0), '+')
                    var.put('F', Js([var.get('O').get((Js(2.0)*var.get('I'))), var.get('O').get(((Js(2.0)*var.get('I'))+Js(1.0)))]))
                    var.put('T', var.get('n').get('faces').get(var.get('t')))
                    var.put('t', Js(1.0), '+')
                    var.put('L', Js([var.get('O').get((Js(2.0)*var.get('T'))), var.get('O').get(((Js(2.0)*var.get('T'))+Js(1.0)))]))
                    var.put('N', var.get('n').get('faces').get(var.get('t')))
                    var.put('t', Js(1.0), '+')
                    var.put('V', Js([var.get('O').get((Js(2.0)*var.get('N'))), var.get('O').get(((Js(2.0)*var.get('N'))+Js(1.0)))]))
                    var.put('H', var.get('n').get('faces').get(var.get('t')))
                    var.put('t', Js(1.0), '+')
                    var.put('B', Js([var.get('O').get((Js(2.0)*var.get('H'))), var.get('O').get(((Js(2.0)*var.get('H'))+Js(1.0)))]))
                    var.put('A', var.get('e').get('uvs').get(var.get('D'))).get('push').callprop('apply', var.get('A'), var.get('F').callprop('concat', var.get('L'), var.get('B'), var.get('L'), var.get('V'), var.get('B')))
                finally:
                        var.put('D', Js(1.0), '+')
            if var.get('a').get('hasFaceNormal'):
                var.put('E', (Js(3.0)*var.get('n').get('faces').get(var.get('t'))))
                def PyJs_LONG_14_(var=var):
                    return PyJsComma(var.put('t', Js(1.0), '+'),var.get('e').get('faceNormals').callprop('push', var.get('n').get('normals').get(var.get('E')), var.get('n').get('normals').get((var.get('E')+Js(1.0))), var.get('n').get('normals').get((var.get('E')+Js(2.0))), var.get('n').get('normals').get(var.get('E')), var.get('n').get('normals').get((var.get('E')+Js(1.0))), var.get('n').get('normals').get((var.get('E')+Js(2.0)))))
                PyJs_LONG_14_()
            if var.get('a').get('hasFaceVertexNormal'):
                var.put('q', (Js(3.0)*var.get('n').get('faces').get(var.get('t'))))
                var.put('t', Js(1.0), '+')
                var.put('W', Js([var.get('n').get('normals').get(var.get('q')), var.get('n').get('normals').get((var.get('q')+Js(1.0))), var.get('n').get('normals').get((var.get('q')+Js(3.0)))]))
                var.put('G', (Js(3.0)*var.get('n').get('faces').get(var.get('t'))))
                var.put('t', Js(1.0), '+')
                var.put('U', Js([var.get('n').get('normals').get(var.get('G')), var.get('n').get('normals').get((var.get('G')+Js(1.0))), var.get('n').get('normals').get((var.get('G')+Js(3.0)))]))
                var.put('Q', (Js(3.0)*var.get('n').get('faces').get(var.get('t'))))
                var.put('t', Js(1.0), '+')
                var.put('K', Js([var.get('n').get('normals').get(var.get('Q')), var.get('n').get('normals').get((var.get('Q')+Js(1.0))), var.get('n').get('normals').get((var.get('Q')+Js(3.0)))]))
                var.put('X', (Js(3.0)*var.get('n').get('faces').get(var.get('t'))))
                var.put('t', Js(1.0), '+')
                var.put('Y', Js([var.get('n').get('normals').get(var.get('X')), var.get('n').get('normals').get((var.get('X')+Js(1.0))), var.get('n').get('normals').get((var.get('X')+Js(3.0)))]))
                var.put('Z', var.get('e').get('vertexNormals')).get('push').callprop('apply', var.get('Z'), var.get('W').callprop('concat', var.get('U'), var.get('Y'), var.get('U'), var.get('K'), var.get('Y')))
            PyJsComma(PyJsComma((var.get('a').get('hasFaceColor') and var.put('t', Js(1.0), '+')),((var.get('a').get('hasFaceVertexColor') and var.get('n').get('colors')) and var.put('t', Js(4.0), '+'))),var.put('R', var.get('e').get('position')).get('push').callprop('apply', var.get('R'), PyJsComma(Js(0.0),var.get('d').get('Z'))(var.get('f'))))
        return var.get('t')
    except PyJsException as PyJsTempException:
        PyJsHolder_24_20825798 = var.own.get('$')
        var.force_own_put('$', PyExceptionToJs(PyJsTempException))
        try:
            var.get('console').callprop('log', var.get('$'))
        finally:
            if PyJsHolder_24_20825798 is not None:
                var.own['$'] = PyJsHolder_24_20825798
            else:
                del var.own['$']
            del PyJsHolder_24_20825798
PyJs_anonymous_13_._set_name('anonymous')
var.put('gt', PyJs_anonymous_13_)
@Js
def PyJs_anonymous_15_(e, t, n, a, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'n':n, 'a':a, 'this':this, 'arguments':arguments}, var)
    var.registers(['k', 'c', 'l', 'P', 'p', 'C', 'z', 'x', 'M', 'w', 'g', 'e', 'd', 'm', 'i', 'f', 'h', 'n', 'u', 'j', 'R', '_', 'S', 'v', 's', 't', 'y', 'r', 'o', 'b', 'a'])
    var.put('o', var.get('e').get('nUVLayers'))
    var.put('s', var.get('n').get('faces').get(var.get('t')))
    var.put('c', var.get('n').get('faces').get((var.get('t')+Js(1.0))))
    var.put('l', var.get('n').get('faces').get((var.get('t')+Js(2.0))))
    var.put('u', Js([var.get('s'), var.get('c'), var.get('l')]))
    var.put('d', Js([var.get('n').get('vertices').get((Js(3.0)*var.get('s'))), var.get('n').get('vertices').get(((Js(3.0)*var.get('s'))+Js(1.0))), var.get('n').get('vertices').get(((Js(3.0)*var.get('s'))+Js(2.0))), var.get('n').get('vertices').get((Js(3.0)*var.get('c'))), var.get('n').get('vertices').get(((Js(3.0)*var.get('c'))+Js(1.0))), var.get('n').get('vertices').get(((Js(3.0)*var.get('c'))+Js(2.0))), var.get('n').get('vertices').get((Js(3.0)*var.get('l'))), var.get('n').get('vertices').get(((Js(3.0)*var.get('l'))+Js(1.0))), var.get('n').get('vertices').get(((Js(3.0)*var.get('l'))+Js(2.0)))]))
    if PyJsComma(var.put('t', Js(3.0), '+'),(var.get('n').get('skinWeights') and var.get('n').get('skinIndices'))):
        var.put('m', (var.get('n').get('influencesPerVertex') if PyJsStrictNeq(PyJsComma(Js(0.0), Js(None)),var.get('n').get('influencesPerVertex')) else Js(2.0)))
        if ((var.get('n').get('skinIndices').get('length')>Js(1.0)) and (var.get('n').get('skinWeights').get('length')>Js(1.0))):
            var.put('h', (var.get('s')*var.get('m')))
            var.put('f', (var.get('c')*var.get('m')))
            var.put('p', (var.get('l')*var.get('m')))
            def PyJs_LONG_16_(var=var):
                return var.get('e').get('skinWeight').callprop('push', var.get('n').get('skinWeights').get(var.get('h')), (var.get('n').get('skinWeights').get((var.get('h')+Js(1.0))) if (var.get('m')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('h')+Js(2.0))) if (var.get('m')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('h')+Js(3.0))) if (var.get('m')>Js(3.0)) else Js(0.0)), var.get('n').get('skinWeights').get(var.get('f')), (var.get('n').get('skinWeights').get((var.get('f')+Js(1.0))) if (var.get('m')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('f')+Js(2.0))) if (var.get('m')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('f')+Js(3.0))) if (var.get('m')>Js(3.0)) else Js(0.0)), var.get('n').get('skinWeights').get(var.get('p')), (var.get('n').get('skinWeights').get((var.get('p')+Js(1.0))) if (var.get('m')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('p')+Js(2.0))) if (var.get('m')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinWeights').get((var.get('p')+Js(3.0))) if (var.get('m')>Js(3.0)) else Js(0.0)))
            def PyJs_LONG_17_(var=var):
                return var.get('e').get('skinIndex').callprop('push', var.get('n').get('skinIndices').get(var.get('h')), (var.get('n').get('skinIndices').get((var.get('h')+Js(1.0))) if (var.get('m')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinIndices').get((var.get('h')+Js(2.0))) if (var.get('m')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinIndices').get((var.get('h')+Js(3.0))) if (var.get('m')>Js(3.0)) else Js(0.0)), var.get('n').get('skinIndices').get(var.get('f')), (var.get('n').get('skinIndices').get((var.get('f')+Js(1.0))) if (var.get('m')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinIndices').get((var.get('f')+Js(2.0))) if (var.get('m')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinIndices').get((var.get('f')+Js(3.0))) if (var.get('m')>Js(3.0)) else Js(0.0)), var.get('n').get('skinIndices').get(var.get('p')), (var.get('n').get('skinIndices').get((var.get('p')+Js(1.0))) if (var.get('m')>Js(1.0)) else Js(0.0)), (var.get('n').get('skinIndices').get((var.get('p')+Js(2.0))) if (var.get('m')>Js(2.0)) else Js(0.0)), (var.get('n').get('skinIndices').get((var.get('p')+Js(3.0))) if (var.get('m')>Js(3.0)) else Js(0.0)))
            PyJsComma(PyJs_LONG_16_(),PyJs_LONG_17_())
        else:
            var.put('x', Js([var.get('n').get('skinWeights').get('0'), Js(0.0), Js(0.0), Js(0.0)]))
            var.put('v', var.get('e').get('skinWeight')).get('push').callprop('apply', var.get('v'), var.get('x').callprop('concat', var.get('x'), var.get('x')))
            var.put('C', Js([var.get('n').get('skinIndices').get('0'), Js(0.0), Js(0.0), Js(0.0)]))
            var.put('g', var.get('e').get('skinIndex')).get('push').callprop('apply', var.get('g'), var.get('C').callprop('concat', var.get('C'), var.get('C')))
    if var.get('a').get('hasMaterial'):
        var.put('_', var.get('n').get('faces').get(var.get('t')))
        PyJsComma(var.put('t', Js(1.0), '+'),var.get('e').get('materialIndices').callprop('push', var.get('_'), var.get('_'), var.get('_')))
    if var.get('a').get('hasFaceVertexUv'):
        #for JS loop
        var.put('w', Js(0.0))
        while (var.get('w')<var.get('o')):
            try:
                #for JS loop
                var.put('y', var.get('n').get('uvs').get(var.get('w')))
                var.put('j', Js(0.0))
                while (var.get('j')<Js(3.0)):
                    try:
                        var.put('b', var.get('n').get('faces').get(var.get('t')))
                        var.put('t', Js(1.0), '+')
                        var.put('k', var.get('y').get((Js(2.0)*var.get('b'))))
                        var.put('S', var.get('y').get(((Js(2.0)*var.get('b'))+Js(1.0))))
                        var.get('e').get('uvs').get(var.get('w')).callprop('push', var.get('k'), var.get('S'))
                    finally:
                            var.put('j', Js(1.0), '+')
            finally:
                    var.put('w', Js(1.0), '+')
    if var.get('a').get('hasFaceNormal'):
        var.put('M', (Js(3.0)*var.get('n').get('faces').get(var.get('t'))))
        PyJsComma(var.put('t', Js(1.0), '+'),var.get('e').get('faceNormals').callprop('push', var.get('n').get('normals').get(var.get('M')), var.get('n').get('normals').get((var.get('M')+Js(1.0))), var.get('n').get('normals').get((var.get('M')+Js(2.0)))))
    if var.get('a').get('hasFaceVertexNormal'):
        #for JS loop
        var.put('P', Js(0.0))
        while (var.get('P')<Js(3.0)):
            try:
                var.put('z', (Js(3.0)*var.get('n').get('faces').get(var.get('t'))))
                PyJsComma(var.put('t', Js(1.0), '+'),var.get('e').get('vertexNormals').callprop('push', var.get('n').get('normals').get(var.get('z')), var.get('n').get('normals').get((var.get('z')+Js(1.0))), var.get('n').get('normals').get((var.get('z')+Js(2.0)))))
            finally:
                    var.put('P', Js(1.0), '+')
    if PyJsComma((var.get('a').get('hasFaceColor') and var.put('t', Js(1.0), '+')),var.get('a').get('hasFaceVertexColor')):
        #for JS loop
        var.put('R', Js(0.0))
        while (var.get('R')<Js(3.0)):
            try:
                var.put('t', Js(1.0), '+')
            finally:
                    var.put('R', Js(1.0), '+')
    return PyJsComma(PyJsComma(var.put('r', var.get('e').get('index')).get('push').callprop('apply', var.get('r'), var.get('u')),var.put('i', var.get('e').get('position')).get('push').callprop('apply', var.get('i'), var.get('d'))),var.get('t'))
PyJs_anonymous_15_._set_name('anonymous')
var.put('xt', PyJs_anonymous_15_)
@Js
def PyJs_anonymous_18_(e, t, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
    var.registers(['t', 'e'])
    return (var.get('e')&(Js(1.0)<<var.get('t')))
PyJs_anonymous_18_._set_name('anonymous')
var.put('Ct', PyJs_anonymous_18_)
@Js
def PyJs_anonymous_19_(e, t, this, arguments, var=var):
    var = Scope({'e':e, 't':t, 'this':this, 'arguments':arguments}, var)
    var.registers(['n', 'i', 't', 'r', 'a', 'e'])
    #for JS loop
    var.put('n', var.get('e').get('faces').get('length'))
    var.put('a', Js(0.0))
    while (var.get('a')<var.get('n')):
        var.put('r', var.get('e').get('faces').get(var.get('a')))
        var.put('a', Js(1.0), '+')
        var.put('i', Js({'isQuad':var.get('Ct')(var.get('r'), Js(0.0)),'hasMaterial':var.get('Ct')(var.get('r'), Js(1.0)),'hasFaceVertexUv':var.get('Ct')(var.get('r'), Js(3.0)),'hasFaceNormal':var.get('Ct')(var.get('r'), Js(4.0)),'hasFaceVertexNormal':var.get('Ct')(var.get('r'), Js(5.0)),'hasFaceColor':var.get('Ct')(var.get('r'), Js(6.0)),'hasFaceVertexColor':var.get('Ct')(var.get('r'), Js(7.0))}))
        var.put('a', (var.get('gt')(var.get('t'), var.get('a'), var.get('e'), var.get('i')) if var.get('i').get('isQuad') else var.get('xt')(var.get('t'), var.get('a'), var.get('e'), var.get('i'))))
    
PyJs_anonymous_19_._set_name('anonymous')
var.put('_t', PyJs_anonymous_19_)
@Js
def PyJs_anonymous_20_(e, this, arguments, var=var):
    var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
    var.registers(['n', 't', 'r', 'a', 'e'])
    if var.get('e').get('uvs'):
        #for JS loop
        var.put('t', Js(0.0))
        var.put('n', Js([]))
        var.put('a', Js(0.0))
        while (var.get('a')<var.get('e').get('uvs').get('length')):
            try:
                (var.get('e').get('uvs').get(var.get('a')).get('length') and var.put('t', Js(1.0), '+'))
            finally:
                    (var.put('a',Js(var.get('a').to_number())+Js(1))-Js(1))
        #for JS loop
        var.put('r', Js(0.0))
        while (var.get('r')<var.get('t')):
            try:
                var.get('n').callprop('push', Js([]))
            finally:
                    (var.put('r',Js(var.get('r').to_number())+Js(1))-Js(1))
        return Js([var.get('t'), var.get('n')])
    return Js([Js(0.0), Js([])])
PyJs_anonymous_20_._set_name('anonymous')
var.put('wt', PyJs_anonymous_20_)
@Js
def PyJs_anonymous_21_(e, this, arguments, var=var):
    var = Scope({'e':e, 'this':this, 'arguments':arguments}, var)
    var.registers(['e', 'n', 'i', 't', 'r', 'o', 'a'])
    var.put('t', (((var.get('arguments').get('length')>Js(1.0)) and PyJsStrictNeq(PyJsComma(Js(0.0), Js(None)),var.get('arguments').get('1'))) and var.get('arguments').get('1')))
    var.put('n', var.get('wt')(var.get('e')))
    var.put('a', var.get('has_algo')(var.get('n'), Js(2.0)))
    var.put('r', var.get('a').get('0'))
    var.put('i', var.get('a').get('1'))
    var.put('o', Js({'nUVLayers':var.get('r'),'index':Js([]),'position':Js([]),'skinWeight':Js([]),'skinIndex':Js([]),'uvs':var.get('i'),'faceNormals':Js([]),'vertexNormals':Js([]),'faceColor':Js([]),'vertexColor':Js([]),'materialIndices':Js([])}))
    var.get('_t')(var.get('e'), var.get('o'))
    return Js({'object':var.get('o'),'t':var.get('t')})
PyJs_anonymous_21_._set_name('anonymous')
var.put('yt', PyJs_anonymous_21_)


# Add lib to the module scope
utilsWeb = var.to_python()