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

## reviewer-2/comment-7

### part-01

- Location: Abstract, sentence beginning 'The Heavy Road score attained'
- Reason: Replace snapshot-level road validation language with the approved event-deduplicated trigger-audit interpretation.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:17:26Z
- Author: Mike Li
- Markup SHA-256 before: `7860226fbdb1d7818ececb3e5329bf746fa778990f204e0cd8bfa505978319fe`
- Markup SHA-256 after: `24c7af6bb61d6784897c498c48085b10347e22cbf0ea6079b7aa8f9d15ecfd5e`
- Revision IDs: `90, 91`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T201726993491.reviewer-2-comment-7.part-01.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The Heavy Road score attained matched concordance of 0.646, compared with 0.556 for road length and 0.494 for warning-zone exposure under the same matched-control design.
~~~~

- After:

~~~~text
An event-deduplicated audit identified 10 earthquake-proximate mass-movement restriction episodes; their Heavy-score concordance was 0.723 (episode-cluster bootstrap 95% CI 0.598–0.840), but zero preceding 72-h rainfall across the audited JMA station network means that this evidence provides only supplementary road-ranking correspondence, not validation of rainfall-triggered disruption.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "The Heavy Road score attained matched concordance of 0.646, compared with 0.556 for road length and 0.494 for warning-zone exposure under the same matched-control design."
     - After: "An event-deduplicated audit identified 10 earthquake-proximate mass-movement restriction episodes; their Heavy-score concordance was 0.723 (episode-cluster bootstrap 95% CI 0.598–0.840), but zero preceding 72-h rainfall across the audited JMA station network means that this evidence provides only supplementary road-ranking correspondence, not validation of rainfall-triggered disruption."

### part-02

- Location: Study Area, sentence beginning 'The interpreted 2016 landslide inventory'
- Reason: Clarify the distinct validation roles of the 2016 landslide inventory and the dry 2026 restriction evidence.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:17:27Z
- Author: Mike Li
- Markup SHA-256 before: `24c7af6bb61d6784897c498c48085b10347e22cbf0ea6079b7aa8f9d15ecfd5e`
- Markup SHA-256 after: `c23c7e9ef11c7f8e18d11866e3722ae42019e3e23f8bf82f53510b647f89e1f3`
- Revision IDs: `92, 93`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T201727859544.reviewer-2-comment-7.part-02.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
The interpreted 2016 landslide inventory is used only for historical slope-ranking validation; late-July to early-August 2026 restriction records provide separate road-ranking evidence for the application stage.
~~~~

- After:

~~~~text
The interpreted 2016 landslide inventory is used only for historical slope-ranking validation. Late-July to early-August 2026 restriction records are retained only as supplementary correspondence evidence for earthquake-proximate mass-movement effects on roads; the absence of preceding rainfall prevents their use as validation of rainfall-triggered disruption.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "The interpreted 2016 landslide inventory is used only for historical slope-ranking validation; late-July to early-August 2026 restriction records provide separate road-ranking evidence for the application stage."
     - After: "The interpreted 2016 landslide inventory is used only for historical slope-ranking validation. Late-July to early-August 2026 restriction records are retained only as supplementary correspondence evidence for earthquake-proximate mass-movement effects on roads; the absence of preceding rainfall prevents their use as validation of rainfall-triggered disruption."

### part-03

- Location: Methods > Road Network, Communities, Population, and Basic Services
- Reason: State the event-deduplication and trigger-audit boundary before using restriction records as supplementary correspondence evidence.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:17:28Z
- Author: Mike Li
- Markup SHA-256 before: `c23c7e9ef11c7f8e18d11866e3722ae42019e3e23f8bf82f53510b647f89e1f3`
- Markup SHA-256 after: `e28c18ce75d0fe48b65f198a1c806dc32806fbc70c46d7dde42ed5b0381bf585`
- Revision IDs: `94, 95`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T201728612117.reviewer-2-comment-7.part-03.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Restriction snapshots are deduplicated and linked to plausible network edges for an independent test of whether the road score ranks observed landslide-related disruption above comparator rankings. Because reporting intensity and restriction causes vary, these records validate correspondence with observed disruption but do not define the rate at which unreported road sections remained open.
~~~~

- After:

