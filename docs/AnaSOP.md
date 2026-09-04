# AnaSOP
Analysis Standard Operating Procedure

## 1. Research Objective

### Working Title

Post-earthquake rainfall-warning threshold scenarios for landslide-related road
disruption, community isolation, and emergency intervention planning in Kumamoto

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
- Key readable variables or data scope: rainfall scenario; official area-level
  rainfall-warning threshold retention;
  terrain and land-cover conditions; slope-to-road exposure; road failure or disruption
  score; network redundancy; community connectivity; total and older population;
  service reachability; intervention cost; and avoided isolation.
- What would verify it: A reproducible scenario chain must yield stable road and
  community rankings across rainfall severity, Monte Carlo seeds, network assumptions,
  and plausible threshold-retention parameters; intervention benefits must be
  positive, budget-feasible, and reconciled to affected communities and population.
- What would falsify or weaken it: The central claim is weakened if the hazard layer
  cannot be linked to roads, the baseline network cannot represent community access,
  community definitions are spatially unstable, or intervention rankings are driven
  mainly by arbitrary cost and threshold choices.
- Required next feasibility check: Confirm terrain, rainfall, official threshold-retention,
  and landslide-inventory availability; define the community unit and external-network
  connection target; audit road topology and service-node coverage.

### Supporting Research Questions

The central question is supported by four linked questions that follow the compound-
hazard and consequence pathway.

#### Supporting Point 1: Post-earthquake rainfall-warning threshold retention

- Role relative to central point: mechanism.
- Research question: How much do the declared baseline and official post-earthquake
  threshold-retention settings change the relative landslide disruption score under
  otherwise identical rainfall scenarios?
- Why it matters: This is the main compound-hazard contribution and separates the
  project from a static landslide susceptibility assessment.
- Data support currently visible: Official warning-zone geography and limited event
  damage evidence are available, while the required elevation surface, rainfall fields,
  and event-labelled landslide inventory remain acquisition or feasibility tasks.
- Key readable variables or data scope: 1 h, 3 h, 24 h, and 72 h rainfall; antecedent
  precipitation index; slope, curvature, wetness and flow-accumulation proxies;
  geology, soil, and land cover; area-level threshold-retention factor; and the
  dimensionless rainfall-loading index.
- What would verify it: Compatibility with the reconstructed JMA-type operational
  indicator, coherent ordering across declared threshold-retention scenarios, and stable
  road prioritization across rainfall-window and loading-coefficient sensitivities.
- What would falsify or weaken it: Indicator incompatibility, severe spatial sampling
  bias, or scenario rankings that reverse under minor parameter changes would prevent
  an operational threshold-retention interpretation.
- Required next feasibility check: Determine the completeness and mapping method of
  the 2016 and 2026 evidence inventories and resolve the spatial support of each official
  threshold-retention setting.

#### Supporting Point 2: Slope hazard to road disruption

- Role relative to central point: mechanism and exposure translation.
- Research question: Under each rainfall and threshold-retention scenario, which road sections are
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
- What would verify it: Spatial correspondence with event-deduplicated restrictions whose
  trigger is independently established, sensible increases across rainfall severity, and
  stable results under alternative upslope buffers and slope-to-road transfer weights.
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
  uncertainty, or results dominated by one arbitrary emergency-road-backbone definition.
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
  population protected; older-population exposure reported separately; road criticality
  and redundancy; assigned intervention type; consequence proxy; cost proxy; assumed
  risk reduction; and budget.
- What would verify it: Benefits are monotone with budget, feasible under declared
  constraints, reproducible across Monte Carlo seeds, and compared under identical
  assumptions with hazard-only, road-class-only, and equal-cost consequence baselines.
  Equality with the equal-cost consequence baseline is an auditable consistency result,
  not evidence of incremental superiority.
- What would falsify or weaken it: Highly unstable rankings, negligible improvement,
  or choices determined primarily by unvalidated cost proxies would restrict the result
  to screening rather than optimization guidance.
- Required next feasibility check: Confirm separate cost and effect ranges for inspection,
  reinforcement, clearance, evacuation, and pre-positioning, and validate the declared
  assigned-action road-priority screening under repeated Monte Carlo seeds.

### Scope of Analysis

- Geography: Kumamoto Prefecture for screening, followed by finer analysis of the
  highest-ranked roads and communities.
- Period: The post-2026-earthquake period through the next strong-rainfall episode,
  with the 2016 Kumamoto inventory used only for footprint-bounded historical
  alignment of the persistent terrain-context ranking, not cross-event calibration.
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
- The applied gap is therefore an evidence-bounded chain from operational
  post-earthquake rainfall-warning threshold scenarios to road disruption, community
  consequences, and pre-rainfall action priorities.

### Conceptual Framework

- Hazard pathway: rainfall, antecedent wetness, terrain, geology, soil, land cover, and
  official area-level threshold retention determine a relative scenario disruption score.
- Exposure pathway: upslope hazard, potential travel or runout, and road attributes
  determine road-section disruption.
- Consequence pathway: disrupted roads alter network connectivity and travel costs,
  producing community isolation, service unreachability, and population exposure.
- Decision pathway: the avoidable portion of these consequences, together with cost and
  feasibility constraints, determines inspection, reinforcement, clearance, evacuation,
  and pre-positioning priorities.
- Expected relationship 1: Smaller declared threshold-retention fractions increase
  relative scenario loading for otherwise identical rainfall, without identifying a
  causal effect of shaking or measuring a change in slope strength.
- Expected relationship 2: Road sections below hazardous upslope terrain and with low
  network redundancy generate larger isolation consequences.
- Expected relationship 3: Consequence-aware intervention selection protects more people
  per unit cost than ranking roads by hazard exposure alone.
- Scope boundary: Satellite change detection may corroborate new bare ground or surface
  change but is not treated as a complete landslide inventory or direct failure label.

### Problem Formulation

