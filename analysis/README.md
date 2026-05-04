
### Classification Reference

| Code | Label | Meaning |
|------|-------|---------|
| 1 | HIGH | Transition Leader — Changed main heating system and did thermal renovation |
| 2 | MED_CO2 | CO2 Reducers — Changed main heating to renewable |
| 3 | MED_SAV | Energy Savers — Thermally insulated only |
| 4 | LOW | Technology Adopters — Only minor innovations (PV, battery, etc.) |
| 5 | NEW | New Builders — Built/rebuilt rather than retrofitted |
| 6 | NO | No Actions — Did nothing. |
| — | — | Cannot be assigned (the 192 missing) |

**ADOPTED = 1-3**

**IN PROCESS = 4-5**

**Not Adopted = 6 and missing**

## BUILD_HS_Age
Wann wurde Ihre Heizungsanlage zuletzt erneuert (Hauptheizungssystem)?
*we can look for some initiatives that been made during or before the dates and make a correlation 


## Survey Data

The raw input is `data/raw/survey.json` — a list of **1,651 respondents × 143 fields**, one record per Styrian homeowner. Missing values are encoded as the string `"."` (not `null`). IDs run 1…1651 with no duplicates. A sibling file `data/raw/survey1.json` is byte-identical (same MD5 `ce798ae7…`); the comment in `analysis/main.py` (`survey1 not survey`) currently makes no functional difference.

The variable codebook is `data/survey_description.xlsx` (sheet `Variablen`). It documents 140 of the 143 columns — only `id`, `TRIG_1Text`, and `TRIG_2Text` (free-text trigger annotations) are undocumented. Variable names are German; this section translates the ones the simulation depends on.

Fields fall into eight blocks: identification & location (`id`, `Gemeindename`, `Gemeindenummer`); building (`BUILD_*`); measures already taken (`MEAS_*`, `REF_*`, `REN_*`, `NEW_*`); subsidies (`SUB`, `SUB_1…5`); information / awareness (`INFO_S1…12`, `INFO_C1…9`, `INFO_PAS`, `INFO_ACT`); triggers (`TRIG_1…4` plus free text); personal characteristics (`CHAR_B*`, `CHAR_HS*`); and socio-demographics (`SOCIO_*`, `HOUSE_*`). The behaviour group `GROUP_BEH` is a derived persona cluster, not a raw answer — the dictionary notes it was assigned via cluster analysis on the measure variables.

### `GROUP_BEH` persona definitions

| Code | Label | Definition |
|---|---|---|
| 1 | HIGH — Transition Leader | Changed main heating system **and** did thermal renovation |
| 2 | MED_CO2 — CO2 Reducers | Changed main heating to a renewable system |
| 3 | MED_SAV — Energy Savers | Thermally insulated only |
| 4 | LOW — Technology Adopters | Only minor innovations (PV, battery, energy management) |
| 5 | NEW — New Builders | Built/rebuilt (new development, floor addition, replacement) |
| 6 | NO — No Actions | No renovation measures |
| `.` | — | Cannot be assigned (192 records, ~11.6 %) |

Sample distribution: 1=581, 2=247, 3=169, 4=105, 5=183, 6=174, missing=192.

### `HOUSE_Income` (monthly net household income, €) - *good plot graph*

| Code | Band |
|---|---|
| 1 | < 1,500 |
| 2 | 1,500 – 3,000 |
| 3 | 3,000 – 4,500 |
| 4 | 4,500 – 6,000 |
| 5 | 6,000 – 7,500 |
| 6 | 7,500 – 9,000 *(inferred — dictionary truncates at 5)* |
| 7 | > 9,000 *(inferred)* |

Sample distribution: 3=539, 4=413, 2=356, 5=129, 6=63, 1=35, 7=28, missing=88.

### `BUILD_Age` cohorts

| Code | Cohort |
|---|---|
| 1 | before 1919 |
| 2 | 1919 – 1944 |
| 3 | 1945 – 1960 |
| 4 | 1961 – 1970 |
| 5 | 1971 – 1980 |
| 6 | 1981 – 1990 |
| 7 | 1991 – 2000 |
| 8 | 2001 – 2010 |
| 9 | 2011 – 2020 |
| 10 | 2021 + |
| 11 | Don't know |

Sample peak in 1971–2000 stock (~36 %), with 14 % built post-2010.

### `BUILD_ES_Cur` (current energy standard) - *might be a good plot graph*

