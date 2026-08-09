# AnaSOP
Analysis Standard Operating Procedure

## 1. Research Objective

### Working Title

Earthquake-adjusted rainfall-triggered landslide risk, community isolation, and
emergency intervention priorities in Kumamoto

### Central Research Question

- Research question: Under moderate, heavy, and extreme rainfall after the 2026
  Kumamoto earthquake, which road disruptions are most likely to isolate communities
  or remove access to basic emergency services, and which feasible pre-rainfall
  interventions yield the largest population-weighted reduction in these consequences?
- Why it matters: A susceptibility map alone does not identify where slope failure
  becomes a network emergency or where limited inspection, reinforcement, clearance,
  evacuation, and pre-positioning resources have the greatest protective value.
- Data support currently visible: The exploratory evidence contains a prefecture-wide
  routable road graph and road sections, populated 125 m meshes, age-structured
  disclosure groups, administrative areas, landslide warning zones, designated and
  current shelters, emergency water points, public facilities, fire stations, 2026
  road-restriction snapshots, and limited geolocated earthquake-damage evidence.
- Key readable variables or data scope: rainfall scenario; earthquake disturbance;
  terrain and land-cover conditions; slope-to-road exposure; road failure or disruption
  score; network redundancy; community connectivity; total and older population;
  service reachability; intervention cost; and avoided isolation.
- What would verify it: A reproducible scenario chain must yield stable road and
  community rankings across rainfall severity, Monte Carlo seeds, network assumptions,
  and plausible earthquake-adjustment parameters; intervention benefits must be
  positive, budget-feasible, and reconciled to affected communities and population.
- What would falsify or weaken it: The central claim is weakened if the hazard layer
  cannot be linked to roads, the baseline network cannot represent community access,
  community definitions are spatially unstable, or intervention rankings are driven
  mainly by arbitrary cost and threshold choices.
- Required next feasibility check: Confirm terrain, rainfall, earthquake-disturbance,
  and landslide-inventory availability; define the community unit and external-network
  connection target; audit road topology and service-node coverage.

### Supporting Research Questions

The central question is supported by four linked questions that follow the compound-
hazard and consequence pathway.

#### Supporting Point 1: Earthquake-adjusted rainfall threshold

- Role relative to central point: mechanism.
- Research question: Does stronger earthquake disturbance make the same rainfall
  exposure correspond to greater slope-instability risk, or, if event labels are
  insufficient, how much do low, central, and high threshold-reduction scenarios
  change the landslide disruption score?
- Why it matters: This is the main compound-hazard contribution and separates the
  project from a static landslide susceptibility assessment.
- Data support currently visible: Official warning-zone geography and limited event
  damage evidence are available, while the required elevation surface, rainfall fields,
  ground-motion surface, and event-labelled landslide inventory remain acquisition or
  feasibility tasks.
- Key readable variables or data scope: 1 h, 3 h, 24 h, and 72 h rainfall; antecedent
  precipitation index; slope, curvature, wetness and flow-accumulation proxies;
  geology, soil, and land cover; shaking intensity or ground motion; and the rainfall-
  disturbance interaction.
- What would verify it: With a suitable inventory, a positive and spatially stable
  rainfall-by-earthquake interaction under event-wise or spatially blocked validation;
  without one, coherent and ordered sensitivity across declared threshold-reduction
  scenarios calibrated where possible against the 2016 event.
- What would falsify or weaken it: No inventory support, unstable interaction estimates,
  severe spatial sampling bias, or scenario rankings that reverse under minor parameter
  changes would prevent a probability or threshold-shift claim.
- Required next feasibility check: Determine the completeness and mapping method of
  the 2016 and 2026 landslide inventories and select one primary earthquake-disturbance
  measure without treating intensity, PGA, and PGV as interchangeable.

#### Supporting Point 2: Slope hazard to road disruption

- Role relative to central point: mechanism and exposure translation.
- Research question: Under each earthquake-rainfall scenario, which road sections are
  most exposed to landslide, rockfall, or debris-flow impact from upslope terrain?
- Why it matters: Community consequences depend on whether hazardous slopes can reach
  and block specific road sections, not only on where high-hazard terrain exists.
- Data support currently visible: Detailed road edges, nodes, and sections; warning
  zones; road classifications; emergency-route membership; and repeated 2026 road-
  restriction observations with candidate edge matches are available.
- Key readable variables or data scope: upslope hazard share; slope-road distance,
  aspect, and elevation difference; warning-zone overlap; cut-and-fill proxy; bridge,
  tunnel, valley, and channel proximity; road class and width; alternative-route
  availability; and observed restriction cause and status.
- What would verify it: Spatial correspondence with independently classified landslide-
  related restrictions, sensible increases across rainfall severity, and stable results
  under alternative upslope buffers and slope-to-road transfer weights.
- What would falsify or weaken it: Poor road matching, absence of usable runout or
  transfer information, or no improvement over warning-zone overlap alone would weaken
  a road-failure interpretation.
- Required next feasibility check: Deduplicate restriction events, validate candidate
  edge matches, classify landslide-related causes, and test whether road sections are at
  a defensible scale for slope exposure.

#### Supporting Point 3: Community isolation and service loss

- Role relative to central point: consequence and heterogeneity.
- Research question: Which communities become isolated, which shelters and basic supply
  or municipal emergency facilities become unreachable, and how many residents and
  older residents are affected under each disruption scenario?
- Why it matters: Isolation, rather than hospital accessibility, is the primary outcome
  that makes this project distinct from the existing road-healthcare study.
- Data support currently visible: Populated meshes, age-structured disclosure groups,
  nominal and current shelter layers, emergency water points, public facilities, fire
  stations, and a routable road network provide a strong consequence-analysis base.
- Key readable variables or data scope: baseline network component; single-exit status;
  alternative-route count; connection to a major external road; shelter and supply-node
  travel time; unreachable-service indicators; total and older population; unresolved
  facility locations; and municipality dependence.
- What would verify it: Repeated road-failure simulations produce reproducible isolation
  probabilities, travel-time changes, and service-loss distributions; all exposed
  population reconciles to its spatial support and disconnected or unresolved cases are
  reported explicitly.
- What would falsify or weaken it: A poorly defined community unit, baseline communities
  already disconnected because of network preprocessing, excessive facility-location
  uncertainty, or results dominated by one arbitrary external-road definition.
- Required next feasibility check: Compare settlement polygons, population-mesh
  clusters, and road-connected populated components as candidate community units, then
  validate baseline access before simulating failures.

#### Supporting Point 4: Intervention priority under limited resources

- Role relative to central point: decision optimization and robustness.
- Research question: Under limited inspection, reinforcement, clearance, evacuation,
  and resource-pre-positioning budgets, which road or community interventions maximize
  the reduction in population-weighted isolation and basic-service loss?
- Why it matters: The intended output is an actionable pre-rainfall priority list, not
  only a descriptive risk surface.
- Data support currently visible: Road sections, network attributes, population and
  vulnerability supports, service nodes, and reusable repeated-routing and budgeted-
  selection patterns are available; engineering costs and intervention-effect sizes
  are not yet observed.
- Key readable variables or data scope: baseline isolation risk; communities and
  population protected; older-population weight; road criticality and redundancy;
  intervention type; cost proxy; assumed risk reduction; marginal benefit; and budget.
