# Manuscript Revision Changes

Schema: `kila-revision-changes/v1`

## reviewer-2/comment-3

### part-01

- Location: Methods > Rainfall and Official Threshold Scenarios, paragraph beginning 'Moderate, Heavy, and Extreme rainfall...'
- Reason: Define the all-area 100% threshold case as a no-retention model baseline rather than a physical no-earthquake counterfactual.
- Kila decisions: KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:07:49Z
- Author: Mike Li
- Markup SHA-256 before: `9a5b2cc11405513e2b5ab0cfc2d0c2ee396e31a3dde22f285bbf7ff0414a2f2d`
- Markup SHA-256 after: `8ac98ca9d82c13169c772666088776c4bafb3cd2676b70bc5264e31cbdb2f43e`
- Revision IDs: `1`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120749422359.reviewer-2-comment-3.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Because the available municipality geometry does not distinguish the two official Yatsushiro subareas, the central municipality-wide analysis uses an analyst-defined midpoint of 0.75, bounded by separate 0.70 and 0.80 assignments; the midpoint is not an official Yatsushiro value.
~~~~

- After:

~~~~text
For the paired comparison, f = 1.00 is assigned throughout Kumamoto to disable threshold retention while holding rainfall, terrain, road, network, service, and simulation inputs fixed. This is a no-retention-adjustment model baseline, not a physical no-earthquake counterfactual. Because the available municipality geometry does not distinguish the two official Yatsushiro subareas, the central municipality-wide analysis uses an analyst-defined midpoint of 0.75, bounded by separate 0.70 and 0.80 assignments; the midpoint is not an official Yatsushiro value.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "For the paired comparison, f = 1.00 is assigned throughout Kumamoto to disable threshold retention while holding rainfall, terrain, road, network, service, and simulation inputs fixed. This is a no-retention-adjustment model baseline, not a physical no-earthquake counterfactual. "

## reviewer-2/comment-2

### part-01

- Location: Methods > Rainfall and Official Threshold Scenarios, Equation 4 explanation
- Reason: Report the quantitative compatibility test and retain Equation 4 only as a relative scenario index.
- Kila decisions: KILA-D-20260903-001, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:03Z
- Author: Mike Li
- Markup SHA-256 before: `8ac98ca9d82c13169c772666088776c4bafb3cd2676b70bc5264e31cbdb2f43e`
- Markup SHA-256 after: `67c6b0935770a9bf799f574cecabc28d222ee6a9c84235c81168c8df4ab0376d`
- Revision IDs: `2`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120804044709.reviewer-2-comment-2.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The analysis assigns equal weights of 0.25 to the 1, 3, 24, and 72 h windows.
~~~~

- After:

~~~~text
The analysis assigns equal weights of 0.25 to the 1, 3, 24, and 72 h windows. The equal-weight choice is a transparent central reference rather than an empirically optimized parameterization. Compatibility was evaluated against a JMA-type reconstruction based on the published tank equations and Level-4 grid curves for 2,438 eligible events. The pooled Spearman correlation was 0.862 (station-cluster bootstrap 95% CI, 0.842–0.884), and applying the official factors produced median and 95th-percentile absolute relative errors of 0.0022 and 0.0054 across 513,702 valid grid–rainfall cells. All prespecified compatibility criteria were met; Equation 4 is therefore retained as a relative scenario index and is not relabelled as the operational JMA indicator.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The equal-weight choice is a transparent central reference rather than an empirically optimized parameterization. Compatibility was evaluated against a JMA-type reconstruction based on the published tank equations and Level-4 grid curves for 2,438 eligible events. The pooled Spearman correlation was 0.862 (station-cluster bootstrap 95% CI, 0.842–0.884), and applying the official factors produced median and 95th-percentile absolute relative errors of 0.0022 and 0.0054 across 513,702 valid grid–rainfall cells. All prespecified compatibility criteria were met; Equation 4 is therefore retained as a relative scenario index and is not relabelled as the operational JMA indicator."

### part-02

- Location: Discussion > Compound-Hazard Interpretation, paragraph beginning 'We use threshold retention...'
- Reason: Bound the compatibility claim and distinguish robust road ordering from scenario-sensitive consequence magnitude.
- Kila decisions: KILA-D-20260903-001, KILA-D-20260903-002, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:09:04Z
- Author: Mike Li
- Markup SHA-256 before: `9253328055ed544d6d7849a44c4f94f9f48865cbbe23ca5a812a208c0b4a8915`
- Markup SHA-256 after: `abe3a86a53b116db4dcbd9ed94ed586256ac3b4f549bd1ef2b07fac5191eb22f`
- Revision IDs: `6`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120904216662.reviewer-2-comment-2.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
It therefore does not measure continuous shaking, estimate a location-specific change in soil strength, or identify a causal threshold shift.
~~~~

- After:

~~~~text
The quantitative comparison with the JMA-type reconstruction supports applying the official factors to Equation 4 for directional scenario screening in the present event sample, but it does not turn X or H into an operational warning indicator. Across the tested parameterizations, road-priority order is more stable than absolute isolation estimates; consequence magnitudes are therefore treated as scenario-sensitive. It therefore does not measure continuous shaking, estimate a location-specific change in soil strength, or identify a causal threshold shift.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "The quantitative comparison with the JMA-type reconstruction supports applying the official factors to Equation 4 for directional scenario screening in the present event sample, but it does not turn X or H into an operational warning indicator. Across the tested parameterizations, road-priority order is more stable than absolute isolation estimates; consequence magnitudes are therefore treated as scenario-sensitive. "

## reviewer-2/comment-4

### part-01

- Location: Methods > Rainfall and Official Threshold Scenarios, Equation 6 explanation
- Reason: State the tested gamma range and identify gamma = 1.00 as a transparent reference rather than an estimated local coefficient.
- Kila decisions: KILA-D-20260903-002, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:18Z
- Author: Mike Li
- Markup SHA-256 before: `67c6b0935770a9bf799f574cecabc28d222ee6a9c84235c81168c8df4ab0376d`
- Markup SHA-256 after: `0f1705cf2fc185ab4b0f1d3a06ecbf29eee19fcfb99f0d827b753dc667191aca`
- Revision IDs: `3`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120819002048.reviewer-2-comment-4.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The logarithm represents rainfall intensity and threshold retention as multiplicative changes while reducing saturation at high loading.
~~~~