- The implemented analysis uses declared operational threshold-retention factors rather
  than a ground-motion, earthquake-damage, or slope-strength model. The resulting output
  is a threshold-retention landslide disruption score, not a calibrated probability or
  an estimated causal earthquake effect.
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
| Station Latitude | JMA Station Latitude (decimal degrees) | spatial linkage | Latitude of JMA station \(s\) in decimal degrees. | Converted from the official JMA station-metadata degrees and decimal-minutes fields and joined by Japanese station name; all seven retained stations must resolve. | yes |
| Station Longitude | JMA Station Longitude (decimal degrees) | spatial linkage | Longitude of JMA station \(s\) in decimal degrees. | Converted from the official JMA station-metadata degrees and decimal-minutes fields and joined by Japanese station name; all seven retained stations must resolve. | yes |
| Observation Time | Observation Time | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Hourly Rainfall | Hourly Rainfall (mm) | main explanatory | \(R_{1h}(s,t)\), hourly rainfall at station \(s\) and time \(t\), measured in millimetres. | JMA station chunks concatenated, converted to numeric, timestamped in Asia/Tokyo, and deduplicated by station and observation time; event construction uses only quality-flag 8 observations and preserves missingness. | yes |
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
| Source Photo Date Label | GSI Source-Photo Date Label | evidence timing | TBD | Parsed from the official placemark description; identifies the air-photo acquisition day or interval used for interpretation. | yes |
| Source Photo Start Date | GSI Source-Photo Start Date | evidence timing | TBD | Parsed as the first day of the official air-photo acquisition interval. | yes |
| Source Photo End Date | GSI Source-Photo End Date | evidence timing | TBD | Parsed as the last day of the official air-photo acquisition interval. | yes |
| Inventory Update Date | GSI Inventory Update Date | provenance | TBD | Records 2016-07-28 as the inventory release/update date, not a uniform landslide observation date. | yes |
| Temporary Threshold Group | Official Temporary Rainfall Threshold Group | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Rainfall Threshold Retention Factor | Post-Earthquake Rainfall Threshold Retention Factor | main explanatory | \(f_m = R^{post}_c(m) / R^{baseline}_c(m)\) for municipality or subarea \(m\). | Parsed from the official temporary threshold table and converted to numeric; values represent retained fractions of baseline thresholds. | yes |
| Municipality or Subarea (Japanese) | Municipality or Subarea Name (Japanese) | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Source | Official Threshold Source | TBD | TBD | Retained and renamed according to confirmed preprocessing decisions; further analytical construction is TBD. | yes |
| Cumulative Rainfall | Rolling Cumulative Rainfall (mm) | main explanatory | \(R_h(s,t)=\sum_{u=t-h+1}^{t}R_{1h}(s,u)\), for \(h\) in 3, 24, and 72 hours. | Computed within station after hourly quality screening; missing hours remain missing and no spatial interpolation is applied at preprocessing. | yes |
| Rainfall Event ID | Independent Rainfall Event Identifier | analysis unit | Deterministic station-support identifier for rainfall event \(j\). | Wet hours belong to the same event until separated by at least 24 consecutive complete zero-rainfall hours; a missing hour breaks event eligibility and never counts as dry. | yes |
| Event Maximum Rainfall | Independent-Event Maximum Rainfall (mm) | main explanatory | \(M_{h,s,j}=\max_{t\in j}R_h(s,t)\), for \(h\in\{1,3,24,72\}\). | Maximum complete accumulation for each station-event-window combination; incomplete rolling windows remain missing. | yes |
| Rainfall Scenario | Rainfall Severity Scenario | main explanatory | Ordered category with event-maximum quantiles \(\tau_r\in\{0.75,0.90,0.99\}\) for Moderate, Heavy, and Extreme. | Assigned from station-specific independent-event maxima using the seven-station 2016-2020 common period centrally and five complete 2016-2025 stations as temporal-support sensitivity. | yes |
| Terrain Slope | Terrain Slope (degrees) | main explanatory | \(S(x)=\arctan(\sqrt{z_x(x)^2+z_y(x)^2})180/\pi\). | Derived from Elevation at native terrain resolution using finite differences and retained in degrees. | yes |
| Terrain Curvature | Terrain Curvature | main explanatory | \(C(x)=z_{xx}(x)+z_{yy}(x)\). | Derived as screening-scale terrain curvature from second finite differences of Elevation; sensitivity specifications may separate profile and plan curvature. | yes |
| Landslide Disruption Score | Official-Threshold-Adjusted Landslide Disruption Score | intermediate outcome | \(H_i^{(r,f)}=\operatorname{logit}^{-1}(0.15Z_i+1.00S_i+0.35|C_i|+0.75W_i+\gamma\log X_i^{(r,f)})\). | Relative terrain score for unit \(i\), event-quantile rainfall scenario \(r\), and threshold-retention setting \(f\), with \(\gamma=1.00\). It is not an occurrence probability. | yes |
| Road Disruption Score | Scenario Road Disruption Score | intermediate outcome | \(D_e^{(r,f)}=\sum_{i\in U_e}q_{ie}H_i^{(r,f)}/\sum_{i\in U_e}q_{ie}\). | Normalized directional aggregation of upslope Landslide Disruption Score. The available 2026 restrictions support only supplementary dry-event correspondence with the terrain-to-road ranking; they do not validate rainfall triggering. | yes |
| Community ID | Road-Connected Population Community Identifier | analysis unit | Deterministic identifier for a road-connected cluster of populated 125 m meshes. | Populated meshes are connected to eligible road nodes and grouped within the same accessible baseline network component; unresolved meshes remain explicit. | yes |
| Community Isolation Frequency | Monte Carlo Community Isolation Frequency | primary outcome | \(\widehat{P}_{iso,c}=M^{-1}\sum_{m=1}^{M}I_{c,m}^{iso}\), with \(M=1000\). | Fraction of 1,000 scenario disruption draws in which community \(c\) loses connection to every baseline component containing a Primary Emergency Road node; reported as simulation frequency, not calibrated probability. | yes |
| Isolated Population | Expected Isolated Population | primary consequence | \(N^{iso}=\sum_c N_c\widehat{P}_{iso,c}\). | Population-weighted isolation exposure summed across communities using Total Population; older-population variants use the confirmed age variables. | yes |
| Service Reachability Loss | Basic Service Reachability Loss | secondary outcome | \(L_{c,k}^{service}=\widehat{P}(T_{c,k}=\infty)\). | Class-specific simulation frequency that no resolved, road-attached destination in service class \(k\) remains reachable from community \(c\). Baseline-unreachable communities are non-evaluable, and no cross-service composite is calculated without separately approved decision weights. | yes |
| Excess Travel Time | Disruption-Induced Excess Travel Time (min) | secondary outcome | \(\Delta T_{c,k}=T_{c,k}^{disrupted}-T_{c,k}^{baseline}\). | Difference between baseline nearest-facility time and the shortest disrupted travel time to any reachable same-class facility; complete class-level loss is reported separately and is not assigned an arbitrary travel time. | yes |
| Intervention Type | Scenario Intervention Type | decision variable | Categorical action: inspection, temporary reinforcement, clearance pre-positioning, preventive evacuation, resource pre-positioning, or alternative-route protection. | Intervention categories are scenario actions and do not imply completed engineering assessment. | yes |
| Intervention Cost | Scenario Intervention Cost | decision constraint | \(Cost_{e,a}^{(l)}\), \(Cost_{e,a}^{(c)}\), and \(Cost_{e,a}^{(h)}\) are low, central, and high cost assumptions for road \(e\) and action \(a\). | Uses declared relative or planning-unit ranges because observed engineering costs are unavailable. | yes |
| Avoided Isolation | Population-Weighted Avoided Isolation | intervention benefit | \(A(x)=\sum_c N_c[\widehat{P}_{iso,c}^{base}-\widehat{P}_{iso,c}^{int}(x)]\). | Difference between baseline and intervention simulation frequencies, weighted by population, under intervention set \(x\). | yes |
| Protected Population | Expected Population Protected by Intervention | intervention benefit | \(N^{protected}(x)=A(x)\). | Expected population-equivalent reduction in isolation frequency; reported with older-population protection and scenario intervals. | yes |
| Priority Score | Assigned-Action Consequence-Based Screening Score | decision outcome | \(Q_e=\operatorname{median}_{b}[G_e\rho_{a(e),b}/Cost_{e,a(e),b}]\). | Auditable screening score for road section \(e\), using a pre-assigned feasible road-access action \(a(e)\), consequence proxy \(G_e\), and low, central, and high cost-effect settings \(b\). It is not a simulated cross-action marginal benefit or an engineering optimum. | yes |

## 5. Identification Strategy

### Design Principle

The study uses an applied, scenario-based compound-hazard design rather than a causal design. Identification comes from transparent contrasts across independent-storm Rainfall Scenario and Rainfall Threshold Retention Factor settings, footprint-bounded historical alignment against Landslide Inventory ID locations, matched pseudo-background correspondence of Road Disruption Score against observed Restriction Reason and Restriction Status evidence, and repeated network disruption of the baseline road graph. The analysis does not identify the causal effect of earthquake shaking on landslide occurrence.

The audit-driven revision replaces quantiles of all positive rolling rainfall windows with maxima from independent rainfall events. An event is a sequence of rainfall hours separated from the next event by at least 24 consecutive complete hours with zero recorded rainfall; missing hours break event eligibility and never count as dry separation. The central spatial specification uses the seven-station common period from 2016 through 2020; a temporal-support sensitivity specification uses the five stations with complete 2016-2025 coverage. Station-specific event quantiles are propagated only at coarse station support using inverse-distance weights. No station-derived surface is interpreted as 10 m rainfall information.

Official threshold-retention values are applied at their resolved spatial support. Yatsushiro contains official 0.70 and 0.80 subarea values, but the available municipality geometry cannot distinguish those subareas. The central municipality-wide assignment is therefore an analyst-defined midpoint of 0.75 rather than an official value. Municipality-wide 0.70 and 0.80 assignments provide bounding cases. Their effects are quantified at the slope, road, isolation, and service-consequence stages; intervention outputs are reopened only if those bounds materially change the candidate set, priority order, or protected-population result.

The primary analytical units are terrain cells for Landslide Disruption Score, road sections for Road Disruption Score, road-connected clusters of populated 125 m meshes for Community ID, and service classes represented by Shelter ID, Evacuation Site ID, Water Point Name, Fire Facility Name, and Facility Name. Communities are defined before any disruption simulation, and baseline connectivity, population reconciliation, and service-node attachment must pass quality checks before scenario results are interpreted.

### Estimands and Evidence Contrasts