- What would verify it: Benefits are monotone with budget, feasible under declared
  constraints, reproducible, and superior to hazard-only, road-class-only, and equal-
  cost baselines across sensitivity scenarios.
- What would falsify or weaken it: Highly unstable rankings, negligible improvement,
  or choices determined primarily by unvalidated cost proxies would restrict the result
  to screening rather than optimization guidance.
- Required next feasibility check: Define separate cost and effect ranges for inspection,
  reinforcement, clearance, evacuation, and pre-positioning, and decide whether the
  first version reports a multi-action optimization or a road-priority screening.

### Scope of Analysis

- Geography: Kumamoto Prefecture for screening, followed by finer analysis of the
  highest-ranked roads and communities.
- Period: The post-2026-earthquake period through the next strong-rainfall episode,
  with the 2016 Kumamoto event considered for calibration or external validation.
- Hazard unit: approximately 5-10 m terrain cells or slope units where consistently
  supported; 10 m is sufficient for the prefecture-wide screening stage.
- Network unit: routable road edges aggregated to defensible road sections.
- Consequence unit: settlement or connected population cluster, with 125 m populated
  meshes used for exposure allocation; the final community definition remains subject
  to feasibility testing.
- Primary outcome: community isolation probability or, when probabilities cannot be
  calibrated, the frequency of isolation under declared disruption scenarios.
- Secondary outcomes: loss of access to shelters, supply points, fire-service and
  municipal emergency facilities; affected total and older population; and excess
  travel time where a route remains available.
- Core exclusion: Hospital accessibility is not a central outcome.

### Study Design Declaration

- Research type: applied
- Study design: Applied compound-hazard scenario simulation with spatial screening,
  repeated network disruption, consequence estimation, and budget-constrained
  intervention comparison.
- Decision audience: Prefectural and municipal emergency managers responsible for
  pre-rainfall inspection, temporary reinforcement, clearance capacity, preventive
  evacuation, and resource pre-positioning.
- Interpretation limit: The current design does not identify a causal earthquake effect.
  Calibrated landslide or road-failure probabilities require sufficiently complete event
  labels and validation. Otherwise all outputs must be labelled scenario-based disruption
  scores and simulated consequences.

## 2. Theoretical Background  /  Conceptual Framework  /  Problem Formulation

Research type: applied
Section focus: Empirical context, practical problem, and cautious interpretation limits.

### Research Gap

- Existing susceptibility and warning-zone products identify hazardous terrain but do
  not quantify how post-earthquake rainfall sensitivity propagates through specific road
  failures to community isolation, basic-service loss, and intervention value.
- Existing local network analyses demonstrate emergency-access and intervention methods,
  but their hospital, fire, or water-service outcomes and generic failure probabilities
  cannot answer this project's landslide-specific isolation question.
- The applied gap is therefore an evidence-bounded chain from earthquake-adjusted
  rainfall triggering to road disruption, community consequences, and pre-rainfall
  action priorities.

### Conceptual Framework

- Hazard pathway: rainfall, antecedent wetness, terrain, geology, soil, land cover, and
  earthquake disturbance determine slope-instability risk or a scenario disruption score.
- Exposure pathway: upslope hazard, potential travel or runout, and road attributes
  determine road-section disruption.
- Consequence pathway: disrupted roads alter network connectivity and travel costs,
  producing community isolation, service unreachability, and population exposure.
- Decision pathway: the avoidable portion of these consequences, together with cost and
  feasibility constraints, determines inspection, reinforcement, clearance, evacuation,
  and pre-positioning priorities.
- Expected relationship 1: Stronger earthquake disturbance increases rainfall-related
  instability when the inventory supports estimating an interaction; otherwise this
  relationship is represented only through declared threshold-reduction scenarios.
- Expected relationship 2: Road sections below hazardous upslope terrain and with low
  network redundancy generate larger isolation consequences.
- Expected relationship 3: Consequence-aware intervention selection protects more people
  per unit cost than ranking roads by hazard exposure alone.
- Scope boundary: Satellite change detection may corroborate new bare ground or surface
  change but is not treated as a complete landslide inventory or direct failure label.

### Problem Formulation

- If an event-labelled inventory is adequate, the candidate interpretable hazard model is

  \[
  \operatorname{logit} P(L_i=1)
  = \alpha + f(R_i) + \beta_S S_i + \beta_G G_i + \beta_E E_i
  + \beta_{RE}(R_i E_i).
  \]

  Here, \(R_i\) contains rainfall and antecedent-wetness measures, \(S_i\) terrain
  measures, \(G_i\) geology, soil, and land-cover measures, and \(E_i\) the selected
  earthquake-disturbance measure. The interaction is not interpreted causally without
  an identification design.
- If the inventory is inadequate, the analysis instead declares low, central, and high
  earthquake-sensitivity scenarios:

  \[
  R_c^{post}(x) = R_c^{baseline}(x)[1-\delta E(x)].
  \]

  The resulting output is an earthquake-adjusted landslide disruption score, not a
  calibrated probability.
- Conditional on a defensible slope-to-road transfer weight, road-section failure can
  be represented as

  \[
  P(F_e=1) = 1 - \prod_{i \in U_e}[1-P(L_i=1)q_{ie}],
  \]

  where \(U_e\) is the upslope influence set and \(q_{ie}\) is the conditional transfer
  or scenario weight from slope unit \(i\) to road section \(e\).
- For \(M\) repeated disruption draws, community isolation is summarized as

  \[
  \widehat{P}_{iso,c} = \frac{1}{M}\sum_{m=1}^{M} I_{c,m}^{iso},
  \]

  accompanied by isolated population, older-population exposure, service unreachability,
  and disrupted-minus-baseline travel time.
- A budgeted road-intervention formulation is

  \[
  \max_{x_e} \sum_c w_c
  [\widehat{P}_{iso,c}^{base}-\widehat{P}_{iso,c}^{int}(x)]
  \quad \text{subject to} \quad
  \sum_e Cost_e x_e \leq B.
  \]

  The first version may use declared cost and effect ranges; these must be presented as
  planning assumptions rather than observed engineering costs or guaranteed benefits.
- Interpretation limits: Landslide risk is not observed landslide occurrence; road-
  disruption probability is not a confirmed closure; unreported events are not zeros;
  simulated service loss is not actual response failure; and intervention rankings do
  not replace field or engineering assessment.

## 3. Data Overview

### Data Scope

- Data sources reviewed: 22
- Variables summarized: 280
- Distribution plots generated: 80
- Files skipped during briefing: 0

| Data source | Rows | Columns |
| --- | ---: | ---: |
| Data source 1 | 49 | 8 |
| Data source 2 | 41 | 19 |
| Data source 3 | 1315 | 5 |
| Data source 4 | 9 | 20 |
| Data source 5 | 1713 | 6 |
| Data source 6 | 264 | 13 |
| Data source 7 | 36 | 16 |
| Data source 8 | 1969 | 18 |
| Data source 9 | 94 | 7 |
| Data source 10 | 1044 | 7 |
| Data source 11 | 3904 | 8 |
| Data source 12 | 526056 | 8 |
| Data source 13 | 56424 | 12 |
| Data source 14 | 22 | 4 |
| Data source 15 | 36657 | 19 |
| Data source 16 | 62945 | 10 |
| Data source 17 | 1660 | 8 |
| Data source 18 | 390234 | 21 |
| Data source 19 | 314391 | 5 |
| Data source 20 | 98884 | 12 |
| Data source 21 | 680 | 34 |
| Data source 22 | 343844 | 20 |

