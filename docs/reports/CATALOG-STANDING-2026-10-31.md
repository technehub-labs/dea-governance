# Org-Wide Catalog Standing Report — 2026-10-31

**Landed by:** CR-015 · **Method:** mechanical survey of all 43 registered catalog repositories (GitHub contents + CATALOG.yaml counts, with retries; metamodel `lifecycle` values read from the canonical source) · **Reconciler:** R1–R4 verified post-refresh (Findings: 0)

## 1. Headline

| Metric | Value |
|---|---|
| Registered catalog repositories | 43 (0 missing) |
| Populated (canonical > 0) | 13 |
| Canonical records org-wide | **4,019** |
| Skeleton (repo exists, no canonical) | 25 — of which 18 carry the advancement-programme foundation kit (pointer + schema + gates 1–6 + three CI workflows) |
| Bespoke / pre-index layout | 5 (concepts, skills, blueprints, application-components, system-functions) |
| Open candidate investigations | 0 (the capabilities candidate register closed under CR-DEA-BC-68) |

## 2. The 43 repositories

| Repository | Entities (metamodel) | Observed state | Canonical | Index | Notes |
|---|---|---|---|---|---|
| processes | BusinessProcess | populated | 3722 | yes |  |
| value-streams | ValueStream | populated | 111 | yes |  |
| business-objects | BusinessObject | populated | 74 | yes |  |
| business-capabilities | BusinessCapability | populated | 40 | yes | 3 candidate-state subtrees are closed investigations (CR-DEA-BC-68) |
| controls | Control | populated | 20 | yes |  |
| data-entities | DataEntity | populated | 9 | yes |  |
| information-classes | InformationClass | populated | 8 | yes |  |
| knowledge-assets | KnowledgeAsset | populated | 8 | yes |  |
| regulations | Regulation | populated | 8 | yes |  |
| tenets | Tenet | populated | 8 | yes |  |
| information-assets | InformationAsset | populated | 7 | yes |  |
| actors | Actor | populated | 3 | yes |  |
| roles | Role | populated | 1 | yes |  |
| ai-ml-models | AIMLModel | skeleton | 0 | yes |  |
| api-contracts | IntegrationInterface, API | skeleton | 0 | yes |  |
| application-components | InformationSystemComponent, ApplicationComponent, InfrastructureComponent, IntegrationComponent | skeleton | 0 | bespoke | owner-active series; records present; index refresh is the owner's call |
| blueprints | Blueprint | skeleton | 0 | bespoke | owner-active CR-BL series (foundation) |
| change-initiatives | ChangeInitiative | skeleton | 0 | yes |  |
| concepts | Concept | skeleton | 0 | bespoke |  |
| data-products | DataProduct | skeleton | 0 | yes |  |
| digital-business-service-factory | BusinessService, SolutionComponent | skeleton | 0 | yes |  |
| digital-identities | DigitalIdentity | skeleton | 0 | yes |  |
| ecosystem-platforms | EcosystemPlatform | skeleton | 0 | yes |  |
| event-streams | Event | skeleton | 0 | yes |  |
| experiments | Experiment | skeleton | 0 | yes |  |
| financial-resources | FinancialResource | skeleton | 0 | yes |  |
| guardrails | Guardrail | skeleton | 0 | yes |  |
| intangible-resources | IntangibleResource | skeleton | 0 | yes |  |
| investment-initiatives | InvestmentInitiative | skeleton | 0 | yes |  |
| journey-touchpoints | JourneyTouchpoint | skeleton | 0 | yes |  |
| metrics | PerformanceMetric | skeleton | 0 | yes | owner-active series; records present; index refresh is the owner's call |
| model-deployments | ModelDeployment, ModelFeedbackSignal | skeleton | 0 | yes |  |
| organizational-units | OrganizationalUnit | skeleton | 0 | yes | owner-active series; records present; index refresh is the owner's call |
| patterns | ArchitecturePattern, Technology | skeleton | 0 | yes |  |
| physical-resources | PhysicalResource | skeleton | 0 | yes |  |
| platform-services | InformationSystemService, PlatformService | skeleton | 0 | yes |  |
| risk-register | Risk | skeleton | 0 | yes |  |
| signals | Signal | skeleton | 0 | yes |  |
| skills | Skill | skeleton | 0 | bespoke |  |
| stakeholders | Stakeholder | skeleton | 0 | yes | owner-active series; records present; index refresh is the owner's call |
| strategic-objectives | StrategicObjective | skeleton | 0 | yes |  |
| system-functions | InformationSystemFunction, SystemFunction | skeleton | 0 | bespoke | owner-active series; records present; index refresh is the owner's call |
| technology-radar | TechnologyRadarEntry | skeleton | 0 | yes |  |
## 3. Lifecycle truth

Every metamodel entity `lifecycle` value agrees with the observed state of its declared `catalog_repo`, with one deliberate, named exception family: `dea:BusinessService`, `dea:SolutionComponent`, and `dea:PerformanceMetric` are `existing` while their registered repositories show no canonical content (the CR-MET-014 §6 stale-`existing` trio — downgrade-or-repoint is an owner decision, still standing). The survey's other candidate drifts dissolved on direct verification (processes and tenets indexes exist; the initial read flaked).

## 4. Standing follow-ups (unchanged or renewed)

1. **Owner-active index refreshes:** organizational-units, stakeholders, metrics, application-components, system-functions carry records with owner-side CR series; their CATALOG.yaml adoption (or bespoke flag stewardship) is the owner's call.
2. **Stale-`existing` trio** (BusinessService, SolutionComponent, PerformanceMetric): downgrade or repoint decision.
3. **`catalog_repo` naming drifts:** `dea-catalog-processes` vs `dea-catalog-business-processes`; `dea-catalog-digital-business-service-factory` vs `dea-catalog-business-services`.
4. **Bespoke-index adoption:** concepts, skills, blueprints, application-components, system-functions.
5. **Consumer-workflow pinning:** the ECF drift consumers float on `--depth 1 main`.
6. **CR-006 promotion:** the admission-linkage gate to other catalogs via the check_id_system vendoring route.

## 5. Method note

Observation is index-based; the five bespoke repos' record presence is stewarded (register `index: bespoke`), not machine-counted. GitHub API single-flight flakes were retried; two residual flakes (processes, tenets) were corrected by direct verification and are recorded in the table's corrected totals.