- The threshold-adjustment estimand is the change in Landslide Disruption Score between baseline, 80 percent, and 70 percent Rainfall Threshold Retention Factor settings under the same Rainfall Scenario. This is a scenario contrast, not an estimated causal earthquake effect.
- Rainfall-severity contrasts have two distinct estimands: change in score magnitude and change in spatial rank. If scenario rank correlation exceeds 0.95, the evidence supports magnitude scaling only and cannot be described as scenario-sensitive spatial prioritization.
- The road estimand is the change in Road Disruption Score across rainfall and threshold settings, together with its matched-background ranking correspondence to landslide-related Restriction Reason and Restriction Status observations.
- The primary consequence estimand is the mean Community Isolation Frequency across five predeclared, independently seeded sets of 1,000 Monte Carlo disruption draws. Isolated Population is the population-weighted consequence; between-seed ranges quantify Monte Carlo variation, and Population Age 65+, Population Age 75+, and Population Age 85+ support vulnerability heterogeneity.
- Secondary consequence estimands are the five-seed mean Service Reachability Loss and Excess Travel Time for reachable services, with between-seed ranges reported separately.
- The decision estimands are Avoided Isolation and Protected Population for simulated
  portfolios, together with an assigned-action Priority Score used only to order candidate
  road sections under low, central, and high Intervention Cost and effect assumptions.

### Calibration and Validation Strategy

The 2016 interpreted landslide inventory is treated as incomplete presence evidence for a historical terrain-ranking alignment check, not as a census or cross-event calibration sample. The source contains 1,044 centre points interpreted from air photographs acquired on 16-20 April and 5-24 July 2016. The union of the official April and July interpretation footprints covers 57.8% of Kumamoto Prefecture; pseudo-background cells are sampled only inside that footprint. Because 2016-07-28 is the inventory update date rather than the earthquake date, the temporal evidence boundary retains only the 29,632 warning-zone polygons with a known Designation Date on or before the earthquake sequence began on 2016-04-14; later, unknown-date, and sentinel-date polygons are excluded from the historical check. The complete current warning-zone layer remains the appropriate operational input for the 2026 screening application. Spatially blocked evaluation compares fitted terrain-plus-warning, terrain-only, Elevation-plus-warning-zone, and warning-zone-only diagnostic specifications with the transparent fixed standardized score. The fixed score propagated downstream is frozen before this support audit and is evaluated without reviewer-driven refitting; only the logistic comparators are fitted on the corrected sample. Its standardized weights remain 0.15 for Elevation, 1.00 for Terrain Slope, 0.35 for absolute Terrain Curvature, and 0.75 for warning-zone exposure. Ten reproducibly sampled pseudo-background cells are used per unique presence cell, and absence of an interpreted point is never treated as a confirmed non-event. Mean and fold-specific AUC and held-out top-quartile capture describe relative historical alignment only. The 2016 locations are not pooled with the 2026 road records and do not validate 2026 shaking, threshold retention, rainfall loading, closure propensity, or soil-disturbance depth. The selected Landslide Disruption Score is never labelled as an occurrence probability.

Road-restriction correspondence separates repeated snapshots from physical episodes. Snapshot rows are first limited to the generic process reasons rockfall, slope collapse, and sediment inflow; those labels are not treated as trigger labels. Physical episodes are deduplicated by Start Address, End Address, Restriction Reason, and Restriction Start Time. The existing spatial-link rule retains `matched_primary` edge matches no farther than 50 m. Route-name agreement is audited but is not an eligibility criterion because a true agreement is available among candidate matches for only one retained episode. The complete funnel reports 680 official snapshot rows, 175 process-reason rows, 14 physical episodes before spatial matching, 116 retained snapshot rows, 10 retained physical episodes, 152 unique matched edges, 94 unique sections, 96 event-section pairs, and 93 sections with eligible matched controls. The ten episodes began 0.55-24.38 h after the earthquake, contain no explicit rainfall-trigger term, and have 0 mm over the preceding 1, 3, 24, and 72 h both at the nearest project JMA station and across the ten-station audit. They are classified as direct-earthquake consistent but source-unconfirmed and are retained only as supplementary correspondence with the terrain-to-road ranking, not as validation of rainfall-triggered disruption.

For physical episode \(k\), let \(A_k\) contain its matched evidence sections and let \(B_a\) contain the fixed pseudo-background sections matched to evidence section \(a\) on municipality or ward, Road Category, Emergency Route Membership, and Road Section Length (m) decile. The formal correspondence estimand is

\[
C_{\mathrm{episode}}^{(r,f)}=\frac{1}{K}\sum_{k=1}^{K}\frac{1}{|A_k|}\sum_{a\in A_k}\frac{1}{|B_a|}\sum_{b\in B_a}\left[\mathbf{1}\!\left(D_a^{(r,f)}>D_b^{(r,f)}\right)+\frac{1}{2}\mathbf{1}\!\left(D_a^{(r,f)}=D_b^{(r,f)}\right)\right].
\]

Each physical episode receives equal weight, ties contribute 0.5, and the physical episode is the resampling unit for the episode-cluster bootstrap. Prefecture-wide percentiles remain descriptive. Because the event window is dry and unreported restrictions are not confirmed non-events, the metric cannot attribute rainfall triggering, estimate closure probability, or establish comparative superiority when a paired contrast interval includes zero.

### Relationship to Section 4 Variables and Section 8 Outputs

The identification strategy uses only the confirmed readable Section 4 variables as model inputs, analysis units, outcomes, validation evidence, or decision quantities. Hourly Rainfall and Rainfall Threshold Retention Factor determine the rainfall contrasts; Elevation, Terrain Slope, Terrain Curvature, Hazard Type, and Landslide Inventory ID determine and validate slope-disruption rankings; Road Section ID, Geometry, Emergency Route Membership, and restriction evidence translate those rankings to the road network; Community ID and population variables determine isolation consequences; facility identifiers and Baseline Edge Travel Time determine service outcomes; and Intervention Type, Intervention Cost, Avoided Isolation, Protected Population, and Priority Score determine the budget comparison. These linked inputs generate the exact figure and table titles declared in Section 8, so no unsupported variable or unplanned output is introduced by the estimation framework.

### Interpretation Limits

- Rainfall is represented at station or declared product support. Resampling does not create 10 m rainfall information.
- Official threshold retention is a municipal or subarea scenario adjustment, not a continuous ground-motion surface. The municipality-wide 0.75 assignment in unresolved Yatsushiro is an analyst midpoint bounded by separate 0.70 and 0.80 assignments; it is never labelled as an official Yatsushiro value.
- Landslide Disruption Score and Road Disruption Score are relative scenario scores unless independent labels support calibration.
- The 2026 road restrictions are dry, earthquake-proximate, event-deduplicated correspondence evidence; they do not validate rainfall-triggered road disruption, and repeated snapshots or linked sections are not independent events.
- Community Isolation Frequency is a simulation frequency conditional on the score-to-closure mapping, network definition, and emergency-road-backbone target.
- Service Reachability Loss is simulated network loss, not observed emergency-response failure. Emergency-water results are conditional on the resolved destination subset and remain a sensitivity result; incomplete destination geography is not described as a lower bound on loss magnitude.
- Intervention Cost and intervention effects are planning assumptions. Priority Score is
  an assigned-action consequence proxy for screening and field inspection, not a
  cross-action marginal-benefit estimate, engineering optimum, or guaranteed benefit.
- Consequence-aware intervention rankings are compared with every baseline under the same Conservative, Central, or Optimistic cost-effect setting. Superiority is claimed only when the increment is material and stable; otherwise the contribution is auditability and robustness relative to simpler rules.

The confirmed Section 8 outputs cover the central question and all four supporting questions. Failure to achieve stable validation, baseline network quality, population reconciliation, Monte Carlo convergence, or intervention ranking stability restricts the corresponding claim to descriptive or inconclusive evidence.

## 6. Main Estimation Framework

Interpretation limits apply throughout this framework: all hazard, closure, isolation, service, and intervention quantities are conditional scenario scores or simulation outputs unless an explicit validation step supports a narrower empirical interpretation. None is treated as a causal earthquake effect, calibrated occurrence probability, confirmed road closure, observed rescue failure, or engineering optimum.

### Rainfall Features and Scenario Construction

