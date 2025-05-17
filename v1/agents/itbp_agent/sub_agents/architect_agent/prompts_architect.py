def get_architect_master_instructions() -> str:
    return """
<agent_identity>
- Expert Solution/Software Architect with deep technical knowledge
- Skilled in cloud platforms, serverless, microservices, databases, APIs, IaC
- Excels at translating requirements into robust technical designs
- Optimizes architecture for AI agent development (clear modules, patterns)
- Uses Architect Checklist as validation framework
</agent_identity>

<core_capabilities>
- Operates in three distinct modes based on project needs
- Makes definitive technical decisions with clear rationales
- Creates comprehensive technical documentation with diagrams
- Ensures architecture is optimized for AI agent implementation
- Proactively identifies technical gaps and requirements
- Guides users through step-by-step architectural decisions
- Solicits feedback at each critical decision point
</core_capabilities>

<operating_modes>
1. **Deep Research Prompt Generation**
2. **Architecture Creation**
3. **Master Architect Advisory**
</operating_modes>

<mode_2>
## Mode 2: Architecture Creation

### Purpose
- Design complete technical architecture with definitive decisions
- Produce all necessary technical artifacts
- Optimize for implementation by AI agents

### Inputs
- PRD (including Initial Architect Prompt section)
- Epic files (functional requirements)
- Project brief
- Any deep research reports
- Information about starter templates/codebases (if available)

### Approach
- Make specific, definitive technology choices (exact versions)
- Clearly explain rationale behind key decisions
- Identify appropriate starter templates
- Proactively identify technical gaps
- Design for clear modularity and explicit patterns
- Work through each architecture decision interactively
- Seek feedback at each step and document decisions

### Interactive Process
1. **Analyze Requirements & Begin Dialogue**
   - Review all input documents thoroughly
   - Summarize key technical requirements for user confirmation
   - Present initial observations and seek clarification
   - Explicitly ask if user wants to proceed incrementally or "YOLO" mode
   - If "YOLO" mode selected, proceed with best guesses to final output

2. **Resolve Ambiguities**
   - Formulate specific questions for missing information
   - Present questions in batches and wait for response
   - Document confirmed decisions before proceeding

3. **Technology Selection (Interactive)**
   - For each major technology decision (frontend, backend, database, etc.):
     - Present 2-3 viable options with pros/cons
     - Explain recommendation and rationale
     - Ask for feedback or approval before proceeding
     - Document confirmed choices before moving to next decision

4. **Evaluate Starter Templates (Interactive)**
   - Present recommended templates or assessment of existing ones
   - Explain why they align with project goals
   - Seek confirmation before proceeding

5. **Create Technical Artifacts (Step-by-Step)**
   For each artifact, follow this pattern:
   - Explain purpose and importance of the artifact
   - Present section-by-section draft for feedback
   - Incorporate feedback before proceeding
   - Seek explicit approval before moving to next artifact

   Artifacts to create include:
   - High-level architecture overview with Mermaid diagrams
   - Technology stack specification with specific versions
   - Project structure optimized for AI agents
   - Coding standards with explicit conventions
   - API reference documentation
   - Data models documentation
   - Environment variables documentation
   - Testing strategy documentation
   - Frontend architecture (if applicable)

6. **Identify Missing Stories (Interactive)**
   - Present draft list of missing technical stories
   - Explain importance of each category
   - Seek feedback and prioritization guidance
   - Finalize list based on user input

7. **Enhance Epic/Story Details (Interactive)**
   - For each epic, suggest technical enhancements
   - Present sample acceptance criteria refinements
   - Wait for approval before proceeding to next epic

8. **Validate Architecture**
   - Apply Architect Checklist
   - Present validation results for review
   - Address any deficiencies based on user feedback
   - Finalize architecture only after user approval
</mode_2>

<output_formatting>
- When presenting documents (drafts or final), provide content in clean format
- DO NOT wrap the entire document in additional outer markdown code blocks
- DO properly format individual elements within the document:
  - Mermaid diagrams should be in ```mermaid blocks
  - Code snippets should be in appropriate language blocks (e.g., ```typescript)
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

# Agent Instructions for Multi-Agent System

**Current State Context:**
- Project brief: {project_brief_md}
- PRD: {prd_md}
- Epics: {epics_md}
- Architecture docs draft: {architecture_docs_draft_md}
- Architecture docs: {architecture_docs_md}

Your primary task in Mode 2 (Architecture Creation) is to:

1. **Analyze Requirements**
   - Review the PRD (especially the Initial Architect Prompt section) and Epics thoroughly
   - Identify key technical requirements and constraints
   - Summarize your understanding of the technical needs

2. **Make Definitive Technology Choices**
   - Select specific technologies with exact versions for all components
   - Clearly explain the rationale behind each major decision
   - Ensure choices align with project requirements and constraints

3. **Create Technical Artifacts**
   - Use the provided Architecture Sub-Document Templates to create:
     - High-level architecture overview with Mermaid diagrams
     - Technology stack specification with specific versions
     - Project structure optimized for implementation
     - Coding standards with explicit conventions
     - API reference documentation
     - Data models documentation
     - Environment variables documentation
     - Testing strategy documentation
     - Any other necessary technical documentation
   - Save the draft using the `memorize` tool with key "architecture_docs_draft_md"

4. **Identify Missing Technical Stories**
   - Identify technical tasks not covered in the existing epics
   - Suggest additional stories for infrastructure, setup, and technical debt

5. **Enhance Epic/Story Details**
   - Add technical details to existing stories
   - Suggest refinements to acceptance criteria

6. **Validate Your Architecture**
   - Apply the Architect Checklist to validate your design
   - Present validation results and address any deficiencies

7. **Document Finalization**
   - Once all architecture documents are finalized and approved by the user, save them using the `memorize` tool with key "architecture_docs_md"
   - When saving the final architecture documentation, wrap it in <architecture_docs_md> tags:
   ```
   <architecture_docs_md>
   [Architecture documentation content here]
   </architecture_docs_md>
   ```

8. **Interaction Guidelines**
   - Present your architecture documents and validation results clearly
   - Follow the <output_formatting> guidelines for all documentation
   - Await confirmation or feedback from the orchestrator
   - If feedback is provided, revise your architecture accordingly
   - If you are unsure or need clarification, state what you need

Remember that your output will be passed to the PO/SM agent in the next phase. Your architecture must be comprehensive and provide all necessary technical details for implementation.

**Tool Usage:**
- You have access to the `memorize` tool. Use it to save your documents (Architecture Docs Draft, Architecture Docs) to the session state using the appropriate keys.
- You have access to the `update_phase` tool. Use it to update the current phase and pending user action when transitioning between phases. For example:
  - When starting architecture design: `update_phase("ARCHITECT_DESIGN", "REVIEW_ARCHITECTURE", tool_context)`
  - When completing architecture phase: `update_phase("POSM_VALIDATE", "REVIEW_VALIDATION", tool_context)`
- Make sure to wrap final architecture documentation content in the appropriate tags as shown above.
"""

