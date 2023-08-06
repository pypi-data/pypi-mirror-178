from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CreateResourceJsonBody")


@attr.s(auto_attribs=True)
class CreateResourceJsonBody:
    """
    Attributes:
        path (str):
        value (Any):
        resource_type (str):
        description (Union[Unset, str]):
        is_oauth (Union[Unset, bool]):
    """

    path: str
    value: Any
    resource_type: str
    description: Union[Unset, str] = UNSET
    is_oauth: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        path = self.path
        value = self.value
        resource_type = self.resource_type
        description = self.description
        is_oauth = self.is_oauth

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "path": path,
                "value": value,
                "resource_type": resource_type,
            }
        )
        if description is not UNSET:
            field_dict["description"] = description
        if is_oauth is not UNSET:
            field_dict["is_oauth"] = is_oauth

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        path = d.pop("path")

        value = d.pop("value")

        resource_type = d.pop("resource_type")

        description = d.pop("description", UNSET)

        is_oauth = d.pop("is_oauth", UNSET)

        create_resource_json_body = cls(
            path=path,
            value=value,
            resource_type=resource_type,
            description=description,
            is_oauth=is_oauth,
        )

        create_resource_json_body.additional_properties = d
        return create_resource_json_body

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