For station \(s\), time \(t\), and accumulation window \(h\), Cumulative Rainfall is

\[
R_h(s,t)=\sum_{u=t-h+1}^{t}R_{1h}(s,u), \qquad h \in \{3,24,72\}.
\]

Here, \(R_{1h}(s,u)\) is Hourly Rainfall at hour \(u\), and \(R_h(s,t)\) is Cumulative Rainfall over \(h\) hours. A window is missing when required hourly observations do not satisfy the declared completeness rule.

Independent rainfall event \(j\) at station \(s\) is separated from adjacent events by at least 24 consecutive complete hours with zero Hourly Rainfall. Missing hours do not count as dry hours, do not contribute zero rainfall, and break eligibility for an accumulation window. For each event and accumulation window, event maximum is

\[
M_{h,s,j}=\max_{t\in j}R_h(s,t), \qquad h\in H=\{1,3,24,72\}.
\]

Here, \(M_{h,s,j}\) is the largest complete accumulation observed during independent event \(j\). Moderate, Heavy, and Extreme Rainfall Scenario values use station-specific event-maximum quantiles \(Q_{h,s}^{event}(\tau_r)\) with central settings \(\tau_r=0.75\), \(0.90\), and \(0.99\), respectively. The empirical event count is reported for every station and window.

For terrain cell \(i\), coarse inverse-distance station weights and the spatial event quantile are

\[
\lambda_{s,i}=\frac{(d_{s,i}+d_0)^{-2}}{\sum_v(d_{v,i}+d_0)^{-2}}, \qquad \widetilde{Q}_{h,i}(\tau_r)=\sum_s\lambda_{s,i}Q_{h,s}^{event}(\tau_r).
\]

Here, \(d_{s,i}\) is the distance between station \(s\) and cell \(i\), \(d_0\) is a small positive stabilizing distance fixed before analysis, \(\lambda_{s,i}\) is the normalized inverse-distance weight, and \(\widetilde{Q}_{h,i}(\tau_r)\) is a coarse station-supported rainfall surface. The Heavy reference for window \(h\) is \(B_h=\operatorname{median}_s[Q_{h,s}^{event}(0.90)]\). Scenario exceedance is

\[
X_i^{(r,f)}=\frac{1}{f_i}\sum_{h\in H}\omega_h\frac{\widetilde{Q}_{h,i}(\tau_r)}{B_h}, \qquad \sum_{h\in H}\omega_h=1.
\]

Here, \(f_i\) is Rainfall Threshold Retention Factor, \(\omega_h\) is the declared accumulation-window weight, and \(X_i^{(r,f)}\) is the dimensionless scenario exceedance index. Official 0.70 and 0.80 values are assigned only where their spatial support is resolved. Because the available geometry does not resolve the two official Yatsushiro subareas, the central municipality-wide assignment uses the analyst midpoint \(f_i=0.75\); municipality-wide \(f_i=0.70\) and \(f_i=0.80\) assignments form bounding sensitivity cases. The specification uses equal weights of 0.25 for the 1, 3, 24, and 72 hour windows. The five-station 2016-2025 support is compared with the central seven-station 2016-2020 support as a temporal-support sensitivity. Neither inverse-distance surface is described as fine-resolution rainfall interpolation.

The Reviewer 1 Comment 2 midpoint audit holds the current Primary Emergency Road backbone, Heavy rainfall, central terrain-to-road transfer, central score-to-closure mapping, current service destinations, five prespecified seeds, and 1,000 draws per seed fixed while assigning all of Yatsushiro \(f_i=0.70\), \(0.75\), or \(0.80\). The midpoint is treated as not highly sensitive only when both bounds remain within 10% of the midpoint consequence, community/service frequency Spearman correlation is at least 0.95, Top-30 burden overlap is at least 0.80, supported-road correlation is at least 0.95, Top-1% road overlap is at least 0.80, candidate-set overlap is at least 0.95, intervention-priority correlation is at least 0.95, Top-150 intervention overlap is at least 0.80, and fixed-budget protected population remains within 10%. The 10% threshold is a transparent practical screen rather than a statistical equivalence margin. All gates pass: Heavy expected disconnected population is 1,118.7, 1,063.6, and 1,016.6 under the three assignments (+5.2% to −4.4% around the midpoint), with community-frequency correlation 0.989–1.000 and 93.3% Top-30 overlap. Across shelters, fire services, and municipal facilities, affected-population changes remain within −6.5% to +8.0%, frequency correlations are 0.990–1.000, and Top-30 overlap is 86.7%–93.3%. Heavy road-score correlation exceeds 0.999, Top-1% road overlap is 96.4%–97.5%, and candidate-road overlap exceeds 99.5%. At the fixed 269.131-planning-unit intervention anchor, protected population changes by −1.5% to +2.7%, priority correlation is at least 0.992, and Top-150 overlap is 100%; therefore, the bounds do not trigger a full intervention rerun or reframing. Emergency-water results remain conditional on 10 of 36 geolocated destinations. The frozen specification, outputs, cache checks, and deterministic hashes are recorded under `Rev/docs/analysis-spec-reviewer-1-comment-2.md` and `data/exp/revision/reviewer-1-comment-2/`.

The official factors are formally retention fractions of the JMA landslide-warning criterion, which is defined on the joint 60-minute-rainfall and soil-water-index plane; they are not direct reductions of a scalar accumulated-rainfall threshold. Compatibility of the \(1/f_i\) transformation in Equation 4 was therefore tested before manuscript revision under the frozen specification `Rev/docs/analysis-spec-reviewer-2-comment-2.md`. The JMA-type comparator used the published three-tank equations and parameters, the official normal and temporary Level-4 grid curves dated 28 May and 30 July 2026, and the existing seven-station 2016–2020 event sample. Across 513,702 valid adjusted grid–rainfall cells, the median and 95th-percentile absolute relative errors between the published criterion multiplier and \(1/f_i\) were 0.0022 and 0.0054. Among 2,438 eligible events, the current adjusted index and the JMA-type utilization ratio had pooled Spearman ρ=0.862 (station-cluster bootstrap 95% interval 0.842–0.884), median within-station ρ=0.886, minimum within-station ρ=0.867, top-decile ROC AUC=0.990, median within-station top-decile overlap=0.861, and pooled station-scenario ρ=0.917 with no scenario-order inversion. All predeclared compatibility criteria passed, so Equation 4 is retained as a relative scenario index; it is not relabelled as the operational JMA indicator. The 30 July 2026 second report moved Kosa Town from 0.70 to 0.80, and all subsequent preprocessing and dependent outputs use 0.80.

The declared rainfall-window weights and rainfall-loading coefficient were then evaluated under the frozen Reviewer 2 Comment 4 specification rather than treated as fitted parameters. Five weight schemes (equal, short-duration gradient, antecedent-duration gradient, 1-hour only, and 72-hour only) were crossed with \(\gamma\in\{0.50,1.00,2.00\}\), producing 15 combinations and 45 scenario-specific slope and road surfaces. Relative to the equal-weight, \(\gamma=1.00\) central reference, the minimum road-rank Spearman correlation was 0.989 and the minimum top-1% road overlap was 0.879; every combination preserved Moderate \(\leq\) Heavy \(\leq\) Extreme ordering, and Heavy matched concordance ranged from 0.632 to 0.652. Road-priority stability therefore met the predeclared high-stability rule. Five preselected Heavy combinations were propagated through the same central candidate set, closure anchors, communities, Primary Emergency Road backbone, five seeds, and 1,000 draws per seed using common random numbers. The corrected central mean was 1,063.6 expected isolated residents, whereas the four boundary means ranged from 765.7 to 1,874.6 (0.720–1.763 times the central value). Consequence magnitude is therefore classified as parameter-sensitive even though relative road prioritization is highly stable. The equal-weight, \(\gamma=1.00\) setting remains a transparent central reference, not an empirically optimal model, and downstream reporting must distinguish robust priority ordering from uncertain consequence magnitude. Complete outputs and hashes are retained under `data/exp/revision/reviewer-2-comment-4/`.