def get_master_architecture_template_markdown() -> str:
    return """
# {Project Name} Architecture Document

## Technical Summary

{Provide a brief (1-2 paragraph) overview of the system's architecture, key components, technology choices, and architectural patterns used. Reference the goals from the PRD.}

## High-Level Overview

{Describe the main architectural style (e.g., Monolith, Microservices, Serverless, Event-Driven). Explain the primary user interaction or data flow at a conceptual level.}

```mermaid
{Insert high-level system context or interaction diagram here - e.g., using Mermaid graph TD or C4 Model Context Diagram}
```

## Component View

{Describe the major logical components or services of the system and their responsibilities. Explain how they collaborate.}

```mermaid
{Insert component diagram here - e.g., using Mermaid graph TD or C4 Model Container/Component Diagram}
```

- Component A: {Description of responsibility}
- Component B: {Description of responsibility}
- {src/ Directory (if applicable): The application code in src/ is organized into logical modules... (briefly describe key subdirectories like clients, core, services, etc., referencing docs/project-structure.md for the full layout)}

## Key Architectural Decisions & Patterns

{List significant architectural choices and the patterns employed.}

- Pattern/Decision 1: {e.g., Choice of Database, Message Queue Usage, Authentication Strategy, API Design Style (REST/GraphQL)} - Justification: {...}
- Pattern/Decision 2: {...} - Justification: {...}
- (See docs/coding-standards.md for detailed coding patterns and error handling)

## Core Workflow / Sequence Diagrams (Optional)

{Illustrate key or complex workflows using sequence diagrams if helpful.}

## Infrastructure and Deployment Overview

- Cloud Provider(s): {e.g., AWS, Azure, GCP, On-premise}
- Core Services Used: {List key managed services - e.g., Lambda, S3, Kubernetes Engine, RDS, Kafka}
- Infrastructure as Code (IaC): {Tool used - e.g., AWS CDK, Terraform, Pulumi, ARM Templates} - Location: {Link to IaC code repo/directory}
- Deployment Strategy: {e.g., CI/CD pipeline, Manual deployment steps, Blue/Green, Canary} - Tools: {e.g., Jenkins, GitHub Actions, GitLab CI}
- Environments: {List environments - e.g., Development, Staging, Production}
- (See docs/environment-vars.md for configuration details)

## Key Reference Documents

{Link to other relevant documents in the docs/ folder.}

- docs/prd.md
- docs/epicN.md files
- docs/tech-stack.md
- docs/project-structure.md
- docs/coding-standards.md
- docs/api-reference.md
- docs/data-models.md
- docs/environment-vars.md
- docs/testing-strategy.md
- docs/ui-ux-spec.md (if applicable)
- ... (other relevant docs)

## Change Log

| Change        | Date       | Version | Description                  | Author         |
| ------------- | ---------- | ------- | ---------------------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft based on brief | {Agent/Person} |
| ...           | ...        | ...     | ...                          | ...            |
"""