- After:

~~~~text
Sensitivity analyses use γ = 0.50 and 2.00 around this central value under five rainfall-window weighting schemes; γ = 1.00 is therefore a declared transparent reference rather than an estimated local coefficient. The logarithm represents rainfall intensity and threshold retention as multiplicative changes while reducing saturation at high loading.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "Sensitivity analyses use γ = 0.50 and 2.00 around this central value under five rainfall-window weighting schemes; γ = 1.00 is therefore a declared transparent reference rather than an estimated local coefficient. "

### part-02

- Location: Methods > Robustness, paragraph beginning 'Compound-hazard conclusions...'
- Reason: Align the robustness description with the implemented baseline, rainfall-window-weight, and gamma sensitivity analyses.
- Kila decisions: KILA-D-20260903-002, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:35Z
- Author: Mike Li
- Markup SHA-256 before: `0f1705cf2fc185ab4b0f1d3a06ecbf29eee19fcfb99f0d827b753dc667191aca`
- Markup SHA-256 after: `404c27cd64d1c51b49250a9d08e1694c0ea1a588b40705d3c633f7a6dd99416f`
- Revision IDs: `4`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120835664094.reviewer-2-comment-4.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The implemented checks vary rainfall temporal support, the unresolved Yatsushiro threshold assignment, external-road targets, closure mappings, simulation size, intervention costs and effects, and ranking comparators.
~~~~

- After:

~~~~text
The implemented checks vary rainfall temporal support, five rainfall-window weighting schemes, γ = 0.50, 1.00, and 2.00, the all-area f = 1.00 baseline, the unresolved Yatsushiro threshold assignment, external-road targets, closure mappings, simulation size, intervention costs and effects, and ranking comparators.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: ", five rainfall-window weighting schemes, γ = 0.50, 1.00, and 2.00, the all-area f = 1.00 baseline"

### part-03

- Location: Results > Earthquake-Adjusted Rainfall and Slope Disruption, paragraph beginning 'The declared retention settings...'
- Reason: Summarize that threshold retention and rainfall parameters affect consequence magnitude more than spatial road ordering and direct readers to Appendix Table B5.
- Kila decisions: KILA-D-20260903-002, KILA-D-20260903-003, KILA-D-20260903-005, KILA-D-20260903-006
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T03:08:50Z
- Author: Mike Li
- Markup SHA-256 before: `404c27cd64d1c51b49250a9d08e1694c0ea1a588b40705d3c633f7a6dd99416f`
- Markup SHA-256 after: `9253328055ed544d6d7849a44c4f94f9f48865cbbe23ca5a812a208c0b4a8915`
- Revision IDs: `5`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T120850465996.reviewer-2-comment-4.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The rainfall dimension therefore supports magnitude scaling and broader consequence scenarios, not spatial reprioritization of roads.
~~~~

- After:

~~~~text
The rainfall dimension therefore supports magnitude scaling and broader consequence scenarios, not spatial reprioritization of roads. The paired all-area f = 1.00 comparison and the 15-combination rainfall-parameter sensitivity are reported in Appendix Table B5. Official retention changes downstream consequence magnitude more strongly than road ordering, while alternative window weights and γ values leave road rankings stable but produce wider variation in expected isolation.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The paired all-area f = 1.00 comparison and the 15-combination rainfall-parameter sensitivity are reported in Appendix Table B5. Official retention changes downstream consequence magnitude more strongly than road ordering, while alternative window weights and γ values leave road rankings stable but produce wider variation in expected isolation."

## reviewer-3/comment-1

### part-01

