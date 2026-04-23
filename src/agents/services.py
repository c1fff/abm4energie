from typing import Any, Dict, List, Optional
from src.db.services import load_survey_data
from .schemas import Agent


GROUP_STATE = {
    1: "ADOPTED",
    2: "ADOPTED",
    3: "ADOPTED",
    4: "AWARE",
    5: "AWARE",
    6: "UNAWARE",
}


def parse_int(value: Any) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value or value == ".":
            return None
    try:
        return int(float(str(value)))
    except (ValueError, TypeError):
        return None


def parse_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, str):
        value = value.strip()
        if not value or value == ".":
            return None
    try:
        return float(str(value))
    except (ValueError, TypeError):
        return None


def get_state_by_group(group: Optional[int]) -> Optional[str]:
    if group is None:
        return None
    return GROUP_STATE.get(group)


def record_to_agent(record: Dict[str, Any]) -> Agent:
    group = parse_int(record.get("GROUP_BEH"))
    agent_id = parse_int(record.get("id"))
    if agent_id is None:
        raise ValueError("Record must contain a valid numeric id")

        

    return Agent(
        id=agent_id,
        group=group,
        income=parse_float(record.get("HOUSE_Income")),
        age=parse_int(record.get("SOCIO_Age1")),
        building_type=record.get("BUILD_Type") or None,
        build_age=parse_int(record.get("BUILD_Age")),
        energy_std=record.get("BUILD_ES_Cur") or None,
        subsidy=parse_float(record.get("SUB")),
        info_pas=parse_float(record.get("INFO_PAS")),
        info_s11=parse_float(record.get("INFO_S11")),
        municipality=record.get("Gemeindename") or None,
        state=get_state_by_group(group),
    )


def load_agents() -> List[Agent]:
    """Load and convert cleaned survey data to Agent objects."""
    records = load_survey_data()
    return [record_to_agent(record) for record in records]