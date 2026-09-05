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
Thank you for this comment. We audited all 36 announced emergency-water destinations by municipality, name class, coordinate completeness, and location-resolution status. The revised Data section now shows that the ten resolved destinations are concentrated in Yatsushiro and are all school-named exact matches to the retained 2012 facility register, while every announced point in Uki and Hikawa remains outside the routing denominator. We also expanded the limitations section and Appendix to state explicitly that this conditional result cannot support prefecture-wide deployment, cross-municipality comparison, or conclusions about water availability, operating status, capacity, demand, or routes to unresolved sites. We did not impute missing coordinates; instead, the result is now framed as connectivity to the ten observed destinations and as evidence that location and operational data must be completed before site-level planning.

"The emergency-water source contains 36 announcements from Yatsushiro City (28), Uki City (6), and Hikawa Town (2). Only 10 records (27.8%) have resolved coordinates; all are Yatsushiro school-named locations matched exactly to the retained 2012 facility register, whereas 18 Yatsushiro, six Uki, and two Hikawa announcements remain unmatched. Consequently, the routing denominator represents only one of the three source municipalities and is not a complete prefecture-wide emergency-water inventory."
(Page 10, Lines 208–214)

"In particular, the emergency-water coverage gap prevents immediate site-level operational interpretation of that service result. The model cannot represent routes to the announced water points in Uki or Hikawa, compare municipalities on a common destination inventory, or evaluate water availability, operating status, capacity, demand, or access to unresolved sites. The emergency-water result therefore describes conditional connectivity to ten observed destinations and should guide completion and verification of location and operational data rather than prefecture-wide deployment decisions."
(Pages 41–42, Lines 900–907)

"The emergency-water subset is geographically and institutionally concentrated. The 10 resolved records are Yatsushiro school-named locations matched exactly to the retained 2012 facility register; the unresolved records comprise 18 of 28 Yatsushiro announcements, all six Uki announcements, and both Hikawa announcements. By name class, resolution is 10/13 for schools and 0/14, 0/8, and 0/1 for community centres, government/disaster centres, and other locations, respectively. These counts establish non-uniform data support but cannot identify urban–rural missingness without coordinates."
(Appendix, Pages 1–2, Lines 22–28)

## Comment 2

2. Due to unresolved subarea geometries, an analyst-defined midpoint of 0.75 was assigned. A brief sensitivity statement is needed to clarify if downstream connectivity consequences are highly sensitive to this assumption.

**Response:**
Thank you for this comment. We evaluated municipality-wide Yatsushiro assignments of 0.70 and 0.80 around the analyst-defined 0.75 midpoint while retaining the current Primary Emergency Road backbone, Heavy rainfall scenario, five simulation seeds, and current service-routing specification. The bounds change the Heavy disconnected-population estimate by −4.4% to +5.2%, while community-frequency rank correlations remain 0.989–1.000 and Top-30 burden overlap remains 93.3%. Across shelters, fire services, and municipal facilities, affected-population changes remain within −6.5% to +8.0%, with frequency rank correlations of 0.990–1.000 and Top-30 overlap of 86.7%–93.3%. We therefore added the requested sensitivity statement, synchronized the service results and Figure 7, and retained the explicit limitation that 0.75 is an analyst-defined midpoint rather than an official municipality-wide value.

"Municipality-wide Yatsushiro assignments of 0.70 and 0.80 bound the Heavy result at 1,016.6–1,118.7 residents (−4.4% to +5.2% relative to the 0.75 midpoint), with community-frequency rank correlations of 0.989–1.000 and 93.3% Top-30 population-burden overlap. The midpoint assumption therefore changes consequence magnitude modestly without materially changing the community-priority pattern within the tested bounds."
(Page 29, Lines 631–636)

"Municipality-wide Yatsushiro assignments of 0.70 and 0.80 bound affected populations at 570.5–657.0 for shelters, 1,215.1–1,389.7 for fire services, 898.6–984.2 for municipal facilities, and 7,582.5–8,238.8 for emergency water. Relative to the 0.75 midpoint, changes remain within −6.5% to +8.0% across the three primary service classes; frequency rank correlations are 0.990–1.000 and Top-30 burden overlap is 86.7%–93.3%."
(Page 32, Lines 690–694)

"Figure 7. Basic-service reachability loss under road disruption"
(Page 51, Line 48)

## Comment 3

3. The directional slope-to-road transfer approximates runout using basic terrain characteristics rather than a physical model. A sentence discussing the feasibility of integrating physical models in future iterations would add useful context.

**Response:**
Thank you for this suggestion. The revised Discussion, under “Strengths, Limitations, and Future Research,” explains how a physically based runout model could replace the directional transfer approximation when event-specific source and deposit mapping, material parameters, and independent observations support calibration and validation. It also identifies blockage-duration and repair-time modeling as a subsequent extension. These are future developments, not capabilities demonstrated by the current screening model. The revised sentence states:

"A physically based runout model could replace the directional transfer approximation once event-specific source and deposit polygons, material or rheological parameters, and independent footprint or road-impact observations are available for calibration and validation; blockage-duration and repair-time models could then distinguish short interruption from prolonged isolation."
(Page 49, Lines 1083–1087)

## Comment 4

4. Because the central assigned-action ranking matches the simple equal-cost consequence baseline, the authors should clarify if any other heuristics or multi-criteria decision models were tested.

**Response:**
Thank you for this important comment. We clarify that the comparison already includes four prespecified heuristic rules: hazard-only; Emergency Route Membership-first with Road Disruption Score as a tie-breaker; Road Category-first with Road Disruption Score as a tie-breaker; and equal-cost consequence ranking. We did not test a formal multi-criteria decision model. A deterministic audit confirms that the Central assigned-action and equal-cost consequence rankings are identical at all seven tested budgets because, for each assigned action, the median low-central-high effect-to-cost ratio used by the assigned-action score equals its Central ratio. We now report this structural reason directly and interpret the result as support for transparent consequence screening rather than superiority over the equivalent simple comparator. We also explain that adding a post hoc multi-criteria model without stakeholder-elicited weights or a validated cross-criterion utility function would introduce an unsupported ranking assumption. The Methods, Results, Discussion, and Appendix have been revised accordingly.

"Intervention portfolios are compared with four prespecified heuristics under matched cost-effect settings: hazard-only; Emergency Route Membership-first with Road Disruption Score as a tie-breaker; Road Category-first with Road Disruption Score as a tie-breaker; and equal-cost consequence ranking. No formal multi-criteria decision model was tested because neither stakeholder-elicited criterion weights nor a validated cross-criterion utility function was available."
(Page 27, Lines 577–582)

"The Central equality holds at all seven tested budgets because, for each assigned action, the median low-central-high effect-to-cost ratio in Equation 16 equals its Central ratio."
(Page 36, Lines 783–785)

"Because the Central assigned-action ranking is identical to the equal-cost consequence comparator, the analytical gain lies in traceable consequence and action assignment rather than demonstrated optimization superiority. We did not add a post hoc multi-criteria decision model because unelicited weights for hazard, network dependence, vulnerable-population protection, service continuity, and cost would create another unsupported ranking assumption. Such a model is appropriate only after decision-makers define those trade-offs. The screening score does not certify an intervention or guarantee continued access."
(Pages 42–43, Lines 932–939)

"The comparator labels denote four fixed heuristics. Hazard only ranks Road Disruption Score; emergency route only and road class only prioritize the named binary or class criterion and use Road Disruption Score to break ties; equal-cost consequence ranks the same consequence-effect-to-cost ratio under each setting. Under the declared action effects and global cost multipliers, the median ratio used by the assigned-action score equals the Central ratio for all three actions, so the two Central orders and all seven budget rows are identical. No formal multi-criteria decision model was tested because the study did not have stakeholder-elicited criterion weights or a validated cross-criterion utility function."
(Appendix, Pages 10–11, Lines 188–196)

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
Thank you for requesting a clearer comparison with existing integrated studies. The revised Introduction compares five precedents spanning compound slope hazards, landslide-related road damage, critical-facility accessibility, population-centered service access, and budget-constrained intervention planning, and the Discussion states the resulting contribution consistently. We explicitly acknowledge that hazard-to-accessibility integration and consequence-based intervention planning already exist. Our contribution is the joint application of official post-earthquake warning settings, directional slope-to-road screening, emergency-road-backbone disconnection, age-structured exposure, and distinct service-access outcomes to complementary road and community preparedness priorities. We therefore identify the specific combination and decision context of this application rather than claim that each component, or hazard-to-intervention integration itself, is unprecedented.