- Location: Manuscript title
- Reason: Replace the potentially physical-sounding earthquake-adjusted title with an explicit post-earthquake rainfall-warning threshold scenario title.
- Kila decisions: KILA-D-20260903-008
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T04:38:19Z
- Author: Kila
- Markup SHA-256 before: `abe3a86a53b116db4dcbd9ed94ed586256ac3b4f549bd1ef2b07fac5191eb22f`
- Markup SHA-256 after: `3c58d205c576ab11abaa2e894368c9bef1fa12f977894048fbdc84fbbe6d8055`
- Revision IDs: `7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T133819803024.reviewer-3-comment-1.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `2e04fe98f25922c0d6367a917809937c6a7c2a5b42022f8c41bb9161722a8c77`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Earthquake-adjusted rainfall-triggered landslide disruption informs community isolation and emergency intervention priorities in Kumamoto Prefecture, Japan
~~~~

- After:

~~~~text
Post-earthquake rainfall-warning threshold scenarios for landslide-related road disruption, community isolation, and emergency intervention planning in Kumamoto Prefecture, Japan
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Earthquake-adjusted"
     - After: "Post-earthquake"
  2. `replace`
     - Before: "rainfall-triggered"
     - After: "rainfall-warning"
  3. `replace`
     - Before: "landslide"
     - After: "threshold scenarios for landslide-related road"
  4. `replace`
     - Before: " informs"
     - After: ","
  5. `insert`
     - Before: ""
     - After: ","
  6. `replace`
     - Before: "priorities"
     - After: "planning"

### part-02

- Location: Abstract, opening sentence
- Reason: State directly that post-earthquake adjustment is an operational warning-threshold scenario and not a physical earthquake-effect model.
- Kila decisions: KILA-D-20260903-008
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T04:38:33Z
- Author: Kila
- Markup SHA-256 before: `3c58d205c576ab11abaa2e894368c9bef1fa12f977894048fbdc84fbbe6d8055`
- Markup SHA-256 after: `9c20d0763000633d481f7d8b58a8e46071aea123e6ecedb628578d9f91acfa48`
- Revision IDs: `18`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T133833161509.reviewer-3-comment-1.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Post-earthquake rainfall can propagate slope instability through road networks into community isolation and service loss.
~~~~

- After:

~~~~text
Post-earthquake rainfall can propagate slope instability through road networks into community isolation and service loss. Here, post-earthquake adjustment denotes area-level operational retention of rainfall-warning criteria, not a model of ground motion, earthquake damage, or measured changes in slope strength.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Here, post-earthquake adjustment denotes area-level operational retention of rainfall-warning criteria, not a model of ground motion, earthquake damage, or measured changes in slope strength."

### part-03

- Location: Keywords
- Reason: Replace the misleading earthquake-adjusted keyword with the operational rainfall-warning criterion terminology.
- Kila decisions: KILA-D-20260903-008
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T04:38:48Z
- Author: Kila
- Markup SHA-256 before: `9c20d0763000633d481f7d8b58a8e46071aea123e6ecedb628578d9f91acfa48`
- Markup SHA-256 after: `6c2a41b755ce12f66f94511dde14fefef713f65dc5a70ad8d229cd8008c5bab1`
- Revision IDs: `19, 20, 21, 22, 23, 24`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T133848670117.reviewer-3-comment-1.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Compound hazards; Earthquake-adjusted rainfall thresholds; Landslide disruption; Road networks; Community isolation; Service accessibility
~~~~

- After:

~~~~text
Compound hazards; Post-earthquake rainfall-warning criteria; Landslide disruption; Road networks; Community isolation; Service accessibility
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Earthquake-adjusted"
     - After: "Post-earthquake"
  2. `replace`
     - Before: "rainfall"
     - After: "rainfall-warning"
  3. `replace`
     - Before: "thresholds"
     - After: "criteria"

### part-05

- Location: Results section heading
- Reason: Name the Results section for the operational threshold-retention contrast actually modeled.
- Kila decisions: KILA-D-20260903-008
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T04:39:32Z
- Author: Kila
- Markup SHA-256 before: `6c2a41b755ce12f66f94511dde14fefef713f65dc5a70ad8d229cd8008c5bab1`
- Markup SHA-256 after: `1f4ca90f560f1848c81691d129b2fee06f7962fe248ad40ff5624a5c48cbb5b0`
- Revision IDs: `25, 26, 27, 28`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T133932275703.reviewer-3-comment-1.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Earthquake-Adjusted Rainfall and Slope Disruption
~~~~

- After:

~~~~text
Operational Threshold Retention and Slope Disruption
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Earthquake-Adjusted"
     - After: "Operational"
  2. `replace`
     - Before: "Rainfall"
     - After: "Threshold Retention"

### part-06

- Location: Conclusions, opening sentence
- Reason: Condition the conclusion on post-earthquake rainfall-warning threshold scenarios instead of implying a physical earthquake-adjusted model.
- Kila decisions: KILA-D-20260903-008
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T04:39:49Z
- Author: Kila
- Markup SHA-256 before: `1f4ca90f560f1848c81691d129b2fee06f7962fe248ad40ff5624a5c48cbb5b0`
- Markup SHA-256 after: `824cac92cf2cdf15897aff4299b9486a9fddd3747403327cb24c8c8a14b5ceb8`
- Revision IDs: `29, 30, 31, 32, 33, 34, 35`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T133949876320.reviewer-3-comment-1.part-06.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Earthquake-adjusted rainfall scenarios identify where relative slope disruption may affect roads, where those road disruptions may isolate communities or remove basic-service access, and which road or community actions have the greatest conditional planning benefit.
~~~~

- After:

~~~~text
Under the post-earthquake rainfall-warning threshold scenarios, the framework identifies where relative slope disruption may affect roads, where those road disruptions may isolate communities or remove basic-service access, and which road or community actions have the greatest conditional planning benefit.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Earthquake-adjusted"
     - After: "Under"
  2. `replace`
     - Before: "rainfall"
     - After: "the post-earthquake rainfall-warning threshold"
  3. `insert`
     - Before: ""
     - After: ","
  4. `replace`
     - Before: "identify"
     - After: "the framework identifies"

### part-04

- Location: Figures > Figure 1 embedded drawing
- Reason: Replace the misleading earthquake-adjusted figure label with the approved post-earthquake threshold-retention wording.
- Kila decisions: KILA-D-20260903-008, KILA-D-20260903-009
- Mode: `figure-replace`
- Timestamp: 2026-09-03T04:47:55.195279Z
- Author: Kila
- Markup SHA-256 before: `824cac92cf2cdf15897aff4299b9486a9fddd3747403327cb24c8c8a14b5ceb8`
- Markup SHA-256 after: `9a2bf7de8a58e87b5521828168e819e7fb8ee6581561d6108ba5c4f2b0d002e7`
- Revision IDs: not applicable (approved embedded-media replacement)
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T134755195279.reviewer-3-comment-1.part-04.docx`
- Figure relationship: `rId9` -> `word/media/image1.png`
- Verified caption: Figure 1. Compound-hazard pathway from rainfall to intervention priorities
- Replacement asset: `data/results/figures/Figure_compound_hazard_decision_pathway.png`
- Original image SHA-256: `b3e8479eab67aec26f0cc4e6c5418bc5479fc6b49c2d09b42e7179aba6029cab`
- Replacement image SHA-256: `f48bc8c9ce314a357ab5b855d8aed5c7247df7066b3ca1f1c413d4a9ca9738af`
- Image format and dimensions preserved: `true` (PNG, 2400 x 1080, RGB)
- Non-target package members preserved byte-for-byte: `true`
- XML and DOCX ZIP verification: `passed`
- Track-revisions setting preserved: `true`
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`

## reviewer-4/comment-6

### part-01

- Location: Study Area and Data > Landslide Hazard and Rainfall Evidence, paragraph beginning 'We treat the interpreted landslide locations'
- Reason: Clarify that the numerical threshold-retention factors are not portable and define the conditions for applying the framework to another event or jurisdiction.
- Kila decisions: KILA-D-20260903-011
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T05:12:24Z
- Author: Kila
- Markup SHA-256 before: `9a2bf7de8a58e87b5521828168e819e7fb8ee6581561d6108ba5c4f2b0d002e7`
- Markup SHA-256 after: `da632f702065fabece747dc3b184474aa0f7f02d936cb51b8bd1b4e80e242f77`
- Revision IDs: `36`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T141225119861.reviewer-4-comment-6.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
We treat the threshold-retention factors as municipality- or subarea-level operational scenario settings rather than continuous shaking or site-specific soil-strength measurements (Zhang et al., 2025).
~~~~

- After:

~~~~text
We treat the threshold-retention factors as municipality- or subarea-level operational scenario settings rather than continuous shaking or site-specific soil-strength measurements (Zhang et al., 2025). The numerical values are event- and area-specific and are not transferred to another earthquake or jurisdiction. Applying the framework elsewhere requires locally issued or empirically estimated retention settings, a rainfall indicator compatible with how those settings were defined, and renewed compatibility and sensitivity checks before downstream consequences are interpreted.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The numerical values are event- and area-specific and are not transferred to another earthquake or jurisdiction. Applying the framework elsewhere requires locally issued or empirically estimated retention settings, a rainfall indicator compatible with how those settings were defined, and renewed compatibility and sensitivity checks before downstream consequences are interpreted."

### part-02

- Location: Discussion > Limitations and Future Research, paragraph beginning 'Future work should replace'
- Reason: Explain how InSAR and field shear-strength evidence could support a calibrated physical model without treating either source as a one-for-one substitute for an operational warning coefficient.
- Kila decisions: KILA-D-20260903-011
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T05:12:38Z
- Author: Kila
- Markup SHA-256 before: `da632f702065fabece747dc3b184474aa0f7f02d936cb51b8bd1b4e80e242f77`
- Markup SHA-256 after: `761a327214dec02ed50d5f8bd2df5b66ebd6cf4ee4518033af9d5c88ac7e0cbd`
- Revision IDs: `37`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T141238417280.reviewer-4-comment-6.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
A more complete post-event inventory using satellite, uncrewed aerial vehicle, and field observations could improve slope validation (Fu et al., 2025).
~~~~

- After:

~~~~text
A more complete post-event inventory using satellite, uncrewed aerial vehicle, and field observations could improve slope validation (Fu et al., 2025). Repeated InSAR deformation observations and targeted geotechnical measurements, including field shear-strength tests, could support a spatially explicit disturbance model where coverage and calibration are adequate. These data are complementary evidence rather than one-for-one substitutes for an operational warning coefficient; once validated, such a physical model could replace the administrative retention proxy at the susceptibility stage while the downstream road-network and consequence modules remain applicable.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Repeated InSAR deformation observations and targeted geotechnical measurements, including field shear-strength tests, could support a spatially explicit disturbance model where coverage and calibration are adequate. These data are complementary evidence rather than one-for-one substitutes for an operational warning coefficient; once validated, such a physical model could replace the administrative retention proxy at the susceptibility stage while the downstream road-network and consequence modules remain applicable."

### part-03

- Location: Conclusions, sentence beginning 'Official threshold adjustments'
- Reason: Limit the decision-use claim to the event and area for which the operational factors were issued.
- Kila decisions: KILA-D-20260903-011
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T05:12:55Z
- Author: Kila
- Markup SHA-256 before: `761a327214dec02ed50d5f8bd2df5b66ebd6cf4ee4518033af9d5c88ac7e0cbd`
- Markup SHA-256 after: `c5fdf67abe4fcd000a56364aebb1ae5a46c9a6f461826e16b48f08afe8725b46`
- Revision IDs: `38, 39`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T141255129132.reviewer-4-comment-6.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Official threshold adjustments can therefore inform more than a revised hazard map: they can support a consistent comparison of inspection targets, access-protection candidates, community preparedness needs, and resource-pre-positioning priorities before heavy rainfall.
~~~~

- After:

~~~~text
Within the event and area for which they are issued, official threshold adjustments can therefore inform more than a revised hazard map: they can support a consistent comparison of inspection targets, access-protection candidates, community preparedness needs, and resource-pre-positioning priorities before heavy rainfall.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Official"
     - After: "Within the event and area for which they are issued, official"

## reviewer-2/comment-5

### part-01

- Location: Methods > slope-to-road transfer paragraph
- Reason: Define the influence set, transfer-weight parameters, physical scale, and Kumamoto applicability checks requested by Reviewer 2.
- Kila decisions: KILA-D-20260903-015, KILA-D-20260903-016
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T06:21:07Z
- Author: Kila
- Markup SHA-256 before: `c5fdf67abe4fcd000a56364aebb1ae5a46c9a6f461826e16b48f08afe8725b46`
- Markup SHA-256 after: `a44e75f67e1c75d36a24066f343bb0498e77407f2555bcd66c53aa8ca237d296`
- Revision IDs: `40, 41, 42, 43, 44`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T152108927655.reviewer-2-comment-5.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
For road section e, influence set Ue contains terrain cells with positive relief above the road and downhill alignment toward it. GIS-based landslide-risk mapping provides a basis for road-slope prioritization and obstruction analysis (Cheng et al., 2026). Transfer weight qie decreases with distance and represents the relative capacity of cell i to affect section e. Nearby cells below the road, or cells whose downslope direction is inconsistent with the road location, do not contribute in the same way as aligned upslope cells. Equation 7 uses a normalized weighted mean, rather than a noisy-OR expression, so a longer section does not receive a larger score solely because it contains more sampled cells.
~~~~

- After:

~~~~text
For road section e, each line component is sampled at normalized fractions 0.20, 0.50, and 0.80 on the 752 × 950 WGS84 road-transfer grid. At the study-area midpoint, a grid cell is approximately 144 m east–west by 170 m north–south after 16 × 16 aggregation of the native 9.55 m DEM pixels. For sample point j, influence set Uej contains every noncentral offset with dx and dy in [−3, 3] for which the candidate cell is at least 10 m above the road point and the cosine alignment between the local upslope gradient and the road-to-cell vector is at least 0.20. These settings correspond to an angular tolerance of 78.5° in raster-coordinate space, axis-aligned reaches of approximately 432–509 m, and a maximum diagonal reach of approximately 668 m. Transfer weight qij multiplies an exponential distance term with a 2.5-cell e-folding length, alignment clipped to [0, 1], and a relief term clipped to [0.20, 1.00] after division by 100 m. Contributions from the three sample points and all line components are pooled to the parent road section. GIS-based landslide-risk mapping provides a basis for road-slope prioritization and obstruction analysis (Cheng et al., 2026). Equation 7 uses a normalized weighted mean, rather than a noisy-OR expression, so a longer section does not receive a larger score solely because it contains more sampled cells. These parameters define a regional directional-screening envelope rather than a calibrated runout model; applicability is evaluated through matched restriction correspondence and the prespecified parameter sensitivity reported in Appendix Tables B6 and B7.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "For road section e, influence set Ue contains terrain cells with positive relief above the road and downhill alignment toward it."
     - After: "For road section e, each line component is sampled at normalized fractions 0.20, 0.50, and 0.80 on the 752 × 950 WGS84 road-transfer grid. At the study-area midpoint, a grid cell is approximately 144 m east–west by 170 m north–south after 16 × 16 aggregation of the native 9.55 m DEM pixels. For sample point j, influence set Uej contains every noncentral offset with dx and dy in [−3, 3] for which the candidate cell is at least 10 m above the road point and the cosine alignment between the local upslope gradient and the road-to-cell vector is at least 0.20. These settings correspond to an angular tolerance of 78.5° in raster-coordinate space, axis-aligned reaches of approximately 432–509 m, and a maximum diagonal reach of approximately 668 m. Transfer weight qij multiplies an exponential distance term with a 2.5-cell e-folding length, alignment clipped to [0, 1], and a relief term clipped to [0.20, 1.00] after division by 100 m. Contributions from the three sample points and all line components are pooled to the parent road section."
  2. `structured-replace`
     - Before: ". Transfer weight qie decreases with distance and represents the relative capacity of cell i to affect section e. Nearby cells below the road, or cells whose downslope direction is inconsistent with the road location, do not contribute in the same way as aligned upslope cells"
     - After: ""
  3. `structured-replace`
     - Before: "."
     - After: ". These parameters define a regional directional-screening envelope rather than a calibrated runout model; applicability is evaluated through matched restriction correspondence and the prespecified parameter sensitivity reported in Appendix Tables B6 and B7."

### part-02

- Location: Results > Road Disruption and Observed Restriction Correspondence, final sentence of the first paragraph
- Reason: Report the validated transfer sensitivity and its ranking boundary.
- Kila decisions: KILA-D-20260903-015
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T06:21:16Z
- Author: Kila
- Markup SHA-256 before: `a44e75f67e1c75d36a24066f343bb0498e77407f2555bcd66c53aa8ca237d296`
- Markup SHA-256 after: `6505def40e66418a6a7099146c80e0f0b1a3185197b0a7b361438d58fea25b84`
- Revision IDs: `45`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T152116687351.reviewer-2-comment-5.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The Heavy-score background in panel d locates the 93 matched road sections used for ranking validation.
~~~~

- After:

~~~~text
The Heavy-score background in panel d locates the 93 matched road sections used for ranking validation. Across the 15 prespecified transfer specifications, the minimum Spearman correlation on the union of supported roads was 0.676, the minimum top-1% overlap was 0.428, and the minimum overlap of Heavy candidate sets was 0.764. Neighborhood reach and minimum relief changed road support and exact top-ranked membership most strongly, whereas alignment, distance decay, relief scaling, and road-sampling alternatives were more stable individually. Matched road-evidence concordance ranged from 0.614 to 0.687 and remained above 0.50 under every specification. The restriction evidence therefore supports a persistent directional ranking signal, but not parameter-invariant identification of the exact highest-ranked roads.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " Across the 15 prespecified transfer specifications, the minimum Spearman correlation on the union of supported roads was 0.676, the minimum top-1% overlap was 0.428, and the minimum overlap of Heavy candidate sets was 0.764. Neighborhood reach and minimum relief changed road support and exact top-ranked membership most strongly, whereas alignment, distance decay, relief scaling, and road-sampling alternatives were more stable individually. Matched road-evidence concordance ranged from 0.614 to 0.687 and remained above 0.50 under every specification. The restriction evidence therefore supports a persistent directional ranking signal, but not parameter-invariant identification of the exact highest-ranked roads."

### part-03

- Location: Results > community isolation paragraph
- Reason: Update five-seed central estimates and report downstream transfer-specification bounds.
- Kila decisions: KILA-D-20260903-015, KILA-D-20260903-016
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T06:21:25Z
- Author: Kila
- Markup SHA-256 before: `6505def40e66418a6a7099146c80e0f0b1a3185197b0a7b361438d58fea25b84`
- Markup SHA-256 after: `7012a736023674728b539112fc50ff86d1e8cfa46869149a2a4632e07eafa0ad`
- Revision IDs: `46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T152126435990.reviewer-2-comment-5.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Expected isolated population rises monotonically with rainfall severity. Across five simulation seeds, Figure 6 reports means of 186.4 residents under Moderate rainfall, 1,106.9 under Heavy rainfall, and 5,031.0 under Extreme rainfall. The Heavy result ranges from 1,093.9 to 1,118.2 across seeds, with a standard deviation of 8.8, indicating small Monte Carlo variation relative to the scenario contrast. The maps show that the increase is concentrated in selected road-dependent communities rather than distributed uniformly across populated cells. Alternative external targets yield 1,044–1,108 isolated residents under Heavy rainfall, whereas alternative closure mappings produce the wider 343–2,309 range.
~~~~

