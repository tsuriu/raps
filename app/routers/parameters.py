from datetime import datetime
import json

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response

from app.controllers.parametersController import *
from app.serializers.parameterSerializers import cfgEntity, cfgListEntity

from app.database import Parameters

from app.oauth2 import require_user, RoleChecker

allow_parameters = RoleChecker(["admin"])


router = APIRouter()


@router.get(
    "/",
    dependencies=[Depends(allow_parameters)]
)
def get_all_parameters(cfg_description: str = "", user_id: str = Depends(require_user)):

    if cfg_description:
        try:
            configs = cfgEntity(Parameters.find_one({"config_description": cfg_description}))
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Description {cfg_description} not found in parameters.")
    else:
        configs = cfgListEntity(Parameters.find())
    
    return configs


# @router.put(
#     "/",
#     dependencies=[Depends(allow_parameters)]
# )
# def update_parameter(cfg_description: str = "", payload: dict = {}, user_id: str = Depends(require_user)):
#     if cfg_description:
#         try:
#             configs = Parameters.find_one_and_update({"config_description": cfg_description})
#         except Exception as e:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Description {cfg_description} not found in parameters.")
#     else:
#         configs = Parameters.update_many()