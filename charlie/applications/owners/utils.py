from charlie.utils.identifier_validators import CNPJValidator, CPFValidator


VALIDATOR_STRATEGY = {
    "tutor": CPFValidator(),
    "org": CNPJValidator(),
}