- After:

~~~~text
Expected isolated population rises monotonically with rainfall severity. Across five simulation seeds, Figure 6 reports means of 189.1 residents under Moderate rainfall, 1,121.7 under Heavy rainfall, and 5,032.2 under Extreme rainfall. The Heavy result ranges from 1,103.7 to 1,139.7 across seeds, with a standard deviation of 13.9, indicating small Monte Carlo variation relative to the scenario contrast. The maps show that the increase is concentrated in selected road-dependent communities rather than distributed uniformly across populated cells. Alternative external targets yield 1,044–1,108 isolated residents under Heavy rainfall, whereas alternative closure mappings produce the wider 343–2,309 range. Reconstructing the candidate-road set and closure mapping for the strict and permissive transfer boundaries changes Heavy expected isolation to 523.5 and 2,256.3 residents, respectively, compared with 1,121.7 centrally.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "186.4"
     - After: "189.1"
  2. `structured-replace`
     - Before: "1,106.9"
     - After: "1,121.7"
  3. `structured-replace`
     - Before: "5,031.0"
     - After: "5,032.2"
  4. `structured-replace`
     - Before: "1,093.9"
     - After: "1,103.7"
  5. `structured-replace`
     - Before: "1,118.2"
     - After: "1,139.7"
  6. `structured-replace`
     - Before: "8.8"
     - After: "13.9"
  7. `structured-replace`
     - Before: "."
     - After: ". Reconstructing the candidate-road set and closure mapping for the strict and permissive transfer boundaries changes Heavy expected isolation to 523.5 and 2,256.3 residents, respectively, compared with 1,121.7 centrally."