### Units of Observation and Time Coverage

The unit of observation and time coverage differ by analytical layer. Terrain is represented by approximately 10 m elevation pixels as a static reference surface. Rainfall is represented by station-hour observations from 2016 through 2025. Interpreted landslide evidence is represented by mapped points from the 2016 event, while warning designations are represented by polygons with a 2025 reference. The baseline network uses 2024 road edges, nodes, emergency routes, and junction-to-junction road sections. Population exposure uses populated 125 m meshes and disclosure groups from the 2020 census. Administrative boundaries and most facility layers are cross-sectional reference records, whereas current shelter, emergency-water, earthquake-damage, and road-restriction observations are irregular event snapshots from late July through early August 2026. Model scores, community isolation frequencies, service losses, and intervention benefits are derived analytical outputs rather than additional observed samples.

### Time-Series Candidates

Potential time-series structure was detected in 10 data source(s).
Specific source files and original column names remain in the data-briefing artifacts, not in AnaSOP.

### Data Limitations

- No skipped files were recorded by the briefing script.
- Treat this section as exploratory; final variable decisions belong to Section 4.
- AnaSOP intentionally avoids raw dataset names, source file paths, and original column names.
## 4. Variable Construction  /  Key Variables

The confirmed preprocessing set uses a multi-resolution spatial design. Terrain and future satellite features retain defensible native resolution; rainfall remains at station or product resolution; roads remain a line network; population consequences use the 125 m mesh; and landslide observations remain point event labels. Missing values are preserved without imputation or row deletion.

Variable naming convention: the `variable_name` and `full_name` columns below contain English readable or article-facing variable names only. Original source labels, dataset identifiers, file names, and implementation-specific field names are deliberately excluded from AnaSOP and retained only in the technical preprocessing lineage. These readable names are used consistently in the estimation framework, analytical workflow, figures, and tables.

