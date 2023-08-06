from __future__ import annotations
from pydantic import BaseModel, Field
from UPS_SDK.models.Response import Response
from UPS_SDK.models.Shipment import Shipment
from typing import Any, List

class TrackResponse(BaseModel):
    Response: Response
    Shipments: List[Shipment] = Field(None, alias="Shipment")
    
    def __init__(__pydantic_self__, **data: Any) -> 'TrackResponse':
        if isinstance(data["Shipment"], dict):
            data["Shipment"] = [data["Shipment"]]
        for shipment in data["Shipment"]:
            if isinstance(shipment["Package"]["Activity"], dict):
                data['Shipment']["Package"]["Activity"] = [data["Shipment"]["Package"]["Activity"]]
            if isinstance(shipment["ReferenceNumber"], dict):
                data["Shipment"]["ReferenceNumber"] = [data['Shipment']["ReferenceNumber"]]
            
        super().__init__(**data)