### part-04

- Location: Results > older-population paragraph
- Reason: Update five-seed central estimates and report downstream transfer-specification bounds for older residents.
- Kila decisions: KILA-D-20260903-015, KILA-D-20260903-016
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T06:21:35Z
- Author: Kila
- Markup SHA-256 before: `7012a736023674728b539112fc50ff86d1e8cfa46869149a2a4632e07eafa0ad`
- Markup SHA-256 after: `3246e55b569ae836fdcc696e68ac9b8f1e446f806e8846909dc0a68071522451`
- Revision IDs: `60, 61`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T152135951152.reviewer-2-comment-5.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Residents aged 65 years or older account for a substantial part of the simulated burden. Their five-seed mean expected isolated population is 96.7 under Moderate rainfall, 603.1 under Heavy rainfall, and 2,789.2 under Extreme rainfall. The age-specific totals follow the same scenario order, but their geography depends on the population composition of affected communities. The Extreme older-population map uses the same isolation-frequency scale as the total-population panels, so demographic burden reflects both network dependence and the number of older residents exposed.
~~~~

- After:

~~~~text
Residents aged 65 years or older account for a substantial part of the simulated burden. Their five-seed mean expected isolated population is 98.0 under Moderate rainfall, 610.2 under Heavy rainfall, and 2,789.3 under Extreme rainfall. Under the strict and permissive transfer boundaries, the Heavy estimate is 280.0 and 1,249.9 older residents, respectively. The age-specific totals follow the same scenario order, but their geography depends on the population composition of affected communities. The Extreme older-population map uses the same isolation-frequency scale as the total-population panels, so demographic burden reflects both network dependence and the number of older residents exposed.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "Their five-seed mean expected isolated population is 96.7 under Moderate rainfall, 603.1 under Heavy rainfall, and 2,789.2 under Extreme rainfall."
     - After: "Their five-seed mean expected isolated population is 98.0 under Moderate rainfall, 610.2 under Heavy rainfall, and 2,789.3 under Extreme rainfall. Under the strict and permissive transfer boundaries, the Heavy estimate is 280.0 and 1,249.9 older residents, respectively."

