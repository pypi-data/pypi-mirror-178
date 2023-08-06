from __future__ import annotations
from pydantic import BaseModel, Field
from UPS_SDK.models.Response import Response
from UPS_SDK.models.Shipment import Shipment
from typing import Any, List

class TrackResponse(BaseModel):
    Response: Response
    Shipments: List[Shipment] = Field(None, alias="Shipment")
    
    def __init__(__pydantic_self__, **data: Any) -> None:
        if isinstance(data["Shipment"], dict):
            data["Shipment"] = [data["Shipment"]]
            
        for shipment in data["Shipment"]:
            if isinstance(shipment["Package"]["Activity"], dict):
                shipment["Package"]["Activity"] = [shipment["Package"]["Activity"]]
            if isinstance(shipment["ReferenceNumber"], dict):
                shipment["ReferenceNumber"] = [shipment["ReferenceNumber"]]
            
        super().__init__(**data)