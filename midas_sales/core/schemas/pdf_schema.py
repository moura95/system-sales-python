from pydantic import BaseModel


class OrderPdf(BaseModel):
    footerHtmlTemplate: str
    headerHtmlTemplate: str
    htmlTemplate: str
    model: dict
    options: dict
    templateEngine: str