"Existing studies already connect several of these stages. Lashgari et al. (2025) integrate sequential seismic and precipitation effects in a compound slope-hazard framework, while Donnini et al. (2017) connect rainfall-landslide inventories to road damage and restoration costs. Mager Pozo et al. (2025) combine hazard maps and network analysis to quantify loss of access roads to critical facilities. From a population-centered perspective, Tariverdi et al. (2023) link disaster scenarios, including compound shocks, to service-provider choices, infrastructure criticality, and targeted resilience measures. Hu et al. (2021) extend integration to budget-constrained retrofit decisions through a chain of cyclone hazard, roadside-tree fragility, economic and network consequences, and investment optimization. Thus, neither hazard-to-accessibility integration nor consequence-based intervention planning is new in itself. Building on these precedents, our application combines official post-earthquake rainfall-warning settings with directional slope-to-road screening, community disconnection from an emergency-road backbone, age-structured exposure and separate service-access outcomes. It carries these conditional consequences into budget-feasible road screening and a separate assessment of residual community preparedness needs, while distinguishing ranking evidence from assumptions about closure and intervention effects."
(Pages 4–5, Lines 77–93)

"The contribution is thus the joint translation of official post-earthquake warning settings into community isolation, distinct service-access outcomes, and complementary road and community preparedness priorities, while retaining explicit limits on probability, causality, and engineering interpretation."
(Pages 5–6, Lines 104–107)

"The main contribution is therefore an evidence-bounded decision chain that translates official warning scenarios into differentiated road and community preparedness priorities, rather than a new landslide-probability model or a claim that hazard-to-intervention integration is unprecedented."
(Page 40, Lines 867–870)

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
Thank you for this important comment. We agree that the exact intervention-effect values, relative planning costs, and the coefficient in Equation 17 were previously under-disclosed and could not be presented as locally calibrated engineering parameters. The revised Methods now distinguishes the mechanisms represented by the three action categories, cites Japanese official road-slope guidance only for inspection, risk-based prioritization, and site-specific countermeasure assessment, and explicitly states that the guidance does not support the numerical assumptions. We disclose the complete Conservative/Central/Optimistic effect matrix; the three Central length-based cost functions and their one-kilometre anchors; and the status of 0.15 as an analyst-set supporting weight. We also added a one-family-at-a-time sensitivity analysis under a fixed Heavy-scenario budget and matched simulation seeds, reported in Appendix Table B13. The analysis shows that effect assumptions govern benefit magnitude (33.3–90.7 protected residents), cost structure affects detailed road membership (Top-30 overlap as low as 40.0%), and the tested Equation 17 coefficient range has limited influence on the Central Top-30 portfolio. We therefore narrow the operational interpretation: the results are auditable planning stress tests, not local engineering-return or cost estimates, and field inspection and site-specific quantities remain necessary before implementation.

"The action categories reflect different ways of maintaining road access during the planning horizon: temporary reinforcement is preventive, clearance pre-positioning represents faster restoration, and alternative-route protection represents continuity through a substitute connection. Equation 14 treats these distinct mechanisms as a common stylized reduction in effective road unavailability so that their network consequences can be compared; it is not a physical model in which all three actions prevent slope failure. Japanese road-slope guidance supports inspection, risk-based prioritization, and evaluation of countermeasure effects under limited resources (Public Works Research Institute, 2015; Ministry of Land, Infrastructure, Transport and Tourism, 2022), but it does not supply transferable values for these heterogeneous actions. We therefore declare Conservative/Central/Optimistic proportional reductions of 0.25/0.45/0.60 for temporary reinforcement, 0.10/0.20/0.30 for clearance pre-positioning, and 0.20/0.35/0.50 for alternative-route protection. These are planning stress assumptions, not locally measured engineering effectiveness."
(Page 24, Lines 508–521)

"The constants encode only an assumed fixed/mobilization component and a length-scaled component. They are neither currency nor official unit prices; actual estimation requires site-specific quantities, terrain, access, design, and procurement information."
(Page 25, Lines 540–542)

"The coefficient 0.15 is an analyst-set scaling weight that gives the attachment term a limited supporting role when a single-section closure does not capture all local dependence; it is not an estimated physical, economic, or engineering coefficient. We test values of 0, 0.075, 0.15, 0.30, and 0.50 while holding the action effects and costs fixed."
(Page 26, Lines 547–550)

"Separating the three assumption families shows different forms of sensitivity (Appendix Table B13). Changing only action effectiveness preserves near-identical road-score ordering (Spearman 1.000; Top-30 overlap 93.3–100%) but changes protected population from 33.3 to 90.7 residents around the Central 62.3. Changing only cost assumptions yields 52.9–67.8 protected residents; Top-30 overlap remains 100% under global scaling, but falls to 70.0% under equal-action costs and 40.0% when fixed cost components are removed. Varying the Equation 17 attachment coefficient from 0 to 0.50 retains all 30 Central top roads and yields 59.8–62.3 protected residents. At zero, only 216 roads retain a positive score, making the all-road Spearman value of 0.353 tie-sensitive despite an unchanged selected portfolio. Thus, effect magnitude governs estimated benefit, detailed road membership depends on cost structure, and 0.15 is not decisive for the tested Top-30 portfolio."
(Page 36, Lines 777–788)

"The separated intervention sensitivity does not validate the Central assumptions. Its ±45–47% effect-driven benefit range shows that protected-population magnitude cannot be interpreted as a locally expected engineering return, while the 40% Top-30 overlap under the length-only cost stress shows that detailed road selection requires site-specific cost estimates. By contrast, the tested attachment-weight range changes protected population by at most 4.1% and retains the Central Top 30. Practical use should therefore begin with field inspection and local bills of quantities, then rerun the transparent screen with action-specific feasibility, effectiveness, restoration time, and cost information."
(Pages 44–45, Lines 970–978)

## Comment 7

7. The road-disruption validation requires clearer identification of the triggering mechanism of the restriction records. The retained records include rockfall, slope collapse, landslide, and sediment inflow shortly after the earthquake, although it is unclear whether these disruptions were rainfall-triggered or directly earthquake-induced. Please clarify the triggering conditions and demonstrate that the selected records are appropriate for validating rainfall-triggered road disruption.

**Response:**
Thank you for identifying this important attribution problem. We audited the restriction records at the physical-episode level, reviewed the recorded process reasons and event timing, and compared each episode with official hourly observations from the project JMA station network. The audit shows that the retained records occurred in a dry, earthquake-proximate window: they are consistent with direct earthquake effects, but the source records do not explicitly establish the trigger. We therefore do not present these records as validation of rainfall-triggered road disruption. Instead, the revised manuscript uses them only as supplementary evidence that the terrain-to-road ranking corresponds with earthquake-proximate mass-movement restrictions. We also replaced the snapshot-weighted comparison with equal episode weighting, episode-cluster bootstrap intervals, and paired comparator contrasts; revised Equation 9, Figure 5, and Appendix Tables B2a–B2c; and narrowed the Abstract, Methods, Results, and Discussion claims accordingly.

"An event-deduplicated audit identified 10 earthquake-proximate mass-movement restriction episodes; their Heavy-score concordance was 0.723 (episode-cluster bootstrap 95% CI 0.598–0.840), but zero preceding 72-h rainfall across the audited JMA station network means that this evidence provides only supplementary road-ranking correspondence, not validation of rainfall-triggered disruption."
(Page 1, Lines 16–21)

"The interpreted 2016 landslide inventory is used only for historical slope-ranking validation. Late-July to early-August 2026 restriction records are retained only as supplementary correspondence evidence for earthquake-proximate mass-movement effects on roads; the absence of preceding rainfall prevents their use as validation of rainfall-triggered disruption."
(Page 6, Lines 117–121)

"Repeated restriction snapshots are consolidated into physical episodes and linked to plausible network edges. Source reasons, timing, and official event-window rainfall observations are audited before the records are used as supplementary correspondence evidence for earthquake-proximate rockfall, slope-collapse, and sediment-inflow restrictions. Because the sources do not explicitly code the trigger and the audited event window was dry, these records do not validate rainfall-triggered closure, identify unaffected roads, or calibrate a failure probability."
(Page 9, Lines 172–178)