| variable_name | full_name | role | formal_definition | construction_or_coding | is_final_variable |
|---|---|---|---|---|---|
| Elevation | Terrain Elevation (m) | main explanatory | \(z(x)\), terrain elevation at location \(x\), measured in metres. | Decoded from native GSI DEM10B RGB elevation tiles; retained as a georeferenced raster at native Web Mercator pixel spacing. | yes |
| Station Slug | Station Slug | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Station ID | JMA Station Identifier | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Station Name (Japanese) | Station Name (Japanese) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Observation Time | Observation Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Hourly Rainfall | Hourly Rainfall (mm) | main explanatory | \(R_{1h}(s,t)\), hourly rainfall at station \(s\) and time \(t\), measured in millimetres. | JMA station chunks concatenated, converted to numeric, timestamped in Asia/Tokyo, and deduplicated by station and observation time; no spatial interpolation or missing-value imputation. | yes |
| No-Phenomenon Flag | JMA No-Phenomenon Flag | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Quality Flag | JMA Rainfall Quality Flag | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Homogeneity Number | JMA Homogeneity Number | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Support Facility ID | Support Facility ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Support Facility Type | Support Facility Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Reference Year | Source Reference Year | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Administrative Area Code | Administrative Area Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Facility Class | Facility Class | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Facility Name | Facility Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Address | Address | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Geometry | Geometry | spatial linkage | TBD | Retained as binary geometry for spatial linkage; geometry type and native information content are preserved. | yes |
| Municipality Code | Municipality Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Prefecture Name | Prefecture Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Subprefecture Name | Subprefecture Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| District Name | District Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Municipality Name | Municipality Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Ward Name | Ward Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Municipality Label | Municipality Label | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Prefecture Code | Prefecture Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Emergency Road Class Code | Emergency Road Class Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Type Code | Road Type Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Route Name | Route Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Route ID | Route ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Branch ID | Branch ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Name | Source Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Date | Source Date | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Service Status | Service Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Notes | Notes | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Emergency Road Class | Emergency Road Class | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Type | Road Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Facility Type | Facility Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Capacity | Capacity | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Facility Area m2 | Facility Area m2 | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Earthquake Hazard | Earthquake Hazard | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Tsunami Hazard | Tsunami Hazard | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Flood Hazard | Flood Hazard | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Volcanic Hazard | Volcanic Hazard | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Other Hazard | Other Hazard | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| No Hazard Specified | No Hazard Specified | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Location Accuracy Level | Location Accuracy Level | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Latitude | Latitude | spatial linkage | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Longitude | Longitude | spatial linkage | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Record ID | Source Record ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Fire Facility Name | Fire Facility Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Fire Facility Type Code | Fire Facility Type Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Fire Facility Type | Fire Facility Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Candidate Dispatch Base | Candidate Dispatch Base | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Hazard Type Code | Hazard Type Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Warning Zone Class Code | Warning Zone Class Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Zone ID | Zone ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Zone Name | Zone Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Designation Date | Designation Date | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Special Warning Zone Pending Code | Special Warning Zone Pending Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Hazard Type | Hazard Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Warning Zone Class | Warning Zone Class | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Special Warning Zone Pending | Special Warning Zone Pending | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Disclosure Group Code | Disclosure Group Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Disclosure Group Size | Disclosure Group Size | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Suppressed Source Mesh Count | Suppressed Source Mesh Count | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Total Population | Total Population | outcome weighting | \(N_c\), resident population represented by spatial unit \(c\). | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Total Households | Total Households | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| General Households | General Households | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Population Age 65+ | Population Age 65+ | outcome weighting | \(N_{65+,c}\), residents aged 65 years or older in spatial unit \(c\). | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Population Age 75+ | Population Age 75+ | outcome weighting | \(N_{75+,c}\), residents aged 75 years or older in spatial unit \(c\). | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Population Age 85+ | Population Age 85+ | outcome weighting | \(N_{85+,c}\), residents aged 85 years or older in spatial unit \(c\). | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| One-Person Households | One-Person Households | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Households with Member Age 65+ | Households with Member Age 65+ | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Older Single-Person Households | Older Single-Person Households | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Older Couple Households | Older Couple Households | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Population Age 65+ Share | Population Age 65+ Share | vulnerability | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Population Age 75+ Share | Population Age 75+ Share | vulnerability | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Population Age 85+ Share | Population Age 85+ Share | vulnerability | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Older Single-Person Household Share | Older Single-Person Household Share | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Older Couple Household Share | Older Couple Household Share | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Mesh Code | Mesh Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Disclosure Status | Disclosure Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Aggregation Destination Mesh Code | Aggregation Destination Mesh Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Aggregated Source Mesh Codes | Aggregated Source Mesh Codes | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Edge ID | Road Edge ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Section ID | Road Section ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| From Node ID | From Node ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| To Node ID | To Node ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Network Component ID | Network Component ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Length (m) | Road Length (m) | control | \(L_e\), length of road edge \(e\), measured in metres. | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Assumed Speed (km/h) | Assumed Speed (km/h) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Baseline Edge Travel Time (min) | Baseline Edge Travel Time (min) | control | \(T^{base}_e\), undisrupted travel time on road edge \(e\), measured in minutes. | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Hazard Exposure Class | Hazard Exposure Class | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Emergency Route Membership | Emergency Route Membership | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Available | Road Available | control | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Network Analysis Eligible | Network Analysis Eligible | control | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Category | Road Category | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road State | Road State | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Vertical Level | Vertical Level | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Width Category | Width Category | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Toll Category | Toll Category | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Secondary Mesh Code | Secondary Mesh Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Network Node ID | Network Node ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Section From Node ID | Section From Node ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Section To Node ID | Section To Node ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Section Length (m) | Road Section Length (m) | control | \(L_s\), length of road section \(s\), measured in metres. | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Edge Count | Road Edge Count | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Baseline Section Travel Time (min) | Baseline Section Travel Time (min) | control | \(T^{base}_s\), undisrupted travel time on road section \(s\), measured in minutes. | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Shelter ID | Shelter ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Shelter Name | Shelter Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Same Address as Emergency Evacuation Site | Same Address as Emergency Evacuation Site | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Accepted Persons | Accepted Persons | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Evidence ID | Evidence ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Event ID | Event ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Municipality | Municipality | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Coordinate Precision | Coordinate Precision | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Coordinate Uncertainty (m) | Coordinate Uncertainty (m) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Evidence Tier | Evidence Tier | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Verification Status | Verification Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Asset Type | Asset Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Observed Damage Type | Observed Damage Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Structural Damage Class | Structural Damage Class | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Reported Affected Asset Count | Reported Affected Asset Count | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Place Description | Place Description | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Organization | Source Organization | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Type | Source Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Report Number | Source Report Number | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Page | Source Page | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source URL | Source URL | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Evacuation Site ID | Evacuation Site ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Evacuation Site Name | Evacuation Site Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Earthquake Designation | Earthquake Designation | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Large-Scale Fire Designation | Large-Scale Fire Designation | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Same Address as Designated Shelter | Same Address as Designated Shelter | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Shelter Number | Shelter Number | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| District | District | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Maximum Capacity | Maximum Capacity | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Evacuee Households | Evacuee Households | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Evacuee People | Evacuee People | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Water Status | Water Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Electricity Status | Electricity Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Air Conditioning Status | Air Conditioning Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Toilet Count | Toilet Count | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Portable Toilet Count | Portable Toilet Count | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Snapshot Time | Snapshot Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source File | Source File | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Retrieved At UTC | Source Retrieved At UTC | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Location Resolution Status | Location Resolution Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Water Point Name | Water Point Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Valid From Date | Valid From Date | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Valid To Date | Valid To Date | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Opening Time | Opening Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Closing Time | Closing Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Allocation Basis | Allocation Basis | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Allocation Limit (L) | Allocation Limit (L) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Water Type | Water Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source Status Time | Source Status Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Observation ID | Restriction Observation ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Status | Restriction Status | outcome | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Reason | Restriction Reason | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Matched Road Edge ID | Matched Road Edge ID | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Edge Match Distance (m) | Road Edge Match Distance (m) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Route Name Agreement | Route Name Agreement | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Edge Match Candidate Count | Road Edge Match Candidate Count | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Edge Match Method | Road Edge Match Method | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Road Edge Match Status | Road Edge Match Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Feature Index | Feature Index | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Start Address | Start Address | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| End Address | End Address | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Type | Restriction Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Start Time | Restriction Start Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Start Status | Restriction Start Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Affected Length (km) | Affected Length (km) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Geometry Type | Geometry Type | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Geometry JSON | Geometry JSON | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Record Name | Restriction Record Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Start Point Name | Start Point Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| End Point Name | End Point Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Direction | Restriction Direction | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restricted Length (km) | Restricted Length (km) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Regional Bureau Code | Regional Bureau Code | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Regional Bureau Name | Regional Bureau Name | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Change Time | Restriction Change Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Restriction Change Status | Restriction Change Status | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Detour Available | Detour Available | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Isolated Settlement Present | Isolated Settlement Present | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Personal Injury Present | Personal Injury Present | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Property Damage Present | Property Damage Present | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Power Outage Present | Power Outage Present | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Landslide Inventory ID | Landslide Inventory Identifier | outcome | TBD | Assigned sequentially to interpreted 2016 GSI landslide point placemarks; points remain event labels and are not interpolated into probabilities. | yes |
| Landslide Size Class | Interpreted Landslide Size Class | outcome | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Observation Date | Inventory Observation Date | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Temporary Threshold Group | Official Temporary Rainfall Threshold Group | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Rainfall Threshold Retention Factor | Post-Earthquake Rainfall Threshold Retention Factor | main explanatory | \(f_m = R^{post}_c(m) / R^{baseline}_c(m)\) for municipality or subarea \(m\). | Parsed from the official temporary threshold table and converted to numeric; values represent retained fractions of baseline thresholds. | yes |
| Municipality or Subarea (Japanese) | Municipality or Subarea Name (Japanese) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source | Official Threshold Source | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Cumulative Rainfall | Rolling Cumulative Rainfall (mm) | main explanatory | \(R_h(s,t)=\sum_{u=t-h+1}^{t}R_{1h}(s,u)\), for \(h\) in 3, 24, and 72 hours. | Computed within station after hourly quality screening; missing hours remain missing and no spatial interpolation is applied at preprocessing. | yes |
| Rainfall Scenario | Rainfall Severity Scenario | main explanatory | Ordered category with levels Moderate, Heavy, and Extreme. | Assigned from historical rainfall distributions and official threshold context; exact cut points are declared in the estimation framework. | yes |
| Terrain Slope | Terrain Slope (degrees) | main explanatory | \(S(x)=\arctan(\sqrt{z_x(x)^2+z_y(x)^2})180/\pi\). | Derived from Elevation at native terrain resolution using finite differences and retained in degrees. | yes |
| Terrain Curvature | Terrain Curvature | main explanatory | \(C(x)=z_{xx}(x)+z_{yy}(x)\). | Derived as screening-scale terrain curvature from second finite differences of Elevation; sensitivity specifications may separate profile and plan curvature. | yes |
| Landslide Disruption Score | Official-Threshold-Adjusted Landslide Disruption Score | intermediate outcome | \(H_i^{(r,f)}=\operatorname{logit}^{-1}(\theta_0+\theta_z Z_i+\theta_s S_i+\theta_c C_i+\theta_w W_i+\theta_r X_i^{(r,f)})\). | Scenario score for terrain unit \(i\), rainfall scenario \(r\), and threshold-retention setting \(f\); calibrated for ranking with 2016 inventory evidence and not labelled as occurrence probability. | yes |
| Road Disruption Score | Scenario Road Disruption Score | intermediate outcome | \(D_e^{(r,f)}=1-\prod_{i\in U_e}(1-H_i^{(r,f)}q_{ie})\). | Aggregates upslope Landslide Disruption Score over influence set \(U_e\) using transfer weight \(q_{ie}\); validated against observed restriction evidence and interpreted as a score. | yes |
| Community ID | Road-Connected Population Community Identifier | analysis unit | Deterministic identifier for a road-connected cluster of populated 125 m meshes. | Populated meshes are connected to eligible road nodes and grouped within the same accessible baseline network component; unresolved meshes remain explicit. | yes |
| Community Isolation Frequency | Monte Carlo Community Isolation Frequency | primary outcome | \(\widehat{P}_{iso,c}=M^{-1}\sum_{m=1}^{M}I_{c,m}^{iso}\), with \(M=1000\). | Fraction of 1,000 scenario disruption draws in which community \(c\) loses connection to the declared external-road target; reported as simulation frequency, not calibrated probability. | yes |
| Isolated Population | Expected Isolated Population | primary consequence | \(N^{iso}=\sum_c N_c\widehat{P}_{iso,c}\). | Population-weighted isolation exposure summed across communities using Total Population; older-population variants use the confirmed age variables. | yes |
| Service Reachability Loss | Basic Service Reachability Loss | secondary outcome | \(L_c^{service}=\sum_k w_k\widehat{P}(T_{c,k}=\infty)\). | Weighted simulation frequency that service class \(k\) becomes unreachable from community \(c\); service weights are declared and varied in sensitivity analysis. | yes |
| Excess Travel Time | Disruption-Induced Excess Travel Time (min) | secondary outcome | \(\Delta T_{c,k}=T_{c,k}^{disrupted}-T_{c,k}^{baseline}\). | Computed only when service \(k\) remains reachable; unreachable cases are reported separately and are not assigned arbitrary travel times. | yes |
| Intervention Type | Scenario Intervention Type | decision variable | Categorical action: inspection, temporary reinforcement, clearance pre-positioning, preventive evacuation, resource pre-positioning, or alternative-route protection. | Intervention categories are scenario actions and do not imply completed engineering assessment. | yes |
| Intervention Cost | Scenario Intervention Cost | decision constraint | \(Cost_{e,a}^{(l)}\), \(Cost_{e,a}^{(c)}\), and \(Cost_{e,a}^{(h)}\) are low, central, and high cost assumptions for road \(e\) and action \(a\). | Uses declared relative or planning-unit ranges because observed engineering costs are unavailable. | yes |
| Avoided Isolation | Population-Weighted Avoided Isolation | intervention benefit | \(A(x)=\sum_c N_c[\widehat{P}_{iso,c}^{base}-\widehat{P}_{iso,c}^{int}(x)]\). | Difference between baseline and intervention simulation frequencies, weighted by population, under intervention set \(x\). | yes |
| Protected Population | Expected Population Protected by Intervention | intervention benefit | \(N^{protected}(x)=A(x)\). | Expected population-equivalent reduction in isolation frequency; reported with older-population protection and scenario intervals. | yes |
| Priority Score | Robust Intervention Priority Score | decision outcome | \(Q_e=\operatorname{median}_{a,b}[\Delta N_{e,a,b}^{protected}/Cost_{e,a,b}]\). | Median protected-population benefit per planning cost across intervention actions \(a\) and sensitivity settings \(b\), accompanied by rank-stability diagnostics rather than treated as an engineering optimum. | yes |

