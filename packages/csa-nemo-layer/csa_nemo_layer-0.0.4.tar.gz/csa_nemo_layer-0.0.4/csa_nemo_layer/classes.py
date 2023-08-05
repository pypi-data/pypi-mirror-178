class Finding:
    def __init__(self, **kwargs) -> None:
        """
        Class for CSA Nemo project's findings
        :params:
        id: string
        target: string
        controlId: string
        Reason: list of strings
        Identifier: string
        """
        self.id = kwargs.get('id')
        self.target = kwargs.get('target', '')
        self.controlId = kwargs.get('controlId', '')
        self.Reason = kwargs.get('reason', [])
        self.Identifier = kwargs.get('identifier', '')
        self.IdentifierType = kwargs.get('identifier_type', '')

    def json(self) -> dict:
        json_obj = self.__dict__
        json_obj['Reason'] = '\n'.join(self.Reason)
        return json_obj

# TO-DO: Add classes for targets