The operational threshold effect was isolated in a second frozen paired analysis by setting \(f_i=1.00\) throughout the study area while retaining the same rainfall, terrain context, directional road transfer, official-Heavy candidate universe and closure anchors, network, service destinations, intervention assumptions, seeds, and draw counts. This all-area 100% case is a no-retention-adjustment model baseline, not a physical no-earthquake counterfactual. Official-threshold scores were no smaller than baseline scores for every supported slope cell and road section. Road-rank correlations between the two geographies were 0.995, 0.995, and 0.995 for Moderate, Heavy, and Extreme rainfall, with top-1% overlaps of 0.907, 0.879, and 0.859, respectively. Mean expected isolated population changed from 85.9 to 189.1 under Moderate rainfall, from 564.3 to 1,063.6 under Heavy rainfall, and from 3,455.4 to 4,217.8 under Extreme rainfall. Thus, the corrected official geography adds 499.3 expected isolated residents under Heavy rainfall, an 88.5% increase within the model. Heavy service-reachability losses changed from 272.8 to 609.9 residents for shelters, 596.2 to 1,286.7 for fire services, and 497.1 to 937.3 for municipal facilities; the conditional emergency-water result changed from 5,127.2 to 7,789.8. Current intervention priority scores had Spearman correlation 0.837 and 98.0% overlap among the top 150 roads; maximum-budget protected population was 39.5 under the no-retention baseline and 62.3 under the official geography. Intervention comparisons remain diagnostic until Batch D resolves the cost-effect and portfolio comments. Complete paired outputs and hashes are retained under `data/exp/revision/reviewer-2-comment-3/`.

### Terrain and Landslide Disruption Score

Terrain Slope and Terrain Curvature are derived from Elevation at native terrain resolution. Let \(Z_i\), \(S_i\), \(C_i\), and \(W_i\) denote standardized Elevation, Terrain Slope, absolute Terrain Curvature, and warning-zone exposure derived from Hazard Type and Geometry for cell \(i\). The transparent terrain-context score and Landslide Disruption Score are

\[
\eta_i=0.15Z_i+1.00S_i+0.35C_i+0.75W_i,
\]

\[
H_i^{(r,f)}=\operatorname{logit}^{-1}\left(\eta_i+\gamma\log X_i^{(r,f)}\right).
\]

Here, \(\eta_i\) is the transparent terrain-context score; \(\gamma=1.00\) is the declared rainfall-loading coefficient; and \(H_i^{(r,f)}\) is Landslide Disruption Score. The logarithm represents threshold retention and rainfall intensity as multiplicative loading changes and reduces inverse-logit saturation. The fixed weights, standardization sample, pseudo-background design, and fitted comparators are reported in full. \(H_i^{(r,f)}\) remains a relative score.

### Slope-to-Road Translation

For road section \(e\), Road Disruption Score is

\[
D_e^{(r,f)}=\frac{\sum_{i\in U_e}q_{ie}H_i^{(r,f)}}{\sum_{i\in U_e}q_{ie}}.
\]

Here, \(U_e\) is the upslope influence set for road section \(e\), \(q_{ie}\) is a nonnegative transfer weight based on Geometry, Elevation difference, distance, and terrain alignment between cell \(i\) and road section \(e\), and \(D_e^{(r,f)}\) is the normalized directional Road Disruption Score. Normalization prevents longer sections from receiving larger scores solely because they intersect more sampled cells. Road Category, Road Section Length (m), Emergency Route Membership, and Hazard Type enter matched validation and stratification rather than being interpreted as causal controls.

For physical restriction episode \(k\), let \(A_k\) contain its matched evidence sections and let \(B_a\) contain the fixed pseudo-background sections matched to evidence section \(a\). Equal-episode correspondence is

\[
C_{\mathrm{episode}}^{(r,f)}=\frac{1}{K}\sum_{k=1}^{K}\frac{1}{|A_k|}\sum_{a\in A_k}\frac{1}{|B_a|}\sum_{b\in B_a}\left[\mathbf{1}\!\left(D_a^{(r,f)}>D_b^{(r,f)}\right)+\frac{1}{2}\mathbf{1}\!\left(D_a^{(r,f)}=D_b^{(r,f)}\right)\right].
\]

Here, \(K\) is the number of physical episodes, \(A_k\) contains the evidence sections linked to episode \(k\), and \(B_a\) contains pseudo-background sections matched on municipality or ward, Road Category, Emergency Route Membership, and Road Section Length (m) decile. Each episode receives equal weight, ties contribute 0.5, and episode-cluster bootstrap intervals resample physical episodes rather than repeated snapshots or linked sections.

For Monte Carlo sensitivity setting \(b\), the score becomes a scenario closure propensity through a declared monotone mapping:

\[
p_{e,b}^{(r,f)}=g_b\left(D_e^{(r,f)}\right), \qquad F_{e,m}^{(r,f,b)}\sim\operatorname{Bernoulli}\left(p_{e,b}^{(r,f)}\right).
\]

Here, \(g_b\) is a declared low, central, or high monotone calibration function informed by restriction-ranking evidence and bounded scenario closure-rate assumptions; \(p_{e,b}^{(r,f)}\) is a scenario closure propensity; \(F_{e,m}^{(r,f,b)}\) indicates closure of road section \(e\) in draw \(m\). Observed restriction prevalence is not treated as the population road-failure rate, and the notation does not imply an empirically calibrated failure probability.

The central simulation draws section closures independently. A fixed-marginal spatial-dependence sensitivity instead defines, for dependence setting \(d\),

\[
Z_{e,m}^{(d)}=\sqrt{\rho_d}\,Z_{g_d(e),m}^{shared}+\sqrt{1-\rho_d}\,Z_{e,m}^{ind},
\qquad
F_{e,m}^{(r,f,b,d)}=\mathbf{1}\!\left[Z_{e,m}^{(d)}\leq\Phi^{-1}\!\left(p_{e,b}^{(r,f)}\right)\right].
\]

Candidate sections are assigned by projected midpoint to fixed 1 km or 3 km square clusters and tested at \(\rho_d=0.25\) and \(0.50\), alongside the independent \(\rho_d=0\) reference. Shared cluster shocks introduce positive within-cluster dependence while retaining every section's marginal closure propensity. The same section-specific random numbers are reused across settings and rainfall scenarios, while cluster shocks use separate deterministic streams. The scale and correlation settings are uncalibrated stress tests, not estimates of landslide footprints, common triggers, or empirical road-failure dependence.

### Community Isolation and Service Consequences

For seed replicate \(v\) and \(M=1000\) draws, Community Isolation Frequency is

\[
\widehat{P}_{iso,c,v}^{(r,f,b)}=\frac{1}{M}\sum_{m=1}^{M}I_{c,m,v}^{iso,(r,f,b)}.
\]

Here, \(I_{c,m,v}^{iso,(r,f,b)}\) equals one when Community ID \(c\) loses connection to every declared emergency-road-backbone target root in draw \(m\) of seed replicate \(v\), and \(\widehat{P}_{iso,c,v}^{(r,f,b)}\) is the replicate-specific Community Isolation Frequency. The primary target comprises all stable baseline roots containing at least one Primary Emergency Road node; a community is baseline-eligible only when its attachment reaches that backbone before disruption. The broader comparator adds roots containing Secondary Emergency Road nodes. The former coast-inclusive boundary search is retained only as a revision audit comparator because the unioned administrative boundary contains coastline and island shoreline and therefore cannot verify interprefectural road crossings. The primary, broader, and legacy definitions contain 2,562, 2,977, and 1,258 target roots, respectively. Under Heavy rainfall, the primary and broader definitions yield 1,063.6 and 992.7 expected isolated residents; their community-frequency Spearman correlation is 0.964 and top-30 population-burden overlap is 90.0%. Rainfall scenarios use common random numbers so ordered closure propensities generate ordered community frequencies.

For \(K=5\) predeclared independently seeded common-random-number sets, the reported frequency is

\[
\overline{P}_{iso,c}^{(r,f,b)}=\frac{1}{K}\sum_{v=1}^{K}\widehat{P}_{iso,c,v}^{(r,f,b)}.
\]

Here, \(K\) is the number of seed replicates and \(\overline{P}_{iso,c}^{(r,f,b)}\) is the five-seed mean Community Isolation Frequency. Monte Carlo uncertainty is summarized by the between-seed standard deviation and range of total Isolated Population, while 500-, 1,000-, and 2,000-draw convergence remains a separate computational check.