~~~~text
Repeated restriction snapshots are consolidated into physical episodes and linked to plausible network edges. Source reasons, timing, and official event-window rainfall observations are audited before the records are used as supplementary correspondence evidence for earthquake-proximate rockfall, slope-collapse, and sediment-inflow restrictions. Because the sources do not explicitly code the trigger and the audited event window was dry, these records do not validate rainfall-triggered closure, identify unaffected roads, or calibrate a failure probability.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "Restriction snapshots are deduplicated and linked to plausible network edges for an independent test of whether the road score ranks observed landslide-related disruption above comparator rankings. Because reporting intensity and restriction causes vary, these records validate correspondence with observed disruption but do not define the rate at which unreported road sections remained open."
     - After: "Repeated restriction snapshots are consolidated into physical episodes and linked to plausible network edges. Source reasons, timing, and official event-window rainfall observations are audited before the records are used as supplementary correspondence evidence for earthquake-proximate rockfall, slope-collapse, and sediment-inflow restrictions. Because the sources do not explicitly code the trigger and the audited event window was dry, these records do not validate rainfall-triggered closure, identify unaffected roads, or calibrate a failure probability."

### part-06

- Location: Results > Analytical Coverage and Validation Performance
- Reason: Report event-weighted concordance, episode-cluster uncertainty, and paired comparator contrasts with the correct trigger boundary.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:17:29Z
- Author: Mike Li
- Markup SHA-256 before: `e28c18ce75d0fe48b65f198a1c806dc32806fbc70c46d7dde42ed5b0381bf585`
- Markup SHA-256 after: `4d89b322be97ea86df028166a4eb673ce832636e698a29a4eac18e28b08d97ff`
- Revision IDs: `96, 97`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T201730201872.reviewer-2-comment-7.part-06.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Road validation retains 93 matched sections representing 94 evidence cases. Under the Heavy score, matched concordance is 0.646 with a section-bootstrap 95% interval of 0.586–0.705, compared with 0.556 for road length and 0.494 for warning-zone exposure. These contrasts support relative ranking correspondence under the matched-control design, although the intervals and presence-only evidence preclude claims of calibrated closure probability or decisive predictive superiority.
~~~~

- After:

~~~~text
The trigger audit retains 10 physical restriction episodes linked to 94 sections, of which 93 have eligible controls. Under equal episode weighting, Heavy-score concordance is 0.723 (episode-cluster bootstrap 95% CI 0.598–0.840), compared with 0.698 (0.554–0.845) for road length and 0.545 (0.409–0.683) for warning-zone exposure. The Heavy-minus-length contrast is 0.025 (−0.073 to 0.116), and the Heavy-minus-warning contrast is 0.178 (−0.011 to 0.353). Because all retained episodes occurred in a dry earthquake-proximate window and both paired contrast intervals include zero, these results provide only supplementary ranking correspondence; they do not validate rainfall triggering or establish predictive superiority.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "Road validation retains 93 matched sections representing 94 evidence cases. Under the Heavy score, matched concordance is 0.646 with a section-bootstrap 95% interval of 0.586–0.705, compared with 0.556 for road length and 0.494 for warning-zone exposure. These contrasts support relative ranking correspondence under the matched-control design, although the intervals and presence-only evidence preclude claims of calibrated closure probability or decisive predictive superiority."
     - After: "The trigger audit retains 10 physical restriction episodes linked to 94 sections, of which 93 have eligible controls. Under equal episode weighting, Heavy-score concordance is 0.723 (episode-cluster bootstrap 95% CI 0.598–0.840), compared with 0.698 (0.554–0.845) for road length and 0.545 (0.409–0.683) for warning-zone exposure. The Heavy-minus-length contrast is 0.025 (−0.073 to 0.116), and the Heavy-minus-warning contrast is 0.178 (−0.011 to 0.353). Because all retained episodes occurred in a dry earthquake-proximate window and both paired contrast intervals include zero, these results provide only supplementary ranking correspondence; they do not validate rainfall triggering or establish predictive superiority."

### part-04