"The 10 episodes began 0.55–24.38 h after the earthquake, their reasons contained no explicit rainfall-trigger term, and official hourly observations gave 0 mm over the preceding 1, 3, 24, and 72 h both at the nearest project station and across the ten-station audit. We therefore classify them as direct-earthquake consistent but source-unconfirmed and use them only for supplementary correspondence with the terrain-to-road ranking, not for validation of rainfall triggering."
(Page 18, Lines 374–379)

Equation 9 (mathematical transcription):
$$
C_{\mathrm{episode}}^{(r,f)}=
\frac{1}{K}\sum_{k=1}^{K}\frac{1}{|A_k|}\sum_{a\in A_k}
\frac{1}{|B_a|}\sum_{b\in B_a}
\left[\mathbf{1}\!\left(D_a^{(r,f)}>D_b^{(r,f)}\right)
+\frac{1}{2}\mathbf{1}\!\left(D_a^{(r,f)}=D_b^{(r,f)}\right)\right].
$$
(Page 19, Line 389)

"The trigger audit retains 10 physical restriction episodes linked to 94 sections, of which 93 have eligible controls. Under equal episode weighting, Heavy-score concordance is 0.723 (episode-cluster bootstrap 95% CI 0.598–0.840), compared with 0.698 (0.554–0.845) for road length and 0.545 (0.409–0.683) for warning-zone exposure. The Heavy-minus-length contrast is 0.025 (−0.073 to 0.116), and the Heavy-minus-warning contrast is 0.178 (−0.011 to 0.353). Because all retained episodes occurred in a dry earthquake-proximate window and both paired contrast intervals include zero, these results provide only supplementary ranking correspondence; they do not validate rainfall triggering or establish predictive superiority."
(Pages 24–25, Lines 510–518)

"Episode-weighted correspondence ranged from 0.711 to 0.741 across the 15 specifications. This range indicates consistent correspondence with the terrain-to-road ranking under alternative transfer settings, but the 10 clustered dry-event episodes neither validate rainfall triggering nor identify the exact highest-ranked roads independently of parameter choice."
(Page 26, Lines 554–558)

"Across the 10 earthquake-proximate restriction episodes, episode-weighted concordance is 0.723 for the Heavy road score, 0.545 for warning-zone exposure, and 0.698 for section length. Within the same matched controls, the Heavy-minus-warning contrast is 0.178 (episode-cluster bootstrap 95% CI −0.011 to 0.353), whereas the Heavy-minus-length contrast is 0.025 (−0.073 to 0.116). The score therefore shows positive correspondence with the retained road restrictions but does not establish improvement over the length comparator. More importantly, the dry event window means that this comparison evaluates only whether the terrain-to-road ranking corresponds with earthquake-proximate mass-movement restrictions; it does not validate rainfall-triggered disruption, scenario-sensitive spatial ranking, closure probability, landslide-deposit extent, or physical runout geometry."
(Pages 26–27, Lines 559–569)

"The 2026 restriction evidence comprises only 10 physical episodes in a dry earthquake-proximate window; repeated snapshots and multiple linked sections are not independent events, and the source reasons do not explicitly code the trigger. Consequently, these records cannot validate rainfall-triggered road disruption, and a future target-mechanism validation requires event-deduplicated road impacts with confirmed rainfall timing, event rainfall fields, and credible unaffected-road comparators."
(Pages 35–36, Lines 762–767)

"Note: Panels a, b, and c map relative road disruption scores under Moderate, Heavy, and Extreme rainfall, with the Extreme panel also identifying emergency transport roads. Panel d locates the 10 event-deduplicated rockfall, slope-collapse, or sediment-inflow restriction episodes and their linked sections on the Heavy-score background. These episodes occurred in a dry earthquake-proximate window and provide supplementary terrain-to-road ranking correspondence, not validation of rainfall-triggered disruption."
(Page 44, Lines 29–33)

## Comment 8

8. The service-accessibility analysis fixes the nearest baseline facility as the destination after disruption. Please discuss how this assumption affects the interpretation of service loss in cases where another facility of the same service class remains reachable.

**Response:**
Thank you for raising this important point. We found that the manuscript description, rather than the production implementation, was inaccurate: after each disruption draw, the model recomputes access to every resolved, road-attached destination within a service class, so the baseline-nearest facility is not fixed. We corrected the Methods and Figure 7 note, added a paired comparison with a restrictive fixed-baseline-destination estimator, and report the full comparison in Appendix Table B9. Under Heavy rainfall, fixing the baseline destination would increase affected population from 609.9 to 1,217.4 for shelters, from 1,286.7 to 7,106.4 for fire services, and from 937.3 to 2,811.3 for municipal facilities. Thus, a fixed-destination assumption materially overstates class-level network reachability loss, especially for fire services. Conversely, the any-same-class estimand represents network availability and does not establish that an alternative facility is operating, adequately staffed, or able to absorb additional demand. Emergency-water results remain conditional on the 10 of 36 announced destinations with resolved coordinates.

"Service analysis includes only communities that can reach a destination of the relevant class at baseline. For each eligible community, baseline travel time is the shortest time to any reachable designated shelter, resolved emergency water point, fire-service facility, or municipal facility on the complete weighted road graph. After each disruption draw, shortest paths are recomputed to all resolved, road-attached destinations in that class, so a farther same-class facility may replace the baseline-nearest facility. Service reachability is lost only when no destination in the class remains reachable. This rerouting rule does not imply that residents would necessarily choose the identified facility during an emergency or that every mapped facility would be operating or have sufficient capacity. A facility without a resolved network attachment remains outside the routing denominator, and a community that is already unreachable at baseline is not counted as a disruption-induced loss."
(Pages 21–22, Lines 453–464)

"Travel-time change is evaluated only when at least one destination in the class remains reachable."
(Page 22, Line 473)

"A paired destination-estimand audit confirms that the principal results already allow substitution among facilities in the same class. If the baseline-nearest destination were instead held fixed, Heavy-scenario affected population would increase from 609.9 to 1,217.4 for shelters, from 1,286.7 to 7,106.4 for fire services, and from 937.3 to 2,811.3 for municipal facilities. Same-class rerouting therefore prevents 607.4, 5,819.7, and 1,874.1 residents, respectively, from being classified as losing the service, equal to 49.9%, 81.9%, and 66.7% of the corresponding fixed-destination losses (Appendix Table B9). The conditional emergency-water comparison is reported separately in the Appendix because only 10 of 36 announced destinations are geolocated."
(Page 31, Lines 658–666)

"The service-destination comparison further separates class-level network availability from continuity with one baseline facility. Holding the baseline-nearest destination fixed would overstate the primary loss estimate because it counts communities that can still reach another same-class facility, with the largest difference occurring for fire services. The any-same-class estimand is more appropriate for network availability, but it does not establish realized service continuity: an alternative facility may be closed, understaffed, capacity-constrained, inaccessible for non-network reasons, or unable to accept additional demand. The estimates therefore bound road-network reachability rather than operational service adequacy."
(Pages 36–37, Lines 789–797)

"Note: Panels a, b, and c map Heavy-rainfall reachability loss for shelters, fire services, and municipal facilities; panel d compares expected affected population and median excess travel time and marks emergency water as conditional sensitivity evidence for the 10 of 36 geolocated destinations. A community loses a service class only when no resolved, road-attached facility in that class remains reachable; the baseline-nearest destination is not fixed after disruption."
(Page 50, Lines 47–51)

## Comment 9

9. The relationship between Equation 15 and the ranking procedure in Equations 16-17 is unclear. Please explain how the intervention portfolio is selected under the budget constraint and clarify whether Equation 15 is explicitly optimized or whether portfolios are constructed from the screening ranking. The methodological description and terminology should be consistent with the implemented procedure.

**Response:**
Thank you for identifying this ambiguity. We clarified throughout the manuscript that Equations 16–17 construct a screening order, whereas Equation 15 evaluates the network benefit of a portfolio only after that portfolio has been assembled. Specifically, the implementation computes the Equation 17 consequence proxy, assigns one feasible road-access action, computes the Equation 16 priority score, ranks all roads, retains the first 150 candidates, and scans that ordered list once for each of seven budgets. An action is selected when its setting-specific cost fits the remaining budget; otherwise it is skipped and the scan continues. The procedure does not backtrack, swap items, search all feasible combinations, or explicitly maximize Equation 15. We therefore now describe the output consistently as a greedy rank-and-pack screening portfolio rather than an optimizer solution. We also revised the research question, conceptual description, conclusion, Appendix, and analytical protocol to use the same terminology.