### part-05

- Location: Results > service-loss paragraph
- Reason: Update five-seed service estimates and report downstream transfer-specification bounds.
- Kila decisions: KILA-D-20260903-015, KILA-D-20260903-016
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T06:21:46Z
- Author: Kila
- Markup SHA-256 before: `3246e55b569ae836fdcc696e68ac9b8f1e446f806e8846909dc0a68071522451`
- Markup SHA-256 after: `23c7fc1582af3b2a1ea19150f1c9ebea92e4782611e1b894a0d7fb4cf4a6443b`
- Revision IDs: `62, 63, 64, 65, 66, 67`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T152147192829.reviewer-2-comment-5.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Heavy-rainfall road disruption produces different burdens across service classes. Figure 7 gives five-seed mean populations losing reachability of 600.3 for shelters, 1,251.5 for fire services, and 923.0 for municipal facilities. These primary comparisons show that destination geography and network alternatives shape service consequences beyond external-road isolation. Emergency-water routing yields 7,969.1 affected residents, but only 10 geolocated destinations among 36 announcements enter the network. That result is retained as conditional sensitivity evidence rather than a fourth co-equal service estimate, and incomplete destination geography does not establish the direction of bias in the loss magnitude.
~~~~

- After:

~~~~text
Heavy-rainfall road disruption produces different burdens across service classes. Figure 7 gives five-seed mean populations losing reachability of 609.9 for shelters, 1,286.7 for fire services, and 937.3 for municipal facilities. Across the strict and permissive transfer boundaries, the corresponding ranges are 264.6–1,303.9, 799.8–3,433.9, and 480.6–1,698.5 residents. These primary comparisons show that destination geography, network alternatives, and slope-to-road transfer assumptions shape service consequences beyond external-road isolation. Emergency-water routing yields 7,789.8 affected residents centrally and 3,872.8–21,189.4 across the transfer boundaries, but only 10 geolocated destinations among 36 announcements enter the network. That result is retained as conditional sensitivity evidence rather than a fourth co-equal service estimate, and incomplete destination geography does not establish the direction of bias in the loss magnitude.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "Figure 7 gives five-seed mean populations losing reachability of 600.3 for shelters, 1,251.5 for fire services, and 923.0 for municipal facilities."
     - After: "Figure 7 gives five-seed mean populations losing reachability of 609.9 for shelters, 1,286.7 for fire services, and 937.3 for municipal facilities. Across the strict and permissive transfer boundaries, the corresponding ranges are 264.6–1,303.9, 799.8–3,433.9, and 480.6–1,698.5 residents."
  2. `structured-replace`
     - Before: "destination geography and network alternatives"
     - After: "destination geography, network alternatives, and slope-to-road transfer assumptions"
  3. `structured-replace`
     - Before: "Emergency-water routing yields 7,969.1 affected residents"
     - After: "Emergency-water routing yields 7,789.8 affected residents centrally and 3,872.8–21,189.4 across the transfer boundaries"

### part-06

- Location: Discussion > Compound-Hazard Interpretation, sentence beginning 'Across the tested parameterizations'
- Reason: Distinguish stable rainfall-parameter rankings from materially sensitive slope-to-road boundaries.
- Kila decisions: KILA-D-20260903-015
- Mode: `reedit`
- Revises prior parts: reviewer-2/comment-2#part-02
- Timestamp: 2026-09-03T06:21:54Z
- Author: Kila
- Markup SHA-256 before: `23c7fc1582af3b2a1ea19150f1c9ebea92e4782611e1b894a0d7fb4cf4a6443b`
- Markup SHA-256 after: `e1c0085e4883c99cb752e0cb119566e42ba712c7a41d9748a9ec64509a7b7e4e`
- Revision IDs: `6`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T152154938953.reviewer-2-comment-5.part-06.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Across the tested parameterizations, road-priority order is more stable than absolute isolation estimates; consequence magnitudes are therefore treated as scenario-sensitive.
~~~~