- Location: Methods > Road disruption validation, paragraph beginning 'Report-derived hazard catalogs'
- Reason: Replace snapshot-level validation with the approved physical-episode funnel, trigger audit, equal-episode concordance, and inference boundary while preserving protected citations.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:21:02Z
- Author: Mike Li
- Markup SHA-256 before: `4d89b322be97ea86df028166a4eb673ce832636e698a29a4eac18e28b08d97ff`
- Markup SHA-256 after: `5797e35833305b07a4dcf046e2d84255e90d5aedaf26e7c3ee9881865d288931`
- Revision IDs: `98, 99, 100, 101`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202103743247.reviewer-2-comment-7.part-04.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Report-derived hazard catalogs require event deduplication and validation of triggering attributes (Zhao et al., 2026). Road validation therefore removes repeated snapshots and retains restriction reasons associated with rockfall, slope collapse, landslide, or sediment inflow. The funnel begins with 680 restriction snapshots, resolves 116 deduplicated landslide-related observations, and retains 93 matched road sections representing 94 evidence cases after spatial and route-agreement checks. Each evidence section a is compared with pseudo-background sections Ba matched on municipality or ward, road category, emergency-route membership, and section-length decile. Equation 9 is the mean share of matched comparisons in which the evidence section has the higher score. Report-based infrastructure records can miss less severe but disruptive hazard exposures (Ghoreishi et al., 2025). Because roads without reports are therefore not confirmed non-events, the metric supports ranking correspondence rather than closure probability.
~~~~

- After:

~~~~text
Report-derived hazard catalogs require event deduplication and validation of triggering attributes (Zhao et al., 2026). We first retained snapshot reasons describing rockfall, slope collapse, or sediment inflow, without treating those process labels as trigger labels. The 680 snapshot rows contained 175 such rows. Deduplication by start address, end address, process reason, and restriction start time yielded 14 physical episodes before network matching; the existing matched_primary and no-more-than-50-m rule retained 116 snapshot rows belonging to 10 physical episodes. These episodes mapped to 152 unique network edges, 94 unique sections, and 96 event–section pairs, of which 93 sections had eligible matched controls. Route-name agreement was audited but was not an eligibility criterion because agreement was available among candidate matches for only one retained episode. The 10 episodes began 0.55–24.38 h after the earthquake, their reasons contained no explicit rainfall-trigger term, and official hourly observations gave 0 mm over the preceding 1, 3, 24, and 72 h both at the nearest project station and across the ten-station audit. We therefore classify them as direct-earthquake consistent but source-unconfirmed and use them only for supplementary correspondence with the terrain-to-road ranking, not for validation of rainfall triggering. Each evidence section a within episode k is compared with pseudo-background sections Ba matched on municipality or ward, road category, emergency-route membership, and section-length decile. Because multiple sections can arise from the same episode, Equation 9 first averages within an episode and then gives each episode equal weight; ties contribute 0.5. Episode-cluster bootstrap intervals preserve the physical episode as the resampling unit. Report-based infrastructure records can miss less severe but disruptive hazard exposures (Ghoreishi et al., 2025). Roads without reports are therefore not confirmed non-events, and the metric supports only supplementary ranking correspondence rather than closure probability or trigger attribution.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "Road validation therefore removes repeated snapshots and retains restriction reasons associated with rockfall, slope collapse, landslide, or sediment inflow. The funnel begins with 680 restriction snapshots, resolves 116 deduplicated landslide-related observations, and retains 93 matched road sections representing 94 evidence cases after spatial and route-agreement checks. Each evidence section a is compared with pseudo-background sections Ba matched on municipality or ward, road category, emergency-route membership, and section-length decile. Equation 9 is the mean share of matched comparisons in which the evidence section has the higher score."
     - After: "We first retained snapshot reasons describing rockfall, slope collapse, or sediment inflow, without treating those process labels as trigger labels. The 680 snapshot rows contained 175 such rows. Deduplication by start address, end address, process reason, and restriction start time yielded 14 physical episodes before network matching; the existing matched_primary and no-more-than-50-m rule retained 116 snapshot rows belonging to 10 physical episodes. These episodes mapped to 152 unique network edges, 94 unique sections, and 96 event–section pairs, of which 93 sections had eligible matched controls. Route-name agreement was audited but was not an eligibility criterion because agreement was available among candidate matches for only one retained episode. The 10 episodes began 0.55–24.38 h after the earthquake, their reasons contained no explicit rainfall-trigger term, and official hourly observations gave 0 mm over the preceding 1, 3, 24, and 72 h both at the nearest project station and across the ten-station audit. We therefore classify them as direct-earthquake consistent but source-unconfirmed and use them only for supplementary correspondence with the terrain-to-road ranking, not for validation of rainfall triggering. Each evidence section a within episode k is compared with pseudo-background sections Ba matched on municipality or ward, road category, emergency-route membership, and section-length decile. Because multiple sections can arise from the same episode, Equation 9 first averages within an episode and then gives each episode equal weight; ties contribute 0.5. Episode-cluster bootstrap intervals preserve the physical episode as the resampling unit."
  2. `structured-replace`
     - Before: "Because roads without reports are therefore not confirmed non-events, the metric supports ranking correspondence rather than closure probability."
     - After: "Roads without reports are therefore not confirmed non-events, and the metric supports only supplementary ranking correspondence rather than closure probability or trigger attribution."

