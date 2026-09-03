# Response to reviewers and editors of manuscript number [MANUSCRIPT ID]

# Revision Summary

Thanks for the editor and reviewers' careful review. We hereby resubmit a substantially revised version of our manuscript that addresses all points raised by the editor and reviewers.

The main changes in the revised manuscript are:

- [Revision summary item 1: describe the major manuscript-level change.]
- [Revision summary item 2: describe the major theoretical or conceptual change.]
- [Revision summary item 3: describe the major methodological or robustness-check change.]
- [Revision summary item 4: describe the major results, discussion, table, or figure change.]
- [Revision summary item 5: describe language polishing, consistency checks, or formatting changes.]

The revised manuscript also addresses the editor's and reviewers' other comments, and detailed responses to each reviewer follow.

Finally, we would like to express our sincere gratitude to the editor and reviewers. We hope that these changes meet your expectations, and we look forward to receiving your decision on the improved version of our manuscript.

# Editor

Reviewers have now commented on your paper. You will see that they are advising that you revise your manuscript. If you are prepared to undertake the work required, I would be pleased to reconsider my decision. 

If you decide to revise the work, please submit a list of changes or a rebuttal against each point which is being raised when you submit the revised manuscript.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

# Reviewer 1

## Comment 1

Reviewer 1: 1. Only 10 of the 36 announced emergency water points were geolocated and included in the routing network. The authors should expand on how this significant data gap restricts immediate operational planning.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 2

2. Due to unresolved subarea geometries, an analyst-defined midpoint of 0.75 was assigned. A brief sensitivity statement is needed to clarify if downstream connectivity consequences are highly sensitive to this assumption.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 3

3. The directional slope-to-road transfer approximates runout using basic terrain characteristics rather than a physical model. A sentence discussing the feasibility of integrating physical models in future iterations would add useful context.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 4

4. Because the central assigned-action ranking matches the simple equal-cost consequence baseline, the authors should clarify if any other heuristics or multi-criteria decision models were tested.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

# Reviewer 2

## Overall Comment

Reviewer 2: This paper presents an integrated framework for assessing post-earthquake rainfall-triggered landslide disruption and its consequences for communities and road networks. The study addresses a practically important problem and has potential value for disaster management. However, several substantial issues need to be adequately addressed before the manuscript can be considered for publication. The reviewer recommends that the authors address the following comments and revise the manuscript for resubmission.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 1

1. The literature review does not sufficiently establish the novelty of the proposed framework. Although previous studies are cited for individual analytical components, the manuscript does not clearly compare the proposed complete decision chain with existing integrated studies on landslide or hazard-induced road disruption, network accessibility, community isolation, and intervention prioritization. Please expand the literature review and clearly identify which elements of the proposed framework have not been addressed in previous studies.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 2

2. The direct application of the official threshold-retention factors of 0.80 and 0.70 to Equation 4 requires further justification. The official factors were established for warning criteria based on rainfall-related indicators that differ from the rainfall-loading index used in this study. Please use a consistent rainfall indicator or quantitatively demonstrate that the proposed index is compatible with the application of these factors.

**Response:**
Thank you for identifying the need to establish quantitative compatibility before applying the official retention factors. We now compare Equation 4 with a JMA-type reconstruction based on the published tank equations and Level-4 grid curves. Among 2,438 eligible independent rainfall events, the pooled Spearman correlation is 0.862 (station-cluster bootstrap 95% CI, 0.842–0.884); the minimum within-station correlation is 0.867, the top-decile ROC AUC is 0.990, and no scenario-order inversion occurs. Applying the 0.70 and 0.80 factors also reproduces the intended scale transformation with median and 95th-percentile absolute relative errors of 0.0022 and 0.0054 across 513,702 valid grid–rainfall cells. These results support retaining Equation 4 for directional scenario screening in the present event sample. We nevertheless keep it explicitly distinct from the operational JMA warning indicator because the reconstruction distributes archived hourly rainfall uniformly over six 10-min steps. The Methods, Discussion, and Appendix B now report this test and its interpretation boundary.