"Fourth, how does the transparent screening procedure prioritize budget-feasible road actions and residual community preparedness needs, and what population-weighted reduction do the resulting road portfolios achieve?"
(Page 6, Lines 105–108)

"The costs are relative planning units and the effects are declared assumptions. Equation 15 is evaluated only after a budget-feasible screening portfolio has been constructed; it is not explicitly maximized over all feasible action combinations and does not represent an observed engineering return."
(Page 25, Lines 527–531)

"Seven budgets span zero to the Central cost of the first 100 ranked candidates. For each budget and sensitivity setting, the same ordered list is scanned once: the assigned action is selected when its setting-specific cost fits the remaining budget, otherwise it is skipped and the scan continues. There is no backtracking, item swapping, or combinatorial search."
(Page 26, Lines 560–564)

"Under the post-earthquake rainfall-warning threshold scenarios, the framework identifies where relative slope disruption may affect roads, where those road disruptions may isolate communities or remove basic-service access, and how road-access actions and community preparedness needs rank under the declared screening rules."
(Page 47, Lines 1035–1038)

"Portfolio construction follows a fixed greedy rank-and-pack rule. Equation 17 is evaluated first to obtain the consequence proxy, Equation 16 converts that proxy to the assigned-action priority score, and the first 150 ranked roads form the planning candidate set. For each budget and sensitivity setting, the ordered candidates are scanned once and an action is added only when its cost fits the remaining budget. Equation 15 is evaluated by network simulation after that set has been constructed; it is not maximized over all feasible portfolios."
(Appendix, Page 11, Lines 199–205)

## Comment 10

10. The numerical values reported in the Highlights are inconsistent with those in the Abstract and Results. Please correct these values and confirm numerical consistency throughout the manuscript.

**Response:**
Thank you for identifying this inconsistency. The submitted Highlights contained incorrect, outdated population values, and we apologize for the error. The revised Highlights now agrees with the Abstract and Results. Under the revised Primary Emergency Road backbone definition, the central Heavy-scenario means are 1,063.6 disconnected residents, including 576.6 residents aged 65 or older; the Abstract and Highlights report these as 1,064 and 577 after rounding. These are simulation-based mean expected populations, not observed counts of isolated residents. The revised numerical highlight states:

"Heavy-scenario mean disconnection is 1,064 residents, including 577 aged 65 or older."
(Highlights, Page 1, Item 2)

We also checked the headline outcomes and their repeated numerical summaries across the main text, figures and supplementary tables against the underlying results, including reconciliation of the municipality-level totals. This check identified an outdated section-weighted correspondence result in Appendix Table B5 and its accompanying explanation. Both now use the episode-weighted measure: 0.723 centrally, with a range of 0.711–0.726 across 15 rainfall-parameter combinations. This is a specification range, not a confidence interval. The corrected explanation reads:

"Across five window-weight schemes and three γ values, the minimum road-ranking correlation was 0.989, minimum top-1% overlap was 0.879, and episode-weighted road-restriction correspondence ranged from 0.711 to 0.726."
(Appendix, Page 5, Lines 103–105)

The Highlights and Table B5 also consistently identify the limited role of the ten dry-window physical restriction episodes. The revised highlight reads:

"Ten dry-window restriction episodes provide supplementary ranking evidence."
(Highlights, Page 1, Item 3)

The interpretation cell in the corresponding Table B5 row states:

"Supplementary dry-event correspondence; not rainfall-trigger validation"
(Appendix, Page 29, Table B5, Episode-weighted road-restriction correspondence row)

Finally, the Appendix clarifies why summing rounded municipality-level displays can differ slightly from the prefecture-wide totals calculated before rounding:

"Prefecture-wide totals are calculated from unrounded values; sums of the displayed municipality-level values can differ slightly because of rounding."
(Appendix, Page 12, Lines 237–239)

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
Thank you for identifying the need to examine these assumptions more systematically. The revised Methods, Results, Discussion, and Appendix Tables B14–B15 add terrain-weight sensitivity and bring the completed parameter tests together, while distinguishing transparent reference settings from empirically calibrated parameters. The new terrain experiment retains the original standardization, perturbs each coefficient by factors of 0.50 and 1.50, and renormalizes the vector to preserve its total weight. No alternative is selected for favorable validation or consequence results. The Methods state:

"To test dependence on relative composition, we multiply one coefficient at a time by 0.50 or 1.50 and renormalize all four coefficients to their original sum of 2.25, yielding eight alternatives to Central. The original feature standardization remains fixed, and no alternative is selected using validation or consequence performance. These perturbations are declared stress tests, not empirical coefficient bounds or evidence that the Central weights are optimal."
(Page 16, Lines 333–338)

Each specification reaches the Heavy-rainfall disconnection and intervention endpoints, with road candidates and portfolios rebuilt rather than held at their Central membership. The Methods define the propagation and its limits:

"All nine terrain-weight specifications produce slope and road scores for three rainfall scenarios; Heavy disconnection and fixed-budget Central intervention are propagated with five seeds and 1,000 draws per seed. Candidate roads, reduced networks, and priorities are rebuilt for each specification, with common random variates aligned by road-section identity. Appendix Tables B14–B15 separate within-specification Monte Carlo variation from parameter and structural stress ranges. This staged analysis does not evaluate all cross-family interactions or terrain-weight effects on service endpoints and is not a comprehensive probabilistic uncertainty propagation."
(Page 28, Lines 593–601)

The results reveal material dependence on terrain-weight composition, despite positive-support road-score correlations of at least 0.963 across the three rainfall scenarios. Table B14 reports every prespecified alternative, and the Results distinguish consequence magnitude from shortlist stability:

"Across the nine specifications, Heavy disconnected population ranges from 490.5 to 3,323.7 residents, including 248.7–1,845.2 aged 65 and older, compared with Central values of 1,063.6 and 576.6. With Central intervention effects and costs and the same budget, protected population ranges from 41.6 to 115.7 residents around 62.3. Community Top-30 overlap falls to 56.7%, intervention Top-30 overlap to 50.0%, and selected-portfolio overlap to 51.0%."
(Page 38, Lines 828–833)

Table B15 also summarizes the tested rainfall-window weights and rainfall coefficient, slope-to-road transfer, closure mapping and dependence, intervention effectiveness and costs, and the attachment coefficient. It identifies which settings reach downstream endpoints. In particular, the effectiveness-only tests yield 33.3–90.7 protected residents, cost-only tests yield 52.9–67.8, and attachment coefficients of 0–0.50 yield 59.8–62.3. These are family-specific stress ranges, not a pooled confidence interval. The new Appendix notes make that distinction explicit:

"Within-specification seed variation, parameter/structural stress ranges, and limitations of data or validation support represent different uncertainties. Existing within-family combinations do not test all cross-family interactions across the complete decision chain. These are staged sensitivity checks, not a comprehensive probabilistic propagation."
(Appendix, Page 37, Lines 31–33)

The contribution remains the linked, auditable comparison of slope disruption, road dependence, community consequences, and intervention priorities. The additional evidence identifies where assumptions materially change those comparisons; it does not establish an optimal weight vector or validate local engineering returns. The Discussion now states:

"The terrain-weight stress test also shows that the fixed context coefficients materially affect both consequence magnitude and detailed road selection. The framework therefore offers an auditable chain of conditional comparisons, not an empirically preferred weight vector or a universally stable local shortlist."
(Page 47, Lines 1042–1045)

## Comment 3

Third, road rankings are almost identical across rainfall scenarios, with correlations of 0.999-1.000, indicating that rainfall severity changes score magnitude but provides virtually no spatial reprioritization; this substantially weakens the central scenario-based claim.

**Response:**
Thank you for identifying this limitation. We agree that the rainfall scenarios do not demonstrate meaningful spatial reprioritization of roads. The revised Abstract and Discussion limit the contribution to changes in disruption-score magnitude and conditional network consequences, and the Results now report the correlation denominators explicitly.