### part-05

- Location: Methods > Road disruption validation, Equation 9
- Reason: Give each physical restriction episode equal weight, include ties, and define event-level concordance used in the revised analysis.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:21:04Z
- Author: Mike Li
- Markup SHA-256 before: `5797e35833305b07a4dcf046e2d84255e90d5aedaf26e7c3ee9881865d288931`
- Markup SHA-256 after: `beca98701d2ff3beafc317bc7a7acfe16d01241f4c0dc4cadb95a757fd4c086c`
- Revision IDs: `102, 103`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202104613198.reviewer-2-comment-7.part-05.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
C(r,f)=1Aa=1A1|Ba|b∈Ba​1Da(r,f)>Db(r,f).
~~~~

- After:

~~~~text
Cepisode(r,f)=1Kk=1K1|Ak|a∈Ak​1|Ba|b∈Ba​1​Da(r,f)>Db(r,f)+121​Da(r,f)=Db(r,f).
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "C(r,f)=1Aa=1A1|Ba|b∈Ba​1Da(r,f)>Db(r,f)."
     - After: "Cepisode(r,f)=1Kk=1K1|Ak|a∈Ak​1|Ba|b∈Ba​1​Da(r,f)>Db(r,f)+121​Da(r,f)=Db(r,f)."

### part-07a

- Location: Results > Road Disruption and Observed Restriction Correspondence, first paragraph
- Reason: Identify the physical episodes shown in revised Figure 5 rather than snapshot-derived matched sections.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:25:09Z
- Author: Mike Li
- Markup SHA-256 before: `beca98701d2ff3beafc317bc7a7acfe16d01241f4c0dc4cadb95a757fd4c086c`
- Markup SHA-256 after: `826b6d7edc68a62b33e8f0b117518aad0303e3bf750909ea41660e0b4e1cd38a`
- Revision IDs: `104, 105`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202509512422.reviewer-2-comment-7.part-07a.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: OMML inside tracked insertion
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
The Heavy-score background in panel d locates the 10 earthquake-proximate physical restriction episodes and their linked road sections.
~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "The Heavy-score background in panel d locates the 93 matched road sections used for ranking validation."
     - After: "The Heavy-score background in panel d locates the 10 earthquake-proximate physical restriction episodes and their linked road sections."

### part-07b-reedit

- Location: Results > Road Disruption and Observed Restriction Correspondence, first paragraph sensitivity insertion
- Reason: Re-express the previously added transfer-sensitivity result using episode-weighted correspondence and the approved dry-event inference boundary.
- Kila decisions: KILA-D-20260903-021
- Mode: `reedit`
- Revises prior parts: reviewer-2/comment-5#part-02
- Timestamp: 2026-09-03T11:25:09Z
- Author: Mike Li
- Markup SHA-256 before: `826b6d7edc68a62b33e8f0b117518aad0303e3bf750909ea41660e0b4e1cd38a`
- Markup SHA-256 after: `f22a7e429974d9fc5fb6d43946f05ee2d057ac8f2dff65481bae6a422afada2e`
- Revision IDs: `45`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202509828416.reviewer-2-comment-7.part-07b-reedit.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
 Across the 15 prespecified transfer specifications, the minimum Spearman correlation on the union of supported roads was 0.676, the minimum top-1% overlap was 0.428, and the minimum overlap of Heavy candidate sets was 0.764. Neighborhood reach and minimum relief changed road support and exact top-ranked membership most strongly, whereas alignment, distance decay, relief scaling, and road-sampling alternatives were more stable individually. Matched road-evidence concordance ranged from 0.614 to 0.687 and remained above 0.50 under every specification. The restriction evidence therefore supports a persistent directional ranking signal, but not parameter-invariant identification of the exact highest-ranked roads.
~~~~

- After:

