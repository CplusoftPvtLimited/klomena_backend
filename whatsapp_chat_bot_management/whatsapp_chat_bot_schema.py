from schemas import CamelModel

"""
Request Schema's
"""


class AskQuestionSchema(CamelModel):
    question: str
    number: str
