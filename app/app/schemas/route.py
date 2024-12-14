from typing import List, Optional

from pydantic import BaseModel, Field

# class RouteProps(BaseModel):


class RouteMeta(BaseModel):
    title: str
    i18n_key: str = Field(serialization_alias="i18nKey")
    hide_in_menu: bool = Field(serialization_alias="hideInMenu")
    constant: Optional[bool] = None
    icon: Optional[str] = None
    order: Optional[int] = None
    active_menu: Optional[str] = Field(default=None, serialization_alias="activeMenu")


class Route(BaseModel):
    id: int = Field(default=None, exclude=True)
    parent_id: int = Field(default=None, exclude=True)
    name: str
    path: str
    component: str
    props: bool
    meta: RouteMeta
    children: Optional[List["Route"]] = None


class UserRoute(BaseModel):
    routes: List[Route]
    home: str