~~~~text
 Across the 15 prespecified transfer specifications, the minimum Spearman correlation on the union of supported roads was 0.676, the minimum top-1% overlap was 0.428, and the minimum overlap of Heavy candidate sets was 0.764. Neighborhood reach and minimum relief changed road support and exact top-ranked membership most strongly, whereas alignment, distance decay, relief scaling, and road-sampling alternatives were more stable individually. Episode-weighted correspondence ranged from 0.711 to 0.741 across the 15 specifications. This range indicates consistent correspondence with the terrain-to-road ranking under alternative transfer settings, but the 10 clustered dry-event episodes neither validate rainfall triggering nor identify the exact highest-ranked roads independently of parameter choice.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Matched"
     - After: "Episode-weighted"
  2. `replace`
     - Before: "road-evidence concordance"
     - After: "correspondence"
  3. `replace`
     - Before: "614"
     - After: "711"
  4. `replace`
     - Before: "687"
     - After: "741"
  5. `replace`
     - Before: "and"
     - After: "across"
  6. `replace`
     - Before: "remained"
     - After: "the"
  7. `replace`
     - Before: "above"
     - After: "15"
  8. `replace`
     - Before: "0"
     - After: "specifications"
  9. `replace`
     - Before: "50"
     - After: " This range indicates consistent correspondence with the terrain-to-road ranking"
  10. `replace`
     - Before: "every"
     - After: "alternative"
  11. `replace`
     - Before: "specification."
     - After: "transfer"
  12. `replace`
     - Before: "The restriction evidence therefore supports a persistent directional ranking signal"
     - After: "settings"
  13. `replace`
     - Before: "not"
     - After: "the"
  14. `replace`
     - Before: "parameter-invariant"
     - After: "10"
  15. `replace`
     - Before: "identification"
     - After: "clustered"
  16. `replace`
     - Before: "of"
     - After: "dry-event episodes neither validate rainfall triggering nor identify"
  17. `insert`
     - Before: ""
     - After: " independently of parameter choice"

### part-08a

- Location: Results > Road Disruption and Observed Restriction Correspondence, second paragraph
- Reason: Replace snapshot-weighted claims with event-weighted concordance, paired uncertainty, and the approved supplementary-only interpretation.
- Kila decisions: KILA-D-20260903-021
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:25:09Z
- Author: Mike Li
- Markup SHA-256 before: `f22a7e429974d9fc5fb6d43946f05ee2d057ac8f2dff65481bae6a422afada2e`
- Markup SHA-256 after: `79e39e5b19335f2e6676250e16f4eefbe2e923fd24cfd9f6fe74aa022edd8e7b`
- Revision IDs: `106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202510141050.reviewer-2-comment-7.part-08a.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Observed restriction evidence ranks higher under the Heavy road score than under the official warning-zone and road-length comparators.
~~~~

- After:

~~~~text
Across the 10 earthquake-proximate restriction episodes, episode-weighted concordance is 0.723 for the Heavy road score, 0.545 for warning-zone exposure, and 0.698 for section length. Within the same matched controls, the Heavy-minus-warning contrast is 0.178 (episode-cluster bootstrap 95% CI −0.011 to 0.353), whereas the Heavy-minus-length contrast is 0.025 (−0.073 to 0.116). The score therefore shows positive correspondence with the retained road restrictions but does not establish improvement over the length comparator. More importantly, the dry event window means that this comparison evaluates only whether the terrain-to-road ranking corresponds with earthquake-proximate mass-movement restrictions; it does not validate rainfall-triggered disruption, scenario-sensitive spatial ranking, closure probability, landslide-deposit extent, or physical runout geometry.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "Observed"
     - After: "Across the 10 earthquake-proximate"
  2. `replace`
     - Before: "evidence"
     - After: "episodes,"
  3. `replace`
     - Before: "ranks"
     - After: "episode-weighted"
  4. `replace`
     - Before: "higher"
     - After: "concordance"
  5. `replace`
     - Before: "under"
     - After: "is 0.723 for"
  6. `insert`
     - Before: ""
     - After: ","
  7. `replace`
     - Before: "than"
     - After: "0.545"
  8. `replace`
     - Before: "under"
     - After: "for warning-zone exposure, and 0.698 for section length. Within"
  9. `replace`
     - Before: "official"
     - After: "same"
  10. `replace`
     - Before: "warning-zone"
     - After: "matched"
  11. `replace`
     - Before: "and"
     - After: "controls,"
  12. `replace`
     - Before: "road-length"
     - After: "the"
  13. `replace`
     - Before: "comparators"
     - After: "Heavy-minus-warning contrast is 0"
  14. `insert`
     - Before: ""
     - After: "178 (episode-cluster bootstrap 95% CI −0.011 to 0.353), whereas the Heavy-minus-length contrast is 0.025 (−0.073 to 0.116). The score therefore shows positive correspondence with the retained road restrictions but does not establish improvement over the length comparator. More importantly, the dry event window means that this comparison evaluates only whether the terrain-to-road ranking corresponds with earthquake-proximate mass-movement restrictions; it does not validate rainfall-triggered disruption, scenario-sensitive spatial ranking, closure probability, landslide-deposit extent, or physical runout geometry."

### part-08a2

- Location: Results > Road Disruption and Observed Restriction Correspondence, superseded comparator passage
- Reason: Delete the superseded snapshot-weighted comparator passage after inserting the approved event-weighted result.
- Kila decisions: KILA-D-20260903-021
- Mode: `structured-replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:25:24Z
- Author: Mike Li
- Markup SHA-256 before: `79e39e5b19335f2e6676250e16f4eefbe2e923fd24cfd9f6fe74aa022edd8e7b`
- Markup SHA-256 after: `dcd84d5857ca49d0dfefc4220bda919c5c7279dabc4c4e2d0d065eed7d19045a`
- Revision IDs: `132`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202524690671.reviewer-2-comment-7.part-08a2.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Matched concordance is 0.646 for the Heavy score, compared with 0.494 for warning-zone exposure and 0.556 for section length. The comparison is made within matched municipality, road category, emergency-route status, and length-decile strata, limiting the ability of section length or reporting geography to explain the difference. The result supports the directional score as a relative screening device. It does not establish scenario-sensitive spatial ranking, because 
~~~~

