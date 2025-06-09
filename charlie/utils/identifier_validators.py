from abc import ABC, abstractmethod
from validate_docbr import CPF, CNPJ


class IdentifierValidator(ABC):
    @abstractmethod
    def validate(self, identifier: str) -> None:
        """Validate the identifier or raise ValueError if invalid."""
        pass


class CPFValidator(IdentifierValidator):
    def validate(self, identifier: str) -> None:
        if not CPF().validate(identifier):
            raise ValueError(
                f"Invalid CPF '{identifier}' for owner type 'tutor'. "
                "Expected format: XXX.XXX.XXX-XX or 11 digits without punctuation."
            )


class CNPJValidator(IdentifierValidator):
    def validate(self, identifier: str) -> None:
        if not CNPJ().validate(identifier):
            raise ValueError(
                f"Invalid CNPJ '{identifier}' for owner type 'org'. "
                "Expected format: XX.XXX.XXX/XXXX-XX or 14 digits without punctuation."
            )