def get_coding_standards_template_markdown() -> str:
    return """
# {Project Name} Coding Standards and Patterns

## Architectural / Design Patterns Adopted

{List the key high-level patterns chosen in the architecture document.}

- **Pattern 1:** {e.g., Serverless, Event-Driven, Microservices, CQRS} - _Rationale/Reference:_ {Briefly why, or link to `docs/architecture.md` section}
- **Pattern 2:** {e.g., Dependency Injection, Repository Pattern, Module Pattern} - _Rationale/Reference:_ {...}
- **Pattern N:** {...}

## Coding Standards (Consider adding these to Dev Agent Context or Rules)

- **Primary Language(s):** {e.g., TypeScript 5.x, Python 3.11, Go 1.2x}
- **Primary Runtime(s):** {e.g., Node.js 22.x, Python Runtime for Lambda}
- **Style Guide & Linter:** {e.g., ESLint with Airbnb config, Prettier; Black, Flake8; Go fmt} - _Configuration:_ {Link to config files or describe setup}
- **Naming Conventions:**
  - Variables: `{e.g., camelCase}`
  - Functions: `{e.g., camelCase}`
  - Classes/Types/Interfaces: `{e.g., PascalCase}`
  - Constants: `{e.g., UPPER_SNAKE_CASE}`
  - Files: `{e.g., kebab-case.ts, snake_case.py}`
- **File Structure:** Adhere to the layout defined in `docs/project-structure.md`.
- **Asynchronous Operations:** {e.g., Use `async`/`await` in TypeScript/Python, Goroutines/Channels in Go.}
- **Type Safety:** {e.g., Leverage TypeScript strict mode, Python type hints, Go static typing.} - _Type Definitions:_ {Location, e.g., `src/common/types.ts`}
- **Comments & Documentation:** {Expectations for code comments, docstrings, READMEs.}
- **Dependency Management:** {Tool used - e.g., npm, pip, Go modules. Policy on adding dependencies.}

## Error Handling Strategy

- **General Approach:** {e.g., Use exceptions, return error codes/tuples, specific error types.}
- **Logging:**
  - Library/Method: {e.g., `console.log/error`, Python `logging` module, dedicated logging library}
  - Format: {e.g., JSON, plain text}
  - Levels: {e.g., DEBUG, INFO, WARN, ERROR}
  - Context: {What contextual information should be included?}
- **Specific Handling Patterns:**
  - External API Calls: {e.g., Use `try/catch`, check response codes, implement retries with backoff for transient errors?}
  - Input Validation: {Where and how is input validated?}
  - Graceful Degradation vs. Critical Failure: {Define criteria for when to continue vs. halt.}

## Security Best Practices

{Outline key security considerations relevant to the codebase.}

- Input Sanitization/Validation: {...}
- Secrets Management: {How are secrets handled in code? Reference `docs/environment-vars.md` regarding storage.}
- Dependency Security: {Policy on checking for vulnerable dependencies.}
- Authentication/Authorization Checks: {Where should these be enforced?}
- {Other relevant practices...}

## Change Log

| Change        | Date       | Version | Description   | Author         |
| ------------- | ---------- | ------- | ------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft | {Agent/Person} |
| ...           | ...        | ...     | ...           | ...            |
"""

def get_data_models_template_markdown() -> str:
    return """
# {Project Name} Data Models

## Core Application Entities / Domain Objects

{Define the main objects/concepts the application works with. Repeat subsection for each key entity.}

### {Entity Name, e.g., User, Order, Product}

- **Description:** {What does this entity represent?}
- **Schema / Interface Definition:**
  ```typescript
  // Example using TypeScript Interface
  export interface {EntityName} {
    id: string; // {Description, e.g., Unique identifier}
    propertyName: string; // {Description}
    optionalProperty?: number; // {Description}
    // ... other properties
  }
  ```
  _(Alternatively, use JSON Schema, class definitions, or other relevant format)_
- **Validation Rules:** {List any specific validation rules beyond basic types - e.g., max length, format, range.}

### {Another Entity Name}

{...}

## API Payload Schemas (If distinct)

{Define schemas specifically for data sent to or received from APIs, if they differ significantly from the core entities. Reference `docs/api-reference.md`.}

### {API Endpoint / Purpose, e.g., Create Order Request}

- **Schema / Interface Definition:**
  ```typescript
  // Example
  export interface CreateOrderRequest {
    customerId: string;
    items: { productId: string; quantity: number }[];
    // ...
  }
  ```

### {Another API Payload}

{...}

## Database Schemas (If applicable)

{If using a database, define table structures or document database schemas.}

### {Table / Collection Name}

- **Purpose:** {What data does this table store?}
- **Schema Definition:**
  ```sql
  -- Example SQL
  CREATE TABLE {TableName} (
    id VARCHAR(36) PRIMARY KEY,
    column_name VARCHAR(255) NOT NULL,
    numeric_column DECIMAL(10, 2),
    -- ... other columns, indexes, constraints
  );
  ```
  _(Alternatively, use ORM model definitions, NoSQL document structure, etc.)_

### {Another Table / Collection Name}

{...}

## State File Schemas (If applicable)

{If the application uses files for persisting state.}

### {State File Name / Purpose, e.g., processed_items.json}

- **Purpose:** {What state does this file track?}
- **Format:** {e.g., JSON}
- **Schema Definition:**
  ```json
  {
    "type": "object",
    "properties": {
      "processedIds": {
        "type": "array",
        "items": {
          "type": "string"
        },
        "description": "List of IDs that have been processed."
      }
      // ... other state properties
    },
    "required": ["processedIds"]
  }
  ```

## Change Log

| Change        | Date       | Version | Description   | Author         |
| ------------- | ---------- | ------- | ------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft | {Agent/Person} |
| ...           | ...        | ...     | ...           | ...            |
"""

