from gtool.core.types.core import FunctionType
import pyparsing as p
from gtool.core.utils.misc import striptoclassname

class Slice(FunctionType):
    """
    Truncates a single string. Will return None if the attributes in the config string is missing.
    Does not work with multiple value attributes or attributes that are dynamic objects.

    Example strings are:
    '@text1[:5] returns the first 5 characters of the string'
    '@text2[1:-1] returns the string without the first and last character'
    '@text3[1:4] returns the string without the first character stopping at the 4th'
    '@text4[1:] returns the string without the first character'

    """

    def __init__(self, obj, config=str()):
        
        self.stringvalue = ""
        self.slicestart = None
        self.sliceend = None
        super(Slice, self).__init__(obj, config=config)

        if self.config is None or len(self.config) < 1 or not isinstance(self.config, str):
            raise ValueError('Slice plugin function requires a attribute and string slice be specified such as "@state[1:3]"')

    def compute(self):

        def slicer(stringvalue, start=None, end=None):
            if not isinstance(stringvalue, str):
                raise ValueError('Slice plugin only works on string '
                                 'or string like attributes but got '
                                 'a %s instead' %  striptoclassname(type(self.targetobject)))

            if start is None and end is None:
                raise ValueError('Slice plugin expects at least one of either a start and stop value')

            if isinstance(start, int) or start is None:
                pass
            else:
                raise ValueError('Slice plugin start value must be empty or an number but it got %s' % start)

            if isinstance(end, int) or end is None:
                pass
            else:
                raise ValueError('Slice plugin finish value must be empty or an number but it got %s' % end)

            if start is None:
                _ret = stringvalue[:end]
            elif end is None:
                _ret = stringvalue[start:]
            else:
                _ret = stringvalue[start:end]

            return _ret

        def getname(obj, name):

            _val = None

            if hasattr(obj, name):
                _val = getattr(obj, name, None)

            if _val is None:
                return _val

            # handling for values from a method
            if isinstance(_val, str):
                return _val

            # handling for values in an Attribute
            # TODO integrate logic for value native string and strings in Attributes
            try:
                if _val.isdynamic: #TODO make this work for non-attributes, non-dynamics (use .issingleton? - what about a concat mode?)
                    raise ValueError('Slice plugin cannot process %s because it contains a dynamic class' % name)
            except AttributeError:
                raise TypeError('Expected an attribute but got a %s' % type(_val))

            if _val.issingleton():
                _ret = '%s' % _val[0].raw()
            else:
                raise ValueError('Slice method plugin specified in user defined class %s '
                                 'only works on singleton attributes' % striptoclassname(type(self.targetobject)))

            return _ret

        attrexpr = (p.Literal('@') | p.Literal('!')).suppress() + p.Word(p.alphanums)
        slicestartexpr = p.Literal('[').suppress() + p.Optional(p.Word(p.nums))
        sliceendexpr = p.Optional(p.Word(p.nums)) + p.Literal(']').suppress()

        sliceexpr = attrexpr.setResultsName('attribute') + \
                    slicestartexpr.setResultsName('start') + \
                    p.Suppress(p.Literal(':')) + \
                    sliceendexpr.setResultsName('end')

        parseresult = sliceexpr.parseString(self.config)


        _attrname = parseresult.get('attribute', None)[0]
        _slicestart = parseresult.get('start', None)
        _sliceend = parseresult.get('end', None)

        if isinstance(_slicestart, p.ParseResults) and len(_slicestart) > 0:
            self.slicestart = int(_slicestart[0]) if len(_slicestart[0]) > 0 else None

        if isinstance(_sliceend, p.ParseResults) and len(_sliceend) > 0:
            self.sliceend = int(_sliceend[0]) if len(_sliceend[0]) > 0 else None

        if _attrname is None:
            raise ValueError('The configuration string provided to the Slice method '
                             'plugin in user defined class %s does not contain an '
                             'identifiable attribute. Please provide a configuration '
                             'string in the form of \'@attribute[#:#]\'' % striptoclassname(type(self.targetobject)))

        self.stringvalue = getname(self.targetobject, _attrname)

        if isinstance(self.stringvalue, str):
            self.computable = True

        if self.computable:
            self.__result__ = slicer(self.stringvalue, start=self.slicestart, end=self.sliceend)


def load():
    return Slice
