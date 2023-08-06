import string


class RouteTemplate:
    """The template to an API route.  Route instances are callable and can be passed
    values at runtime to be substituted into the template path.  Calling a route will
    return the full API path (excluding the base url).

    Template variables should be prefixed with $value.

    Templates can contain the literal `$` by escaping it with `$$`.
    Templates can use identifier, these are restricted to case-insensitive ASCII alphanum strings.
    Templates should use ${identifier} when valid identifiers follow the placeholder.
    """

    def __init__(self, template: str) -> None:
        self.template = string.Template(template)

    def __call__(self, **subtitutions) -> str:
        return self.template.substitute(**subtitutions)