- After:

~~~~text

~~~~

- Minimal tracked fragments:
  1. `structured-replace`
     - Before: "Matched concordance is 0.646 for the Heavy score, compared with 0.494 for warning-zone exposure and 0.556 for section length. The comparison is made within matched municipality, road category, emergency-route status, and length-decile strata, limiting the ability of section length or reporting geography to explain the difference. The result supports the directional score as a relative screening device. It does not establish scenario-sensitive spatial ranking, because "
     - After: ""

### part-08a3

- Location: Results > Road Disruption and Observed Restriction Correspondence, second paragraph rendered-page continuation
- Reason: Delete the superseded continuation after inserting the approved event-weighted result while preserving the page marker.
- Kila decisions: KILA-D-20260903-021
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:25:32Z
- Author: Mike Li
- Markup SHA-256 before: `dcd84d5857ca49d0dfefc4220bda919c5c7279dabc4c4e2d0d065eed7d19045a`
- Markup SHA-256 after: `30ecd854a30d33ab17a5d1aeb6e3e2d640f1beca09342b13d0e107cddcdf7714`
- Revision IDs: `133`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202532835986.reviewer-2-comment-7.part-08a3.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Moderate, Heavy, and Extreme scores preserve almost the same order, and it does not identify a closure rate among unreported roads.
~~~~

- After:

~~~~text

~~~~

- Minimal tracked fragments:
  1. `delete`
     - Before: "Moderate, Heavy, and Extreme scores preserve almost the same order, and it does not identify a closure rate among unreported roads."
     - After: ""

### part-08b-reedit

- Location: Results > Road Disruption and Observed Restriction Correspondence, prior runout-limitation insertion
- Reason: Remove the superseded prior insertion after integrating its boundary into the approved event-audit paragraph.
- Kila decisions: KILA-D-20260903-021
- Mode: `reedit`
- Revises prior parts: reviewer-4/comment-2#part-04
- Timestamp: 2026-09-03T11:25:50Z
- Author: Mike Li
- Markup SHA-256 before: `30ecd854a30d33ab17a5d1aeb6e3e2d640f1beca09342b13d0e107cddcdf7714`
- Markup SHA-256 after: `fff0b368ac215ce72973b2094611a4fdd50e92d7236017aa42ecd8f971034c51`
- Revision IDs: `77`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202550497531.reviewer-2-comment-7.part-08b-reedit.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
 The matched restriction comparison evaluates road-level ranking correspondence; it does not independently validate landslide-deposit extent or physical runout geometry, because the available GSI inventory comprises 1,044 interpreted point locations rather than mapped deposit polygons.
