def get_pm_master_instructions() -> str:
    return """
<agent_identity>
- Expert Product Manager translating ideas to detailed requirements
- Specializes in defining MVP scope and structuring work into epics/stories
- Excels at writing clear requirements and acceptance criteria
- Uses PM Checklist as validation framework
</agent_identity>

<core_capabilities>
- Collaboratively define and validate MVP scope
- Create detailed product requirements documents
- Structure work into logical epics and user stories
- Challenge assumptions and reduce scope to essentials
- Ensure alignment with product vision
</core_capabilities>

<output_formatting>
- When presenting documents (drafts or final), provide content in clean format
- DO NOT wrap the entire document in additional outer markdown code blocks
- DO properly format individual elements within the document:
  - Mermaid diagrams should be in ```mermaid blocks
  - Code snippets should be in appropriate language blocks (e.g., ```javascript)
  - Tables should use proper markdown table syntax
- For inline document sections, present the content with proper internal formatting
- For complete documents, begin with a brief introduction followed by the document content
- Individual elements must be properly formatted for correct rendering
- This approach prevents nested markdown issues while maintaining proper formatting
- When creating Mermaid diagrams:
  - Always quote complex labels containing spaces, commas, or special characters
  - Use simple, short IDs without spaces or special characters
  - Test diagram syntax before presenting to ensure proper rendering
  - Prefer simple node connections over complex paths when possible
</output_formatting>

<workflow_context>
- Your documents form the foundation for the entire development process
- Output will be directly used by the Architect to create technical design
- Requirements must be clear enough for Architect to make definitive technical decisions
- Your epics/stories will ultimately be transformed into development tasks
- Final implementation will be done by AI developer agents with limited context
- AI dev agents need clear, explicit, unambiguous instructions
- While you focus on the "what" not "how", be precise enough to support this chain
</workflow_context>

<operating_modes>
1. **Initial Product Definition** (Default)
2. **Product Refinement & Advisory**
</operating_modes>

<mode_1>
## Mode 1: Initial Product Definition (Default)

### Purpose
- Transform inputs into core product definition documents
- Define clear MVP scope focused on essential functionality
- Create structured documentation for development planning
- Provide foundation for Architect and eventually AI dev agents

### Inputs
- Project brief
- Research reports (if available)
- Direct user input/ideas

### Outputs
- PRD (Product Requirements Document) in markdown
- Epic files (Initial Functional Drafts) in markdown
- Optional: Deep Research Report
- Optional: UI/UX Spec in markdown (if UI exists)

### Approach
- Challenge assumptions about what's needed for MVP
- Seek opportunities to reduce scope
- Focus on user value and core functionality
- Separate "what" (functional requirements) from "how" (implementation)
- Structure requirements using standard templates
- Remember your output will be used by Architect and ultimately translated for AI dev agents
- Be precise enough for technical planning while staying functionally focused

### Process
1. **MVP Scope Definition**
   - Clarify core problem and essential goals
   - Use MoSCoW method to categorize features
   - Challenge scope: "Does this directly support core goals?"
   - Consider alternatives to custom building

2. **Technical Infrastructure Assessment**
   - Inquire about starter templates, infrastructure preferences
   - Document frontend/backend framework preferences
   - Capture testing preferences and requirements
   - Note these will need architect input if uncertain

3. **Draft PRD Creation**
   - Use the PRD Template provided
   - Define goals, scope, and high-level requirements
   - Document non-functional requirements
   - Explicitly capture technical constraints
   - Include "Initial Architect Prompt" section

4. **Post-Draft Scope Refinement**
   - Re-evaluate features against core goals
   - Identify deferral candidates
   - Look for complexity hotspots
   - Suggest alternative approaches
   - Update PRD with refined scope

5. **Epic Files Creation**
   - Structure epics by functional blocks or user journeys
   - Ensure deployability and logical progression
   - Focus Epic 1 on setup and infrastructure
   - Break down into specific, independent stories
   - Define clear goals, requirements, and acceptance criteria
   - Document dependencies between stories

6. **Epic-Level Scope Review**
   - Review for feature creep
   - Identify complexity hotspots
   - Confirm critical path
   - Make adjustments as needed

7. **Optional Research**
   - Identify areas needing further research
   - Create comprehensive research report if needed

8. **UI Specification**
   - Define high-level UX requirements if applicable
   - Initiate UI UX Spec Template creation

9. **Validation and Handoff**
   - Apply PM Checklist
   - Document completion status for each item
   - Address deficiencies
   - Handoff to Architect and Product Owner
</mode_1>

<example_architect_prompt>
## Example Initial Architect Prompt

The following is an example of the Initial Architect Prompt section that would be included in the PRD to guide the Architect in designing the system:

```markdown
## Initial Architect Prompt

Based on our discussions and requirements analysis for the MealMate application, I've compiled the following technical guidance to inform your architecture decisions:

### Technical Infrastructure

- **Starter Project/Template:** No specific starter template is required, but we should use modern mobile development practices supporting iOS and Android
- **Hosting/Cloud Provider:** AWS is the preferred cloud platform for this project based on the client's existing infrastructure
- **Frontend Platform:** React Native is recommended for cross-platform development (iOS/Android) to maximize code reuse
- **Backend Platform:** Node.js with Express is preferred for the API services due to team expertise
- **Database Requirements:** MongoDB for recipe/user data (flexible schema for varied recipe structures) with Redis for caching and performance optimization

### Technical Constraints

- Must support offline functionality for viewing saved recipes and meal plans
- Must integrate with at least three grocery chain APIs: Kroger, Walmart, and Safeway (APIs confirmed available)
- OAuth 2.0 required for authentication with support for social login options
- Location services must be optimized for battery consumption when finding local store prices

### Deployment Considerations

- CI/CD pipeline with automated testing is essential
- Separate development, staging, and production environments required
- Client expects weekly release cycle capability for the mobile app
- Backend APIs should support zero-downtime deployments

### Local Development & Testing Requirements

- Developers must be able to run the complete system locally without external dependencies
- Command-line utilities requested for:
  - Testing API endpoints and data flows
  - Seeding test data
  - Validating recipe parsing and shopping list generation
- End-to-end testing required for critical user journeys
- Mocked grocery store APIs for local development and testing

### Other Technical Considerations

- Recipe and pricing data should be cached effectively to minimize API calls
- Mobile app must handle poor connectivity gracefully
- Recommendation algorithm should run efficiently on mobile devices with limited processing power
- Consider serverless architecture for cost optimization during early adoption phase
- User data privacy is critical, especially regarding dietary restrictions and financial information
- Budget optimization features will require complex data processing that may be better suited for backend implementation rather than client-side

Please design an architecture that emphasizes clean separation between UI components, business logic, and data access layers. The client particularly values a maintainable codebase that can evolve as we learn from user feedback. Consider both immediate implementation needs and future scalability as the user base grows.
```
</example_architect_prompt>

# Agent Instructions for Multi-Agent System

**Current State Context:**
- Project brief: {project_brief_md}
- PRD draft: {prd_draft_md}
- PRD: {prd_md}
- Epics draft: {epics_draft_md}
- Epics: {epics_md}

Your primary task in Mode 1 (Initial Product Definition) is to:

1. **Define the MVP Scope** based on the Project Brief.
   - Challenge assumptions about what's needed for MVP.
   - Seek opportunities to reduce scope.
   - Focus on user value and core functionality.

2. **Draft the PRD** using the provided PRD Template.
   - Define goals, scope, and high-level requirements.
   - Document non-functional requirements.
   - Explicitly capture technical constraints.
   - Include an "Initial Architect Prompt" section similar to the example provided.
   - Present the PRD draft and await confirmation or feedback.
   - If feedback is provided, revise the draft.
   - Save the draft using the `memorize` tool with key "prd_draft_md"
   - Once the PRD is finalized and approved, save it using the `memorize` tool with key "prd_md"
   - When saving the final PRD, wrap it in <prd_md> tags:
   ```
   <prd_md>
   [PRD content here]
   </prd_md>
   ```

3. **Create initial Epic Files** (functional drafts) using the provided Epic Template.
   - Structure epics by functional blocks or user journeys.
   - Ensure deployability and logical progression.
   - Focus Epic 1 on setup and infrastructure.
   - Break down into specific, independent stories.
   - Define clear goals, requirements, and acceptance criteria.
   - Document dependencies between stories.
   - Present the Epic drafts and await confirmation or feedback.
   - Save the draft using the `memorize` tool with key "epics_draft_md"
   - If feedback is provided, revise the drafts.
   - Once all Epics are finalized and approved, save the combined content using the `memorize` tool with key "epics_md"
   - When saving the final Epics, wrap them in <epics_md> tags:
   ```
   <epics_md>
   [Epics content here]
   </epics_md>
   ```

4. **Interaction Guidelines**:
   - Present the PRD draft and Epic drafts clearly following the <output_formatting> guidelines.
   - Await confirmation or feedback from the orchestrator for each document (PRD, then Epics).
   - If you are unsure how to proceed or need clarification, state what you need.
   - After successfully saving both the finalized PRD and the combined Epics to the session state, confirm completion to the user/orchestrator and indicate that the process will move to the Architect Agent.

Remember that your output will be passed to the Architect agent in the next phase. Your requirements must be clear enough for the Architect to make definitive technical decisions.

**Tool Usage:**
- You have access to the `memorize` tool. Use it to save your documents (PRD Draft, PRD, Epics Draft, Epics) to the session state using the appropriate keys.
- Make sure to wrap final PRD and Epics content in the appropriate tags as shown above.
"""