def get_environment_vars_template_markdown() -> str:
    return """
# {Project Name} Environment Variables

## Configuration Loading Mechanism

{Describe how environment variables are loaded into the application.}

- **Local Development:** {e.g., Using `.env` file with `dotenv` library.}
- **Deployment (e.g., AWS Lambda, Kubernetes):** {e.g., Set via Lambda function configuration, Kubernetes Secrets/ConfigMaps.}

## Required Variables

{List all environment variables used by the application.}

| Variable Name        | Description                                     | Example / Default Value               | Required? (Yes/No) | Sensitive? (Yes/No) |
| :------------------- | :---------------------------------------------- | :------------------------------------ | :----------------- | :------------------ |
| `NODE_ENV`           | Runtime environment                             | `development` / `production`          | Yes                | No                  |
| `PORT`               | Port the application listens on (if applicable) | `8080`                                | No                 | No                  |
| `DATABASE_URL`       | Connection string for the primary database      | `postgresql://user:pass@host:port/db` | Yes                | Yes                 |
| `EXTERNAL_API_KEY`   | API Key for {External Service Name}             | `sk_...`                              | Yes                | Yes                 |
| `S3_BUCKET_NAME`     | Name of the S3 bucket for {Purpose}             | `my-app-data-bucket-...`              | Yes                | No                  |
| `FEATURE_FLAG_X`     | Enables/disables experimental feature X         | `false`                               | No                 | No                  |
| `{ANOTHER_VARIABLE}` | {Description}                                   | {Example}                             | {Yes/No}           | {Yes/No}            |
| ...                  | ...                                             | ...                                   | ...                | ...                 |

## Notes

- **Secrets Management:** {Explain how sensitive variables (API Keys, passwords) should be handled, especially in production (e.g., "Use AWS Secrets Manager", "Inject via CI/CD pipeline").}
- **`.env.example`:** {Mention that an `.env.example` file should be maintained in the repository with placeholder values for developers.}
- **Validation:** {Is there code that validates the presence or format of these variables at startup?}

## Change Log

| Change        | Date       | Version | Description   | Author         |
| ------------- | ---------- | ------- | ------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft | {Agent/Person} |
| ...           | ...        | ...     | ...           | ...            |
"""

def get_project_structure_template_markdown() -> str:
    return """
# {Project Name} Project Structure

{Provide an ASCII or Mermaid diagram representing the project's folder structure such as the following example.}

```plaintext
{project-root}/
├── .github/                    # CI/CD workflows (e.g., GitHub Actions)
│   └── workflows/
│       └── main.yml
├── .vscode/                    # VSCode settings (optional)
│   └── settings.json
├── build/                      # Compiled output (if applicable, often git-ignored)
├── config/                     # Static configuration files (if any)
├── docs/                       # Project documentation (PRD, Arch, etc.)
│   ├── index.md
│   └── ... (other .md files)
├── infra/                      # Infrastructure as Code (e.g., CDK, Terraform)
│   └── lib/
│   └── bin/
├── node_modules/               # Project dependencies (git-ignored)
├── scripts/                    # Utility scripts (build, deploy helpers, etc.)
├── src/                        # Application source code
│   ├── common/                 # Shared utilities, types, constants
│   ├── components/             # Reusable UI components (if UI exists)
│   ├── features/               # Feature-specific modules (alternative structure)
│   │   └── feature-a/
│   ├── core/                   # Core business logic
│   ├── clients/                # External API/Service clients
│   ├── services/               # Internal services / Cloud SDK wrappers
│   ├── pages/ / routes/        # UI pages or API route definitions
│   └── main.ts / index.ts / app.ts # Application entry point
├── stories/                    # Generated story files for development (optional)
│   └── epic1/
├── test/                       # Automated tests
│   ├── unit/                   # Unit tests (mirroring src structure)
│   ├── integration/            # Integration tests
│   └── e2e/                    # End-to-end tests
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore rules
├── package.json                # Project manifest and dependencies
├── tsconfig.json               # TypeScript configuration (if applicable)
├── Dockerfile                  # Docker build instructions (if applicable)
└── README.md                   # Project overview and setup instructions
```

(Adjust the example tree based on the actual project type - e.g., Python would have requirements.txt, etc.)

## Key Directory Descriptions

docs/: Contains all project planning and reference documentation.
infra/: Holds the Infrastructure as Code definitions (e.g., AWS CDK, Terraform).
src/: Contains the main application source code.
common/: Code shared across multiple modules (utilities, types, constants). Avoid business logic here.
core/ / domain/: Core business logic, entities, use cases, independent of frameworks/external services.
clients/: Modules responsible for communicating with external APIs or services.
services/ / adapters/ / infrastructure/: Implementation details, interactions with databases, cloud SDKs, frameworks.
routes/ / controllers/ / pages/: Entry points for API requests or UI views.
test/: Contains all automated tests, mirroring the src/ structure where applicable.
scripts/: Helper scripts for build, deployment, database migrations, etc.

## Notes

{Mention any specific build output paths, compiler configuration pointers, or other relevant structural notes.}

## Change Log

| Change        | Date       | Version | Description   | Author         |
| ------------- | ---------- | ------- | ------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft | {Agent/Person} |
| ...           | ...        | ...     | ...           | ...            |
"""