"The analysis assigns equal weights of 0.25 to the 1, 3, 24, and 72 h windows. The equal-weight choice is a transparent central reference rather than an empirically optimized parameterization. Compatibility was evaluated against a JMA-type reconstruction based on the published tank equations and Level-4 grid curves for 2,438 eligible events. The pooled Spearman correlation was 0.862 (station-cluster bootstrap 95% CI, 0.842–0.884), and applying the official factors produced median and 95th-percentile absolute relative errors of 0.0022 and 0.0054 across 513,702 valid grid–rainfall cells. All prespecified compatibility criteria were met; Equation 4 is therefore retained as a relative scenario index and is not relabelled as the operational JMA indicator."
(Pages 13–14, Lines 269–277)

"The quantitative comparison with the JMA-type reconstruction supports applying the official factors to Equation 4 for directional scenario screening in the present event sample, but it does not turn X or H into an operational warning indicator. Across the tested parameterizations, road-priority order is more stable than absolute isolation estimates; consequence magnitudes are therefore treated as scenario-sensitive."
(Pages 28–29, Lines 613–618)

## Comment 3

3. To clarify the effect of the earthquake, please add results assuming the baseline threshold (100%) throughout the study area and compare them with the results obtained using the official threshold-retention settings.

**Response:**
Thank you for this suggestion. We add an all-area 100% threshold case and compare it with the corrected official threshold-retention geography while holding rainfall, terrain, roads, network definitions, service destinations, simulation seeds, and Monte Carlo draws fixed. The all-area case is defined by f = 1.00, which switches off the temporary retention adjustment; it is not interpreted as a complete physical no-earthquake counterfactual. Appendix Table B5 shows that expected isolated population increases from 85.9 to 189.1 persons under Moderate rainfall, from 571.0 to 1,121.7 under Heavy rainfall, and from 4,121.7 to 5,032.2 under Extreme rainfall when the official geography is applied. Under Heavy rainfall, expected reachability losses increase from 272.8 to 609.9 persons for shelters, from 596.2 to 1,286.7 for fire services, and from 497.1 to 937.3 for municipal facilities. The Heavy road-score ordering remains similar between the two threshold geographies (Spearman correlation, 0.995; top-1% overlap, 0.879). We therefore interpret the official retention settings as changing consequence magnitude more strongly than spatial road ordering within the present model.

"For the paired comparison, f = 1.00 is assigned throughout Kumamoto to disable threshold retention while holding rainfall, terrain, road, network, service, and simulation inputs fixed. This is a no-retention-adjustment model baseline, not a physical no-earthquake counterfactual."
(Page 12, Lines 245–248)

## Comment 4

4. The parameter settings used to construct the landslide disruption score require further justification for the study area. In particular, please justify the equal weights assigned to the 1-, 3-, 24-, and 72-h rainfall windows and the declared rainfall coefficient of 1.00 using evidence applicable to the study area or appropriate sensitivity analyses.

**Response:**
Thank you for this comment. We agree that the equal rainfall-window weights and γ = 1.00 are declared parameters rather than locally estimated coefficients. The revised Methods therefore identify the equal-weight, γ = 1.00 specification as a transparent central reference rather than an empirical optimum. We add a sensitivity analysis crossing five window-weight schemes—equal, short-duration gradient, long-duration gradient, 1-h only, and 72-h only—with γ values of 0.50, 1.00, and 2.00. Across the resulting 15 combinations and three rainfall scenarios, all scenario orders remain stable, the minimum road-ranking Spearman correlation with the central specification is 0.989, and the minimum top-1% overlap is 0.879. Matched road-evidence concordance varies only from 0.632 to 0.652. Absolute community consequences are less stable: Heavy expected isolated population ranges from 786.2 to 2,135.9 persons, or 0.701–1.904 times the central estimate of 1,121.7. We now distinguish this high stability in road prioritization from the sensitivity of absolute consequence magnitude, and Appendix Table B5 reports the complete comparison.

"Sensitivity analyses use γ = 0.50 and 2.00 around this central value under five rainfall-window weighting schemes; γ = 1.00 is therefore a declared transparent reference rather than an estimated local coefficient."
(Page 14, Lines 294–296)

"The implemented checks vary rainfall temporal support, five rainfall-window weighting schemes, γ = 0.50, 1.00, and 2.00, the all-area f = 1.00 baseline, the unresolved Yatsushiro threshold assignment, external-road targets, closure mappings, simulation size, intervention costs and effects, and ranking comparators."
(Page 21, Lines 443–446)