## 5. Identification Strategy

### Design Principle

The study uses an applied, scenario-based compound-hazard design rather than a causal design. Identification comes from transparent contrasts across Rainfall Scenario and Rainfall Threshold Retention Factor settings, spatial ranking calibration against Landslide Inventory ID locations, validation of Road Disruption Score against observed Restriction Reason and Restriction Status evidence, and repeated network disruption of the baseline road graph. The analysis does not identify the causal effect of earthquake shaking on landslide occurrence.

The primary analytical units are terrain cells for Landslide Disruption Score, road sections for Road Disruption Score, road-connected clusters of populated 125 m meshes for Community ID, and service classes represented by Shelter ID, Evacuation Site ID, Water Point Name, Fire Facility Name, and Facility Name. Communities are defined before any disruption simulation, and baseline connectivity, population reconciliation, and service-node attachment must pass quality checks before scenario results are interpreted.

### Estimands and Evidence Contrasts

- The threshold-adjustment estimand is the change in Landslide Disruption Score between baseline, 80 percent, and 70 percent Rainfall Threshold Retention Factor settings under the same Rainfall Scenario. This is a scenario contrast, not an estimated causal earthquake effect.
- The road estimand is the change in Road Disruption Score across rainfall and threshold settings, together with its ranking correspondence to landslide-related Restriction Reason and Restriction Status observations.
- The primary consequence estimand is Community Isolation Frequency from 1,000 Monte Carlo disruption draws. Isolated Population is the population-weighted consequence, and Population Age 65+, Population Age 75+, and Population Age 85+ support vulnerability heterogeneity.
- Secondary consequence estimands are Service Reachability Loss and Excess Travel Time for reachable services.
- The decision estimands are Avoided Isolation, Protected Population, and Priority Score under low, central, and high Intervention Cost and intervention-effect assumptions.

### Calibration and Validation Strategy

The 2016 interpreted landslide inventory is treated as incomplete presence evidence. Spatially blocked calibration evaluates a fitted terrain-plus-warning logistic score, terrain-only and Elevation-plus-warning-zone comparators, a warning-zone-only comparator, and a transparent fixed standardized score. The fitted score is retained only when its mean spatial AUC is at least 0.60, no evaluable fold is below 0.50, it beats the Elevation-plus-warning-zone comparator, and it is within 0.02 AUC of the transparent score. Otherwise the transparent score is selected for scenario screening. The selected Landslide Disruption Score is never labelled as an occurrence probability.

Road validation deduplicates repeated Restriction Observation ID and Snapshot Time records, restricts the validation target to landslide-, rockfall-, slope-collapse-, or sediment-related Restriction Reason categories, and uses Matched Road Edge ID and Road Edge Match Distance (m) to separate reliable from uncertain matches. Because unreported restrictions are not confirmed non-events, validation supports ranking and screening claims rather than calibrated failure probabilities.

### Relationship to Section 4 Variables and Section 8 Outputs

The identification strategy uses only the confirmed readable Section 4 variables as model inputs, analysis units, outcomes, validation evidence, or decision quantities. Hourly Rainfall and Rainfall Threshold Retention Factor determine the rainfall contrasts; Elevation, Terrain Slope, Terrain Curvature, Hazard Type, and Landslide Inventory ID determine and validate slope-disruption rankings; Road Section ID, Geometry, Emergency Route Membership, and restriction evidence translate those rankings to the road network; Community ID and population variables determine isolation consequences; facility identifiers and Baseline Edge Travel Time determine service outcomes; and Intervention Type, Intervention Cost, Avoided Isolation, Protected Population, and Priority Score determine the budget comparison. These linked inputs generate the exact figure and table titles declared in Section 8, so no unsupported variable or unplanned output is introduced by the estimation framework.

### Interpretation Limits

- Rainfall is represented at station or declared product support. Resampling does not create 10 m rainfall information.
- Official threshold retention is a municipal or subarea scenario adjustment, not a continuous ground-motion surface.
- Landslide Disruption Score and Road Disruption Score are relative scenario scores unless independent labels support calibration.
- Community Isolation Frequency is a simulation frequency conditional on the score-to-closure mapping, network definition, and external-road target.
- Service Reachability Loss is simulated network loss, not observed emergency-response failure. Emergency-water results use only resolved locations and are reported as a resolved-point lower bound.
- Intervention Cost and intervention effects are planning assumptions. Priority Score supports robust screening and field inspection, not an engineering optimum or guaranteed benefit.