Recalculation from the unchanged road-score arrays gives Moderate–Heavy and Extreme–Heavy Spearman correlations of 0.9993 and 0.9988 across all 343,844 analysis-eligible sections. The earlier Moderate–Heavy value of 1.000 is corrected. Removing the 120,218 sections with zero scores in every scenario leaves correlations of 0.9977 and 0.9960 across 223,626 positively scored sections. Thus, shared zero scores partly increase the full-network correlations but do not account for the near-invariant ordering. With terrain and transfer structure fixed, the station-supported quantile scenarios serve as magnitude stress tests rather than event-specific storm footprints. The simulated consequence contrasts remain conditional on the declared closure mapping and network target; larger burdens are not evidence of improved spatial prioritization. The revised passages state:

"Rainfall severity mainly changes score magnitude and simulated disconnection burden, with little spatial reprioritization of roads."
(Page 2, Lines 25–27)

"Spatial rankings, however, change little: across all 343,844 analysis-eligible road sections, Moderate and Heavy road scores have Spearman rank correlation 0.9993, and Extreme and Heavy scores have correlation 0.9988. Excluding the 120,218 sections with zero scores in all three scenarios leaves correlations of 0.9977 and 0.9960 across 223,626 positively scored sections, respectively."
(Page 29, Lines 633–637)

"Their purpose is comparative planning, not reconstruction of the physical state of every slope. Within the fixed threshold geography, the rainfall scenarios combine unchanged terrain and transfer structure with station-supported quantile loading rather than event-specific storm footprints. Their principal role is to stress-test disruption and network-consequence magnitudes; the larger simulated burdens do not demonstrate improved spatial road prioritization."
(Page 39, Lines 859–864)

## Comment 4

The landslide validation performance is only moderate (AUC = 0.665), while the road validation contains only 94 evidence cases and does not clearly demonstrate statistically significant improvement over the road-length comparator.

**Response:**
Thank you for this comment. We agree that the current road evidence does not establish statistically significant improvement over the road-length comparator. This comparison evaluates road-ranking correspondence, whereas the study’s principal contribution is to connect scenario-based disruption screening with community isolation, service accessibility, and budget-constrained intervention comparisons. The revised Introduction describes historical slope-ranking alignment and supplementary road-ranking correspondence, while the Discussion explicitly acknowledges moderate terrain discrimination, the small number of physical road-restriction episodes, and the distinction between unproven superiority and equivalence.

The revised historical evaluation restricts pseudo-background sampling to the GSI interpretation footprint and warning-zone exposure to polygons designated before the 2016 earthquake sequence. Under this corrected support, the frozen terrain score has a mean spatial AUC of 0.705, a fold range of 0.550–0.787, and held-out top-quartile capture of 46.5%. The change from the earlier 0.665 reflects the evaluation-support correction, not refitting of the propagated score. We retain a moderate, spatially variable interpretation; this historical alignment does not validate the 2026 rainfall scenarios or calibrated failure probabilities.

The revised road audit distinguishes 10 physical restriction episodes from their 94 linked sections, of which 93 have eligible matched controls. Matching accounts for municipality or ward, road category, emergency-route membership, and section-length decile. Equal episode weighting and episode-cluster bootstrapping avoid treating multiple sections from one episode as independent events. Heavy-score concordance is 0.723 (95% CI 0.598–0.840), compared with 0.698 (0.554–0.845) for road length. The paired Heavy-minus-length contrast is 0.025 (−0.073 to 0.116); the Heavy-minus-warning contrast is 0.178 (−0.011 to 0.353). Both intervals include zero, so neither comparison demonstrates superiority. Nor do these wide intervals establish equivalence. Because the retained episodes occur in a dry earthquake-proximate window, the comparison remains supplementary terrain-to-road correspondence rather than validation of rainfall-triggered disruption. The revised passages state:

"The framework evaluates historical slope-ranking alignment and supplementary road-ranking correspondence, converts road scores into bounded closure propensities, simulates network consequences, and compares consequence-aware interventions under planning budgets."
(Page 4, Lines 78–81)

"The main limitations arise from incomplete inventories and simplified process representation. The historical terrain score shows moderate, spatially variable discrimination, while the road comparison has only 10 physical episodes and wide paired confidence intervals. Failure to establish superiority over a comparator is not evidence of equivalence."
(Page 45, Lines 997–1001)

## Comment 5

The independent Bernoulli closure assumption also neglects spatially correlated failures caused by the same rainfall event or landslide process.

**Response:**
Thank you for identifying the omitted dependence among road-section failures. We retained the independent Bernoulli implementation as the transparent central reference, but added a fixed-marginal spatial-cluster Gaussian-copula sensitivity analysis. Candidate sections were grouped into 1 km and 3 km projected square clusters and evaluated at within-cluster dependence levels of 0.25 and 0.50 for all three rainfall scenarios, five seeds, and 1,000 draws per seed. This construction introduces shared cluster shocks while preserving each section's central marginal closure propensity, so the comparison isolates the consequence of co-occurring closures rather than changing marginal hazards.

The new results show that dependence is consequential but not uniformly directional. Under the broad strong setting, mean expected isolated population changes by +9.2%, +15.7%, and −10.5% under Moderate, Heavy, and Extreme rainfall, respectively; the corresponding per-draw 95th percentiles change by +8.7%, +15.8%, and −5.3%. Community rankings remain broadly stable, but the Heavy top-30 burden overlap falls to 66.7%, indicating greater sensitivity in exact local priorities. We therefore clarify that independent closure is neither uniformly conservative nor anti-conservative, and that the uncalibrated cluster scales and correlations are stress-test bounds rather than fitted process parameters. All 15 settings and validation-relevant priority metrics are reported in Appendix Table B8.

"To test departure from independent section closures while holding every marginal propensity fixed, we additionally use a spatial-cluster Gaussian copula. For section \(e\) in cluster \(g(e)\) and draw \(m\), \(Z_{e,m}=\sqrt{\rho}Z_{g(e),m}+\sqrt{1-\rho}Z^{\mathrm{ind}}_{e,m}\), and the section closes when \(Z_{e,m}\leq\Phi^{-1}(p_e)\). Candidate sections are grouped by projected midpoint into fixed 1 km or 3 km square clusters and evaluated at \(\rho=0.25\) and \(0.50\), alongside the independent \(\rho=0\) reference, for each rainfall scenario, five seeds, and 1,000 draws per seed. Shared cluster shocks introduce positive within-cluster dependence while preserving \(p_e\) as the marginal closure propensity. The cluster scales and correlations are stress-test assumptions rather than estimated landslide-footprint or failure-process parameters."
(Page 21, Lines 435–443)

"Spatial closure dependence changes consequence magnitude and local priority membership without a uniform direction across rainfall scenarios. Relative to independent closure, the broad strong setting (3 km clusters, \(\rho=0.50\)) changes mean expected isolated population from 189.1 to 206.4 under Moderate rainfall (+9.2%), from 1,121.7 to 1,298.1 under Heavy rainfall (+15.7%), and from 5,032.2 to 4,501.5 under Extreme rainfall (−10.5%). The corresponding per-draw 95th percentiles change by +8.7%, +15.8%, and −5.3%. Under Heavy rainfall, community isolation-frequency rank correlation with the independent reference is 0.948 and top-30 population-burden overlap is 66.7% in the broad strong setting. Across all correlated settings and scenarios, rank correlation remains 0.938–0.996, whereas top-30 overlap ranges from 66.7% to 100% (Appendix Table B8)."
(Pages 29–30, Lines 629–638)

"The sensitivity analysis distinguishes two forms of network dependence. Network topology determines the consequence of a realized closure set, whereas spatial dependence determines which section closures co-occur. Under Heavy rainfall, positive cluster dependence increases both mean and upper-tail isolation; under Extreme rainfall, the same fixed-marginal construction produces less spatially dispersed closure sets and lowers both quantities despite very high community-rank agreement. Independent closure is therefore neither uniformly conservative nor uniformly anti-conservative. The independent model remains a transparent reference, but correlated stress tests are necessary when local preparedness decisions depend on the exact highest-burden communities."
(Page 36, Lines 775–783)

"The 1 km and 3 km square clusters and \(\rho=0.25\) and \(0.50\) dependence levels are deliberately broad sensitivity settings rather than estimates from observed co-failures. Square-grid boundaries also discretize processes that would vary continuously in space. The correlated results therefore bound dependence uncertainty but cannot identify an event-specific correlation length, attribute a common physical trigger, or replace calibration using geocoded and time-resolved multi-road failure observations."
(Page 39, Lines 847–852)