"The paired all-area f = 1.00 comparison and the 15-combination rainfall-parameter sensitivity are reported in Appendix Table B5. Official retention changes downstream consequence magnitude more strongly than road ordering, while alternative window weights and γ values leave road rankings stable but produce wider variation in expected isolation."
(Page 23, Lines 486–490)

## Comment 5

5. The directional slope-to-road translation requires further methodological justification. Please clarify the criteria and parameter settings used to define the influence set and transfer weight in Equation 7, and justify their applicability to the study area.

**Response:**
Thank you for highlighting the need to make the directional slope-to-road translation reproducible and locally interpretable. The revised Methods now reports the road-sampling fractions, grid scale, influence-set neighborhood, relief and alignment criteria, angular and distance equivalents, and the complete distance–alignment–relief weighting rule. We also added a prespecified 15-specification sensitivity analysis, matched road-restriction correspondence, and strict-to-permissive downstream bounds in Appendix Tables B6a, B6b, and B7. The revised text now distinguishes evidence of directional applicability in Kumamoto from calibration of a physical runout model: the matched restriction comparison supports a persistent ranking signal, while the sensitivity results show that neighborhood reach and relief criteria materially affect exact priorities and consequence magnitude.

"For sample point j, influence set Uej contains every noncentral offset with dx and dy in [−3, 3] for which the candidate cell is at least 10 m above the road point and the cosine alignment between the local upslope gradient and the road-to-cell vector is at least 0.20. These settings correspond to an angular tolerance of 78.5° in raster-coordinate space, axis-aligned reaches of approximately 432–509 m, and a maximum diagonal reach of approximately 668 m. Transfer weight qij multiplies an exponential distance term with a 2.5-cell e-folding length, alignment clipped to [0, 1], and a relief term clipped to [0.20, 1.00] after division by 100 m."
(Page 16, Lines 329–336)

"Across the 15 prespecified transfer specifications, the minimum Spearman correlation on the union of supported roads was 0.676, the minimum top-1% overlap was 0.428, and the minimum overlap of Heavy candidate sets was 0.764. Neighborhood reach and minimum relief changed road support and exact top-ranked membership most strongly, whereas alignment, distance decay, relief scaling, and road-sampling alternatives were more stable individually. Matched road-evidence concordance ranged from 0.614 to 0.687 and remained above 0.50 under every specification. The restriction evidence therefore supports a persistent directional ranking signal, but not parameter-invariant identification of the exact highest-ranked roads."
(Page 25, Lines 527–535)

"Reconstructing the candidate-road set and closure mapping for the strict and permissive transfer boundaries changes Heavy expected isolation to 523.5 and 2,256.3 residents, respectively, compared with 1,121.7 centrally."
(Page 26, Lines 555–557)

"Across the strict and permissive transfer boundaries, the corresponding ranges are 264.6–1,303.9, 799.8–3,433.9, and 480.6–1,698.5 residents. These primary comparisons show that destination geography, network alternatives, and slope-to-road transfer assumptions shape service consequences beyond external-road isolation."
(Page 27, Lines 571–575)

"Slope-to-road transfer approximates runout through relief, alignment, and distance on an approximately 150 m screening grid rather than through a calibrated physical runout model. Its neighborhood and relief settings materially affect road support, exact top-ranked membership, and downstream consequence magnitude; the central specification is therefore a transparent reference rather than an optimized local model."
(Page 34, Lines 737–741)

## Comment 6

6. The assumptions used in the intervention analysis require further justification. Please provide the basis for the intervention effectiveness, relative planning costs, and the coefficient of 0.15 in Equation 17, preferably using engineering evidence or previous studies applicable to the study area.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 7

7. The road-disruption validation requires clearer identification of the triggering mechanism of the restriction records. The retained records include rockfall, slope collapse, landslide, and sediment inflow shortly after the earthquake, although it is unclear whether these disruptions were rainfall-triggered or directly earthquake-induced. Please clarify the triggering conditions and demonstrate that the selected records are appropriate for validating rainfall-triggered road disruption.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 8