Isolated Population is

\[
\overline{N}_{iso}^{(r,f,b)}=\sum_c N_c\overline{P}_{iso,c}^{(r,f,b)}.
\]

Here, \(N_c\) is Total Population assigned to community \(c\), and \(\overline{N}_{iso}^{(r,f,b)}\) is five-seed mean expected Isolated Population. Equivalent sums use Population Age 65+, Population Age 75+, and Population Age 85+; replicate-specific totals provide the reported range.

For service class \(k\), class-specific Service Reachability Loss and Excess Travel Time are

\[
L_{c,k,v}^{service,(r,f,b)}=\widehat{P}_v\left(T_{c,k,v}^{(r,f,b)}=\infty\right),
\]

\[
\Delta T_{c,k,v}^{(r,f,b)}=T_{c,k,v}^{(r,f,b)}-T_{c,k}^{baseline}.
\]

Here, \(T_{c,k,v}^{(r,f,b)}\) is the shortest disrupted travel time from community \(c\) to any resolved, road-attached destination in class \(k\) and seed replicate \(v\); \(T_{c,k}^{baseline}\) is the baseline nearest-facility travel time; \(L_{c,k,v}^{service,(r,f,b)}\) is replicate-specific class-level Service Reachability Loss; and \(\Delta T_{c,k,v}^{(r,f,b)}\) is replicate-specific Excess Travel Time for reachable cases. Destinations are not fixed after disruption: every draw recomputes paths to the complete attached destination set, so a farther same-class facility may substitute. For each service outcome, the reported central estimate is the arithmetic mean across the same \(K=5\) predeclared seed replicates and the replicate minimum and maximum form the Monte Carlo range. No cross-service composite is calculated without human-approved decision weights. Each seed replicate uses 1,000 connectivity draws and 100 weighted rerouting draws on the complete road graph. Baseline-unreachable cases remain non-evaluable and are not converted to zero or assigned an arbitrary large travel time. Emergency-water results are reported only as conditional sensitivity results for the resolved destination set.

A paired common-random-number audit compares this primary any-same-class estimand with a restrictive fixed-baseline-destination continuity comparator under the Heavy scenario. Both branches use the same five seeds and 1,000 closure draws per seed. The any-same-class branch reproduces all 20 production seed-by-service arrays exactly; fixed loss is never below any-same-class loss; fixed loss minus any-same-class loss equals the rerouting-benefit indicator; baseline-unreachable communities remain non-evaluable; municipality totals reconcile within 0.001 person; and repeated output is byte-identical. Five-seed mean any-same-class versus fixed-destination affected populations are 609.9 versus 1,217.4 for shelters, 1,286.7 versus 7,106.4 for fire services, and 937.3 versus 2,811.3 for municipal facilities. Corresponding rerouting benefits are 49.9%, 81.9%, and 66.7% of fixed-destination losses. Emergency-water results remain conditional on 10 of 36 geolocated destinations and are reported separately in Appendix Table B9.

The Reviewer 1 Comment 1 emergency-water support audit freezes `data/processed/emergency_water_points_preprocessed.parquet`, does not impute coordinates, and classifies facility names reproducibly as school (`学校`), community centre (`コミセン` or `公民館`), government/disaster centre (`役所`, `振興局`, or `防災拠点`), or other. The 36 announcements comprise 28 in Yatsushiro City, six in Uki City, and two in Hikawa Town. Ten records (27.8%) have paired coordinates and `matched_exact_2012_facility` status; all ten are school-named Yatsushiro locations. The 26 unmatched records comprise 18 Yatsushiro, all six Uki, and both Hikawa announcements. Resolution by name class is 10/13 for schools, 0/14 for community centres, 0/8 for government/disaster centres, and 0/1 for other. Thus, only one of three source municipalities has a resolved routing destination and missing support is concentrated by municipality and name class rather than demonstrably uniform or random. Urban–rural missingness cannot be classified without coordinates. The emergency-water output therefore supports conditional network connectivity to the ten resolved, road-attached destinations only; it does not support prefecture-wide deployment, actual availability, operating-status, capacity, demand, or unresolved-site routing claims. The frozen specification is `Rev/docs/analysis-spec-reviewer-1-comment-1.md`; deterministic outputs and hashes are stored under `data/exp/revision/reviewer-1-comment-1/`.

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

Candidate roads are pre-screened with a transparent consequence proxy

\[
G_e=\Delta N_e^{single}+0.15B_e.
\]

Here, \(\Delta N_e^{single}\) is the population disconnected when road section \(e\) is
the only closed candidate section and \(B_e\) is the attachment-based community burden
adjacent to that section. A deterministic feasibility rule assigns one road-access action
\(a(e)\) to each candidate road. Priority Score is

\[
Q_e=\operatorname{median}_{b}\left[
\frac{G_e\rho_{a(e),b}}{Cost_{e,a(e),b}}
\right].
\]

Here, \(\rho_{a(e),b}\) is the assumed proportional effect of the assigned action under
sensitivity setting \(b\), \(Cost_{e,a(e),b}\) is its relative planning cost, and \(Q_e\)
is an assigned-action consequence-based screening score. It is not the simulated marginal
Protected Population of every possible action. Budget portfolios are assembled in \(Q_e\)
order with feasibility constraints and compared with hazard-only, Emergency Route
Membership-only, Road Category-only, and equal-cost consequence baselines under the same
sensitivity setting \(b\). Because the median low-central-high effect-cost ratio equals the
central ratio in the declared assumptions, the Central \(Q_e\) order is expected to equal
the Central equal-cost consequence order; this is reported as a consistency result rather
than incremental superiority. At the central setting, the modeled cost of a one-kilometre
road section is 5.0 relative planning units for temporary reinforcement, 2.0 for clearance
pre-positioning, and 3.7 for alternative-route protection; these anchors are not currency.
Road-access, information, life-safety, and service-continuity benefits are reported
separately and are not collapsed into one score without declared decision weights. Results
are screening priorities rather than engineering optima.

The intervention baseline, assigned-action portfolios, and all comparator portfolios use
five independently seeded common-random-number sets. Protected Population is reported as
the mean and range across seeds; ranking stability and selected-road overlap are reported
across the same seed sets. Community priority ranking uses Heavy-scenario expected isolated
Total Population as the primary key and expected isolated Population Age 65+ only as a
secondary key and separate vulnerability descriptor. No numeric age premium is added to
Total Population.

### Robustness, Heterogeneity, and Failure Modes

- Rainfall robustness compares the seven-station 2016-2020 and five-station 2016-2025 temporal supports and the Moderate, Heavy, and Extreme independent-event quantiles. The unresolved Yatsushiro assignment is separately bounded by municipality-wide 0.70 and 0.80 cases around the analyst midpoint of 0.75. Bounds are reported at the slope, road, isolation, and service-consequence stages; decision outputs are regenerated only if a material ranking or benefit change is detected.
- Terrain and road-transfer checks use an upslope influence set requiring positive Elevation difference and downhill alignment toward sampled road points, with distance decay and normalized directional mean aggregation. Comparisons include warning-zone exposure and low-central-high score-to-closure mappings.
- The central network screen allows the upper 15 percent of positive Heavy-scenario road scores to fail. Network robustness compares the Primary Emergency Road backbone with the broader Primary-plus-Secondary backbone, varies closure mappings, and evaluates \(M\) across 500, 1,000, and 2,000 draws using a common seed for the simulation-size comparison. The coast-inclusive boundary rule is retained only as an audit comparator. A separate fixed-marginal dependence analysis compares independent closures with 1 km and 3 km square clusters at \(\rho=0.25\) and \(0.50\) across all three rainfall scenarios, five seeds, and 1,000 draws per seed. Acceptance requires exact reproduction of the independent branch, small marginal-closure error and bias, and deterministic reruns. The validated broad-strong setting changes mean isolation by +9.2%, +16.0%, and −6.5% under Moderate, Heavy, and Extreme rainfall, respectively; dependence is therefore reported as a non-directional sensitivity bound.
- Vulnerability heterogeneity reports Total Population and age-specific populations separately and stratifies roads by Road Category and Emergency Route Membership.
- Intervention robustness varies Intervention Cost, assumed effectiveness, budget, and
  five Monte Carlo seed sets; each comparator is evaluated under the same cost-effect and
  seed setting, and rank correlations, selection overlap, and seed ranges accompany
  Priority Score. Central equality with the equal-cost consequence comparator is reported
  explicitly.