The confirmed Section 8 outputs cover the central question and all four supporting questions. Failure to achieve stable validation, baseline network quality, population reconciliation, Monte Carlo convergence, or intervention ranking stability restricts the corresponding claim to descriptive or inconclusive evidence.

## 6. Main Estimation Framework

Interpretation limits apply throughout this framework: all hazard, closure, isolation, service, and intervention quantities are conditional scenario scores or simulation outputs unless an explicit validation step supports a narrower empirical interpretation. None is treated as a causal earthquake effect, calibrated occurrence probability, confirmed road closure, observed rescue failure, or engineering optimum.

### Rainfall Features and Scenario Construction

For station \(s\), time \(t\), and accumulation window \(h\), Cumulative Rainfall is

\[
R_h(s,t)=\sum_{u=t-h+1}^{t}R_{1h}(s,u), \qquad h \in \{3,24,72\}.
\]

Here, \(R_{1h}(s,u)\) is Hourly Rainfall at hour \(u\), and \(R_h(s,t)\) is Cumulative Rainfall over \(h\) hours. A window is missing when required hourly observations do not satisfy the declared completeness rule.

Moderate, Heavy, and Extreme Rainfall Scenario values use station-specific historical quantiles \(\tau_r\) with central settings \(0.75\), \(0.90\), and \(0.99\), respectively. For terrain cell \(i\), scenario exceedance is

\[
X_i^{(r,f)}=\sum_{h\in H}\omega_h\frac{Q_{h,s(i)}(\tau_r)}{f_iQ_{h,s(i)}(0.90)}, \qquad \sum_{h\in H}\omega_h=1.
\]

Here, \(H=\{1,3,24,72\}\) is the rainfall-window set, \(Q_{h,s}(\tau)\) is the historical quantile \(\tau\) for window \(h\) at station \(s\), \(s(i)\) is the declared station-support assignment for cell \(i\), \(f_i\) is Rainfall Threshold Retention Factor, \(\omega_h\) is the declared window weight, and \(X_i^{(r,f)}\) is the dimensionless scenario exceedance index. Station assignment is evaluated through nearest-station and coarse inverse-distance sensitivity specifications; neither is described as fine-resolution rainfall interpolation.

### Terrain and Landslide Disruption Score

Terrain Slope and Terrain Curvature are derived from Elevation at native terrain resolution. Let \(Z_i\), \(S_i\), \(C_i\), and \(W_i\) denote standardized Elevation, Terrain Slope, Terrain Curvature, and warning-zone exposure derived from Hazard Type and Geometry for cell \(i\). Landslide Disruption Score is

\[
H_i^{(r,f)}=\operatorname{logit}^{-1}\left(\theta_0+\theta_zZ_i+\theta_sS_i+\theta_cC_i+\theta_wW_i+\theta_rX_i^{(r,f)}\right).
\]

Here, \(\theta_0\) is the intercept; \(\theta_z\), \(\theta_s\), \(\theta_c\), \(\theta_w\), and \(\theta_r\) are score weights; and \(H_i^{(r,f)}\) is Landslide Disruption Score under rainfall scenario \(r\) and threshold setting \(f\). Penalized presence-background calibration with spatial blocks provides the central weights when stable; otherwise standardized scenario weights and their low-high perturbations are reported. In both cases, \(H_i^{(r,f)}\) remains a score.

### Slope-to-Road Translation

For road section \(e\), Road Disruption Score is

\[
D_e^{(r,f)}=1-\prod_{i\in U_e}\left(1-H_i^{(r,f)}q_{ie}\right).
\]

Here, \(U_e\) is the upslope influence set for road section \(e\), \(q_{ie}\) is a transfer weight based on Geometry, Elevation difference, distance, and terrain alignment between cell \(i\) and road section \(e\), and \(D_e^{(r,f)}\) is Road Disruption Score. Road Category, Road Section Length (m), Emergency Route Membership, and Hazard Type enter stratification and sensitivity analysis rather than being interpreted as causal controls.

For Monte Carlo sensitivity setting \(b\), the score becomes a scenario closure propensity through a declared monotone mapping:

\[
p_{e,b}^{(r,f)}=g_b\left(D_e^{(r,f)}\right), \qquad F_{e,m}^{(r,f,b)}\sim\operatorname{Bernoulli}\left(p_{e,b}^{(r,f)}\right).
\]

Here, \(g_b\) is a declared low, central, or high monotone calibration function informed by restriction-ranking evidence and bounded scenario closure-rate assumptions; \(p_{e,b}^{(r,f)}\) is a scenario closure propensity; \(F_{e,m}^{(r,f,b)}\) indicates closure of road section \(e\) in draw \(m\). Observed restriction prevalence is not treated as the population road-failure rate, and the notation does not imply an empirically calibrated failure probability.

### Community Isolation and Service Consequences

For \(M=1000\) draws, Community Isolation Frequency is

\[
\widehat{P}_{iso,c}^{(r,f,b)}=\frac{1}{M}\sum_{m=1}^{M}I_{c,m}^{iso,(r,f,b)}.
\]

Here, \(I_{c,m}^{iso,(r,f,b)}\) equals one when Community ID \(c\) loses connection to the declared external-road target in draw \(m\), and \(\widehat{P}_{iso,c}^{(r,f,b)}\) is Community Isolation Frequency. The primary external target is the set of stable roots containing Primary Emergency Road nodes at prefectural boundary gateways. Robustness targets use all emergency-route boundary gateways and all Primary Emergency Road roots. Rainfall scenarios use common random numbers so ordered closure propensities generate ordered community frequencies.

Isolated Population is

\[
N_{iso}^{(r,f,b)}=\sum_c N_c\widehat{P}_{iso,c}^{(r,f,b)}.
\]

Here, \(N_c\) is Total Population assigned to community \(c\), and \(N_{iso}^{(r,f,b)}\) is expected Isolated Population. Equivalent sums use Population Age 65+, Population Age 75+, and Population Age 85+.

For service class \(k\), Service Reachability Loss and Excess Travel Time are

\[
L_c^{service,(r,f,b)}=\sum_k w_k\widehat{P}\left(T_{c,k}^{(r,f,b)}=\infty\right),
\]

\[
\Delta T_{c,k}^{(r,f,b)}=T_{c,k}^{(r,f,b)}-T_{c,k}^{baseline}.
\]

Here, \(T_{c,k}^{(r,f,b)}\) is disrupted travel time from community \(c\) to the nearest reachable service in class \(k\); \(T_{c,k}^{baseline}\) is baseline travel time; \(w_k\) is a declared service weight; \(L_c^{service,(r,f,b)}\) is Service Reachability Loss; and \(\Delta T_{c,k}^{(r,f,b)}\) is Excess Travel Time for reachable cases. Service loss uses 1,000 connectivity draws, while Excess Travel Time uses 100 weighted rerouting draws on the complete road graph. Baseline-unreachable cases remain non-evaluable and are not converted to zero or assigned an arbitrary large travel time.

### Robust Intervention Screening

