from typing import Optional, List

from pydantic import BaseModel


class StripeBase(BaseModel):
    plan: str
    coupon: Optional[str] | None = None


class StripeCheckout(StripeBase):
    pass


class AutomaticTax(BaseModel):
    enabled: bool
    status: Optional[str]


class Metadata(BaseModel):
    TenantID: str
    CustomerName: str
    Email: str


class Period(BaseModel):
    end: int
    start: int


class Plan(BaseModel):
    id: str
    object: str
    active: bool
    aggregate_usage: Optional[str]
    amount: int
    amount_decimal: str
    billing_scheme: str
    created: int
    currency: str
    interval: str
    interval_count: int
    livemode: bool
    metadata: dict
    nickname: Optional[str]
    product: str
    tiers_mode: Optional[str]
    transform_usage: Optional[str]
    trial_period_days: Optional[int]
    usage_type: str


class Recurring(BaseModel):
    aggregate_usage: Optional[str]
    interval: str
    interval_count: int
    trial_period_days: Optional[int]
    usage_type: str


class Price(BaseModel):
    id: str
    object: str
    active: bool
    billing_scheme: str
    created: int
    currency: str
    custom_unit_amount: Optional[str]
    livemode: bool
    lookup_key: Optional[str]
    metadata: dict
    nickname: Optional[str]
    product: str
    recurring: Recurring
    tax_behavior: str
    tiers_mode: Optional[str]
    transform_quantity: Optional[str]
    type: str
    unit_amount: int
    unit_amount_decimal: str


class LineItem(BaseModel):
    id: str
    object: str
    amount: int
    amount_excluding_tax: int
    currency: str
    description: str
    discount_amounts: List[dict]
    discountable: bool
    discounts: List[dict]
    livemode: bool
    metadata: Metadata
    period: Period
    plan: Plan
    price: Price
    proration: bool
    proration_details: dict
    quantity: int
    subscription: str
    subscription_item: str
    tax_amounts: List[dict]
    tax_rates: List[dict]
    type: str
    unit_amount_excluding_tax: str


class Lines(BaseModel):
    object: str
    data: List[LineItem]
    has_more: bool
    total_count: int
    url: str


class Data(BaseModel):
    object: dict


class InvoicePaidEvent(BaseModel):
    id: str
    object: str
    api_version: str
    created: int
    data: Data
    livemode: bool
    pending_webhooks: int
    request: dict
    type: str