- Ablations compare the full framework with warning-zone-only, terrain-only, no-threshold-adjustment, hazard-only road ranking, and equal-cost intervention baselines.
- Failure modes include below-chance warning-zone validation, disagreement between fold AUC and held-out inventory capture, matched road concordance that does not exceed simple baselines, scenario rank correlation above 0.95, baseline-disconnected communities, unresolved service locations, non-converged simulation frequencies, or intervention gains that are immaterial relative to equal-cost consequence ranking.

## 7. Analytical Workflow

Interpretation limits are enforced through the support-status column: each workflow step may support only the stated scenario-conditional, relative-ranking, or bounded service claim, and any failed upstream quality gate restricts downstream evidence to partial support or inconclusive status.

| step | variables used | formula/model used | generated figure/table title | theory or claim evaluated | support status |
|---|---|---|---|---|---|
| Confirm analytical coverage and spatial support | Geometry, Observation Time, Station ID, Road Section ID, Network Node ID, Mesh Code, Total Population, Location Resolution Status | Study-area coverage, missingness, geometry validity, temporal range, population reconciliation, and baseline network checks | Analytical Data Coverage and Quality | Establishes whether the data chain is sufficiently complete for the central question | Supported for the principal analytical layers; DEM noncoverage within Kumamoto is 0.000212%, while unresolved facilities remain explicit and excluded from primary routing claims |
| Define rainfall and threshold scenarios | Observation Time, Hourly Rainfall, Cumulative Rainfall, Rainfall Scenario, Rainfall Threshold Retention Factor, Municipality or Subarea (Japanese), Latitude, Longitude | Independent-event maxima, event quantiles, coarse inverse-distance surface, \(X_i^{(r,f)}\), official resolved values, and Yatsushiro analyst-midpoint and bounding assignments | Rainfall History and Official Threshold Adjustment; Rainfall and Threshold Scenarios | Evaluates the declared post-earthquake threshold-adjustment mechanism for RQ1 | Supports ordered event-based loading magnitudes under declared station and threshold support; Yatsushiro is bounded rather than spatially resolved, and near-unity cross-scenario rank correlation precludes spatial reprioritization or a causal earthquake claim |
| Construct terrain context and landslide score | Elevation, Terrain Slope, Terrain Curvature, Hazard Type, Landslide Inventory ID, Landslide Size Class, Landslide Disruption Score | Transparent fixed weights, logarithmic rainfall loading, footprint-bounded historical alignment, and \(H_i^{(r,f)}\) | Terrain, Landslide Evidence, and Emergency Network Context; Official-Threshold-Adjusted Landslide Disruption Score | Tests whether the frozen terrain-context ranking aligns with interpreted landslide evidence without post-sequence warning-zone information | Partially supported as a transparent directional ranking: within the 57.8% GSI interpretation footprint and after restricting warning zones to 29,632 polygons designated by 2016-04-14, mean spatial AUC is 0.705 with 0.465 held-out top-quartile capture; incomplete centre-point evidence, unavailable disturbance depth, and fold variation preclude an occurrence-probability or cross-event validation claim |
| Evaluate slope-to-road correspondence | Road Section ID, Road Category, Road Section Length (m), Emergency Route Membership, Restriction Reason, Restriction Start Time, Matched Road Edge ID, Road Edge Match Distance (m), Road Disruption Score | Normalized directional aggregation \(D_e^{(r,f)}\), equal-episode correspondence \(C_{\mathrm{episode}}^{(r,f)}\), paired contrasts, and episode-cluster bootstrap | Road Disruption Scores and Earthquake-Proximate Restriction Correspondence; Road-Restriction Correspondence and Trigger Audit | Evaluates RQ2 and whether the directional ranking corresponds with the available road evidence beyond simple comparators | Partially supported as supplementary dry-event correspondence: Heavy episode-weighted concordance is 0.723, compared with 0.698 for road length and 0.545 for warning-zone exposure; both paired contrast intervals include zero, and the records do not validate rainfall triggering or closure probability |
| Define baseline communities and access targets | Community ID, Network Component ID, Mesh Code, Total Population, Population Age 65+, Population Age 75+, Population Age 85+, Network Analysis Eligible, Emergency Route Membership | Road-connected populated-mesh clustering, baseline reachability to every Primary Emergency Road root, broader Primary-plus-Secondary target sensitivity, and audit-only reconstruction of the former coast-inclusive boundary proxy | Community Isolation Frequency and Exposed Population; High-Isolation-Risk Communities | Establishes a defensible consequence unit for RQ3 | Supported for 4,346 communities, 62,291 meshes, and 1,728,644 residents; the broader-target Heavy estimate is 992.7 versus 1,063.6 centrally, with community-frequency Spearman correlation 0.964 and top-30 burden overlap 90.0% |
| Simulate road closures and isolation | Road Disruption Score, Community ID, Community Isolation Frequency, Isolated Population, Total Population, Population Age 65+, Population Age 75+, Population Age 85+ | Monotone closure mapping, independent Bernoulli disruption draws, fixed-marginal Gaussian-copula dependence sensitivity, five-seed mean \(\overline{P}_{iso,c}^{(r,f,b)}\) with \(M=1000\) per seed, 500-2,000 draw convergence, and Yatsushiro 0.70-0.80 bounds | Community Isolation Frequency and Exposed Population; Spatial Closure-Dependence Sensitivity; Municipality Isolation and Service-Loss Summary; High-Isolation-Risk Communities | Evaluates which communities and populations are repeatedly isolated under declared scenarios and whether spatial co-failure changes mean, tail, or local priority results | Supports conditional-frequency claims after convergence and exact independent reproduction; correlated settings preserve marginal closure propensities but change consequence magnitude and top-community membership, so independence is neither uniformly conservative nor uniformly anti-conservative |
| Estimate service consequences | Shelter ID, Evacuation Site ID, Water Point Name, Fire Facility Name, Facility Name, Baseline Edge Travel Time (min), Service Reachability Loss, Excess Travel Time | Five predeclared seed replicates, each with 1,000-draw any-same-class connectivity loss \(L_{c,k,v}^{service,(r,f,b)}\) and 100-draw full-network weighted rerouting \(\Delta T_{c,k,v}^{(r,f,b)}\); a paired common-random-number audit compares the primary estimand with fixed-baseline-destination continuity | Basic Service Reachability Loss; Service-Destination Estimand and Rerouting Comparison; Municipality Isolation and Service-Loss Summary | Evaluates the secondary RQ3 claim on basic-service loss and quantifies the effect of permitting same-class substitution | Partially supported for shelters, fire services, and municipal facilities after between-seed, Yatsushiro-bound, and paired destination-estimand checks; emergency water is conditional sensitivity evidence for the resolved destination set |
| Screen road and community interventions | Road Section ID, Emergency Route Membership, Road Category, Intervention Type, Intervention Cost, Avoided Isolation, Protected Population, Priority Score, Total Population, Population Age 65+ | Assigned-action consequence proxy \(G_e\), screening score \(Q_e\), budget constraint \(A_b(x)\), five-seed portfolio evaluation, and setting-matched comparator portfolios | Intervention Priorities and Budgeted Benefits; Priority Road Sections; Intervention Portfolios; Comparator Robustness | Evaluates RQ4 and whether assigned-action consequence screening is stable and auditable relative to simpler rules | Supports an assigned-action screening claim when seed stability is adequate; equality with equal-cost consequence ranking does not support incremental superiority |
| Integrate the full evidence chain | Elevation, Hourly Rainfall, Rainfall Threshold Retention Factor, Landslide Disruption Score, Road Disruption Score, Community Isolation Frequency, Service Reachability Loss, Priority Score | Linked scenario, validation, network simulation, and intervention framework | Compound-Hazard Decision Pathway | Evaluates the central compound-hazard decision question | Supported only when every upstream checkpoint is supported or transparently bounded; otherwise partially supported or inconclusive |

## 8. Figure and Table Plan

### Figures

