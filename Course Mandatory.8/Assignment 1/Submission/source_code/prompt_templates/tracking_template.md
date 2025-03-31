# Performance Tracking Prompt Template

This template provides a flexible structure for prompts related to project performance tracking, including setting up metrics, creating dashboards, and reporting. It can be adapted for various performance tracking scenarios by modifying the specific parameters and requests.

## Basic Template Structure

```
Act as a project analytics consultant specializing in [METHODOLOGY] projects in the [INDUSTRY] sector. I'm managing a [PROJECT TYPE] project and need to establish effective [TRACKING FOCUS]. Key stakeholders are particularly interested in [STAKEHOLDER CONCERNS]. My experience level as a project manager is [EXPERIENCE LEVEL], and we currently use [TOOLS/PLATFORMS] for project management.

Project context:
- Team size/composition: [TEAM DESCRIPTION]
- Project duration: [TIMELINE]
- Reporting frequency: [REPORTING CADENCE]
- Key constraints: [CONSTRAINTS]

Please provide:
1. [NUMBER] specific [METRICS/KPIs] most relevant for our project context, with calculation methods
2. [SPECIFIC VISUALIZATION REQUEST] that effectively communicates our project status
3. [DATA COLLECTION REQUEST] that minimizes team overhead
4. Guidance on [SPECIFIC TRACKING CHALLENGE]
5. [SPECIFIC REPORTING/ANALYSIS REQUEST]

For each recommendation:
- Explain its specific relevance to our project type and methodology
- Provide implementation steps using our available tools
- Include examples of how to interpret the data for decision-making
- Address common pitfalls and how to avoid them

Please focus on practical solutions that can be implemented with reasonable effort, and consider both immediate setup needs and long-term sustainability.
```

## Parameter Guidance

When using this template, replace the placeholders with specific information:

- **[METHODOLOGY]**: Project approach (e.g., "Agile," "Waterfall," "Hybrid")
- **[INDUSTRY]**: Specific industry context (e.g., "software development," "construction," "healthcare")
- **[PROJECT TYPE]**: Nature of the project (e.g., "product development," "system implementation")
- **[TRACKING FOCUS]**: Monitoring emphasis (e.g., "performance metrics," "status reporting system")
- **[STAKEHOLDER CONCERNS]**: Key interests (e.g., "delivery predictability and quality," "budget adherence")
- **[EXPERIENCE LEVEL]**: Your PM experience (e.g., "Beginner," "Intermediate," "Advanced")
- **[TOOLS/PLATFORMS]**: Tools being used (e.g., "Microsoft Project and Power BI," "Jira and Confluence")
- **[TEAM DESCRIPTION]**: Team makeup (e.g., "12 cross-functional team members," "5 internal staff with contractors")
- **[TIMELINE]**: Project duration (e.g., "6-month project," "2-year program with quarterly releases")
- **[REPORTING CADENCE]**: Frequency (e.g., "weekly," "bi-weekly," "monthly")
- **[CONSTRAINTS]**: Limitations (e.g., "limited tool access," "minimal team availability for reporting")
- **[NUMBER]**: Quantity requested (e.g., "5-7," "3-5")
- **[METRICS/KPIs]**: Metric type (e.g., "KPIs," "performance indicators," "quality metrics")
- **[SPECIFIC VISUALIZATION REQUEST]**: Visual needs (e.g., "dashboard design," "executive summary visualization")
- **[DATA COLLECTION REQUEST]**: Collection needs (e.g., "data collection methods," "automated tracking approaches")
- **[SPECIFIC TRACKING CHALLENGE]**: Particular issue (e.g., "establishing meaningful baselines," "tracking remote team productivity")
- **[SPECIFIC REPORTING/ANALYSIS REQUEST]**: Reporting needs (e.g., "stakeholder-specific reporting templates," "variance analysis framework")

## Adaptation Examples

### For Setting Up Project Metrics

```
Act as a project analytics consultant specializing in Agile projects in the software development sector. I'm managing a customer portal development project and need to establish effective performance metrics. Key stakeholders are particularly interested in delivery predictability and quality. My experience level as a project manager is Intermediate, and we currently use Jira and Confluence for project management.

Project context:
- Team size/composition: 8 developers, 2 QA specialists, 1 UX designer
- Project duration: 6-month project with 2-week sprints
- Reporting frequency: Weekly team metrics, bi-weekly stakeholder updates
- Key constraints: Limited familiarity with metrics beyond basic velocity tracking

Please provide:
1. 5-7 specific KPIs most relevant for our Agile development project, with calculation methods
2. Dashboard design recommendations that effectively communicate our project status to different audiences
3. Data collection methods that minimize manual tracking and leverage our Jira implementation
4. Guidance on establishing appropriate baselines and targets for each metric
5. Framework for using metrics to identify risks and improvement opportunities

For each recommendation:
- Explain its specific relevance to our project type and methodology
- Provide implementation steps using our available tools
- Include examples of how to interpret the data for decision-making
- Address common pitfalls and how to avoid them

Please focus on practical solutions that can be implemented with reasonable effort, and consider both immediate setup needs and long-term sustainability.
```

### For Project Status Reporting

```
Act as a project analytics consultant specializing in Waterfall projects in the construction sector. I'm managing a commercial building renovation project and need to establish effective status reporting. Key stakeholders are particularly interested in budget adherence and timeline compliance. My experience level as a project manager is Advanced, and we currently use Microsoft Project and Excel for project management.

Project context:
- Team size/composition: 3 internal project team members managing multiple contractors
- Project duration: 12-month project with phased completion milestones
- Reporting frequency: Weekly team updates, monthly executive committee reviews
- Key constraints: Executive stakeholders have limited time and prefer concise visual reporting

Please provide:
1. 3-5 specific reporting templates tailored to different stakeholder groups
2. Visual dashboard design that effectively communicates budget, schedule, and risk status
3. Data collection methods that can be completed in under 2 hours per week
4. Guidance on reporting variances and recovery plans
5. Approach for integrating contractor progress reports into overall project status

For each recommendation:
- Explain its specific relevance to our project type and methodology
- Provide implementation steps using our available tools
- Include examples of how to interpret the data for decision-making
- Address common pitfalls and how to avoid them

Please focus on practical solutions that can be implemented with reasonable effort, and consider both immediate setup needs and long-term sustainability.
```

## Usage Notes

- Begin with the system prompt template before using this performance tracking template
- Customize parameters based on the specific tracking needs and project context
- Be specific about stakeholder interests to get the most relevant metrics and reporting approaches
- Consider the effort required for data collection and maintenance when requesting metrics
- For complex reporting needs, consider separate prompts for metrics definition, data collection, and reporting
- Emphasize the connection between metrics and decision-making to ensure actionable insights