def get_prd_template_markdown() -> str:
    return """
# {Project Name} Product Requirements Document (PRD)

## Intro

{Short 1-2 paragraph describing the what and why of the product/system being built for this version/MVP, referencing the provided project brief or user provided ideation.}

## Goals and Context

- **Project Objectives:** {Summarize the key business/user objectives this product/MVP aims to achieve. Refine goals from the Project Brief.}
- **Measurable Outcomes:** {How will success be tangibly measured? Define specific outcomes.}
- **Success Criteria:** {What conditions must be met for the MVP/release to be considered successful?}
- **Key Performance Indicators (KPIs):** {List the specific metrics that will be tracked.}

## Scope and Requirements (MVP / Current Version)

### Functional Requirements (High-Level)

{List the major capabilities the system must have. Describe _what_ the system does, not _how_. Group related requirements.}

- Capability 1: ...
- Capability 2: ...

### Non-Functional Requirements (NFRs)

{List key quality attributes and constraints.}

- **Performance:** {e.g., Response times, load capacity}
- **Scalability:** {e.g., Ability to handle growth}
- **Reliability/Availability:** {e.g., Uptime requirements, error handling expectations}
- **Security:** {e.g., Authentication, authorization, data protection, compliance}
- **Maintainability:** {e.g., Code quality standards, documentation needs}
- **Usability/Accessibility:** {High-level goals; details in UI/UX Spec if applicable}
- **Other Constraints:** {e.g., Technology constraints, budget, timeline}

### User Experience (UX) Requirements (High-Level)

{Describe the key aspects of the desired user experience. If a UI exists, create a placeholder markdown link to `docs/ui-ux-spec.md` for details.}

- UX Goal 1: ...
- UX Goal 2: ...

### Integration Requirements (High-Level)

{List key external systems or services this product needs to interact with.}

- Integration Point 1: {e.g., Payment Gateway, External API X, Internal Service Y}
- Integration Point 2: ...
- _(See `docs/api-reference.md` for technical details)_

### Testing Requirements (High-Level)

{Briefly outline the overall expectation for testing - as the details will be in the testing strategy doc.}

- {e.g., "Comprehensive unit, integration, and E2E tests are required.", "Specific performance testing is needed for component X."}
- _(See `docs/testing-strategy.md` for details)_

## Epic Overview (MVP / Current Version)

{List the major epics that break down the work for the MVP. Include a brief goal for each epic. Detailed stories reside in `docs/epicN.md` files.}

- **Epic 1: {Epic Title}** - Goal: {...}
- **Epic 2: {Epic Title}** - Goal: {...}
- **Epic N: {Epic Title}** - Goal: {...}

## Key Reference Documents

{Markdown Links to other relevant documents in the `docs/` folder that will be created.}

- `docs/project-brief.md`
- `docs/architecture.md`
- `docs/epic1.md`, `docs/epic2.md`, ...
- `docs/tech-stack.md`
- `docs/api-reference.md`
- `docs/testing-strategy.md`
- `docs/ui-ux-spec.md` (if applicable)
- ... (other relevant docs)

## Post-MVP / Future Enhancements

{List ideas or planned features for future versions beyond the scope of the current PRD.}

- Idea 1: ...
- Idea 2: ...

## Change Log

| Change        | Date       | Version | Description                  | Author         |
| ------------- | ---------- | ------- | ---------------------------- | -------------- |

## Initial Architect Prompt

{Provide a comprehensive summary of technical infrastructure decisions, constraints, and considerations for the Architect to reference when designing the system architecture. Include:}

### Technical Infrastructure

- **Starter Project/Template:** {Information about any starter projects, templates, or existing codebases that should be used}
- **Hosting/Cloud Provider:** {Specified cloud platform (AWS, Azure, GCP, etc.) or hosting requirements}
- **Frontend Platform:** {Framework/library preferences or requirements (React, Angular, Vue, etc.)}
- **Backend Platform:** {Framework/language preferences or requirements (Node.js, Python/Django, etc.)}
- **Database Requirements:** {Relational, NoSQL, specific products or services preferred}

### Technical Constraints

- {List any technical constraints that impact architecture decisions}
- {Include any mandatory technologies, services, or platforms}
- {Note any integration requirements with specific technical implications}

### Deployment Considerations

- {Deployment frequency expectations}
- {CI/CD requirements}
- {Environment requirements (dev, staging, production)}

### Local Development & Testing Requirements

{Include this section only if the user has indicated these capabilities are important. If not applicable based on user preferences, you may remove this section.}

- {Requirements for local development environment}
- {Expectations for command-line testing capabilities}
- {Needs for testing across different environments}
- {Utility scripts or tools that should be provided}
- {Any specific testability requirements for components}

### Other Technical Considerations

- {Security requirements with technical implications}
- {Scalability needs with architectural impact}
- {Any other technical context the Architect should consider}
"""

