# CivicAssist — Agents Architecture

This folder contains all AI agents and specifications for the CivicAssist multi-agent system.

## Agents
1. Main Agent (CivicAssistAgent)
2. ClassifierAgent
3. MapperAgent
4. PlannerAgent

## Flow
Complaint → ClassifierAgent → MapperAgent → PlannerAgent → Final JSON Response

## Responsibilities
- ClassifierAgent: Identify issue_type, confidence, highlights.
- MapperAgent: Map issue_type → department.
- PlannerAgent: Generate step-by-step action plan.

Each agent must output ONLY valid JSON.

Reference schemas:
- specs/a2a_schema.json
- specs/agent_api_schema.json
