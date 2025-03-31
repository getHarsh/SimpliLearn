# Virtual Project Management Consultant

## Project Overview

This project develops a series of optimized prompts that enable ChatGPT to function as a virtual project management consultant. The prompts are designed to provide practical, relevant, and actionable advice on four key areas of project management:

1. Project Planning
2. Risk Management
3. Team Collaboration
4. Performance Tracking

The development process followed a systematic approach to prompt engineering, from initial research and design through multiple iterations of testing, refinement, and user feedback.

## Objectives

- Design and refine prompts that help ChatGPT offer practical, relevant, and actionable project management advice
- Demonstrate proficiency in prompt engineering by optimizing prompts for clarity, relevance, and user engagement
- Evaluate the effectiveness of the prompts based on user interactions and feedback

## Repository Structure

```
├── PM_Consultant_Project.ipynb        # Main notebook documenting the entire process
├── README.md                          # This file - project overview and instructions
├── docs/
│   ├── 00_DOMAIN_RESEARCH.md          # Research on project management methodologies & tools
│   ├── 01_INTERACTION_SCENARIOS.md    # Key scenarios and expected query types
│   ├── 02_PROMPT_DESIGN.md            # Initial prompt development process
│   ├── 03_TESTING_REFINEMENT.md       # Testing results and improvements
│   ├── 04_EVALUATION_CRITERIA.md      # Criteria for assessing prompt performance 
│   └── 05_USER_FEEDBACK.md            # User testing feedback and final optimizations
├── interactions/
│   ├── initial_prompts/               # Records of first-iteration prompt testing
│   ├── refined_prompts/               # Records of refined prompt testing
│   └── user_testing/                  # Records of user testing sessions
├── source_code/
│   ├── initial_prompts.md             # Document containing all initial prompts
│   ├── refined_prompts.md             # Document containing all refined prompts
│   ├── final_prompts.md               # Document containing final optimized prompts
│   └── prompt_templates/              # Reusable prompt templates for each scenario
├── evaluation/
│   ├── criteria_metrics.md            # Detailed evaluation criteria and metrics
│   ├── prompt_assessment.md           # Assessment of each prompt against criteria
│   └── improvement_log.md             # Log of improvements made through iterations
└── final_report.md                    # Comprehensive project report
```

## Development Process

This project follows the 10-step process outlined in the problem statement:

1. **Domain Selection and Research**: Investigated project management methodologies, common challenges, and best practices to establish a strong foundation for prompt design.

2. **Define Interaction Scenarios**: Identified key scenarios where a project manager would need assistance and outlined expected query types and responses.

3. **Initial Prompt Design**: Created initial prompts for each project management area based on domain research and interaction scenarios.

4. **Testing and Refinement**: Tested initial prompts with ChatGPT and analyzed responses for accuracy, relevance, and helpfulness.

5. **Iterative Optimization**: Conducted multiple iterations of testing and refinement, experimenting with different phrasing, context provision, and follow-up prompts.

6. **Evaluation Criteria Development**: Established specific criteria for evaluating prompt performance, including accuracy, relevance, clarity, and user satisfaction.

7. **User Feedback Collection**: Shared refined prompts with test users and collected feedback on interaction quality and usefulness.

8. **Final Optimization**: Incorporated user feedback to make final adjustments to the prompts.

9. **Documentation**: Documented the entire prompt engineering process, from initial designs to final optimized prompts.

10. **Future Improvement Suggestions**: Identified potential areas for further enhancement and proposed strategies for ongoing optimization.

## Key Features

- **Versatile Prompt Templates**: Adaptable templates for different project management scenarios
- **Context-Aware Responses**: Prompts designed to elicit responses that consider project context
- **Practical Actionability**: Focus on generating advice that can be immediately implemented
- **User-Centered Design**: Prompts refined based on actual user feedback and testing

## Usage Instructions

1. Open the main notebook `PM_Consultant_Project.ipynb` to review the complete development process.
2. Explore the `docs/` directory to understand the methodology behind each development phase.
3. Review the `source_code/final_prompts.md` file for the optimized prompts that can be used with ChatGPT.
4. Examine the `interactions/` directory to see example conversations that demonstrate the prompts in action.
5. Check the `evaluation/` directory to understand how prompt effectiveness was assessed.

## Future Work

The `final_report.md` includes suggestions for future improvements to the prompt engineering approach, including:

- Integration with project management tools
- Expansion to additional project management methodologies
- Development of specialized prompts for specific industries
- Creation of a comprehensive prompt library for different project phases
