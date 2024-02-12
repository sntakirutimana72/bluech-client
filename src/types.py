import typing as ty

NumberStringType = ty.Union[str, int]

UserInterfaceType = ty.Dict[str, NumberStringType]
UserInterface: UserInterfaceType = {'email': '', 'nickname': '', 'id': ''}