Interventions are evaluated with action-appropriate outcomes. Temporary reinforcement, clearance pre-positioning, and alternative-route protection are road-access actions that may reduce scenario closure propensity. For selected road action \(a\), the sensitivity model is

\[
\widetilde{p}_{e,b}^{(r,f)}(x)=p_{e,b}^{(r,f)}\prod_{a\in A_{road}}\left(1-\rho_{a,b}x_{e,a}\right).
\]

Here, \(A_{road}\) is the set of road-access actions, \(x_{e,a}\) equals one when action \(a\) is assigned to road section \(e\), \(\rho_{a,b}\) is the declared low, central, or high proportional effectiveness assumption, and \(\widetilde{p}_{e,b}^{(r,f)}(x)\) is the intervention-adjusted closure propensity. Inspection is treated as an information action, preventive evacuation as a life-safety action, and resource pre-positioning as a service-continuity action. These actions are ranked using exposed population, uncertainty, or avoided Service Reachability Loss as appropriate and are not credited with Avoided Isolation unless a separately justified road-access effect exists.

For intervention set \(x\), sensitivity setting \(b\), and budget \(B\), population-weighted Avoided Isolation is

\[
A_b(x)=\sum_cN_c\left[\widehat{P}_{iso,c}^{base,b}-\widehat{P}_{iso,c}^{int,b}(x)\right], \qquad \sum_{e,a}Cost_{e,a,b}x_{e,a}\leq B.
\]

Here, \(x_{e,a}\) indicates selection of Intervention Type \(a\) for road section or community target \(e\); \(Cost_{e,a,b}\) is Intervention Cost; \(\widehat{P}_{iso,c}^{base,b}\) and \(\widehat{P}_{iso,c}^{int,b}(x)\) are baseline and intervention Community Isolation Frequency; and \(A_b(x)\) is Avoided Isolation, numerically equal to Protected Population under population weighting for eligible road-access actions.

Priority Score for road section \(e\) is

\[
Q_e=\operatorname{median}_{a,b}\left(\frac{\Delta N_{e,a,b}^{protected}}{Cost_{e,a,b}}\right).
\]

Here, \(\Delta N_{e,a,b}^{protected}\) is the marginal Protected Population for road section \(e\), eligible road-access action \(a\), and sensitivity setting \(b\); and \(Q_e\) is Priority Score. Budget portfolios are assembled by robust ranking with feasibility constraints and compared with hazard-only, Emergency Route Membership-only, Road Category-only, and equal-cost consequence baselines. Road-access, information, life-safety, and service-continuity benefits are reported in separate columns and are not collapsed into one score without declared decision weights. Results are screening priorities rather than engineering optima.

### Robustness, Heterogeneity, and Failure Modes

- Rainfall robustness varies scenario quantiles, accumulation-window weights, station-support assignment, and official threshold-retention settings.
- Terrain and road-transfer robustness uses an upslope influence set requiring positive Elevation difference and downhill alignment toward sampled road points, with distance decay, warning-zone comparison, and low-central-high score-to-closure mappings.
- The central network screen allows the upper 15 percent of positive Heavy-scenario road scores to fail. Network robustness varies external-road targets, closure mappings, service-node attachment, and \(M\) across 500, 1,000, and 2,000 draws.
- Vulnerability heterogeneity reports Total Population and age-specific populations separately and stratifies roads by Road Category and Emergency Route Membership.
- Intervention robustness varies Intervention Cost, assumed effectiveness, service weights, and budget; rank correlations and selection frequencies accompany Priority Score.
- Ablations compare the full framework with warning-zone-only, terrain-only, no-threshold-adjustment, hazard-only road ranking, and equal-cost intervention baselines.
- Failure modes include weak held-out inventory capture, poor restriction correspondence, baseline-disconnected communities, unresolved service locations, non-converged simulation frequencies, or unstable intervention rankings.

## 7. Analytical Workflow

Interpretation limits are enforced through the support-status column: each workflow step may support only the stated scenario-conditional, relative-ranking, or bounded service claim, and any failed upstream quality gate restricts downstream evidence to partial support or inconclusive status.

| step | variables used | formula/model used | generated figure/table title | theory or claim evaluated | support status |
|---|---|---|---|---|---|
| Confirm analytical coverage and spatial support | Geometry, Observation Time, Station ID, Road Section ID, Network Node ID, Mesh Code, Total Population, Location Resolution Status | Coverage, missingness, geometry validity, temporal range, population reconciliation, and baseline network checks | Analytical Data Coverage and Quality | Establishes whether the data chain is sufficiently complete for the central question | Inconclusive until all quality thresholds pass |
| Define rainfall and threshold scenarios | Observation Time, Hourly Rainfall, Cumulative Rainfall, Rainfall Scenario, Rainfall Threshold Retention Factor, Municipality or Subarea (Japanese) | Rolling rainfall formula and quantile-based scenario exceedance \(X_i^{(r,f)}\) | Rainfall History and Official Threshold Adjustment; Rainfall and Threshold Scenarios | Evaluates the declared post-earthquake threshold-adjustment mechanism for RQ1 | Scenario support only; no causal earthquake claim |
| Construct terrain context and landslide score | Elevation, Terrain Slope, Terrain Curvature, Hazard Type, Landslide Inventory ID, Landslide Size Class, Landslide Disruption Score | Terrain derivatives, spatial validation rule, and \(H_i^{(r,f)}\) | Terrain, Landslide Evidence, and Emergency Network Context; Official-Threshold-Adjusted Landslide Disruption Score | Tests whether score rankings align with interpreted landslide evidence and change monotonically across scenarios | Partially supported as a validation-selected transparent scenario ranking; not an occurrence model |
| Validate slope-to-road translation | Road Section ID, Road Category, Road Section Length (m), Emergency Route Membership, Restriction Reason, Restriction Status, Matched Road Edge ID, Road Edge Match Distance (m), Road Disruption Score | Directional upslope aggregation \(D_e^{(r,f)}\) and observed-restriction ranking validation | Road Disruption Exposure and Observed Restriction Evidence; Hazard and Road-Disruption Validation | Evaluates RQ2 and the mechanism that hazardous upslope terrain affects specific roads | Supported for relative screening because restriction evidence ranks above warning-zone and road-length baselines; not a closure probability |
| Define baseline communities and access targets | Community ID, Network Component ID, Mesh Code, Total Population, Population Age 65+, Population Age 75+, Population Age 85+, Network Analysis Eligible, Emergency Route Membership | Road-connected populated-mesh clustering and baseline reachability audit | Community Isolation Frequency and Exposed Population; High-Isolation-Risk Communities | Establishes a defensible consequence unit for RQ3 | Inconclusive if baseline disconnection or population mismatch remains material |
| Simulate road closures and isolation | Road Disruption Score, Community ID, Community Isolation Frequency, Isolated Population, Total Population, Population Age 65+, Population Age 75+, Population Age 85+ | Monotone closure mapping, Bernoulli disruption draws, and \(\widehat{P}_{iso,c}^{(r,f,b)}\) with \(M=1000\) | Community Isolation Frequency and Exposed Population; Municipality Isolation and Service-Loss Summary; High-Isolation-Risk Communities | Evaluates which communities and populations are repeatedly isolated under declared scenarios | Supports simulation-conditional frequency claims only after convergence and network sensitivity checks |
| Estimate service consequences | Shelter ID, Evacuation Site ID, Water Point Name, Fire Facility Name, Facility Name, Baseline Edge Travel Time (min), Service Reachability Loss, Excess Travel Time | 1,000-draw connectivity loss, 100-draw full-network weighted rerouting, \(L_c^{service,(r,f,b)}\), and \(\Delta T_{c,k}^{(r,f,b)}\) | Basic Service Reachability Loss; Municipality Isolation and Service-Loss Summary | Evaluates the secondary RQ3 claim on basic-service loss | Partially supported; water results are a resolved-point lower bound and baseline-unreachable cases remain explicit |
| Screen road and community interventions | Road Section ID, Emergency Route Membership, Road Category, Intervention Type, Intervention Cost, Avoided Isolation, Protected Population, Priority Score, Total Population, Population Age 65+ | Action-specific effect assumptions, budget constraint, \(A_b(x)\), robust \(Q_e\) ranking, and four comparator portfolios | Intervention Priorities and Budgeted Benefits; Priority Road Sections; Intervention Portfolios and Robustness | Evaluates RQ4 and whether consequence-aware screening outperforms hazard-only priorities | Partially supported: benefits are monotone and all action classes are represented, but superiority varies by comparator and budget |
| Integrate the full evidence chain | Elevation, Hourly Rainfall, Rainfall Threshold Retention Factor, Landslide Disruption Score, Road Disruption Score, Community Isolation Frequency, Service Reachability Loss, Priority Score | Linked scenario, validation, network simulation, and intervention framework | Compound-Hazard Decision Pathway | Evaluates the central compound-hazard decision question | Supported only when every upstream checkpoint is supported or transparently bounded; otherwise partially supported or inconclusive |