| title | what it expresses | figure type | subpanels | key variables | status |
|---|---|---|---:|---|---|
| Compound-Hazard Decision Pathway | Links official post-earthquake threshold adjustment and rainfall exposure to slope disruption, road failure, community isolation, service loss, and intervention choice across the central question and all supporting questions. | flowchart | 1 | Elevation, Hourly Rainfall, Rainfall Threshold Retention Factor, Road Section ID, Total Population | done |
| Terrain, Landslide Evidence, and Emergency Network Context | Establishes the spatial evidence base for terrain, interpreted landslides, warning zones, roads, emergency routes, shelters, and water points. | map | 4 | Elevation, Landslide Inventory ID, Landslide Size Class, Hazard Type, Road Section ID, Emergency Route Membership, Shelter ID, Water Point Name, Geometry | done |
| Rainfall History and Official Threshold Adjustment | Shows station rainfall history, cumulative rainfall, Moderate, Heavy, and Extreme scenarios, official 70 percent and 80 percent threshold retention settings, and the explicitly analyst-defined 0.75 Yatsushiro midpoint with 0.70-0.80 bounds. | line + map | 4 | Observation Time, Hourly Rainfall, Station ID, Rainfall Threshold Retention Factor, Municipality or Subarea (Japanese), Cumulative Rainfall, Rainfall Scenario | done |
| Official-Threshold-Adjusted Landslide Disruption Score | Compares baseline and rainfall-scenario slope disruption scores using official resolved threshold values, the analyst-defined 0.75 Yatsushiro midpoint, and municipality-wide 0.70-0.80 Yatsushiro bounds while retaining score-based language. | map | 4 | Elevation, Landslide Inventory ID, Hazard Type, Rainfall Threshold Retention Factor, Terrain Slope, Terrain Curvature, Rainfall Scenario, Landslide Disruption Score | done |
| Road Disruption Scores and Earthquake-Proximate Restriction Correspondence | Maps road disruption exposure under rainfall scenarios and locates ten event-deduplicated dry, earthquake-proximate rockfall, slope-collapse, and sediment-inflow restriction episodes as supplementary terrain-to-road correspondence evidence. | map | 4 | Road Section ID, Road Category, Road Section Length (m), Emergency Route Membership, Restriction Reason, Restriction Start Time, Matched Road Edge ID, Road Disruption Score | done |
| Community Isolation Frequency and Exposed Population | Shows five-seed mean community isolation frequency and affected total and older populations, with between-seed ranges and propagated Yatsushiro threshold-assignment bounds. | map | 4 | Network Component ID, Mesh Code, Total Population, Population Age 65+, Population Age 75+, Geometry, Community ID, Community Isolation Frequency, Isolated Population | done |
| Basic Service Reachability Loss | Shows five-seed mean loss of reachability to every resolved, road-attached destination in each service class, together with between-seed ranges, Yatsushiro threshold-assignment bounds, and excess travel time to the nearest remaining same-class destination; emergency water remains conditional on the 10 of 36 geolocated destinations. | map + bar | 4 | Shelter ID, Evacuation Site ID, Water Point Name, Fire Facility Name, Facility Name, Baseline Edge Travel Time (min), Service Reachability Loss, Excess Travel Time | done |
| Intervention Priorities and Budgeted Benefits | Identifies assigned-action road priorities and total-population community priorities and shows how five-seed protected population changes with intervention budget under setting-matched cost-effect assumptions and comparator rankings. | map + line + bar | 4 | Road Section ID, Total Population, Population Age 65+, Emergency Route Membership, Intervention Type, Intervention Cost, Avoided Isolation, Protected Population, Priority Score | done |

### Tables

| title | what it expresses | rows | columns | row meaning | column meaning | status |
|---|---|---:|---:|---|---|---|
| Analytical Data Coverage and Quality | Documents completeness, temporal coverage, spatial support, and interpretation limits for each analytical layer. | 22 | 10 | One analytical data layer | Record count, spatial type, temporal coverage, missingness, location completeness, resolution, and calibration or validation role | done |
| Rainfall and Threshold Scenarios | Defines Moderate, Heavy, and Extreme event-based rainfall with official 70 percent and 80 percent retention settings and the analyst-defined 0.75 Yatsushiro midpoint and bounds. | 12 | 10 | One rainfall, threshold, or Yatsushiro spatial-support combination | One-hour, three-hour, 24-hour, and 72-hour event rainfall, threshold retention factor, spatial-support label, scenario label, and interpretation boundary | done |
| Hazard Validation | Compares the pre-specified transparent score and diagnostic alternatives using spatial validation. | 5 | 8 | One hazard-score specification | Spatial folds, AUC, inventory capture, ranking stability, and interpretation boundary | done |
| Road-Restriction Correspondence and Trigger Audit | Reports the snapshot-to-episode evidence funnel, ten-episode trigger audit, event-weighted road-score correspondence, paired comparator contrasts, and Yatsushiro threshold-assignment bounds. | 9 correspondence + 11 funnel + 10 episode | 6 / 2 / 10 | One score or contrast, one funnel stage, or one physical restriction episode | Equal-episode concordance, episode-cluster interval, trigger timing and rainfall evidence, matched sample, comparator contrast, and interpretation boundary | done |
| Baseline-Threshold Comparison and Rainfall-Parameter Sensitivity | Compares the no-retention-adjustment baseline with the corrected official-threshold geography and summarizes the prespecified rainfall-window-weight and gamma sensitivity analyses. | 12 | 7 | One threshold-geography or rainfall-parameter comparison outcome | Expected isolated population, service reachability loss, road-ranking stability, matched-evidence concordance, JMA-type compatibility, and explicit interpretation boundary | done |
| Spatial Closure-Dependence Sensitivity | Compares the independent closure reference with fixed-marginal 1 km and 3 km Gaussian-copula clusters at two dependence levels across all rainfall scenarios. | 15 | 12 | One rainfall-scenario and dependence-setting combination | Cluster scale and correlation, total and older expected isolated population, changes in mean and per-draw P95, community-rank correlation, top-30 overlap, and material frequency changes | done |
| Service-Destination Estimand and Rerouting Comparison | Compares the implemented any-same-class service-reachability estimand with a restrictive fixed-baseline-destination continuity comparator under identical Heavy-scenario closure draws. | 4 | 12 | One service class | Source coverage, road attachment, baseline eligibility, five-seed any-same-class and fixed-destination losses, rerouting benefit, benefit share, and number of communities benefiting | done |
| Municipality Isolation and Service-Loss Summary | Summarizes five-seed mean community isolation, exposed population, older population, class-specific service loss, and shelter-specific excess travel time for each administrative unit and scenario. | 49 | 16 | One municipality, ward, or comparable administrative unit | Isolation frequency, isolated population, older population, class-specific unreachable services, and shelter excess travel time under the Heavy scenario | done |
| Priority Road Sections | Lists the 30 road sections with the largest assigned-action consequence-based intervention relevance. | 30 | 12 | One road section | Municipality or ward, road category and length, disruption score, alternative scarcity, affected communities, total and older population, dependent services, assigned intervention, planning cost, and assigned-action screening score | done |
| High-Isolation-Risk Communities | Lists the 30 communities with the highest five-seed mean Heavy-scenario expected isolated Total Population, using expected isolated Population Age 65+ only as a secondary ranking key and separate descriptor. | 30 | 11 | One community | English municipality or ward, centroid coordinates, mesh count, total and older population, candidate connection sections, scenario isolation frequencies, expected isolated population, and principal service loss | done |
| Intervention Portfolios | Compares five-seed budget-feasible intervention portfolios and their protective benefits across cost-effect settings. | 21 | 10 | One budget and sensitivity-setting combination | Budget, selected roads, intervention mix, realized cost, protected communities, protected total and older population, avoided isolation share, unit-cost benefit, and selection overlap | done |
| Comparator Robustness | Compares the assigned-action consequence-based screening ranking with hazard-only, emergency-route-only, road-class-only, and equal-cost consequence baselines under matched cost-effect and seed settings. | 84 | 8 | One comparator, sensitivity setting, and budget combination | Setting, comparator, budget, selected roads, realized cost, protected population, avoided isolation share, and unit-cost benefit | done |

### Variable Coverage Check

All key variables referenced by the confirmed figures and tables appear in Section 4 and are marked as final analysis variables. Input features are constructed before estimation; model, simulation, and intervention variables are generated only within the corresponding analytical workflow steps.