- After:

~~~~text
Rainfall-window and γ alternatives leave road order comparatively stable, whereas slope-to-road neighborhood and relief boundaries materially change supported and top-ranked roads. Exact road priorities and consequence magnitudes are therefore treated as parameter-conditional.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Across"
     - After: "Rainfall-window"
  2. `replace`
     - Before: "the"
     - After: "and"
  3. `replace`
     - Before: "tested"
     - After: "γ"
  4. `replace`
     - Before: "parameterizations,"
     - After: "alternatives"
  5. `replace`
     - Before: "road-priority"
     - After: "leave road"
  6. `replace`
     - Before: "is more"
     - After: "comparatively"
  7. `insert`
     - Before: ""
     - After: ","
  8. `replace`
     - Before: "than"
     - After: "whereas"
  9. `replace`
     - Before: "absolute"
     - After: "slope-to-road"
  10. `replace`
     - Before: "isolation"
     - After: "neighborhood"
  11. `replace`
     - Before: "estimates;"
     - After: "and relief boundaries materially change supported and top-ranked roads. Exact road priorities and"
  12. `replace`
     - Before: "scenario-sensitive"
     - After: "parameter-conditional"

### part-07

- Location: Discussion > Strengths, Limitations, and Future Work, first paragraph
- Reason: State the transfer-scale, physical-runout, optimization, and local-applicability boundaries.
- Kila decisions: KILA-D-20260903-015
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T06:22:05Z
- Author: Kila
- Markup SHA-256 before: `e1c0085e4883c99cb752e0cb119566e42ba712c7a41d9748a9ec64509a7b7e4e`
- Markup SHA-256 after: `35e43708f8a9b5a6da64b953f36aa78236ab31aa5ccf9af73834f91cc0e0ff22`
- Revision IDs: `68, 69, 70, 71, 72, 73, 74`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T152205871354.reviewer-2-comment-5.part-07.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Landslide points do not define absence, restriction records do not cover every road failure, and slope-to-road transfer approximates runout through relief, alignment, and distance.
~~~~

- After:

~~~~text
Landslide points do not define absence, and restriction records do not cover every road failure. Slope-to-road transfer approximates runout through relief, alignment, and distance on an approximately 150 m screening grid rather than through a calibrated physical runout model. Its neighborhood and relief settings materially affect road support, exact top-ranked membership, and downstream consequence magnitude; the central specification is therefore a transparent reference rather than an optimized local model.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " and"
  2. `replace`
     - Before: ","
     - After: "."
  3. `replace`
     - Before: "and slope-to-road"
     - After: "Slope-to-road"
  4. `insert`
     - Before: ""
     - After: " on an approximately 150 m screening grid rather than through a calibrated physical runout model"
  5. `insert`
     - Before: ""
     - After: " Its neighborhood and relief settings materially affect road support, exact top-ranked membership, and downstream consequence magnitude; the central specification is therefore a transparent reference rather than an optimized local model."

## reviewer-4/comment-2

### part-01

- Location: Methods > Directional Slope-to-Road Translation, transfer-weight sentence
- Reason: Make the transfer-weight index and sample-point aggregation consistent with the implemented Equation 7 definition.
- Kila decisions: KILA-D-20260903-018, KILA-D-20260903-019
- Mode: `structured-reedit`
- Revises prior parts: reviewer-2/comment-5#part-01
- Timestamp: 2026-09-03T07:30:50Z
- Author: Kila
- Markup SHA-256 before: `35e43708f8a9b5a6da64b953f36aa78236ab31aa5ccf9af73834f91cc0e0ff22`
- Markup SHA-256 after: `0f2a0b1082e5e53c80c0901c6c0ec0e9067a7fe1af6cbcc913240ee35c5ef17d`
- Revision IDs: `44`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T163050868009.reviewer-4-comment-2.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Transfer weight qij multiplies an exponential distance term with a 2.5-cell e-folding length, alignment clipped to [0, 1], and a relief term clipped to [0.20, 1.00] after division by 100 m.
~~~~

- After:

~~~~text
With j indexing the component-level sample points described above, the aggregated transfer weight qie sums, over every eligible j, the product of an exponential distance term with a 2.5-cell e-folding length, alignment clipped to [0, 1], and a relief term clipped to [0.20, 1.00] after division by 100 m.
~~~~

- Minimal tracked fragments:
  1. `structured-reedit`
     - Before: "Transfer weight qij multiplies"
     - After: "With j indexing the component-level sample points described above, the aggregated transfer weight qie sums, over every eligible j, the product of"

### part-02

- Location: Methods > Directional Slope-to-Road Translation, final sentence before Equation 7
- Reason: Correct the Appendix table references after the readability-driven split of Table B6.
- Kila decisions: KILA-D-20260903-018
- Mode: `reedit`
- Revises prior parts: reviewer-2/comment-5#part-01
- Timestamp: 2026-09-03T07:30:51Z
- Author: Kila
- Markup SHA-256 before: `0f2a0b1082e5e53c80c0901c6c0ec0e9067a7fe1af6cbcc913240ee35c5ef17d`
- Markup SHA-256 after: `0bdba40991c38f45c0d21831f94c34712734be186153194c0357d008f2bbdb9e`
- Revision IDs: `41`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T163051284917.reviewer-4-comment-2.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
These parameters define a regional directional-screening envelope rather than a calibrated runout model; applicability is evaluated through matched restriction correspondence and the prespecified parameter sensitivity reported in Appendix Tables B6 and B7.
~~~~

- After:

~~~~text
These parameters define a regional directional-screening envelope rather than a calibrated runout model; applicability is evaluated through matched restriction correspondence and the prespecified parameter sensitivity reported in Appendix Tables B6a, B6b, and B7.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "B6"
     - After: "B6a, B6b,"

### part-03

