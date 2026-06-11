from typing import Any, Dict, List, Optional
from src.db.services import load_survey_data
from .schemas import Agent


GROUP_STATE = {
    1: "ADOPTED",
    2: "ADOPTED",
    3: "AWARE",
    4: "AWARE",
    5: "UNAWARE",
    6: "UNAWARE",
}

INFO_SOURCE_KEYS = (
    "INFO_S1",
    "INFO_S2",
    "INFO_S3",
    "INFO_S4",
    "INFO_S5",
    "INFO_S6",
    "INFO_S7",
    "INFO_S8",
    "INFO_S9",
    "INFO_S10",
    "INFO_S12",
)


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


def clamp(value: float, lower: float = 0.0, upper: float = 1.0) -> float:
    return max(lower, min(upper, value))


def map_foerderung(value: Any) -> float:
    subsidy = parse_int(value)
    if subsidy == 1:
        return 1.0
    if subsidy == 0:
        return 0.0
    return 0.3


def map_trigger(record: Dict[str, Any]) -> float:
    values = [
        parse_float(record.get(key))
        for key in ("TRIG_1", "TRIG_2", "TRIG_3", "TRIG_4")
    ]
    valid_values = [value for value in values if value is not None]
    if not valid_values:
        return 0.0
    average = sum(valid_values) / len(valid_values)
    return clamp((5.0 - average) / 4.0)


def map_social_influence(value: Any) -> float:
    return {
        0: 0.0,
        1: 0.5,
        2: 1.0,
        3: -0.2,
    }.get(parse_int(value), 0.0)


def map_info_sources(record: Dict[str, Any]) -> float:
    influenced_sources = sum(
        1 for key in INFO_SOURCE_KEYS if parse_int(record.get(key)) == 2
    )
    return influenced_sources / len(INFO_SOURCE_KEYS)


def map_known_households(value: Any) -> float:
    return {
        0: 0.0,
        1: 0.33,
        2: 0.66,
        3: 1.0,
    }.get(parse_int(value), 0.0)


def decision_score(agent: Agent) -> float:
    """
    Level 2: Why does an agent decide to adopt green technology?
    Weights derived from survey analysis of Gleisdorf energy transition data.

    Survey variable mapping:
      foerderung       <- SUB        (subsidy received)
      trigger          <- TRIG_1-4   (life event trigger, avg + normalised)
      social_influence <- INFO_S11   (personal environment as info source)
      info_sources     <- INFO_S1-10,S12 (professional info sources)
      known_households <- INFO_PAS   (known households that renovated)
    """
    score = (
        0.30 * agent.foerderung +  # SUB
        0.30 * agent.trigger +  # TRIG_1-TRIG_4
        0.20 * max(agent.social_influence, 0.0) +  # INFO_S11
        0.10 * agent.info_sources +  # INFO_S1-INFO_S10, INFO_S12
        0.10 * agent.known_households  # INFO_PAS
    )
    return float(clamp(score))


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
        foerderung=map_foerderung(record.get("SUB")),  # SUB
        trigger=map_trigger(record),  # TRIG_1-TRIG_4
        social_influence=map_social_influence(record.get("INFO_S11")),  # INFO_S11
        info_sources=map_info_sources(record),  # INFO_S1-INFO_S10, INFO_S12
        known_households=map_known_households(record.get("INFO_PAS")),  # INFO_PAS
        municipality=record.get("Gemeindename") or None,
        state=get_state_by_group(group),
    )


def load_agents() -> List[Agent]:
    """Load and convert cleaned survey data to Agent objects."""
    records = load_survey_data()
    return [record_to_agent(record) for record in records]