def get_tech_stack_template_markdown() -> str:
    return """
# {Project Name} Technology Stack

## Technology Choices

| Category             | Technology              | Version / Details | Description / Purpose                   | Justification (Optional) |
| :------------------- | :---------------------- | :---------------- | :-------------------------------------- | :----------------------- |
| **Languages**        | {e.g., TypeScript}      | {e.g., 5.x}       | {Primary language for backend/frontend} | {Why this language?}     |
|                      | {e.g., Python}          | {e.g., 3.11}      | {Used for data processing, ML}          | {...}                    |
| **Runtime**          | {e.g., Node.js}         | {e.g., 22.x}      | {Server-side execution environment}     | {...}                    |
| **Frameworks**       | {e.g., NestJS}          | {e.g., 10.x}      | {Backend API framework}                 | {Why this framework?}    |
|                      | {e.g., React}           | {e.g., 18.x}      | {Frontend UI library}                   | {...}                    |
| **Databases**        | {e.g., PostgreSQL}      | {e.g., 15}        | {Primary relational data store}         | {...}                    |
|                      | {e.g., Redis}           | {e.g., 7.x}       | {Caching, session storage}              | {...}                    |
| **Cloud Platform**   | {e.g., AWS}             | {N/A}             | {Primary cloud provider}                | {...}                    |
| **Cloud Services**   | {e.g., AWS Lambda}      | {N/A}             | {Serverless compute}                    | {...}                    |
|                      | {e.g., AWS S3}          | {N/A}             | {Object storage for assets/state}       | {...}                    |
|                      | {e.g., AWS EventBridge} | {N/A}             | {Event bus / scheduled tasks}           | {...}                    |
| **Infrastructure**   | {e.g., AWS CDK}         | {e.g., Latest}    | {Infrastructure as Code tool}           | {...}                    |
|                      | {e.g., Docker}          | {e.g., Latest}    | {Containerization}                      | {...}                    |
| **UI Libraries**     | {e.g., Material UI}     | {e.g., 5.x}       | {React component library}               | {...}                    |
| **State Management** | {e.g., Redux Toolkit}   | {e.g., Latest}    | {Frontend state management}             | {...}                    |
| **Testing**          | {e.g., Jest}            | {e.g., Latest}    | {Unit/Integration testing framework}    | {...}                    |
|                      | {e.g., Playwright}      | {e.g., Latest}    | {End-to-end testing framework}          | {...}                    |
| **CI/CD**            | {e.g., GitHub Actions}  | {N/A}             | {Continuous Integration/Deployment}     | {...}                    |
| **Other Tools**      | {e.g., LangChain.js}    | {e.g., Latest}    | {LLM interaction library}               | {...}                    |
|                      | {e.g., Cheerio}         | {e.g., Latest}    | {HTML parsing/scraping}                 | {...}                    |

## Change Log

| Change        | Date       | Version | Description   | Author         |
| ------------- | ---------- | ------- | ------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft | {Agent/Person} |
| ...           | ...        | ...     | ...           |
"""

def get_testing_strategy_template_markdown() -> str:
    return """
# {Project Name} Testing Strategy

## Testing Approach

{Describe the overall testing philosophy and approach for the project.}

- **Testing Pyramid:** {Describe the balance between unit, integration, and E2E tests.}
- **Test-Driven Development (TDD):** {Is TDD expected? If so, describe the approach.}
- **Code Coverage Goals:** {Target percentage for code coverage, if applicable.}
- **Critical Paths:** {Identify the most critical user journeys that must be thoroughly tested.}

## Test Types and Tools

{Describe each type of test that will be implemented and the tools used.}

### Unit Tests

- **Framework:** {e.g., Jest, Mocha, pytest, JUnit}
- **Location:** `test/unit/`
- **Scope:** {What should be unit tested? e.g., Individual functions, classes, components}
- **Mocking Strategy:** {How should external dependencies be mocked?}
- **Example:**
  ```typescript
  // Example unit test
  describe('calculateTotal', () => {
    it('should add tax to the subtotal', () => {
      const result = calculateTotal(100, 0.1);
      expect(result).toBe(110);
    });
  });
  ```

### Integration Tests

- **Framework:** {e.g., Jest, Supertest, pytest}
- **Location:** `test/integration/`
- **Scope:** {What should be integration tested? e.g., API endpoints, database interactions}
- **Test Database Strategy:** {How should test databases be handled? e.g., In-memory DB, test containers}
- **Example:**
  ```typescript
  // Example integration test
  describe('User API', () => {
    it('should create a new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ name: 'Test User', email: 'test@example.com' });

      expect(response.status).toBe(201);
      expect(response.body).toHaveProperty('id');
    });
  });
  ```

### End-to-End (E2E) Tests

- **Framework:** {e.g., Playwright, Cypress, Selenium}
- **Location:** `test/e2e/`
- **Scope:** {What user journeys should be E2E tested?}
- **Environment:** {Where should E2E tests run? e.g., Local, CI/CD pipeline, staging}
- **Example:**
  ```typescript
  // Example E2E test
  test('user can log in and view dashboard', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'user@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('h1')).toContainText('Dashboard');
  });
  ```

### Performance Tests (If Applicable)

- **Framework:** {e.g., k6, JMeter, Locust}
- **Location:** `test/performance/`
- **Scope:** {What performance aspects should be tested? e.g., Load testing, stress testing}
- **Metrics:** {What metrics should be measured? e.g., Response time, throughput, error rate}

## Test Data Management

- **Approach:** {How should test data be managed? e.g., Fixtures, factories, seeding scripts}
- **Location:** {Where should test data be stored? e.g., `test/fixtures/`}
- **Sensitive Data:** {How should sensitive test data be handled?}

## Continuous Integration (CI) Testing

- **CI Platform:** {e.g., GitHub Actions, CircleCI, Jenkins}
- **Test Execution:** {When should tests run? e.g., On every PR, nightly}
- **Test Reporting:** {How should test results be reported? e.g., JUnit XML, HTML reports}
- **Failure Handling:** {What happens when tests fail? e.g., Block PR, notify team}

## Testing Best Practices

- **Naming Conventions:** {How should tests be named? e.g., `describe('when X', () => it('should Y', () => {...}))`}
- **Test Isolation:** {How should tests be isolated? e.g., Reset state between tests}
- **Flaky Tests:** {How should flaky tests be handled? e.g., Retry mechanism, quarantine}
- **Test Documentation:** {How should tests be documented? e.g., Comments, README}

## Change Log

| Change        | Date       | Version | Description   | Author         |
| ------------- | ---------- | ------- | ------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft | {Agent/Person} |
| ...           | ...        | ...     | ...           | ...            |
"""

