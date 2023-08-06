import re

from jija_orm import fields, exceptions
from jija_orm.executors import executors, comparators
from jija_orm import utils


class Template:
    PRIORITY = NotImplemented
    NAME = NotImplemented
    COMPARABLE = False

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        self.model = None
        self.table = None

        self.params = set()

    def set_model(self, model=None, table=None):
        self.model = model
        self.table = table

    def get_table_name(self):
        table_name = self.model.get_name() if self.model else self.table
        return self.correct_name(table_name)

    def validate_field(self, field, value=None):
        if isinstance(value, executors.Param):
            self.params.add(value.name)
            return '{' + value.name + '}'

        validator = None
        if self.model:
            if not hasattr(self.model, field):
                raise exceptions.TemplateAttributeError(self.model, field)

            validator = getattr(self.model, field)

        if value is None:
            return 'null'

        if validator is None:
            validator = fields.get_validator(value)

        return validator.to_sql(value)

    def validate_field_name(self, name):
        if self.model:
            if not hasattr(self.model, name):
                raise exceptions.TemplateAttributeError(self.model, name)

            field = getattr(self.model, name)
            if isinstance(field, fields.RelatedField):
                return f'{name}_id'

        return name

    @staticmethod
    def correct_name(name):
        check = name.split('.')
        for index in range(len(check)):
            if not re.match(r'"\w*"', check[index]):
                check[index] = f'"{check[index]}"'

        return '.'.join(check)

    def calculate(self):
        raise NotImplementedError()

    def __eq__(self, other: 'Template'):
        if type(self) != type(other):
            raise TypeError(f'Cant compare different types {type(self)} and {type(other)}')

        return self.args == other.args and self.kwargs == other.kwargs


class Select(Template):
    PRIORITY = 0
    NAME = 'select'

    def __init__(self, *args, distinct=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.distinct = distinct

    def calculate(self):
        select_items = self.parse_args() + self.parse_kwargs()
        return f'select {"distinct " if self.distinct else ""}{", ".join(select_items) if select_items else "*"} ' \
               f'from {self.get_table_name()}'

    def parse_args(self):
        template = []
        for name in self.args:
            self.validate_field(name)
            name = self.validate_field_name(name)
            template.append(self.correct_name(name))

        return template

    def parse_kwargs(self):
        template = []

        for alias, name in self.kwargs.items():
            self.validate_field(name)
            name = self.validate_field_name(name)
            template.append(f'{self.correct_name(name)} as {self.correct_name(alias)}')

        return template


class Insert(Template):
    PRIORITY = 0
    NAME = 'insert'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def parse_kwargs(self):
        template = {}

        for name, value in self.kwargs.items():
            value = self.validate_field(name, value)
            name = self.correct_name(self.validate_field_name(name))
            template[name] = value

        return template

    def calculate(self):
        params = self.parse_kwargs()
        return f"insert into {self.get_table_name()} ({', '.join(params)}) " \
               f"values ({', '.join(map(str, params.values()))}) " \
               f"returning *"


class MultipleInsert(Template):
    PRIORITY = 0
    NAME = 'insert'

    def __init__(self, rows):
        super().__init__()
        self.__rows = rows

    def get_fields(self):
        model_fields = set()
        for row in self.__rows:
            model_fields.update(row.keys())

        return list(model_fields)

    def parse_row(self, inserter_fields: list, row: dict) -> str:
        if not isinstance(row, dict):
            raise TypeError(type(row))

        params = []
        for field_name in inserter_fields:
            value = row.get(field_name, utils.NotSet)
            if value is utils.NotSet:
                params.append('null')
                continue

            value = self.validate_field(field_name, value)
            params.append(str(value))

        return f'({", ".join(params)})'

    def calculate(self):
        inserter_fields = self.get_fields()
        params = list(map(lambda row: self.parse_row(inserter_fields, row), self.__rows))

        fields_names = list(map(lambda field: self.correct_name(self.validate_field_name(field)), inserter_fields))

        return f"insert into {self.get_table_name()} ({', '.join(fields_names)}) " \
               f"values {', '.join(params)} " \
               f"returning *"


class Update(Template):
    PRIORITY = 0
    NAME = 'update'

    def parse_kwargs(self):
        params = []
        for name, value in self.kwargs.items():
            value = self.validate_field(name, value)
            name = self.correct_name(self.validate_field_name(name))
            params.append(f'{name} = {value}')

        return params

    def calculate(self):
        params = self.parse_kwargs()
        return f'update {self.get_table_name()} set {", ".join(params)}'


class Delete(Template):
    PRIORITY = 0
    NAME = 'delete'

    def __init__(self):
        super().__init__()

    def calculate(self):
        return f'{self.NAME} from {self.get_table_name()}'


class WhereAddParam:
    AND = 'and'
    OR = 'or'


class Where(Template):
    PRIORITY = 1
    NAME = 'where'

    def __init__(self, add_param=WhereAddParam.AND, **kwargs):
        super().__init__(**kwargs)
        self.add_param = add_param

    def calculate(self):
        return f'where {f" {self.add_param} ".join(self.parse_kwargs())}'

    def parse_kwargs(self):
        template = []

        for field_name, value in self.kwargs.items():
            field_name, lookup, *_ = *field_name.split('__'), None

            if isinstance(value, comparators.Comparator):
                value.value = self.validate_field(field_name, value.value)
                query = value.calculate(
                    self.correct_name(self.validate_field_name(field_name)),
                    getattr(self.model, field_name) if hasattr(self.model, field_name) else None
                )
            else:
                value = self.validate_field(field_name, value)
                field_name = self.correct_name(self.validate_field_name(field_name))
                query = f'{field_name} {self.parse_lookup(lookup)} {value}'

            template.append(query)
        return template

    @staticmethod
    def parse_lookup(lookup):
        if lookup is None:
            return '='
        elif lookup == 'lt':
            return '<'
        elif lookup == 'lte':
            return '<='
        elif lookup == 'gt':
            return '>'
        elif lookup == 'gte':
            return '>='
        elif lookup == 'not':
            return '!='
        elif lookup == 'startswith':
            return 'like'
        else:
            raise ValueError('invalid lookup')

    # def __iand__(self, other):
    #     pass

    # def __ior__(self, other):
    #     pass

    # def __ixor__(self, other):
    #     pass
