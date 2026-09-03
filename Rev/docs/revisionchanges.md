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

