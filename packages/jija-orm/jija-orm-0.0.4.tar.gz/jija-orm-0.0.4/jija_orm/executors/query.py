from jija_orm.executors import templates
from jija_orm.executors import executors


class QueryManager:
    def __init__(self, model_class, class_templates=None):
        self.__model_class = model_class
        self.__templates = self.fix_templates(class_templates)

    def __add_templates(self, *new_templates) -> 'QueryManager':
        class_templates = self.__templates.copy()
        class_templates.extend(new_templates)
        return self.__class__(self.__model_class, class_templates)

    @staticmethod
    def fix_templates(class_templates):
        if not class_templates:
            return []

        templates_dict = {}
        for template in class_templates:
            if templates_dict.get(template.PRIORITY):
                if template.COMPARABLE is False:
                    templates_dict[template.PRIORITY] = template
                else:
                    raise NotImplementedError()

            else:
                templates_dict[template.PRIORITY] = template

        return list(templates_dict.values())

    @property
    def model(self):
        return self.__model_class

    @property
    def templates(self):
        return self.__templates

    def select(self, *args, **kwargs) -> 'QueryManager':
        return self.__add_templates(templates.Select(*args, **kwargs))

    def update(self, *args, **kwargs) -> 'QueryManager':
        return self.__add_templates(templates.Update(*args, **kwargs))

    def insert(self, **kwargs) -> 'QueryManager':
        return self.__add_templates(templates.Insert(**kwargs))

    def multiple_insert(self, rows) -> 'QueryManager':
        return self.__add_templates(templates.MultipleInsert(rows))

    def delete(self):
        return self.__add_templates(templates.Delete())

    def where(self, *args, **kwargs) -> 'QueryManager':
        if self.__templates:
            new_templates = []
        else:
            new_templates = [templates.Select()]

        new_templates.append(templates.Where(*args, **kwargs))
        return self.__add_templates(*new_templates)

    def __await__(self):
        async def wrapper():
            executor = executors.Executor(self.__model_class, *self.__templates)
            return await executor.execute()

        return wrapper().__await__()