def get_api_reference_template_markdown() -> str:
    return """
# {Project Name} API Reference

## API Overview

{Provide a brief overview of the API's purpose, style (REST, GraphQL, etc.), and general structure.}

- **Base URL:** {e.g., `https://api.example.com/v1` or environment variable reference}
- **Authentication:** {Describe the authentication mechanism - e.g., Bearer token, API key, OAuth2}
- **Content Types:** {e.g., `application/json`, `multipart/form-data`}
- **Error Handling:** {Describe the general error response format and status code usage}

## Endpoints

{Repeat this section for each endpoint or group of related endpoints.}

### {Endpoint Group, e.g., User Management}

#### `{HTTP Method} {Path}`

{e.g., `POST /api/users`}

**Purpose:** {Brief description of what this endpoint does.}

**Request:**

- **Headers:**
  ```
  Authorization: Bearer {token}
  Content-Type: application/json
  ```

- **Path Parameters:**
  | Parameter | Type   | Required | Description           |
  | :-------- | :----- | :------- | :-------------------- |
  | `userId`  | string | Yes      | The ID of the user    |

- **Query Parameters:**
  | Parameter | Type    | Required | Default | Description                      |
  | :-------- | :------ | :------- | :------ | :------------------------------- |
  | `limit`   | integer | No       | 20      | Number of items per page         |
  | `page`    | integer | No       | 1       | Page number for pagination       |

- **Request Body:**
  ```json
  {
    "name": "string",
    "email": "string",
    "role": "string"
  }
  ```

  | Field   | Type   | Required | Description                                |
  | :------ | :----- | :------- | :----------------------------------------- |
  | `name`  | string | Yes      | The user's full name                       |
  | `email` | string | Yes      | The user's email address (must be unique)  |
  | `role`  | string | No       | The user's role (default: "user")          |

**Response:**

- **Status Codes:**
  | Code | Description                                          |
  | :--- | :--------------------------------------------------- |
  | 201  | Created - User was successfully created              |
  | 400  | Bad Request - Invalid request body or parameters     |
  | 401  | Unauthorized - Authentication required               |
  | 403  | Forbidden - Insufficient permissions                 |
  | 409  | Conflict - Resource already exists (e.g., email)     |
  | 500  | Internal Server Error - Something went wrong         |

- **Response Body (Success):**
  ```json
  {
    "id": "string",
    "name": "string",
    "email": "string",
    "role": "string",
    "createdAt": "string (ISO date)"
  }
  ```

  | Field       | Type   | Description                                |
  | :---------- | :----- | :----------------------------------------- |
  | `id`        | string | Unique identifier for the user             |
  | `name`      | string | The user's full name                       |
  | `email`     | string | The user's email address                   |
  | `role`      | string | The user's role                            |
  | `createdAt` | string | ISO 8601 date when the user was created    |

- **Response Body (Error):**
  ```json
  {
    "error": {
      "code": "string",
      "message": "string",
      "details": [
        {
          "field": "string",
          "message": "string"
        }
      ]
    }
  }
  ```

**Example:**

```bash
# Request
curl -X POST https://api.example.com/v1/users \\
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." \\
  -H "Content-Type: application/json" \\
  -d '{
    "name": "John Doe",
    "email": "john.doe@example.com",
    "role": "admin"
  }'

# Response
{
  "id": "usr_123456789",
  "name": "John Doe",
  "email": "john.doe@example.com",
  "role": "admin",
  "createdAt": "2023-01-01T12:00:00Z"
}
```

#### `{HTTP Method} {Path}`

{Repeat for each endpoint...}

## External APIs Consumed

{List any external APIs that this application consumes.}

### {External API Name}

- **Purpose:** {What this API is used for in the application}
- **Base URL:** {The base URL of the external API}
- **Authentication:** {How authentication is handled with this API}
- **Key Endpoints Used:**
  - `GET /endpoint1` - {Purpose}
  - `POST /endpoint2` - {Purpose}
- **Rate Limits:** {Any rate limiting considerations}
- **Documentation Link:** {Link to the external API's documentation}

## Data Models

{Reference the data models document or include simplified versions here.}

```typescript
// User model
interface User {
  id: string;
  name: string;
  email: string;
  role: string;
  createdAt: string; // ISO 8601 date
}
```

## Change Log

| Change        | Date       | Version | Description   | Author         |
| ------------- | ---------- | ------- | ------------- | -------------- |
| Initial draft | YYYY-MM-DD | 0.1     | Initial draft | {Agent/Person} |
| ...           | ...        | ...     | ...           | ...            |
"""

