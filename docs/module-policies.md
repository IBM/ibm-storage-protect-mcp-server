# IBM Storage Protect MCP - Policy Module

## Overview
The **Policy Module** governs data retention, lifecycle management, and protection rules. It manages policy domains, sets, management classes, and copy groups.

## Micro-MCP-Servers

This module consists of 2 specialized micro-mcp-servers:

### 1. `mcp-server-policies-lifecycle`
**Focus**: High-level policy structures and activation.

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefinePolicyDomain` | Create policy domain | `DEFINE DOMAIN` |
| `DefinePolicySet` | Create policy set | `DEFINE POLICYSET` |
| `ActivatePolicySet` | **Activate** a policy set | `ACTIVATE POLICYSET` |
| `ValidatePolicySet` | Verify a policy set | `VALIDATE POLICYSET` |
| `QueryPolicySet` | View policy hierarchy | `QUERY POLICYSET` |

### 2. `mcp-server-policies-management`
**Focus**: Granular retention rules (Management Classes).

| Tool | Capability | IBM Command |
| :--- | :--- | :--- |
| `DefineManagementClass` | Create management class | `DEFINE MGMTCLASS` |
| `DefineCopyGroup` | Create copy group | `DEFINE COPYGROUP` |
| `DefineSchedule` | Create admin/client schedule | `DEFINE SCHEDULE` |
| `QueryProtectionPolicy` | View retention rules | `QUERY MGMTCLASS` |

## Usage

### Running as Micro-MCP-Servers (Recommended for Context Optimization)

```bash
# Terminal 1: Lifecycle Management
mcp-server-policies-lifecycle
```

### Running as Unified Module
You can run both policy micro-mcp-servers together:

```bash
python -m sp_mcp_server.main --enable-servers policy
```

## Detailed Tools Reference

The following tool descriptions are taken verbatim from the source `commands/policies` modules.

### Policy Domains

`DefinePolicyDomain` (`define_policy_domain`)
Defines a new **Policy Domain** (SLA). a logical grouping of clients with similar backup requirements.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Unique name for the Policy Domain.
- description (Optional): Description of the domain's purpose.
**Output Parameters**:
- Result: Success message indicating the domain was defined.

`UpdatePolicyDomain` (`update_policy_domain`)
Updates the description of an existing **Policy Domain** (SLA).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The name of the policy domain to update.
- description (Optional): The new description for the domain.
**Output Parameters**:
- Result: Success message indicating the domain was updated.

`UpdateObjectDomain` (`update_object_domain`)
Updates an existing **Object Policy Domain**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Domain name.
- description (Optional): New description.
**Output Parameters**:
- Result: Success message indicating the domain was updated.

`DeletePolicyDomain` (`delete_policy_domain`)
Deletes a **Policy Domain** (SLA). Use carefully as it can impact all assigned clients.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Name of the domain to delete.
**Output Parameters**:
- Result: Success message indicating the domain was deleted.

`QueryPolicyGroup` (`query_policy_group`)
Queries **Policy Domains**. Defines distinct SLAs or business groups for nodes.


**Output Parameters**:
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Optional): Specific Policy Domain name to query. (historically `policy_group` in code)

**Output Parameters**:
- Policy Domain Name: The domain identifier.
- Activated Policy Set: The currently active Policy Set enforcing rules.
- Description: Domain description.

### Policy Sets & Profiles

`DefinePolicySet` (`define_policy_set`)
Defines a **Policy Set** within a domain. Contains a collection of management classes that can be activated together.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The parent Policy Domain.
- policy_set_name (Required): Name for the new Policy Set.
- description (Optional): Description.
**Output Parameters**:
- Result: Success message indicating the profile was defined.

`UpdatePolicySet` (`update_policy_set`)
Updates an existing **Policy Set** description.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The parent Policy Domain.
- policy_set_name (Required): The name of the Policy Set to update.
- description (Optional): The new description.
**Output Parameters**:
- Result: Success message indicating the policy set was updated.

`ActivatePolicySet` (`activate_policy_set`)
Activates a **Policy Set**. This makes the policy set the effective policy for the domain, applying retention and management rules.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The name of the policy domain.
- profile_name (Required): The name of the Policy Set to activate.
**Output Parameters**:
- Result: Success message indicating the policy set was activated.

`ValidatePolicySet` (`validate_policy_set`)
Validates the consistency and completeness of a **Policy Set** before deployment.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The name of the policy domain.
- profile_name (Required): The name of the Policy Set to validate.
**Output Parameters**:
- Result: Success message or list of validation errors.

`DeletePolicySet` (`delete_policy_set`)
Deletes a **Policy Set**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- policy_set_name (Required): Name of the Policy Set to delete.
**Output Parameters**:
- Result: Success message indicating the policy set was deleted.

`QueryPolicySet` (`query_policy_set`)
Queries **Policy Sets**. A collection of policy sets that can be validated and activated.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- policy_group (Optional): Parent Policy Domain.
- policy_set (Optional): Specific profile name.

**Output Parameters**:
- Policy Domain Name: Parent domain.
- Policy Set Name: Profile name.
- Description: Profile description.

### Management Classes & Protection Policies

`DefineManagementClass` (`define_management_class`)
Defines a **Management Class** (policy object within a Policy Set). A management class is the binding point users apply to individual files or objects to specify how they are managed; it contains one or more Copy Groups that define versioning and retention behavior.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- policy_set_name (Required): Parent Policy Set.
- class_name (Required): Name for the Management Class (policy object).
- description (Optional): Description.
**Output Parameters**:
- Result: Success message indicating the policy was defined.

`UpdateManagementClass` (`update_management_class`)
Updates a **Management Class** (policy object) description.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The parent Policy Domain.
- policy_set_name (Required): The parent Policy Set.
- class_name (Required): The name of the Management Class (policy object).
- description (Optional): The new description.
**Output Parameters**:
- Result: Success message indicating the management class was updated.

`DeleteManagementClass` (`delete_management_class`)
Deletes a **Management Class** (policy object).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- policy_set_name (Required): Parent Policy Set.
- class_name (Required): Name of the Management Class to delete.
**Output Parameters**:
- Result: Success message indicating the management class was deleted.

`QueryProtectionPolicy` (`query_protection_policy`)
Queries **Management Classes**. Returns management-class objects that are used to bind policies to files and reference Copy Groups.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Optional): Parent Policy Domain. (historically `policy_group`)
- policy_set (Optional): Parent profile.
- policy_name (Optional): Specific Management Class name.

**Output Parameters**:
- Policy Domain: Parent domain.
- Policy Set: Parent profile.
- Mgmt Class Name: Service level identifier.
- Default Mgmt Class: Indicates if this is the default policy.

### Legal Holds & Retention Rules

`DefineHold` (`define_hold`)
Define a **Hold** on retention set data. Prevents deletion of retention sets until the hold is released.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- hold_name (Required): The name of the hold to define.
**Output Parameters**:
- Result: Success message indicating the hold was defined.

`DeleteHold` (`delete_hold`)
Deletes a **Hold** on retention set data.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- hold_name (Required): The name of the hold to delete.
**Output Parameters**:
- Result: Success message indicating the hold was deleted.

`DefineRetentionRule` (`define_retention_rule`)
Define a **Retention Rule** for managing long-term data retention (Retention Sets).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- rule_name (Required): The name of the retention rule.
- node_name (Required): The node name pattern to apply the rule to.
**Output Parameters**:
- Result: Success message indicating the rule was defined.

### Schedules, Subscribers & Associations

`DefineSchedule` (`define_schedule`)
Defines a **Client Schedule** to automate backup tasks.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- schedule_name (Required): Name for the Schedule.
- action (Optional): The type of action (e.g., 'INCREMENTAL', 'SELECTIVE').
- start_time (Optional): Schedule start time.
- duration (Optional): execution window duration.
- period (Optional): Frequency (days) between runs.
**Output Parameters**:
- Result: Success message indicating the schedule was defined.

`QuerySchedule` (`query_schedule`)
Display information about administrative and client data protection schedules.


**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- schedule_name (Optional): Name of the schedule.
- domain_name (Optional): Policy Domain for client schedules. (historically `policy_group`)
- type (Optional): Type of schedule (admin or client).

**Output Parameters**:
- Schedule Name: Name of the schedule.
- Start Date/Time: When the schedule activates.
- Duration: How long the window is open.
- Period: Frequency (e.g., Daily, Weekly).

`QueryScheduleAssociation` (`query_schedule_association`)
Display associations between client nodes and schedules.

**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Optional): Policy Domain. (historically `policy_group`)
- schedule_name (Optional): Schedule name.
- client_name (Optional): Client/node name.

**Output Parameters**:
- Schedule Name: The schedule.
- Node Name: The associated node.

`QuerySubscriber` / `QuerySubscription` (`query_subscriber`, `query_subscription`)
Display information about subscribers and subscription details linking subscribers to profiles or services.

### Copy Groups & Retention

`DefineCopyGroup` (`define_copy_group`)
- Description: Defines a **Copy Group** that specifies exact retention parameters (e.g., how many versions to keep).
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- policy_set_name (Required): Parent Policy Set.
- class_name (Required): Parent Management Class.
- type (Required): 'BACKUP' or 'ARCHIVE' (Defaults to BACKUP).
- destination (Required): The **Storage Pool** where data will be stored.
**Output Parameters**:
- Result: Success message indicating the rule was defined.

`UpdateCopyGroup` (`update_copy_group`)
- Description: Updates a **Copy Group** to modify retention parameters.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- policy_set_name (Required): Parent Policy Set.
- class_name (Required): Parent Management Class.
- type (Optional): 'BACKUP' or 'ARCHIVE' (Defaults to BACKUP).
- destination (Optional): New Storage Pool.
**Output Parameters**:
- Result: Success message indicating the rule was updated.

`DeleteCopyGroup` (`delete_copy_group`)
- Description: Deletes a **Copy Group**. This removes specific retention settings from a management class.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- policy_set_name (Required): Parent Policy Set.
- class_name (Required): Parent Management Class.
**Output Parameters**:
- Result: Success message indicating the rule was deleted.

`QueryRetentionRuleConfig` (`query_retention_rule_config`)
- Description: Queries **Copy Groups**. Shows exact numeric values for retention limits.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- policy_group (Optional): Parent domain.
- policy_set (Optional): Parent profile.
- policy_name (Optional): Parent Management Class.
**Output Parameters**:
- Mgmt Class Name: Parent policy.
- Copy Group Name: Rule identifier.
- Versions Data Exists: Max versions retained.
- Versions Data Deleted: Versions retained after deletion.
- Retain Extra Versions: Days to keep inactive versions.
- Retain Only Version: Days to keep final version.

### Schedules

`UpdateSchedule` (`update_schedule`)
- Description: Updates a **Client Schedule**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): The Policy Domain.
- schedule_name (Required): The Schedule name.
- action (Optional): New action type.
- start_time (Optional): New start time.
- duration (Optional): New duration.
**Output Parameters**:
- Result: Success message indicating the schedule was updated.

`DeleteSchedule` (`delete_schedule`)
- Description: Deletes a **Client Schedule**.
**Input Parameters**:
- isp_server_name (Optional): Target ISP Server name from registry.
- domain_name (Required): Parent Policy Domain.
- schedule_name (Required): Name of the schedule to delete.
**Output Parameters**:
- Result: Success message indicating the schedule was deleted.