~~~~

- After:

~~~~text

~~~~

- Minimal tracked fragments:
  1. `delete`
     - Before: " The matched restriction comparison evaluates road-level ranking correspondence; it does not independently validate landslide-deposit extent or physical runout geometry, because the available GSI inventory comprises 1,044 interpreted point locations rather than mapped deposit polygons."
     - After: ""

### part-09-reedit

- Location: Discussion > Strengths, Limitations, and Future Research, first paragraph
- Reason: Qualify the separate road-restriction evidence as event-deduplicated and trigger-audited.
- Kila decisions: KILA-D-20260903-021
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:25:59Z
- Author: Mike Li
- Markup SHA-256 before: `fff0b368ac215ce72973b2094611a4fdd50e92d7236017aa42ecd8f971034c51`
- Markup SHA-256 after: `4c144f92db0facf9d02ef6f9ecb15d2180fcc436775db82602358d56d1315ed9`
- Revision IDs: `134`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202559897996.reviewer-2-comment-7.part-09-reedit.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
road-restriction correspondence
~~~~

- After:

~~~~text
event-deduplicated and trigger-audited road-restriction correspondence
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "event-deduplicated and trigger-audited "

### part-10a

- Location: Figure 5 caption title
- Reason: Rename Figure 5 to reflect earthquake-proximate supplementary restriction correspondence.
- Kila decisions: KILA-D-20260903-021
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:26:29Z
- Author: Mike Li
- Markup SHA-256 before: `4c144f92db0facf9d02ef6f9ecb15d2180fcc436775db82602358d56d1315ed9`
- Markup SHA-256 after: `2f67c6babd96efbed0bdb636b811ece748695d4ebf42354581480015c94b4c89`
- Revision IDs: `135, 136, 137, 138`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202629472154.reviewer-2-comment-7.part-10a.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `3ed02e454dab3dedfb8d6f75472db6dd289f38cf7eb0541008bf00b626a56413`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Figure 5. Road disruption scores and observed restriction evidence
~~~~

- After:

~~~~text
Figure 5. Road disruption scores and earthquake-proximate restriction correspondence
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: "observed"
     - After: "earthquake-proximate"
  2. `replace`
     - Before: "evidence"
     - After: "correspondence"

### part-10b

