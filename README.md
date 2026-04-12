---
title: Openenv
emoji: 🐠
colorFrom: blue
colorTo: pink
sdk: docker
app_port: 7860
pinned: false
license: mit
tags:
  - openenv
---

# Helpdesk OpenEnv Environment

This project simulates a realistic customer support system where an agent handles helpdesk tickets. The goal is to mimic how real support teams process user issues by taking a sequence of meaningful actions and completing the ticket lifecycle.

## Overview

In this environment, the agent behaves like a support executive. It receives a customer query and must decide how to handle it step by step — identifying the issue type, setting the urgency, assigning it to the correct team, responding to the user, and finally resolving the ticket.

This setup is designed to reflect real-world workflows used in companies that manage large volumes of customer requests.

## Tasks

Each task represents a different level of complexity in handling support tickets.

| Task   | Description                                  | Max Steps | Difficulty |
| ------ | -------------------------------------------- | --------- | ---------- |
| easy   | Identify issue category and priority         | 6         | Easy       |
| medium | Classify issue and assign correct team       | 8         | Medium     |
| hard   | Complete full workflow including reply + fix | 10        | Hard       |

## Action Space

The agent interacts with the environment by returning a JSON object containing an `action_type` and an optional `value`.

| Action           | Value                                                                         |
| ---------------- | ----------------------------------------------------------------------------- |
| `set_category`   | `billing`, `technical`, `account`, `shipping`, `security`                     |
| `set_priority`   | `low`, `medium`, `high`                                                       |
| `assign_team`    | `billing_team`, `tech_team`, `account_team`, `shipping_team`, `security_team` |
| `send_reply`     | free-text response to the customer                                            |
| `resolve_ticket` | `null`                                                                        |
| `request_info`   | short clarification question                                                  |
| `noop`           | `null`                                                                        |

## Observation Space

Each step returns structured information about the current ticket:

| Field            | Type   | Description                       |
| ---------------- | ------ | --------------------------------- |
| `task_name`      | string | Current task level                |
| `ticket_id`      | string | Unique identifier for the ticket  |
| `customer_tier`  | string | `free` or `premium`               |
| `message`        | string | Customer’s issue description      |
| `status`         | string | `open`, `in_progress`, `resolved` |
| `sla_hours_left` | int    | Remaining SLA time                |
| `history`        | string | Previous agent responses          |

## Reward Function

The environment provides feedback at every step to guide the agent toward a correct solution.

- Correct actions (`set_category`, `set_priority`, `assign_team`): **+0.05**
- Sending a meaningful reply: **+0.10**
- Resolving a ticket: **+0.10**
- Progress-based reward: **+0.2 × current_score**
- No operation (`noop`): **-0.02**
- Missing required value: **-0.05**
- Invalid or unknown action: **-0.10**
- Resolving without proper reply (hard task): **-0.10**

This reward design ensures the agent improves gradually rather than relying only on final outcomes.

## Setup

```bash
pip install -r requirements.txt
```