8. The service-accessibility analysis fixes the nearest baseline facility as the destination after disruption. Please discuss how this assumption affects the interpretation of service loss in cases where another facility of the same service class remains reachable.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 9

9. The relationship between Equation 15 and the ranking procedure in Equations 16-17 is unclear. Please explain how the intervention portfolio is selected under the budget constraint and clarify whether Equation 15 is explicitly optimized or whether portfolios are constructed from the screening ranking. The methodological description and terminology should be consistent with the implemented procedure.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 10

10. The numerical values reported in the Highlights are inconsistent with those in the Abstract and Results. Please correct these values and confirm numerical consistency throughout the manuscript.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

# Reviewer 3

## Overall Comment

Reviewer 3: Major revision is recommended. The manuscript presents a relevant and potentially useful framework linking post-earthquake rainfall-threshold adjustment, landslide disruption, road-network failure, community isolation, service accessibility, and intervention priorities; however, several methodological issues must be addressed before the results can be considered reliable.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 1

First, "earthquake-adjusted" is potentially misleading because the model does not include ground motion, earthquake damage, or measured changes in slope strength, but only operational reductions in rainfall-warning thresholds.

**Response:**
Thank you for highlighting this terminology issue. We agree that “earthquake-adjusted” could imply a physical earthquake-effect model. We therefore replace that term in the title, keywords, Results heading, conclusion, and Figure 1 with language that identifies the analysis as an operational post-earthquake rainfall-warning threshold scenario. The Abstract now explicitly states that the model does not include ground motion, earthquake damage, or measured changes in slope strength. The revised text reads:

"Post-earthquake rainfall-warning threshold scenarios for landslide-related road disruption, community isolation, and emergency intervention planning in Kumamoto Prefecture, Japan"
(Page 1, Lines 2–5)

"Here, post-earthquake adjustment denotes area-level operational retention of rainfall-warning criteria, not a model of ground motion, earthquake damage, or measured changes in slope strength."
(Page 1, Lines 9–11)

"Compound hazards; Post-earthquake rainfall-warning criteria; Landslide disruption; Road networks; Community isolation; Service accessibility"
(Page 2, Lines 28–29)

"Operational Threshold Retention and Slope Disruption"
(Page 23, Line 482)

"Under the post-earthquake rainfall-warning threshold scenarios, the framework identifies where relative slope disruption may affect roads, where those road disruptions may isolate communities or remove basic-service access, and which road or community actions have the greatest conditional planning benefit."
(Page 34, Lines 732–735)

## Comment 2

Second, many influential parameters—including terrain weights, equal rainfall-duration weights, the rainfall coefficient, score-to-closure functions, intervention effectiveness, relative costs, and the 0.15 consequence coefficient—are assumed without sufficient justification or comprehensive uncertainty analysis.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 3

Third, road rankings are almost identical across rainfall scenarios, with correlations of 0.999-1.000, indicating that rainfall severity changes score magnitude but provides virtually no spatial reprioritization; this substantially weakens the central scenario-based claim.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 4

The landslide validation performance is only moderate (AUC = 0.665), while the road validation contains only 94 evidence cases and does not clearly demonstrate statistically significant improvement over the road-length comparator.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 5

The independent Bernoulli closure assumption also neglects spatially correlated failures caused by the same rainfall event or landslide process.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 6

In addition, defining isolation through connection to prefectural-boundary gateways requires stronger operational justification, and service loss should allow communities to reroute to alternative facilities rather than only assessing access to the baseline nearest destination.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 7

The intervention analysis relies on hypothetical costs and effects, and the Central ranking is identical to the equal-cost consequence benchmark, so no incremental optimization advantage has been demonstrated.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 8

Finally, the Highlights report 12,000 isolated residents and 3,000 elderly residents, whereas the abstract and main text report approximately 1,107 and 603, respectively; all numerical results must therefore be comprehensively checked. These issues require substantial methodological clarification, additional sensitivity analyses, possible recalculation of the network and service-access results, and more cautious interpretation of the operational implications.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

# Reviewer 4

## Overall Comment