"Appendix Table B8 isolates spatial closure dependence while retaining each candidate section's central marginal closure propensity. The independent implementation exactly reproduces the existing five-seed simulation. Under the broad strong setting, mean expected isolated population changes by +9.2%, +15.7%, and −10.5% for Moderate, Heavy, and Extreme rainfall, respectively, and the corresponding per-draw 95th percentiles change by +8.7%, +15.8%, and −5.3%. Community-frequency rank correlations remain high, but lower top-30 overlap under Heavy rainfall shows that local preparedness priorities are more dependence-sensitive than the broad geographic ordering. Because the scale and correlation settings are not calibrated, the table reports sensitivity bounds rather than alternative forecasts."
(Appendix, Pages 5–6, Lines 114–123; Table B8 on Appendix Page 28)

## Comment 6

In addition, defining isolation through connection to prefectural-boundary gateways requires stronger operational justification, and service loss should allow communities to reroute to alternative facilities rather than only assessing access to the baseline nearest destination.

**Response:**
Thank you for identifying both the unsupported boundary-gateway interpretation and the need to make facility substitution explicit. We agree that proximity to the unioned prefectural boundary, which also contains coastline and island shoreline, does not establish an operational interprefectural gateway. We therefore replaced that rule with a network-based definition. The primary target now comprises every stable baseline root containing at least one Primary Emergency Road node. Baseline eligibility requires a community attachment to a full-network component containing such a root, and disconnection occurs only when every community attachment loses access to every remaining primary-backbone target root. The text also clarifies that this outcome represents disconnection from the designated emergency-road backbone, not literal separation from every road, destination, or place outside Kumamoto Prefecture.

We recalculated the complete network-consequence chain under this definition for all three rainfall scenarios and five seeds. The revised Heavy estimate is 1,063.6 expected disconnected residents, with a five-seed range of 1,050.4–1,078.9. Expanding the target to roots containing Primary or Secondary Emergency Road nodes gives 992.7 expected disconnected residents, a community-frequency rank correlation of 0.964, and 90.0% overlap in the top-30 population-burden communities. The former coast-inclusive boundary rule is retained only as a traceability audit and is clearly distinguished from the operational analysis. Figures 6 and 8, the downstream tables, and Appendix Table B10 were updated accordingly.

We also clarified that the principal service analysis already reroutes each eligible community after every disruption draw to all resolved, road-attached facilities in the same service class. A service is classified as unreachable only when no such facility remains reachable. To demonstrate the effect of this choice, Appendix Table B9 reports a paired restrictive comparator that holds the baseline-nearest destination fixed. Under Heavy rainfall, allowing same-class rerouting avoids classifying an additional 607.4 residents as losing shelter access, 5,819.7 as losing fire-service access, and 1,874.1 as losing municipal-facility access. We explicitly state that this network substitution does not guarantee facility operability, capacity, or actual destination choice during an emergency.

"Under the Heavy rainfall scenario, the simulations yielded a mean expected 1,064 residents disconnected from the Primary Emergency Road backbone, including 577 residents aged 65 years or older."
(Page 1, Lines 15–17)

"Third, which communities and residents lose access to the Primary Emergency Road backbone or to any resolved same-class basic-service facility under conditional road disruption?"
(Pages 5–6, Lines 102–104)

"Six quality gates precede scenario interpretation: valid geometry, complete rainfall windows, coherent road topology, reconciled population totals, baseline connection to the Primary Emergency Road backbone, and valid service-node attachment."
(Page 11, Lines 222–224)

"We define the primary operational target as every stable baseline root containing at least one Primary Emergency Road node, and baseline eligibility requires a community attachment to a full-network component containing such a root. A community is disconnected when simulated closures remove access from all of its attachments to every remaining primary-backbone target root. This definition measures access to the designated backbone for wide-area emergency movement; it does not imply separation from every road, destination, or place outside the prefecture. A broader comparator additionally admits roots containing Secondary Emergency Road nodes, whereas the former coast-inclusive administrative-boundary search is retained only as an audit comparator. Communities without valid baseline linkage are classified as non-evaluable rather than newly disconnected."
(Page 20, Lines 422–432)

"The former coast-inclusive administrative-boundary rule is reproduced only as a traceability audit and is not treated as an operational target."
(Page 25, Lines 530–532)

"Expanding the target to the Primary-plus-Secondary Emergency Road backbone yields 992.7 expected disconnected residents under Heavy rainfall; community-frequency rank correlation with the primary definition is 0.964 and top-30 population-burden overlap is 90.0%. The former coast-inclusive boundary proxy yields 1,121.7 residents only in the traceability audit."
(Page 29, Lines 631–635)

"After each disruption draw, shortest paths are recomputed to all resolved, road-attached destinations in that class, so a farther same-class facility may replace the baseline-nearest facility. Service reachability is lost only when no destination in the class remains reachable."
(Page 22, Lines 464–467)

"A paired destination-estimand audit confirms that the principal results already allow substitution among facilities in the same class. If the baseline-nearest destination were instead held fixed, Heavy-scenario affected population would increase from 609.9 to 1,217.4 for shelters, from 1,286.7 to 7,106.4 for fire services, and from 937.3 to 2,811.3 for municipal facilities. Same-class rerouting therefore prevents 607.4, 5,819.7, and 1,874.1 residents, respectively, from being classified as losing the service, equal to 49.9%, 81.9%, and 66.7% of the corresponding fixed-destination losses (Appendix Table B9)."
(Page 31, Lines 673–679)

"A road with a high disruption score may have modest consequences when alternatives remain available, whereas a moderately exposed section may be consequential when it provides a scarce connection from populated communities to the emergency-road backbone (Nitheesh & Bhavathrathan, 2025)."
(Page 34, Lines 732–735)

"Isolation denotes loss of connection to every stable root containing a Primary Emergency Road node; the all-emergency-road result is the broader target comparator."
(Page 50, Lines 44–45)

## Comment 7

The intervention analysis relies on hypothetical costs and effects, and the Central ranking is identical to the equal-cost consequence benchmark, so no incremental optimization advantage has been demonstrated.

**Response:**
Thank you for this important observation. We agree that the hypothetical costs and effects do not establish engineering returns and that the identical Central ranking provides no evidence of incremental optimization advantage. The Abstract now explicitly ties the screening priorities to declared cost and effectiveness assumptions, and the Conclusions state this limitation directly.

The Methods describe a greedy rank-and-pack screening procedure, not an explicit optimization solution. The separate cost and effectiveness comparisons in Appendix Table B13 characterize sensitivity to assumptions rather than validate those assumptions. The Results and Discussion explain why the Central ranking is structurally identical to the equal-cost consequence benchmark under the declared formulation; this equality is not an empirical demonstration of non-inferiority. We therefore frame the contribution as auditable consequence-aware screening, with local cost, effectiveness, and feasibility evidence required before implementation. The revised summary passages read:

"Consequence-aware intervention screening identified auditable road and community priorities under declared cost and effectiveness assumptions, although the Central assigned-action ranking coincided with an equal-cost consequence ranking and therefore did not establish incremental superiority over that simple benchmark."
(Pages 1–2, Lines 22–25)

"The framework keeps relative disruption scores distinct from calibrated failure probabilities, simulation-conditional isolation distinct from observed outcomes, and planning-unit benefits distinct from engineering returns. Intervention costs and effects remain hypothetical, and the Central ranking equals the equal-cost consequence benchmark; no incremental optimization advantage is demonstrated."
(Page 48, Lines 1068–1073)

## Comment 8

Finally, the Highlights report 12,000 isolated residents and 3,000 elderly residents, whereas the abstract and main text report approximately 1,107 and 603, respectively; all numerical results must therefore be comprehensively checked. These issues require substantial methodological clarification, additional sensitivity analyses, possible recalculation of the network and service-access results, and more cautious interpretation of the operational implications.

**Response:**
Thank you for identifying this serious inconsistency. The submitted Highlights values of 12,000 and 3,000 were incorrect, and we apologize for the error. We have corrected the Highlights and checked the main outcome aggregates and their repeated displays in the Abstract, Results, figures and supplementary tables against the underlying calculations.

The revised results also reflect the change to a Primary Emergency Road backbone definition of disconnection, described in our response to Comment 6. The central Heavy-scenario mean is now 1,063.6 disconnected residents, including 576.6 aged 65 or older, calculated from five seeds with 1,000 draws per seed. The Abstract and Highlights round these means to 1,064 and 577. Thus, the revised numbers are not simply rounded versions of the earlier 1,107 and 603. They are conditional simulation outputs under the revised network definition, not observed counts of isolated residents. The corrected highlight reads:

