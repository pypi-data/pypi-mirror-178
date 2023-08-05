from typing import Union

from sqlalchemy.orm import Session, scoped_session

Validate_Session = Union[Session, scoped_session]