Reviewer 4: This paper proposes a composite disaster framework that couples post-earthquake rainfall threshold adjustment, landslide susceptibility assessment, and road network accessibility analysis, applying it as a case study in Kumamoto Prefecture. The core contribution lies in extending the traditional "slope-based hazard evaluation" to a "network-dependent consequence assessment," emphasizing that road criticality depends not only on upslope exposure but also on its role as a bottleneck within the network topology. This approach holds clear practical value for disaster emergency planning. However, this version of the paper has the following issues requiring resolution:

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 1

1. The 2016 landslide inventory is used solely for validating historical slope rankings, while the 2026 restricted records are employed for road ranking validation. Please further discuss the comparability of these two events in terms of earthquake magnitude, rainfall patterns, and soil disturbance depth, and clarify why the spatial distribution of 2016 landslides remains suitable for validating 2026 slope susceptibility scores.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 2

2. In Equation 7, the transfer weight qie is described as "decreasing with distance," but no specific functional form (e.g., exponential decay, power-law, or threshold distance) is provided. Additionally, the criteria for determining "downslope alignment" (e.g., tolerance angle between flow direction and road orientation) remain unspecified. Please provide the explicit mathematical expression for qie, the algorithm for extracting the upslope influence set Ue, including angular tolerance, and whether this transfer method has been independently validated (e.g., by comparing predicted landslide deposit extents with observed data).

**Response:**
Thank you for identifying this gap. We revised the Directional Slope-to-Road Translation subsection to define the component-level sample index, the upslope influence set, the relief and cosine-alignment filters, the 78.5° angular tolerance, the exponential distance decay, and the section-level aggregation explicitly. Equation 7 now presents the complete implemented formulation, including the union of sample-point influence sets and the normalized weighted road score. We also corrected the Appendix cross-references to Tables B6a, B6b, and B7. Regarding validation, we now distinguish road-level ranking correspondence on a separate restriction dataset from physical runout validation. The available GSI inventory contains interpreted points rather than deposit polygons, so it cannot independently validate deposit extent or runout geometry. We state this limitation directly and identify the event-specific source, deposit, material, and independent footprint data needed for a future physically based model.

"With j indexing the component-level sample points described above, the aggregated transfer weight qie sums, over every eligible j, the product of an exponential distance term with a 2.5-cell e-folding length, alignment clipped to [0, 1], and a relief term clipped to [0.20, 1.00] after division by 100 m."
(Page 16, Lines 334–337)

Equation 7 (mathematical transcription):
$$
\begin{gathered}
\Delta z_{ije}=z_i-z_{je},\qquad d_{ije}=\lVert\mathbf{o}_{ije}\rVert_2,\qquad a_{ije}=\frac{\nabla z_i^{\mathsf T}\mathbf{o}_{ije}}{\max\!\left(\lVert\nabla z_i\rVert_2d_{ije},10^{-6}\right)},\\
U_{ej}=\left\{i:\mathbf{o}_{ije}=(d_x,d_y),\ d_x,d_y\in\{-3,\ldots,3\},\ (d_x,d_y)\ne(0,0),\ \Delta z_{ije}\ge10,\ a_{ije}\ge0.20\right\},\\
U_e=\bigcup_{j\in J_e}U_{ej},\\
q_{ie}=\sum_{j:i\in U_{ej}}\exp\!\left(-\frac{d_{ije}}{2.5}\right)\operatorname{clip}(a_{ije},0,1)\operatorname{clip}\!\left(\frac{\Delta z_{ije}}{100},0.20,1.00\right),\\
D_e^{(r,f)}=\begin{cases}\displaystyle\frac{\sum_{i\in U_e}q_{ie}H_i^{(r,f)}}{\sum_{i\in U_e}q_{ie}}, & \sum_{i\in U_e}q_{ie}>0,\\0, & \text{otherwise}.\end{cases}
\end{gathered}
$$
(Page 17, Line 346)

"The matched restriction comparison evaluates road-level ranking correspondence; it does not independently validate landslide-deposit extent or physical runout geometry, because the available GSI inventory comprises 1,044 interpreted point locations rather than mapped deposit polygons."
(Page 26, Lines 545–548)

"The framework uses readable score construction, spatially separated slope validation, road-restriction correspondence on a separate infrastructure dataset, ordered common-random-number simulations, age-specific population consequences, and comparator portfolios."
(Page 34, Lines 729–732)

