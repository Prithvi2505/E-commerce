from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class AddressTypeEnum(str, Enum):
    SHIPPING = "shipping"
    BILLING = "billing"
    BOTH = "both"


class AddressBase(BaseModel):
    address_type: AddressTypeEnum = AddressTypeEnum.BOTH
    street_address: str = Field(..., min_length=1, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: str = Field(..., min_length=1, max_length=100)
    state: str = Field(..., min_length=1, max_length=100)
    postal_code: str = Field(..., min_length=1, max_length=20)
    country: str = Field(default="United States", max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)


class AddressCreate(AddressBase):
    is_default: bool = False


class AddressUpdate(BaseModel):
    address_type: Optional[AddressTypeEnum] = None
    street_address: Optional[str] = Field(None, min_length=1, max_length=255)
    address_line_2: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, min_length=1, max_length=100)
    state: Optional[str] = Field(None, min_length=1, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=1, max_length=20)
    country: Optional[str] = Field(None, max_length=100)
    first_name: Optional[str] = Field(None, max_length=100)
    last_name: Optional[str] = Field(None, max_length=100)
    company: Optional[str] = Field(None, max_length=200)
    phone: Optional[str] = Field(None, max_length=20)
    is_default: Optional[bool] = None


class AddressResponse(AddressBase):
    address_id: int
    user_id: int
    is_default: bool
    full_address: str
    full_name: Optional[str]

    class Config:
        from_attributes = True