"Heavy-scenario mean disconnection is 1,064 residents, including 577 aged 65 or older."
(Highlights, Page 1, Item 2)

The numerical checks include reconciliation of the eight principal population and service-loss aggregates across all 49 municipality and ward entries in Appendix Table C1, as well as the reported intervention and comparator population benefits. The Appendix now explains the small differences that can arise when readers sum individually rounded entries:

"Prefecture-wide totals are calculated from unrounded values; sums of the displayed municipality-level values can differ slightly because of rounding."
(Appendix, Page 12, Lines 237–239)

The accompanying methodological revisions and sensitivity analyses are detailed in our responses to Comments 1–7. The revised manuscript retains the distinction between scenario-conditional screening and validated forecasts: simulated service loss is not observed response failure, and the intervention ranking does not establish superiority over the equal-cost consequence benchmark.

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
Thank you for asking us to clarify the relationship between the two event datasets. We now state explicitly that the 2016 and 2026 earthquakes are geographically relevant but physically non-interchangeable. The revised manuscript reports the JMA magnitudes, depths, intensities, approximate epicentral separation, and the rainfall observations associated with the two evidence windows. It also states that neither dataset contains measurements of slip-surface depth, soil-profile disturbance, or post-earthquake shear-strength change, so the analysis does not assume equivalent subsurface disturbance.

We also corrected the historical inventory chronology and support definition. The date 28 July 2016 is the inventory update date, not the earthquake date. Historical slope-ranking evaluation is now restricted to the union of the official April and July GSI air-photo interpretation footprints, and warning-zone exposure is limited to polygons designated before the 2016 earthquake sequence. Pseudo-background cells are sampled only inside that mapped support. The propagated terrain-context score was frozen before this correction and was not refitted; therefore, the correction changes the historical-alignment evidence but not the downstream 2026 scenario results.

The revised manuscript now separates the evidential roles of the two datasets throughout the Methods, Results, Discussion, limitations, Figure 2, Figure 4, and Appendix Tables A1 and B1. The 2016 inventory provides a same-region test of whether persistent terrain covariates rank mapped mass-movement locations higher across held-out spatial blocks. The 2026 records provide only supplementary road-ranking correspondence after terrain-to-road translation. The datasets are not pooled, and neither check validates transfer of the 2016 shaking state, a 2026 rainfall trigger, disturbance depth, closure probability, or calibrated physical susceptibility. Official JMA and GSI source URLs have also been added to the Data Availability statement.

"The two earthquakes are geographically relevant but not physically interchangeable. Official JMA records identify the 16 April 2016 main shock as magnitude 7.3 (Mw 7.0) at 12 km depth and the 28 July 2026 earthquake as magnitude 7.1 at 16 km depth; both reached JMA intensity 7, and their epicentres were approximately 16.3 km apart. At the 2016 main-shock time, seven project stations recorded 0 mm over the preceding 24 h and 1.0–6.5 mm over the preceding 72 h, whereas all ten retained 2026 road-restriction episodes had 0 mm over the preceding 72 h across the ten-station audit."
(Page 7, Lines 139–146)

"Historical alignment with the interpreted 2016 landslide inventory is evaluated only within the union of the official April and July GSI air-photo interpretation footprints. Because 28 July 2016 is the inventory update date rather than the earthquake date, warning-zone exposure is restricted to 29,632 polygons designated on or before the earthquake sequence began on 14 April 2016; later and unknown-date polygons are excluded, while the complete current warning-zone layer remains available for 2026 screening."
(Page 16, Lines 333–338)

"Within the GSI interpretation footprint, the corrected historical comparison uses 857 unique presence cells, 8,570 pseudo-background cells, and 29,632 warning-zone polygons designated before the 2016 earthquake sequence. The frozen transparent terrain score has a mean spatial area under the curve of 0.705, a fold range of 0.550–0.787, and held-out top-quartile capture of 46.5%; the fitted full terrain-plus-warning comparator has a mean of 0.685 and a fold range of 0.500–0.804."
(Page 25, Lines 529–534)

"The 2016 and 2026 evidence checks are deliberately non-pooled and do not constitute cross-event validation. Within the GSI interpretation footprint, the 2016 inventory tests whether the frozen terrain-context score ranks mapped earthquake-generated mass-movement centres higher across held-out spatial blocks. That same-region check is relevant because the terrain covariates are persistent, but it does not establish transfer of the 2016 shaking or disturbance state to 2026."
(Page 33, Lines 712–717)

"The station-supported rainfall surface cannot reproduce local variability between gauges, and the official retention factors are area-level settings rather than a measured shaking or soil-strength field. Neither event dataset measures slip-surface depth, soil-profile disturbance, or post-earthquake change in shear strength, so no equivalence of subsurface damage is assumed between 2016 and 2026."
(Page 37, Lines 805–810)

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
Thank you for identifying this important limitation. The revised Discussion and Appendix B explain that the Central equality is an algebraic identity, not an empirical demonstration that a more elaborate method performs as well as a simpler one. Both rankings use the same consequence proxy and assigned action, and each action's median effect-to-cost ratio across settings equals its Central ratio. They therefore produce identical road scores and all seven Central budget comparisons. The linear form of the consequence proxy is not the determining cause: replacing it with another proxy shared by both rankings would preserve the identity. We accordingly limit the contribution to traceable consequence assessment and action assignment, without claiming an incremental ranking or optimization advantage.

The cost sensitivity distinguishes affordability from selection. Uniform cost scaling preserves ordering, whereas equal-action and length-only costs retain 70.0% and 40.0% of the Central Top 30. These changes demonstrate dependence on cost structure, not superiority over a comparator using the same inputs. The new discussion identifies conditions that could produce divergence, including a median ratio different from Central, portfolio-level marginal benefits and network interactions, or independently elicited objectives and constraints. Such extensions require local engineering evidence or stakeholder preferences; they are not implemented or shown to outperform the comparator in this study.

"The equality is an algebraic identity under the declared comparison, not evidence that the two approaches converged empirically. Both scores use the same consequence proxy and action assignment, and the median cross-setting effect-to-cost ratio equals the Central ratio for every action. The linear form of the consequence proxy makes this common factor explicit but does not by itself explain the identity; applying the same alternative proxy to both scores would preserve equality. Cost structure nevertheless affects membership: global scaling retains 100% of the Central Top 30, whereas equal-action and length-only costs retain 70.0% and 40.0%, respectively. The assigned-action framework could diverge from the Central comparator if site-specific or nonlinear costs make the median ratio differ from Central, if selection uses portfolio-level marginal benefits or network interactions, or if independently elicited objectives and constraints are added. Those extensions require local engineering data or stakeholder weights and are not demonstrated here."
(Page 43, Lines 940–952)

"The identity can be stated at road level. The assigned-action score multiplies the road consequence proxy by the median effect-to-cost ratio across Conservative, Central, and Optimistic settings; the Central comparator multiplies the same proxy by the Central ratio for the same assigned action. Since those two ratios are equal for all three actions, the scores are equal for every road before ranking. The linear definition of the consequence proxy is therefore not a sufficient explanation: any consequence proxy used identically in both branches would leave this ratio identity unchanged. Uniform global cost scaling likewise preserves the score order, although it changes how many roads fit a fixed budget. The existing cost sensitivity shows that equal-action and length-only cost structures reduce Top-30 overlap with the Central reference to 70.0% and 40.0%, respectively, but this sensitivity is not evidence of superiority over a comparator built from the same inputs. Distinct rankings require the robust median ratio to differ from the Central ratio, or require an independently specified decision model with site-specific nonlinear costs, portfolio interactions, constraints, or stakeholder-weighted objectives."
(Appendix, Page 11, Lines 197–210)

## Comment 4

4. Under heavy rainfall, alternative closure mappings produce an isolated population range of 343-2,309, spanning nearly a sevenfold difference. Does this substantial uncertainty imply limited guidance value for policy-making from the current framework? How should emergency managers interpret such a wide range? Should conservative planning adopt "worst-case" mapping scenarios, or should priority be given to data collection to reduce mapping uncertainty?

