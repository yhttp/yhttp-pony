import functools
from collections import OrderedDict
from pony import orm
import yhttp


def _flag(exceptions, default_exception, fieldname):
    defexc = default_exception or yhttp.statuses.badrequest()
    return (exceptions or {}).get(fieldname, defexc)


def _condition(exceptions, default_exception, fieldname, value):
    return (value, _flag(exceptions, default_exception, fieldname))


class FieldMeta:
    minlength = None
    maxlength = None
    name = None
    type = None
    protected = None
    readonly = None
    required = None
    default = None
    nonnone = None
    minimum = None
    maximum = None
    pattern = None
    callback = None
    example = None

    def todict(self):
        assert self.name

        return dict(
            name=self.name,
            type=self.type.__name__,
            protected=self.protected,
            readonly=self.readonly,
            required=self.required,
            notnone=self.notnone,
            default=self.default,
            minlength=self.minlength,
            maxlength=self.maxlength,
            minimum=self.minimum,
            maximum=self.maximum,
            pattern=self.pattern,
            callback=self.callback,
            example=self.example
        )

    def create_validationrules(self, exceptions=None, default_exception=None):
        flag = functools.partial(_flag, exceptions, default_exception)
        cond = functools.partial(_condition, exceptions, default_exception)
        rules = {}

        if self.type:
            rules['type_'] = cond('type', self.type)

        if self.readonly:
            rules['readonly'] = flag('readonly')

        if self.required:
            rules['required'] = flag('required')

        if self.minlength:
            rules['minlength'] = cond('minlength', self.minlength)

        if self.maxlength:
            rules['maxlength'] = cond('maxlength', self.maxlength)

        if self.notnone:
            rules['notnone'] = cond('notnone', self.notnone)

        if self.minimum:
            rules['minimum'] = cond('minimum', self.minimum)

        if self.maximum:
            rules['maximum'] = cond('maximum', self.maximum)

        if self.pattern:
            rules['pattern'] = cond('pattern', self.pattern)

        if self.callback:
            rules['callback'] = cond('callback', self.callback)

        return rules


class Metadata:
    _metadata = None
    _global = {}

    def __init__(self, type_, maxlength=None, minlength=None, protected=False,
                 readonly=False, required=False, nullable=False,
                 default=None, sqldefault=None, notnone=True, minimum=None,
                 maximum=None, pattern=None, callback=None,
                 example=None, **kw):
        # Assertions
        if 'max_len' in kw:
            raise NameError('Use maxlength instead of max_len.')

        _ponykw = kw
        _ponykw['nullable'] = nullable

        if default is not None:
            _ponykw['default'] = default

        if sqldefault is not None:
            _ponykw['sql_default'] = sqldefault

        self.type_ = type_

        self._metadata = FieldMeta()
        self._metadata.type = type_
        self._metadata.protected = protected
        self._metadata.readonly = readonly
        self._metadata.required = required
        self._metadata.notnone = notnone
        self._metadata.default = default
        self._metadata.pattern = pattern
        self._metadata.callback = callback
        self._metadata.example = example

        # String
        if type_ is str:
            self._metadata.minlength = minlength
            self._metadata.maxlength = maxlength
            _ponykw['max_len'] = maxlength

        elif maxlength or minlength:
            raise ValueError(
                'minlength and maxlength keyword arguments are not allowed in'
                'non-string fields.'
            )

        else:
            self._metadata.minimum = minimum
            self._metadata.maximum = maximum

        super().__init__(type_, **_ponykw)

    def _init_(self, entity, name):
        super(Metadata, self)._init_(entity, name)
        entityname = entity.__name__.lower()
        entitymeta = self._global.get(entityname)
        if entitymeta is None:
            entitymeta = self._global[entityname] = OrderedDict()

        entitymeta[name] = self._metadata
        entitymeta[name].name = name
        self._metadata = None

    @classmethod
    def getfield(cls, entity, fieldname):
        return cls._global[entity][fieldname]

    @classmethod
    def getentity(cls, entity):
        return cls._global[entity]

    @classmethod
    def create_validationrules(self, entity, whitelist=None, exceptions=None,
                               default_exception=None):
        rules = {}

        for k, v in self._global[entity].items():
            if whitelist and k not in whitelist:
                continue

            rules[k] = v.create_validationrules(exceptions, default_exception)

        return rules


class PrimaryKey(Metadata, orm.PrimaryKey):
    def __init__(self, type_, **kw):
        super().__init__(type_, **kw)


class Required(Metadata, orm.Required):
    def __init__(self, type_, required=True, **kw):
        super().__init__(type_, required=required, **kw)


class Optional(Metadata, orm.Optional):
    def __init__(self, type_, **kw):
        super().__init__(type_, **kw)


def getfield(entity, name):
    return Metadata.getfield(entity, name)


def get(name):
    entry = Metadata.getentity(name)

    return dict(
        name=name,
        fields=[f.todict() for f in entry.values()]
    )


def validate(entity, whitelist=None, exceptions=None, default_exception=None,
             fields=None, strict=None, **kw):

    strict_ = strict if strict is not None else whitelist is not None
    fields_ = Metadata.create_validationrules(
        entity,
        whitelist=whitelist,
        exceptions=exceptions,
        default_exception=default_exception
    )

    if fields:
        fields_.update(fields)

    return yhttp.validate(fields=fields_, strict=strict_, **kw)