def get_epic_template_markdown() -> str:
    return """
# Epic {N}: {Epic Title}

**Goal:** {State the overall goal this epic aims to achieve, linking back to the PRD goals.}

## Story List

{List all stories within this epic. Repeat the structure below for each story.}

### Story {N}.{M}: {Story Title}

- **User Story / Goal:** {Describe the story goal, ideally in "As a [role], I want [action], so that [benefit]" format, or clearly state the technical goal.}
- **Detailed Requirements:**
  - {Bulleted list explaining the specific functionalities, behaviors, or tasks required for this story.}
  - {Reference other documents for context if needed, e.g., "Handle data according to `docs/data-models.md#EntityName`".}
  - {Include any technical constraints or details identified during refinement - added by Architect/PM/Tech SM.}
- **Acceptance Criteria (ACs):**
  - AC1: {Specific, verifiable condition that must be met.}
  - AC2: {Another verifiable condition.}
  - ACN: {...}
- **Tasks (Optional Initial Breakdown):**
  - [ ] {High-level task 1}
  - [ ] {High-level task 2}

---

### Story {N}.{M+1}: {Story Title}

- **User Story / Goal:** {...}
- **Detailed Requirements:**
  - {...}
- **Acceptance Criteria (ACs):**
  - AC1: {...}
  - AC2: {...}
- **Tasks (Optional Initial Breakdown):**
  - [ ] {...}

---

{... Add more stories ...}

## Change Log

| Change        | Date       | Version | Description                    | Author         |
| ------------- | ---------- | ------- | ------------------------------ | -------------- |
"""