| Code | Class |
|---|---|
| 1 | Passivhaus (A++) |
| 2 | Niedrigstenergiehaus (A+, A) |
| 3 | Niedrigenergiehaus (B) |
| 4 | Bauvorschrift standard |
| 5 | Old, unrenovated (D, E, F, G) |
| 6 | Don't know |

Sample distribution: 6=598, 4=487, 3=272, 2=188, 5=88, 1=17. **36 % answered "don't know"**, which is the modal response — for modeling purposes that's information (low engagement) rather than missingness.

### Awareness indicators - *need more info/explanation*

`INFO_PAS` (number of households in social environment that renovated) is a 4-point ordinal: 0=none, 1=1–2 households, 2=3–5, 3=>5. `INFO_S1…INFO_S12` (information sources) use a non-monotonic 0–3 scale: 0=did not consult, 1=consulted + helpful, 2=consulted + moderately helpful, 3=consulted + not helpful. So within {1,2,3} a higher value means *less satisfied*, not "more aware."

### Other key fields

`SOCIO_Age1` is **birth year** (Geburtsjahr), range 1925–1999 (median 1967), not age. `SOCIO_Gender1`: 1=Weiblich (F, 337), 2=Männlich (M, 1310), 3=Other (2). The sample is ~79 % male — consistent with how Austrian property ownership is registered, but a strong skew worth keeping in mind. `BUILD_Type`: 1=single-family (1339), 2=multi-family (312). `Gemeindename` covers 255 distinct municipalities; Graz dominates with 154 respondents, and the long tail is heavy — **32 municipalities have a single respondent and 104 have ≤3**, so those agents end up isolated or near-isolated in the same-municipality graph.

### Already-derived helpers

The dictionary lists two helpers built from the raw measures: `REF_Thermische_Sanierung` (thermal renovation done; from `REF_1 + REF_2 + …`) and `REF_Heizungstausch` (heating replaced; from `REF_5`). Both are inputs to `GROUP_BEH`, so using them as additional features alongside `GROUP_BEH` introduces collinearity.

## Modeling Notes

A few places where the implementation and the data dictionary disagree, surfaced while reading both end-to-end:

1. **Income clamp drops bands 6–7.** `record_to_agent` in `src/agents/services.py` keeps income only when it equals one of `(1.0, 2.0, 3.0, 4.0, 5.0)`. The survey codes go up to 7 (91 households earning ≥ 7,500 €/month — exactly the segment that drives heat-pump and PV uptake). Those agents end up with `income=None` and fall into the `0.5` similarity fallback in `numeric_similarity`.
2. **`susceptibility()` rescales the wrong axis.** `src/simulation/core.py` normalizes `INFO_PAS` and `INFO_S11` "assuming a 0–100 scale," but both fields are ordinal 0–3. With a 0–100 assumption, an answer of "3 = more than 5 neighbours renovated" gets normalized to 0.03 and mapped to ~0.5 (the lowest susceptibility). The correct denominator is 3.
3. **`Agent.age` is a birth year, not an age.** `SOCIO_Age1` ranges 1925–1999, but the homophily weight then runs `numeric_similarity` on the raw value. This compares year-of-birth differences rather than age differences. Use `current_year - SOCIO_Age1` before storing on the agent.
4. **State mapping interpretation.** `get_state_by_group` maps `4, 5 → AWARE` and `6 → UNAWARE`. Per the persona definitions above, group 5 (NEW) has *already* adopted via new construction, and group 4 (LOW) has adopted some innovation. Whether they belong with `ADOPTED` or `AWARE` is a modeling choice, not implied by the data — worth documenting explicitly.
5. **"Don't know" is signal, not noise.** 36 % of respondents don't know their building's energy class (`BUILD_ES_Cur=6`) and `INFO_S*` distinguishes "didn't consult" from "consulted but unhelpful." Treating either as missing erases information about engagement.
6. **Sparse municipalities.** With 32 single-respondent municipalities, those agents have zero neighbours in the same-municipality graph and can only adopt via the base `p_unaware`/`p_aware` term — never via influence. Consider relaxing the spatial gate to district level for those, or excluding singletons from the simulation.
7. **Project geography.** Earlier README copy described the project as "heating adoption behavior in Salzburg," but every municipality in the data is Styrian (Graz, Feldbach, Weiz, Deutschlandsberg, …). Treat the dataset as **Steiermark**.