- Location: Figure 5 caption note
- Reason: Define the event-deduplicated dry restriction evidence and its supplementary-only interpretation.
- Kila decisions: KILA-D-20260903-021
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:26:29Z
- Author: Mike Li
- Markup SHA-256 before: `2f67c6babd96efbed0bdb636b811ece748695d4ebf42354581480015c94b4c89`
- Markup SHA-256 after: `564325e6bc4acc1e4d7961e55989bd7d4b4ae93ee776b3c8103bbea648baf918`
- Revision IDs: `139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202629780148.reviewer-2-comment-7.part-10b.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `8cc96e2185dbabd7f935b2bba2d43f75fae7c302a7fde587a64321d22c581c27`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Note: Panels a, b, and c map relative road disruption scores under Moderate, Heavy, and Extreme rainfall, with the Extreme panel also identifying emergency transport roads; panel d overlays deduplicated landslide-related restriction evidence on the Heavy- rainfall score and summarizes matching and ranking correspondence.
~~~~

- After:

~~~~text
Note: Panels a, b, and c map relative road disruption scores under Moderate, Heavy, and Extreme rainfall, with the Extreme panel also identifying emergency transport roads. Panel d locates the 10 event-deduplicated rockfall, slope-collapse, or sediment-inflow restriction episodes and their linked sections on the Heavy-score background. These episodes occurred in a dry earthquake-proximate window and provide supplementary terrain-to-road ranking correspondence, not validation of rainfall-triggered disruption.
~~~~

- Minimal tracked fragments:
  1. `replace`
     - Before: ";"
     - After: "."
  2. `replace`
     - Before: "panel"
     - After: "Panel"
  3. `replace`
     - Before: "overlays"
     - After: "locates"
  4. `replace`
     - Before: "deduplicated"
     - After: "the"
  5. `replace`
     - Before: "landslide-related"
     - After: "10 event-deduplicated rockfall, slope-collapse, or sediment-inflow"
  6. `replace`
     - Before: "evidence"
     - After: "episodes and their linked sections"
  7. `replace`
     - Before: "Heavy-"
     - After: "Heavy-score"
  8. `replace`
     - Before: "rainfall"
     - After: "background."
  9. `replace`
     - Before: "score"
     - After: "These episodes occurred in a dry earthquake-proximate window"
  10. `replace`
     - Before: "summarizes"
     - After: "provide"
  11. `replace`
     - Before: "matching"
     - After: "supplementary"
  12. `replace`
     - Before: "and"
     - After: "terrain-to-road"
  13. `insert`
     - Before: ""
     - After: ", not validation of rainfall-triggered disruption"

### part-10c-figure

- Location: Figure 5 embedded raster
- Reason: Replace the snapshot-level validation panel with the approved event-deduplicated, trigger-audited supplementary correspondence figure.
- Kila decisions: KILA-D-20260903-021
- Mode: `figure-replace`
- Timestamp: 2026-09-03T11:27:06.431174Z
- Author: Kila
- Markup SHA-256 before: `564325e6bc4acc1e4d7961e55989bd7d4b4ae93ee776b3c8103bbea648baf918`
- Markup SHA-256 after: `4a7742f669cf8a3459d0c82a492f7d247119fd36314f1a1613d25c60531d23e7`
- Revision IDs: not applicable (approved embedded-media replacement)
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202706431174.reviewer-2-comment-7.part-10c-figure.docx`
- Figure relationship: `rId13` -> `word/media/image5.png`
- Verified caption: Figure 5. Road disruption scores and earthquake-proximate restriction correspondence
- Replacement asset: `data/results/figures/Figure_road_disruption_exposure_and_observed_restriction_evidence.png`
- Original image SHA-256: `485531ff97806572e5941ff6f6bbb8fc03aa3dd80542e5abd2f964211f02e8c0`
- Replacement image SHA-256: `0e125b1e6007464e3c1721812609d07dae0a255b62e2684fe77826579105f9a4`
- Image format and dimensions preserved: `true` (PNG, 4327 x 3335, RGBA)
- Non-target package members preserved byte-for-byte: `true`
- XML and DOCX ZIP verification: `passed`
- Track-revisions setting preserved: `true`
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`

### part-11

- Location: Discussion > Strengths, Limitations, and Future Research, second paragraph
- Reason: State the small, clustered, dry restriction-evidence boundary and the evidence required for future target-mechanism validation.
- Kila decisions: KILA-D-20260903-021
- Mode: `replace`
- Revises prior parts: none
- Timestamp: 2026-09-03T11:28:46Z
- Author: Mike Li
- Markup SHA-256 before: `4a7742f669cf8a3459d0c82a492f7d247119fd36314f1a1613d25c60531d23e7`
- Markup SHA-256 after: `81296ac670959dc569a41720ca56160aa12041c9d40271303041f3066eb1ad65`
- Revision IDs: `164`
- Backup: `Rev/revision/.kila-backups/KE01e.rev.markup.20260903T202846882355.reviewer-2-comment-7.part-11.docx`
- Paragraph properties preserved: `true`
- Run style source SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Formula verification: not applicable
- Endnote hyperlinks preserved: `true`
- Endnote hyperlink count: `0`
- Endnote hyperlink XML SHA-256: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Endnote relationships SHA-256: `absent`
- Before:

~~~~text
Slope-to-road transfer
~~~~

- After:

~~~~text
The 2026 restriction evidence comprises only 10 physical episodes in a dry earthquake-proximate window; repeated snapshots and multiple linked sections are not independent events, and the source reasons do not explicitly code the trigger. Consequently, these records cannot validate rainfall-triggered road disruption, and a future target-mechanism validation requires event-deduplicated road impacts with confirmed rainfall timing, event rainfall fields, and credible unaffected-road comparators. Slope-to-road transfer
~~~~

- Minimal tracked fragments:
  1. `insert`
     - Before: ""
     - After: "The 2026 restriction evidence comprises only 10 physical episodes in a dry earthquake-proximate window; repeated snapshots and multiple linked sections are not independent events, and the source reasons do not explicitly code the trigger. Consequently, these records cannot validate rainfall-triggered road disruption, and a future target-mechanism validation requires event-deduplicated road impacts with confirmed rainfall timing, event rainfall fields, and credible unaffected-road comparators. "