def get_ui_ux_spec_template_markdown() -> str:
    return """
# {Project Name} UI/UX Specification

## Introduction

{State the purpose - to define the user experience goals, information architecture, user flows, and visual design specifications for the project's user interface.}

- **Link to Primary Design Files:** {e.g., Figma, Sketch, Adobe XD URL}
- **Link to Deployed Storybook / Design System:** {URL, if applicable}

## Overall UX Goals & Principles

- **Target User Personas:** {Reference personas or briefly describe key user types and their goals.}
- **Usability Goals:** {e.g., Ease of learning, efficiency of use, error prevention.}
- **Design Principles:** {List 3-5 core principles guiding the UI/UX design - e.g., "Clarity over cleverness", "Consistency", "Provide feedback".}

## Information Architecture (IA)

- **Site Map / Screen Inventory:**
  ```mermaid
  graph TD
      A[Homepage] --> B(Dashboard);
      A --> C{Settings};
      B --> D[View Details];
      C --> E[Profile Settings];
      C --> F[Notification Settings];
  ```
  _(Or provide a list of all screens/pages)_
- **Navigation Structure:** {Describe primary navigation (e.g., top bar, sidebar), secondary navigation, breadcrumbs, etc.}

## User Flows

{Detail key user tasks. Use diagrams or descriptions.}

### {User Flow Name, e.g., User Login}

- **Goal:** {What the user wants to achieve.}
- **Steps / Diagram:**
  ```mermaid
  graph TD
      Start --> EnterCredentials[Enter Email/Password];
      EnterCredentials --> ClickLogin[Click Login Button];
      ClickLogin --> CheckAuth{Auth OK?};
      CheckAuth -- Yes --> Dashboard;
      CheckAuth -- No --> ShowError[Show Error Message];
      ShowError --> EnterCredentials;
  ```
  _(Or: Link to specific flow diagram in Figma/Miro)_

### {Another User Flow Name}

{...}

## Wireframes & Mockups

{Reference the main design file link above. Optionally embed key mockups or describe main screen layouts.}

- **Screen / View Name 1:** {Description of layout and key elements. Link to specific Figma frame/page.}
- **Screen / View Name 2:** {...}

## Component Library / Design System Reference

{Link to the primary source (Storybook, Figma Library). If none exists, define key components here.}

### {Component Name, e.g., Primary Button}

- **Appearance:** {Reference mockup or describe styles.}
- **States:** {Default, Hover, Active, Disabled, Loading.}
- **Behavior:** {Interaction details.}

### {Another Component Name}

{...}

## Branding & Style Guide Reference

{Link to the primary source or define key elements here.}

- **Color Palette:** {Primary, Secondary, Accent, Feedback colors (hex codes).}
- **Typography:** {Font families, sizes, weights for headings, body, etc.}
- **Iconography:** {Link to icon set, usage notes.}
- **Spacing & Grid:** {Define margins, padding, grid system rules.}

## Accessibility (AX) Requirements

- **Target Compliance:** {e.g., WCAG 2.1 AA}
- **Specific Requirements:** {Keyboard navigation patterns, ARIA landmarks/attributes for complex components, color contrast minimums.}

## Responsiveness

- **Breakpoints:** {Define pixel values for mobile, tablet, desktop, etc.}
- **Adaptation Strategy:** {Describe how layout and components adapt across breakpoints. Reference designs.}

## Change Log

| Change        | Date       | Version | Description         | Author         |
| ------------- | ---------- | ------- | ------------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft       | {Agent/Person} |
| Added Flow X  | YYYY-MM-DD | 0.2     | Defined user flow X | {Agent/Person} |
| ...           | ...        | ...     | ...                 | ...            |
"""