**Response:**
Thank you for this important comment. We agree that the wide range indicates substantial structural uncertainty in the score-to-closure mapping and that it must be interpreted explicitly for policy use. We first audited the endpoints. Following the corrected network-target definition described elsewhere in the revision, the quoted values were obsolete; the remaining Low and High sensitivity estimates were each based on one seed, whereas the Central estimate was a five-seed mean. We therefore recalculated all three mappings under matched conditions: the same five prespecified seeds, 1,000 draws per seed, Heavy rainfall, candidate-road set, network, communities, and Primary Emergency Road target. The revised Low, Central, and High estimates are 351.4, 1,063.6, and 2,073.2 expected disconnected residents. The Low-to-High span is about 150 times the Central across-seed standard deviation, confirming that mapping uncertainty dominates Monte Carlo variation in consequence magnitude.

This uncertainty limits use of the model as a precise forecast, but it does not eliminate its value as a screening tool. Community-frequency rank correlations with the Central mapping remain 0.939 under Low and 0.971 under High; Top-30 population-burden overlap is 70.0% and 80.0%, respectively; and 15 communities remain in the Top 30 under all three mappings. We therefore do not recommend automatically treating the High mapping as the most likely case. Instead, the Central mapping is retained as the transparent reference, the High mapping is used as a capacity stress test, and the 15 common communities form a robust first-pass set for field verification and preparedness. Locations whose frequencies or ranks change materially should not be treated as precise priorities and are the appropriate targets for additional geocoded road-failure, event-rainfall, slope-to-road reach, and blockage data. The Low and High mappings are planning stress bounds, not confidence limits or calibrated forecasts.

We revised the Methods, Results, and Discussion accordingly; added the matched five-seed comparison as Appendix Table B12; and regenerated Figure 6 so that its closure-mapping annotation uses the same estimator for all three mappings.

"We apply declared low, central, and high monotone functions \(g_b\) to \(D_e^{(r,f)}\), with maximum section closure propensities of 0.15, 0.30, and 0.45, respectively."
(Pages 18–19, Lines 387–388)

"Under matched five-seed comparisons, the Low, Central, and High closure mappings yield 351.4, 1,063.6, and 2,073.2 expected disconnected residents under Heavy rainfall, respectively. Although the magnitude range is wide, community-frequency rank correlations with the Central mapping are 0.939 for Low and 0.971 for High, with corresponding Top-30 population-burden overlaps of 70.0% and 80.0%; 15 of the 30 communities are common to all three mappings (Appendix Table B12)."
(Page 30, Lines 646–651)

"The closure-mapping sensitivity separates robust screening priorities from magnitude-dependent planning. The Central mapping remains the transparent reference; the High mapping is a capacity stress test, not a most-likely forecast or a substitute for local engineering evidence. The 15 communities retained in the Top 30 under all three mappings provide a robust first-pass set for field verification and preparedness, whereas locations whose frequencies or ranks change materially should not be treated as precise local priorities. Reducing that uncertainty requires geocoded road failures and non-failures linked to event rainfall, together with evidence on slope-to-road reach and blockage, so that the score-to-closure mapping can be calibrated."
(Page 41, Lines 885–893)

"Under matched five-seed comparisons, the Low, Central, and High mappings (maximum section closure propensities 0.15, 0.30, and 0.45) yield 351.4, 1,063.6, and 2,073.2 expected disconnected residents, respectively. Relative to Central, community-frequency rank correlation is 0.939 under Low and 0.971 under High, while Top-30 population-burden overlap is 70.0% and 80.0%; 15 Top-30 communities are common to all three mappings (Appendix Table B12). The Low-to-High span is about 150 times the Central across-seed standard deviation, so mapping uncertainty dominates Monte Carlo variation in magnitude even though much of the priority ordering is retained."
(Appendix, Page 6, Lines 124–132)

## Comment 5

5. Only 10 out of 36 announced water supply points were geolocatable, leading to results for this service category (7,969 affected people) being labeled as "conditionally sensitive evidence." Given that water supply is a lifeline infrastructure, does such a high rate of missing data undermine the reliability of the paper's core conclusion—namely, "loss of service accessibility"? Please clarify whether the 26 missing points are systematically biased toward certain areas (e.g., rural or urban). If we assume these missing points are uniformly distributed, would this significantly alter the relative rankings of fire services or municipal facilities?

**Response:**
Thank you for this important comment. We agree that the 10/36 location coverage prevents the emergency-water estimate from supporting a complete prefecture-wide service-access conclusion or precise local water prioritization. The observed support is non-uniform by municipality and name class: 18 of 28 Yatsushiro announcements, all six Uki announcements, and both Hikawa announcements are unresolved, while the ten resolved records are all school-named Yatsushiro locations. However, because unresolved records have no coordinates, their urban–rural distribution is not identifiable; we therefore do not characterize them as randomly missing or infer an urban–rural bias.

We added a declared municipality-stratified uniform-location sensitivity that retains the ten observed destinations and places the 26 unresolved announcements uniformly over eligible populated 125 m meshes within their source municipality. Across 50 placement replicates and 1,250 common Heavy-scenario closure draws per placement, expected affected population was 7,052.5–7,322.2–7,936.2 at the 5th–median–95th percentiles, compared with 7,976.1 in the matched observed-only diagnostic (−11.6% to −0.5%). Community-frequency rank correlation ranged from 0.725 to 0.998 and Top-30 population-burden overlap from 66.7% to 96.7%. Thus, aggregate emergency-water burden is moderately sensitive, whereas exact local water-priority membership is less stable. We accordingly narrowed the conclusion to conditional emergency-water connectivity rather than precise local water prioritization.

The hypothetical water placements cannot alter fire-service or municipal-facility rankings because each service class is evaluated independently rather than combined through cross-service weights. We verified this directly: shelter, fire-service, and municipal-facility loss, excess-time, and baseline arrays remained exactly unchanged in 9/9 same-seed checks. The emergency-water missingness therefore limits the reliability of that service category, but it does not invalidate the separately estimated community-disconnection, shelter, fire-service, or municipal-facility results. The synthetic placements are sensitivity assumptions, not recovered locations, and do not establish water availability, capacity, operating status, or demand.

"A declared uniform-location sensitivity retained the ten observed emergency-water destinations and placed the 26 unresolved announcements uniformly over eligible populated 125 m meshes within their source municipality across 50 placement replicates. Under 1,250 common Heavy-scenario closure draws per placement, the 5th–median–95th percentile expected affected population was 7,052.5–7,322.2–7,936.2 residents, compared with 7,976.1 in the matched observed-only diagnostic (−11.6% to −0.5%). Community-frequency rank correlations were 0.725–0.736–0.998 and Top-30 population-burden overlap was 66.7%–70.0%–96.7%, indicating greater sensitivity of exact local water priorities than of aggregate burden. Changing only emergency-water destinations left shelter, fire-service, and municipal-facility outputs exactly unchanged in 9/9 same-seed invariance checks because service classes are evaluated separately (Appendix Table B11). These hypothetical placements bound sensitivity and do not identify the actual locations or urban–rural distribution of unresolved announcements."
(Page 33, Lines 704–716)

"Emergency-water loss is an especially clear example of destination geography amplifying network dependence, although incomplete location resolution limits the magnitude and local ranking that can be inferred. Under the uniform-placement sensitivity, aggregate emergency-water burden differed by −11.6% to −0.5% from the matched observed-only diagnostic, but lower-bound Top-30 overlap was 66.7%; the result therefore supports a conditional service-loss conclusion rather than precise local water prioritization. Within the class-separable model, changing emergency-water destinations cannot alter fire-service or municipal-facility rankings."
(Page 38, Lines 827–834)

"Appendix Table B11 treats the 26 unresolved announcements as a declared placement sensitivity rather than recovered data. In 50 replicates, the 18 Yatsushiro, six Uki, and two Hikawa records are distributed uniformly without replacement over eligible populated 125 m meshes in their source municipality and evaluated under five network seeds × 250 common Heavy-scenario closure draws. The expected affected-population range changes by −11.6% to −0.5% relative to the matched observed-only diagnostic, but community-frequency correlation and Top-30 overlap fall to 0.725 and 66.7% at their lower bounds. A same-seed test changes only water destinations and leaves shelter, fire-service, and municipal-facility loss, excess-time, and baseline arrays identical in 9/9 checks. This is a hypothetical sensitivity and not evidence of the actual missing locations."
(Appendix, Page 8, Lines 162–171)

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