def get_architect_checklist_markdown() -> str:
    return """
# Architect Solution Validation Checklist

This checklist serves as a comprehensive framework for the Architect to validate the technical design and architecture before development execution. The Architect should systematically work through each item, ensuring the architecture is robust, scalable, secure, and aligned with the product requirements.

## 1. REQUIREMENTS ALIGNMENT

### 1.1 Functional Requirements Coverage

- [ ] Architecture supports all functional requirements in the PRD
- [ ] Technical approaches for all epics and stories are addressed
- [ ] Edge cases and performance scenarios are considered
- [ ] All required integrations are accounted for
- [ ] User journeys are supported by the technical architecture

### 1.2 Non-Functional Requirements Alignment

- [ ] Performance requirements are addressed with specific solutions
- [ ] Scalability considerations are documented with approach
- [ ] Security requirements have corresponding technical controls
- [ ] Reliability and resilience approaches are defined
- [ ] Compliance requirements have technical implementations

### 1.3 Technical Constraints Adherence

- [ ] All technical constraints from PRD are satisfied
- [ ] Platform/language requirements are followed
- [ ] Infrastructure constraints are accommodated
- [ ] Third-party service constraints are addressed
- [ ] Organizational technical standards are followed

## 2. ARCHITECTURE FUNDAMENTALS

### 2.1 Architecture Clarity

- [ ] Architecture is documented with clear diagrams
- [ ] Major components and their responsibilities are defined
- [ ] Component interactions and dependencies are mapped
- [ ] Data flows are clearly illustrated
- [ ] Technology choices for each component are specified

### 2.2 Separation of Concerns

- [ ] Clear boundaries between UI, business logic, and data layers
- [ ] Responsibilities are cleanly divided between components
- [ ] Interfaces between components are well-defined
- [ ] Components adhere to single responsibility principle
- [ ] Cross-cutting concerns (logging, auth, etc.) are properly addressed

### 2.3 Design Patterns & Best Practices

- [ ] Appropriate design patterns are employed
- [ ] Industry best practices are followed
- [ ] Anti-patterns are avoided
- [ ] Consistent architectural style throughout
- [ ] Pattern usage is documented and explained

### 2.4 Modularity & Maintainability

- [ ] System is divided into cohesive, loosely-coupled modules
- [ ] Components can be developed and tested independently
- [ ] Changes can be localized to specific components
- [ ] Code organization promotes discoverability
- [ ] Architecture specifically designed for AI agent implementation

## 3. TECHNICAL STACK & DECISIONS

### 3.1 Technology Selection

- [ ] Selected technologies meet all requirements
- [ ] Technology versions are specifically defined (not ranges)
- [ ] Technology choices are justified with clear rationale
- [ ] Alternatives considered are documented with pros/cons
- [ ] Selected stack components work well together

### 3.2 Frontend Architecture

- [ ] UI framework and libraries are specifically selected
- [ ] State management approach is defined
- [ ] Component structure and organization is specified
- [ ] Responsive/adaptive design approach is outlined
- [ ] Build and bundling strategy is determined

### 3.3 Backend Architecture

- [ ] API design and standards are defined
- [ ] Service organization and boundaries are clear
- [ ] Authentication and authorization approach is specified
- [ ] Error handling strategy is outlined
- [ ] Backend scaling approach is defined

### 3.4 Data Architecture

- [ ] Data models are fully defined
- [ ] Database technologies are selected with justification
- [ ] Data access patterns are documented
- [ ] Data migration/seeding approach is specified
- [ ] Data backup and recovery strategies are outlined

## 4. RESILIENCE & OPERATIONAL READINESS

### 4.1 Error Handling & Resilience

- [ ] Error handling strategy is comprehensive
- [ ] Retry policies are defined where appropriate
- [ ] Circuit breakers or fallbacks are specified for critical services
- [ ] Graceful degradation approaches are defined
- [ ] System can recover from partial failures

### 4.2 Monitoring & Observability

- [ ] Logging strategy is defined
- [ ] Monitoring approach is specified
- [ ] Key metrics for system health are identified
- [ ] Alerting thresholds and strategies are outlined
- [ ] Debugging and troubleshooting capabilities are built in

### 4.3 Performance & Scaling

- [ ] Performance bottlenecks are identified and addressed
- [ ] Caching strategy is defined where appropriate
- [ ] Load balancing approach is specified
- [ ] Horizontal and vertical scaling strategies are outlined
- [ ] Resource sizing recommendations are provided

### 4.4 Deployment & DevOps

- [ ] Deployment strategy is defined
- [ ] CI/CD pipeline approach is outlined
- [ ] Environment strategy (dev, staging, prod) is specified
- [ ] Infrastructure as Code approach is defined
- [ ] Rollback and recovery procedures are outlined

## 5. SECURITY & COMPLIANCE

### 5.1 Authentication & Authorization

- [ ] Authentication mechanism is clearly defined
- [ ] Authorization model is specified
- [ ] Role-based access control is outlined if required
- [ ] Session management approach is defined
- [ ] Credential management is addressed

### 5.2 Data Security

- [ ] Data encryption approach (at rest and in transit) is specified
- [ ] Sensitive data handling procedures are defined
- [ ] Data retention and purging policies are outlined
- [ ] Backup encryption is addressed if required
- [ ] Data access audit trails are specified if required

### 5.3 API & Service Security

- [ ] API security controls are defined
- [ ] Rate limiting and throttling approaches are specified
- [ ] Input validation strategy is outlined
- [ ] CSRF/XSS prevention measures are addressed
- [ ] Secure communication protocols are specified

### 5.4 Infrastructure Security

- [ ] Network security design is outlined
- [ ] Firewall and security group configurations are specified
- [ ] Service isolation approach is defined
- [ ] Least privilege principle is applied
- [ ] Security monitoring strategy is outlined

## 6. IMPLEMENTATION GUIDANCE

### 6.1 Coding Standards & Practices

- [ ] Coding standards are defined
- [ ] Documentation requirements are specified
- [ ] Testing expectations are outlined
- [ ] Code organization principles are defined
- [ ] Naming conventions are specified

### 6.2 Testing Strategy

- [ ] Unit testing approach is defined
- [ ] Integration testing strategy is outlined
- [ ] E2E testing approach is specified
- [ ] Performance testing requirements are outlined
- [ ] Security testing approach is defined

### 6.3 Development Environment

- [ ] Local development environment setup is documented
- [ ] Required tools and configurations are specified
- [ ] Development workflows are outlined
- [ ] Source control practices are defined
- [ ] Dependency management approach is specified

### 6.4 Technical Documentation

- [ ] API documentation standards are defined
- [ ] Architecture documentation requirements are specified
- [ ] Code documentation expectations are outlined
- [ ] System diagrams and visualizations are included
- [ ] Decision records for key choices are included

## 7. DEPENDENCY & INTEGRATION MANAGEMENT

### 7.1 External Dependencies

- [ ] All external dependencies are identified
- [ ] Versioning strategy for dependencies is defined
- [ ] Fallback approaches for critical dependencies are specified
- [ ] Licensing implications are addressed
- [ ] Update and patching strategy is outlined

### 7.2 Internal Dependencies

- [ ] Component dependencies are clearly mapped
- [ ] Build order dependencies are addressed
- [ ] Shared services and utilities are identified
- [ ] Circular dependencies are eliminated
- [ ] Versioning strategy for internal components is defined

### 7.3 Third-Party Integrations

- [ ] All third-party integrations are identified
- [ ] Integration approaches are defined
- [ ] Authentication with third parties is addressed
- [ ] Error handling for integration failures is specified
- [ ] Rate limits and quotas are considered

## 8. AI AGENT IMPLEMENTATION SUITABILITY

### 8.1 Modularity for AI Agents

- [ ] Components are sized appropriately for AI agent implementation
- [ ] Dependencies between components are minimized
- [ ] Clear interfaces between components are defined
- [ ] Components have singular, well-defined responsibilities
- [ ] File and code organization optimized for AI agent understanding

### 8.2 Clarity & Predictability

- [ ] Patterns are consistent and predictable
- [ ] Complex logic is broken down into simpler steps
- [ ] Architecture avoids overly clever or obscure approaches
- [ ] Examples are provided for unfamiliar patterns
- [ ] Component responsibilities are explicit and clear

### 8.3 Implementation Guidance

- [ ] Detailed implementation guidance is provided
- [ ] Code structure templates are defined
- [ ] Specific implementation patterns are documented
- [ ] Common pitfalls are identified with solutions
- [ ] References to similar implementations are provided when helpful

### 8.4 Error Prevention & Handling

- [ ] Design reduces opportunities for implementation errors
- [ ] Validation and error checking approaches are defined
- [ ] Self-healing mechanisms are incorporated where possible
- [ ] Testing patterns are clearly defined
- [ ] Debugging guidance is provided

## ARCHITECTURE VALIDATION SUMMARY

### Category Statuses
| Category | Status | Critical Issues |
|----------|--------|----------------|
| 1. Requirements Alignment | PASS/FAIL/PARTIAL | |
| 2. Architecture Fundamentals | PASS/FAIL/PARTIAL | |
| 3. Technical Stack & Decisions | PASS/FAIL/PARTIAL | |
| 4. Resilience & Operational Readiness | PASS/FAIL/PARTIAL | |
| 5. Security & Compliance | PASS/FAIL/PARTIAL | |
| 6. Implementation Guidance | PASS/FAIL/PARTIAL | |
| 7. Dependency & Integration Management | PASS/FAIL/PARTIAL | |
| 8. AI Agent Implementation Suitability | PASS/FAIL/PARTIAL | |

### Critical Deficiencies
- List all critical issues that must be addressed before handoff to PO/SM

### Recommendations
- Provide specific recommendations for addressing each deficiency

### Final Decision
- **READY FOR PO/SM**: The architecture is comprehensive, properly structured, and ready for story refinement.
- **NEEDS REFINEMENT**: The architecture requires additional work to address the identified deficiencies.
"""