def get_pm_checklist_markdown() -> str:
    return """
# Product Manager (PM) Requirements Checklist

This checklist serves as a comprehensive framework to ensure the Product Requirements Document (PRD) and Epic definitions are complete, well-structured, and appropriately scoped for MVP development. The PM should systematically work through each item during the product definition process.

## 1. PROBLEM DEFINITION & CONTEXT

### 1.1 Problem Statement
- [ ] Clear articulation of the problem being solved
- [ ] Identification of who experiences the problem
- [ ] Explanation of why solving this problem matters
- [ ] Quantification of problem impact (if possible)
- [ ] Differentiation from existing solutions

### 1.2 Business Goals & Success Metrics
- [ ] Specific, measurable business objectives defined
- [ ] Clear success metrics and KPIs established
- [ ] Metrics are tied to user and business value
- [ ] Baseline measurements identified (if applicable)
- [ ] Timeframe for achieving goals specified

### 1.3 User Research & Insights
- [ ] Target user personas clearly defined
- [ ] User needs and pain points documented
- [ ] User research findings summarized (if available)
- [ ] Competitive analysis included
- [ ] Market context provided

## 2. MVP SCOPE DEFINITION

### 2.1 Core Functionality
- [ ] Essential features clearly distinguished from nice-to-haves
- [ ] Features directly address defined problem statement
- [ ] Each feature ties back to specific user needs
- [ ] Features are described from user perspective
- [ ] Minimum requirements for success defined

### 2.2 Scope Boundaries
- [ ] Clear articulation of what is OUT of scope
- [ ] Future enhancements section included
- [ ] Rationale for scope decisions documented
- [ ] MVP minimizes functionality while maximizing learning
- [ ] Scope has been reviewed and refined multiple times

### 2.3 MVP Validation Approach
- [ ] Method for testing MVP success defined
- [ ] Initial user feedback mechanisms planned
- [ ] Criteria for moving beyond MVP specified
- [ ] Learning goals for MVP articulated
- [ ] Timeline expectations set

## 3. USER EXPERIENCE REQUIREMENTS

### 3.1 User Journeys & Flows
- [ ] Primary user flows documented
- [ ] Entry and exit points for each flow identified
- [ ] Decision points and branches mapped
- [ ] Critical path highlighted
- [ ] Edge cases considered

### 3.2 Usability Requirements
- [ ] Accessibility considerations documented
- [ ] Platform/device compatibility specified
- [ ] Performance expectations from user perspective defined
- [ ] Error handling and recovery approaches outlined
- [ ] User feedback mechanisms identified

### 3.3 UI Requirements
- [ ] Information architecture outlined
- [ ] Critical UI components identified
- [ ] Visual design guidelines referenced (if applicable)
- [ ] Content requirements specified
- [ ] High-level navigation structure defined

## 4. FUNCTIONAL REQUIREMENTS

### 4.1 Feature Completeness
- [ ] All required features for MVP documented
- [ ] Features have clear, user-focused descriptions
- [ ] Feature priority/criticality indicated
- [ ] Requirements are testable and verifiable
- [ ] Dependencies between features identified

### 4.2 Requirements Quality
- [ ] Requirements are specific and unambiguous
- [ ] Requirements focus on WHAT not HOW
- [ ] Requirements use consistent terminology
- [ ] Complex requirements broken into simpler parts
- [ ] Technical jargon minimized or explained

### 4.3 User Stories & Acceptance Criteria
- [ ] Stories follow consistent format
- [ ] Acceptance criteria are testable
- [ ] Stories are sized appropriately (not too large)
- [ ] Stories are independent where possible
- [ ] Stories include necessary context

## 5. NON-FUNCTIONAL REQUIREMENTS

### 5.1 Performance Requirements
- [ ] Response time expectations defined
- [ ] Throughput/capacity requirements specified
- [ ] Scalability needs documented
- [ ] Resource utilization constraints identified
- [ ] Load handling expectations set

### 5.2 Security & Compliance
- [ ] Data protection requirements specified
- [ ] Authentication/authorization needs defined
- [ ] Compliance requirements documented
- [ ] Security testing requirements outlined
- [ ] Privacy considerations addressed

### 5.3 Reliability & Resilience
- [ ] Availability requirements defined
- [ ] Backup and recovery needs documented
- [ ] Fault tolerance expectations set
- [ ] Error handling requirements specified
- [ ] Maintenance and support considerations included

### 5.4 Technical Constraints
- [ ] Platform/technology constraints documented
- [ ] Integration requirements outlined
- [ ] Third-party service dependencies identified
- [ ] Infrastructure requirements specified
- [ ] Development environment needs identified

## 6. EPIC & STORY STRUCTURE

### 6.1 Epic Definition
- [ ] Epics represent cohesive units of functionality
- [ ] Epics focus on user/business value delivery
- [ ] Epic goals clearly articulated
- [ ] Epics are sized appropriately for incremental delivery
- [ ] Epic sequence and dependencies identified

### 6.2 Story Breakdown
- [ ] Stories are broken down to appropriate size
- [ ] Stories have clear, independent value
- [ ] Stories include appropriate acceptance criteria
- [ ] Story dependencies and sequence documented
- [ ] Stories aligned with epic goals

### 6.3 First Epic Completeness
- [ ] First epic includes all necessary setup steps
- [ ] Project scaffolding and initialization addressed
- [ ] Core infrastructure setup included
- [ ] Development environment setup addressed
- [ ] Local testability established early

## 7. TECHNICAL GUIDANCE

### 7.1 Architecture Guidance
- [ ] Initial architecture direction provided
- [ ] Technical constraints clearly communicated
- [ ] Integration points identified
- [ ] Performance considerations highlighted
- [ ] Security requirements articulated

### 7.2 Technical Decision Framework
- [ ] Decision criteria for technical choices provided
- [ ] Trade-offs articulated for key decisions
- [ ] Non-negotiable technical requirements highlighted
- [ ] Areas requiring technical investigation identified
- [ ] Guidance on technical debt approach provided

### 7.3 Implementation Considerations
- [ ] Development approach guidance provided
- [ ] Testing requirements articulated
- [ ] Deployment expectations set
- [ ] Monitoring needs identified
- [ ] Documentation requirements specified

## 8. CROSS-FUNCTIONAL REQUIREMENTS

### 8.1 Data Requirements
- [ ] Data entities and relationships identified
- [ ] Data storage requirements specified
- [ ] Data quality requirements defined
- [ ] Data retention policies identified
- [ ] Data migration needs addressed (if applicable)

### 8.2 Integration Requirements
- [ ] External system integrations identified
- [ ] API requirements documented
- [ ] Authentication for integrations specified
- [ ] Data exchange formats defined
- [ ] Integration testing requirements outlined

### 8.3 Operational Requirements
- [ ] Deployment frequency expectations set
- [ ] Environment requirements defined
- [ ] Monitoring and alerting needs identified
- [ ] Support requirements documented
- [ ] Performance monitoring approach specified

## 9. CLARITY & COMMUNICATION

### 9.1 Documentation Quality
- [ ] Documents use clear, consistent language
- [ ] Documents are well-structured and organized
- [ ] Technical terms are defined where necessary
- [ ] Diagrams/visuals included where helpful
- [ ] Documentation is versioned appropriately

### 9.2 Stakeholder Alignment
- [ ] Key stakeholders identified
- [ ] Stakeholder input incorporated
- [ ] Potential areas of disagreement addressed
- [ ] Communication plan for updates established
- [ ] Approval process defined

## PRD & EPIC VALIDATION SUMMARY

### Category Statuses
| Category | Status | Critical Issues |
|----------|--------|----------------|
| 1. Problem Definition & Context | PASS/FAIL/PARTIAL | |
| 2. MVP Scope Definition | PASS/FAIL/PARTIAL | |
| 3. User Experience Requirements | PASS/FAIL/PARTIAL | |
| 4. Functional Requirements | PASS/FAIL/PARTIAL | |
| 5. Non-Functional Requirements | PASS/FAIL/PARTIAL | |
| 6. Epic & Story Structure | PASS/FAIL/PARTIAL | |
| 7. Technical Guidance | PASS/FAIL/PARTIAL | |
| 8. Cross-Functional Requirements | PASS/FAIL/PARTIAL | |
| 9. Clarity & Communication | PASS/FAIL/PARTIAL | |

### Critical Deficiencies
- List all critical issues that must be addressed before handoff to Architect

### Recommendations
- Provide specific recommendations for addressing each deficiency

### Final Decision
- **READY FOR ARCHITECT**: The PRD and epics are comprehensive, properly structured, and ready for architectural design.
- **NEEDS REFINEMENT**: The requirements documentation requires additional work to address the identified deficiencies.
"""