## 8. Figure and Table Plan

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---:|---|---|
| Compound-Hazard Decision Pathway | Links official post-earthquake threshold adjustment and rainfall exposure to slope disruption, road failure, community isolation, service loss, and intervention choice across the central question and all supporting questions. | flowchart | 1 | Elevation, Hourly Rainfall, Rainfall Threshold Retention Factor, Road Section ID, Total Population | done |
| Terrain, Landslide Evidence, and Emergency Network Context | Establishes the spatial evidence base for terrain, interpreted landslides, warning zones, roads, emergency routes, shelters, and water points. | map | 4 | Elevation, Landslide Inventory ID, Landslide Size Class, Hazard Type, Road Section ID, Emergency Route Membership, Shelter ID, Water Point Name, Geometry | done |
| Rainfall History and Official Threshold Adjustment | Shows station rainfall history, cumulative rainfall, Moderate, Heavy, and Extreme scenarios, and official 70 percent and 80 percent threshold retention settings for the threshold-adjustment question. | line + map | 4 | Observation Time, Hourly Rainfall, Station ID, Rainfall Threshold Retention Factor, Municipality or Subarea (Japanese), Cumulative Rainfall, Rainfall Scenario | done |
| Official-Threshold-Adjusted Landslide Disruption Score | Compares baseline and rainfall-scenario slope disruption scores while retaining score-based language unless event labels support probability calibration. | map | 4 | Elevation, Landslide Inventory ID, Hazard Type, Rainfall Threshold Retention Factor, Terrain Slope, Terrain Curvature, Rainfall Scenario, Landslide Disruption Score | done |
| Road Disruption Exposure and Observed Restriction Evidence | Maps road disruption exposure under rainfall scenarios and compares it with observed rockfall, slope-collapse, and sediment-inflow restriction evidence. | map | 4 | Road Section ID, Road Category, Road Section Length (m), Emergency Route Membership, Hazard Type, Restriction Reason, Restriction Status, Matched Road Edge ID, Road Disruption Score | done |
| Community Isolation Frequency and Exposed Population | Shows community isolation frequency and affected total and older populations under each disruption scenario. | map | 4 | Network Component ID, Mesh Code, Total Population, Population Age 65+, Population Age 75+, Geometry, Community ID, Community Isolation Frequency, Isolated Population | done |
| Basic Service Reachability Loss | Shows loss of reachability to shelters, water points, fire services, and municipal facilities, together with excess travel time where routes remain available. | map + bar | 4 | Shelter ID, Evacuation Site ID, Water Point Name, Fire Facility Name, Facility Name, Baseline Edge Travel Time (min), Service Reachability Loss, Excess Travel Time | done |
| Intervention Priorities and Budgeted Benefits | Identifies priority roads and communities and shows how protected population and avoided isolation change with intervention budget and sensitivity assumptions. | map + line | 3 | Road Section ID, Total Population, Population Age 65+, Emergency Route Membership, Intervention Type, Intervention Cost, Avoided Isolation, Protected Population, Priority Score | done |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|
| Analytical Data Coverage and Quality | Documents completeness, temporal coverage, spatial support, and interpretation limits for each analytical layer. | 22 | 10 | One analytical data layer | Record count, spatial type, temporal coverage, missingness, location completeness, resolution, and calibration or validation role | done |
| Rainfall and Threshold Scenarios | Defines the combinations of Moderate, Heavy, and Extreme rainfall with baseline, 70 percent, and 80 percent threshold-retention settings. | 9 | 10 | One rainfall and threshold combination | One-hour, three-hour, 24-hour, and 72-hour rainfall, antecedent rainfall, threshold retention factor, scenario label, and interpretation boundary | done |
| Hazard and Road-Disruption Validation | Compares the full specification, warning-zone baseline, and simplified scenario models using spatial validation and observed restriction evidence. | 5 + 5 | 8 / 6 | One hazard or road model specification, separated across two worksheets | Hazard sheet: spatial AUC, inventory capture, and ranking stability; road sheet: restriction correspondence, hit rate, and ranking stability | done |
| Municipality Isolation and Service-Loss Summary | Summarizes community isolation, exposed population, older population, and service loss for each administrative unit and scenario. | 49 | 16 | One municipality, ward, or comparable administrative unit | Isolation frequency, isolated population, older population, unreachable services, and excess travel time by scenario | done |
| Priority Road Sections | Lists the 30 road sections with the largest consequence-aware intervention relevance. | 30 | 12 | One road section | Municipality or ward, road category and length, disruption score, alternative scarcity, affected communities, total and older population, dependent services, assigned intervention, planning cost, and robust priority score | done |
| High-Isolation-Risk Communities | Lists the 30 communities with the highest Heavy-scenario population and older-population isolation burden. | 30 | 11 | One community | English municipality or ward, centroid coordinates, mesh count, total and older population, candidate gateway sections, scenario isolation frequencies, expected isolated population, and principal service loss | done |
| Intervention Portfolios and Robustness | Compares budget-feasible intervention portfolios and their protective benefits across sensitivity settings. | 21 | 10 | One budget and sensitivity-setting combination | Budget, selected roads, intervention mix, realized cost, protected communities, protected total and older population, avoided isolation share, unit-cost benefit, and selection overlap | done |

### Variable Coverage Check

All key variables referenced by the confirmed figures and tables appear in Section 4 and are marked as final analysis variables. Input features are constructed before estimation; model, simulation, and intervention variables are generated only within the corresponding analytical workflow steps.
