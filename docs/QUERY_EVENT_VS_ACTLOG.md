# IBM Storage Protect: QUERY EVENT vs QUERY ACTLOG

## Overview

This document clarifies the difference between two commonly confused IBM Storage Protect commands and their corresponding MCP server tools.

## IBM Storage Protect Commands

### 1. QUERY EVENT
- **Purpose**: Display scheduled backup/archive event execution history and status
- **Documentation**: https://www.ibm.com/docs/en/storage-protect/8.1.27?topic=events-query-event-display-client-schedules
- **Use Cases**:
  - Check if scheduled backups ran successfully
  - View past and future scheduled events
  - Monitor schedule execution status
  - Troubleshoot missed or failed scheduled operations

**Example Command**:
```
QUERY EVENT STANDARD VMWARE_MSWINDOWS00007_TUCSON_L
```

**Sample Output**:
```
Scheduled Start          Actual Start             Schedule Name     Node Name         Status
--------------------     --------------------     -------------     -------------     ---------
16/04/26   22:00:00      16/04/26   22:00:51      VMWARE_MSWIN-     MSWINDOWS000-     Started
                                                   DOWS00007_T-      07_TUCSON_L-
                                                   UCSON_L           AB_DM
```

### 2. QUERY ACTLOG
- **Purpose**: Search the activity/audit log for administrative commands, system messages, and events
- **Documentation**: https://www.ibm.com/docs/en/storage-protect/8.1.27?topic=commands-query-actlog-query-activity-log
- **Use Cases**:
  - Search for specific log messages
  - Audit administrative actions
  - Review system events and errors
  - Troubleshoot server operations

**Example Command**:
```
QUERY ACTLOG SEARCH=VMWARE_MSWINDOWS00007_TUCSON_L
```

**Sample Output**:
```
Date/Time: 04/16/2026 22:03:36
Message: ANR2017I Administrator TSMADMIN issued command: QUERY ACTLOG SEARCH=VMWARE_MSWINDOWS00007_TUCSON_L (SESSION: 71596)
```

## MCP Server Tools

### Tool Mapping

| IBM SP Command | MCP Tool Name | Server Group | Purpose |
|----------------|---------------|--------------|---------|
| `QUERY EVENT` | `query_scheduled_event` | policy (ISP_POLICIES_MANAGEMENT) | View scheduled event status |
| `QUERY ACTLOG` | `query_activity_log` | operations (ISP_OPS_MAINTENANCE) | Search activity logs |

### 1. query_scheduled_event (QUERY EVENT)

**Tool Name**: `query_scheduled_event`  
**IBM Command**: `QUERY EVENT`  
**Server Group**: policy (ISP_POLICIES_MANAGEMENT)

**Parameters**:
```json
{
  "policy_group": "STANDARD",           // Policy domain name (Optional)
  "schedule_name": "SCHEDULE_NAME",     // Schedule name (Optional)
  "begindate": "MM/DD/YYYY",            // Filter start date (Optional)
  "starttime": "HH:MM:SS",              // Filter start time (Optional)
  "enddate": "MM/DD/YYYY",              // Filter end date (Optional)
  "endtime": "HH:MM:SS"                 // Filter end time (Optional)
}
```

**Example Usage**:
```json
{
  "policy_group": "STANDARD",
  "schedule_name": "VMWARE_MSWINDOWS00007_TUCSON_L"
}
```

**Output Fields**:
- Scheduled Start: Planned execution time
- Actual Start: When it really ran
- Schedule Name: Name of the schedule
- Node Name: Client node name
- Status: Started, Completed, Missed, Failed, Future
- Result: Return code

### 2. query_activity_log (QUERY ACTLOG)

**Tool Name**: `query_activity_log`  
**IBM Command**: `QUERY ACTLOG`  
**Server Group**: operations (ISP_OPS_MAINTENANCE)

**Parameters**:
```json
{
  "search": "search_string",    // Search string to filter messages (Optional)
  "begintime": "HH:MM:SS",      // Start time (Optional)
  "endtime": "HH:MM:SS"         // End time (Optional)
}
```

**Example Usage**:
```json
{
  "search": "VMWARE_MSWINDOWS00007_TUCSON_L"
}
```

**Output Fields**:
- Date/Time: When the event occurred
- Message: The log message content
- Severity: Level of importance (Info, Warning, Error)

## Common Confusion Scenarios

### Scenario 1: "Query event for a schedule"
**User Intent**: Check if a scheduled backup ran  
**Correct Tool**: `query_scheduled_event`  
**Incorrect Tool**: ~~`query_activity_log`~~ (searches logs, not schedule status)

**Correct Usage**:
```
Prompt: "Query scheduled events for VMWARE_MSWINDOWS00007_TUCSON_L in STANDARD domain"
Tool: query_scheduled_event
Parameters: {"policy_group": "STANDARD", "schedule_name": "VMWARE_MSWINDOWS00007_TUCSON_L"}
```

### Scenario 2: "Search activity log for errors"
**User Intent**: Find error messages in the log  
**Correct Tool**: `query_activity_log`  
**Incorrect Tool**: ~~`query_scheduled_event`~~ (shows schedule status, not log messages)

**Correct Usage**:
```
Prompt: "Search activity log for ANR errors"
Tool: query_activity_log
Parameters: {"search": "ANR"}
```

## Changes Made to MCP Server

### 1. Renamed Tool (Breaking Change)
- **Old Name**: `query_event_log`
- **New Name**: `query_activity_log`
- **Reason**: Match IBM SP command name (QUERY ACTLOG) and avoid confusion with QUERY EVENT

### 2. Added New Tool
- **Tool Name**: `query_scheduled_event`
- **Command**: `QUERY EVENT`
- **Server Group**: ISP_POLICIES_MANAGEMENT
- **Purpose**: Provide proper access to scheduled event status

### 3. Enhanced Descriptions
Both tools now include:
- IBM SP command reference
- Clear purpose statements
- Detailed parameter descriptions
- Usage examples
- Cross-references to related tools

## Migration Guide

If you were using `query_event_log`:
1. Update tool name to `query_activity_log`
2. Verify you're using the correct tool for your use case:
   - For scheduled event status → use `query_scheduled_event`
   - For activity log search → use `query_activity_log`

## Quick Reference

**Want to check if a backup ran?**  
→ Use `query_scheduled_event` with policy_group and schedule_name

**Want to search for log messages?**  
→ Use `query_activity_log` with search parameter

**Want to see schedule definitions?**  
→ Use `query_schedule` (different tool, shows schedule configuration)

## Related Tools

- `query_schedule`: View schedule definitions and configuration
- `query_client`: View client/node information
- `query_protection_policy`: View policy domain and management class details