- Location: Methods > Directional Slope-to-Road Translation, displayed Equation 7
- Reason: Provide the explicit implemented influence-set, transfer-weight, and normalized road-score formulation requested by Reviewer 4.
- Kila decisions: KILA-D-20260903-018, KILA-D-20260903-019
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T07:30:51Z
- Author: Kila
- Markup SHA-256 before: `0bdba40991c38f45c0d21831f94c34712734be186153194c0357d008f2bbdb9e`
- Markup SHA-256 after: `13e2423c9b75978c7558f7a6f6be2964a925f9eb974ca8feece942cf7b34af82`
- Revision IDs: `75, 76`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T163051770588.reviewer-4-comment-2.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
De(r,f)=i∈Ue​qieHi(r,f)i∈Ue​qie.
~~~~

- After:

~~~~text
Δzije=zi−zje,  dije=oije2,  aije=∇ziToijemax​∇zi2dije,10−6,Uej=i:oije=(dx,dy), dx,dy∈{−3,…,3}, (dx,dy)≠(0,0), Δzije≥10, aije≥0.20,Ue=⋃j∈JeUej,qie=j:i∈Uej​exp​−dije2.5clip(aije,0,1)clip​Δzije100,0.20,1.00,De(r,f)=i∈Ue​qieHi(r,f)i∈Ue​qie,i∈Ue​qie>0,0,otherwise.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "De(r,f)=i∈Ue​qieHi(r,f)i∈Ue​qie."
     - After: "Δzije=zi−zje,  dije=oije2,  aije=∇ziToijemax​∇zi2dije,10−6,Uej=i:oije=(dx,dy), dx,dy∈{−3,…,3}, (dx,dy)≠(0,0), Δzije≥10, aije≥0.20,Ue=⋃j∈JeUej,qie=j:i∈Uej​exp​−dije2.5clip(aije,0,1)clip​Δzije100,0.20,1.00,De(r,f)=i∈Ue​qieHi(r,f)i∈Ue​qie,i∈Ue​qie>0,0,otherwise."

### part-04

- Location: Results > Road Disruption and Observed Restriction Correspondence, final sentence of the second paragraph
- Reason: Distinguish road-level ranking correspondence from independent validation of physical runout or deposit extent.
- Kila decisions: KILA-D-20260903-018
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T07:30:52Z
- Author: Kila
- Markup SHA-256 before: `13e2423c9b75978c7558f7a6f6be2964a925f9eb974ca8feece942cf7b34af82`
- Markup SHA-256 after: `65ff60ad786c35761df73031ffdb4e32e3a29d6927ef03a970969f0857ff597f`
- Revision IDs: `77`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T163052166318.reviewer-4-comment-2.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
It does not establish scenario-sensitive spatial ranking, because Moderate, Heavy, and Extreme scores preserve almost the same order, and it does not identify a closure rate among unreported roads.
~~~~

- After:

~~~~text
It does not establish scenario-sensitive spatial ranking, because Moderate, Heavy, and Extreme scores preserve almost the same order, and it does not identify a closure rate among unreported roads. The matched restriction comparison evaluates road-level ranking correspondence; it does not independently validate landslide-deposit extent or physical runout geometry, because the available GSI inventory comprises 1,044 interpreted point locations rather than mapped deposit polygons.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: " The matched restriction comparison evaluates road-level ranking correspondence; it does not independently validate landslide-deposit extent or physical runout geometry, because the available GSI inventory comprises 1,044 interpreted point locations rather than mapped deposit polygons."

### part-05

- Location: Discussion > Strengths, Limitations, and Future Research, first paragraph
- Reason: Avoid implying independent physical runout validation when the evidence is a separate road-restriction dataset.
- Kila decisions: KILA-D-20260903-018
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T07:30:52Z
- Author: Kila
- Markup SHA-256 before: `65ff60ad786c35761df73031ffdb4e32e3a29d6927ef03a970969f0857ff597f`
- Markup SHA-256 after: `9dd73495f367881511e728abdfb2b7d26a015030855cd521a5007b0555d0aa76`
- Revision IDs: `78, 79, 80`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T163052554976.reviewer-4-comment-2.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The framework uses readable score construction, spatially separated validation, independent road-restriction correspondence, ordered common-random-number simulations, age-specific population consequences, and comparator portfolios.
~~~~

- After:

~~~~text
The framework uses readable score construction, spatially separated slope validation, road-restriction correspondence on a separate infrastructure dataset, ordered common-random-number simulations, age-specific population consequences, and comparator portfolios.
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "slope "
  2. `delete`
     - Before: " independent"
     - After: ""
  3. `insert`
     - Before: ""
     - After: " on a separate infrastructure dataset"

### part-06

- Location: Discussion > Strengths, Limitations, and Future Research, second paragraph
- Reason: State the event-specific evidence required to calibrate and independently validate a future physical runout model.
- Kila decisions: KILA-D-20260903-018
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T07:30:52Z
- Author: Kila
- Markup SHA-256 before: `9dd73495f367881511e728abdfb2b7d26a015030855cd521a5007b0555d0aa76`
- Markup SHA-256 after: `7860226fbdb1d7818ececb3e5329bf746fa778990f204e0cd8bfa505978319fe`
- Revision IDs: `81, 82, 83, 84, 85, 86, 87, 88, 89`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T163052946089.reviewer-4-comment-2.part-06.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Physically informed runout could replace the directional transfer approximation, while blockage-duration and repair-time models could distinguish short interruption from prolonged isolation.
~~~~

- After:

~~~~text
A physically based runout model could replace the directional transfer approximation once event-specific source and deposit polygons, material or rheological parameters, and independent footprint or road-impact observations are available for calibration and validation; blockage-duration and repair-time models could then distinguish short interruption from prolonged isolation.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Physically"
     - After: "A"
  2. `replace`
     - Before: "informed"
     - After: "physically based"
  3. `insert`
     - Before: ""
     - After: " model"
  4. `insert`
     - Before: ""
     - After: " once event-specific source and deposit polygons"
  5. `replace`
     - Before: "while"
     - After: "material or rheological parameters, and independent footprint or road-impact observations are available for calibration and validation;"
  6. `insert`
     - Before: ""
     - After: " then"

