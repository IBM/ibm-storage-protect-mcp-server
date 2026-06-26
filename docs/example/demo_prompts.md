# Demo Prompts

## 1. List Tools

What micro-MCP-servers and respective tools are available in the `sp-mcp-server-remote-tumbleweed`?

List all IBM Storage Protect commands that get called by the above tools.

## 2. How To Do

- Create a devclass `foo_devclass1`.
- Create a PRIMARY storage pool named `my_container_pool` using the DISK devclass with description "My storage pool".

## 3. What Is

- What are the steps to tier data from a container-type storage pool to a cloud-type storage pool? Show me an example of how to do this.
- What is `retset` and how is it related to a retention pool?

## 4. Advanced

- Run the tool: `run_servermon`.
- How many threads are running, and what is the DB status (almost full, locked)?
- Servermon log analysis of customer issues.

## 5. Solutioning

### Use Case

On `sp-mcp-server-remote-tumbleweed`, I am a Cloud Architect managing data movement to object storage. I want to validate our tiering efficiency. Analyze the age of data residing on high-performance disk versus the cloud tier. Identify data that meets "cold" criteria but hasn't moved, and automatically adjust migration thresholds to optimize storage costs.

On `sp-mcp-server-remote-tumbleweed`, the Capacity Planner managing IBM Storage Protect storage pools is asking: he wants to assess long-term storage sustainability. Retrieve storage utilization trends for the last 90 days, including deduplication savings, compression ratios, and daily data ingest rates across disk and cloud tiers. Forecast capacity exhaustion timelines and recommend repository expansion or data movement policy adjustments.

On `sp-mcp-server-remote-tumbleweed`, I am a Platform Owner monitoring system stability. I want to ensure the IBM Storage Protect internal database is optimized. Analyze database growth trends, reorganization status, and maintenance job success over the last 30 days. Identify potential performance risks due to database fragmentation and recommend optimization steps to prevent service latencies.

---

## Context Window Exhaustion: Problem and Solution

### Problem

The following prompt leads to a context window exhaustion issue:

> I am a Backup Engineer looking to reduce manual troubleshooting. Identify all failed or missed backup schedules in the last 24 hours. Categorize failures by root cause (e.g., communication errors, locked files, or out-of-space conditions).

### Solution

The following refined prompt avoids context window issues.

**Prompt:**

You are assisting a Backup Engineer to reduce manual troubleshooting in IBM Storage Protect.

**Goal:**
Identify all failed or missed client backup schedules in the last 24 hours and categorize each by likely root cause.

**Query Success Rules:**

1. Prefer the most constrained query possible before expanding scope.
2. Never call `query_scheduled_event` without first discovering a valid policy domain and relevant schedule names.
3. Never call `query_activity_log` without both:
   - a specific search term, and
   - a narrow date/time window.
4. If a query fails, retry once with a simpler but still constrained parameter set.
5. If a query still fails, state the exact failed query pattern and move to the next best constrained query.

**Required Execution Sequence:**

Step 1 — Discover Valid Scope
- Use `query_policy_group` first to identify valid policy domains.
- Use `query_schedule` with `domain_name` and `type="client"` to list candidate backup schedules.
- Focus only on schedules whose start times fall within the last 24 hours or whose period indicates daily execution.

Step 2 — Query Scheduled Events Using Narrow Scope
- Run `query_scheduled_event` only after identifying:
  - one valid `policy_group`
  - one or more exact `schedule_name` values
- Query one schedule at a time.
- Use date filters in `MM/DD/YYYY` format.
- If supported, add start and end times only in exact `HH-SS` format.
- Do not issue broad, all-domain event queries.

Step 3 — Keep Only Abnormal Events
- Retain only events with status Failed, Missed, Incomplete, or abnormal non-success result codes.

Step 4 — Validate Each Abnormal Event With Targeted Log Search
- Use `query_activity_log` only for one failed event at a time.
- Search using the most specific available discriminator, in this order:
  1. exact node name
  2. exact schedule name
  3. specific IBM message code, if already known
- Always include a narrow time window around the scheduled or actual event time.
- Start with a window of ±60 minutes.
- Expand only once to ±180 minutes if no evidence is found.
- Never run broad searches such as all `ANR*`, all `VMWARE_*`, or unbounded 24-hour log scans.

Step 5 — Root Cause Classification

Classify each event as one of the following:
- Communication error
- Locked file / file in use
- Out of space / storage pool full
- Authentication / node locked / password issue
- Schedule window / timeout / missed window
- Other / unknown

Step 6 — If `query_scheduled_event` Fails
- Retry once using a simpler valid call:
  - exact `policy_group`
  - exact `schedule_name`
  - date only, no time filters
- If it still fails, continue schedule-by-schedule using:
  - `query_schedule`
  - `query_client`
  - `query_active_session`
  - `query_storage_container`
- Mark findings as `Likely` instead of `Confirmed`.

Step 7 — If `query_activity_log` Fails
- Retry once with:
  - a single exact node or schedule search term
  - a smaller time window
- If it still fails, do not broaden the query.
- Use operational evidence from:
  - `query_client`
  - `query_active_session`
  - `query_storage_container`

**Output Format:**

- Executive Summary
  - Total confirmed failed events
  - Total confirmed missed events
  - Total likely abnormal schedules requiring validation
  - Count by root-cause category

- Confirmed Failed or Missed Schedules Table
  - Node
  - Schedule
  - Scheduled time
  - Status
  - Result code
  - Root cause category
  - Evidence summary (1 line)
  - Recommended next action (1 line)

- Likely Failed or Abnormal Schedules Table
  - Node
  - Schedule
  - Scheduled time
  - Why flagged
  - Likely root cause category
  - Recommended validation step

- Top Recurring Failure Patterns
- Environmental Risks
- Items Requiring Immediate Attention
- Limitations

**Constraints:**

- Limit analysis to the last 24 hours only.
- Use `query_policy_group` and `query_schedule` to discover valid inputs before `query_scheduled_event`.
- Use `query_activity_log` only with exact search terms and narrow time windows.
- Query one schedule at a time rather than all schedules at once.
- Query one failed event at a time rather than all logs at once.
- Do not include raw log dumps unless a single short message is essential as evidence.
- Clearly distinguish `Confirmed` from `Likely` findings.