"A physically based runout model could replace the directional transfer approximation once event-specific source and deposit polygons, material or rheological parameters, and independent footprint or road-impact observations are available for calibration and validation; blockage-duration and repair-time models could then distinguish short interruption from prolonged isolation."
(Pages 35–36, Lines 766–770)

## Comment 3

3. The implication of the overlap between "central assigned-action ranking" and "equal-cost consequence ranking" is a key finding: the complex consequence-aware screening framework does not outperform the simple equal-cost consequence baseline. The paper downplays this as merely "no incremental superiority established," which actually undermines the framework's practical utility. It is recommended to conduct an in-depth analysis of why the two rankings coincide—could it be due to overly simplified cost assumptions or the linear structure of the consequence proxy Ge? ； Discuss under what conditions (e.g., nonlinear costs, multi-objective optimization) this framework might demonstrate relative advantages.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 4

4. Under heavy rainfall, alternative closure mappings produce an isolated population range of 343-2,309, spanning nearly a sevenfold difference. Does this substantial uncertainty imply limited guidance value for policy-making from the current framework? How should emergency managers interpret such a wide range? Should conservative planning adopt "worst-case" mapping scenarios, or should priority be given to data collection to reduce mapping uncertainty?

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 5

5. Only 10 out of 36 announced water supply points were geolocatable, leading to results for this service category (7,969 affected people) being labeled as "conditionally sensitive evidence." Given that water supply is a lifeline infrastructure, does such a high rate of missing data undermine the reliability of the paper's core conclusion—namely, "loss of service accessibility"? Please clarify whether the 26 missing points are systematically biased toward certain areas (e.g., rural or urban). If we assume these missing points are uniformly distributed, would this significantly alter the relative rankings of fire services or municipal facilities?

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)

## Comment 6

6. The threshold retention factors of 0.80 and 0.70 are explicitly defined as "operational scenario settings" rather than physical measurements, which is commendable. However, the paper also states that these settings "inform more than a revised hazard map." If these factors are purely administrative operational parameters, how does the paper ensure their transferability across other earthquake events or different counties? Is it recommended that future research replace these administrative coefficients with field shear strength tests or InSAR deformation data?

**Response:**
Thank you for this important comment. We agree that the Kumamoto retention values themselves should not be transferred to another earthquake or jurisdiction. We revised the Study Area and Data, Discussion, and Conclusions to distinguish the transferability of the framework from the portability of its upstream coefficients. Application elsewhere now requires locally supported retention settings, a compatible rainfall indicator, and renewed checks before downstream interpretation. We also clarify that InSAR and geotechnical measurements are complementary evidence: where coverage and calibration are adequate, they can support a physical disturbance model that replaces the administrative proxy rather than serving as direct one-for-one substitutes for an operational coefficient.

"The numerical values are event- and area-specific and are not transferred to another earthquake or jurisdiction. Applying the framework elsewhere requires locally issued or empirically estimated retention settings, a rainfall indicator compatible with how those settings were defined, and renewed compatibility and sensitivity checks before downstream consequences are interpreted."
(Page 8, Lines 150–154)

"Repeated InSAR deformation observations and targeted geotechnical measurements, including field shear-strength tests, could support a spatially explicit disturbance model where coverage and calibration are adequate. These data are complementary evidence rather than one-for-one substitutes for an operational warning coefficient; once validated, such a physical model could replace the administrative retention proxy at the susceptibility stage while the downstream road-network and consequence modules remain applicable."
(Pages 33–34, Lines 724–730)

"Within the event and area for which they are issued, official threshold adjustments can therefore inform more than a revised hazard map: they can support a consistent comparison of inspection targets, access-protection candidates, community preparedness needs, and resource-pre-positioning priorities before heavy rainfall."
(Pages 34–35, Lines 749–753)

## Comment 7

7. The Highlights state that "Heavy rainfall isolated 12,000 residents, including 3,000 elderly," but the abstract and results sections report 1,107 people (including 603 aged 65 and above) under heavy rainfall. There is nearly an 11-fold discrepancy between 12,000 and 1,107. Please verify and reconcile this data inconsistency.

**Response:**
[Response to be completed after the revision is verified.]

"[Exact revised manuscript text]"
(Page XX, Lines XX–XX)
