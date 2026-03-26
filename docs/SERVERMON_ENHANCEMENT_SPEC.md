# Servermon Enhancement Specification

## Overview
This document specifies enhancements to the sp-mcp-server's servermon analysis capabilities to support user-specified paths, archive listing, and improved issue detection based on IBM Spectrum Protect servermon best practices.

## Current Limitations

### 1. Fixed Path Pattern
- Current implementation looks for `.20260319T0001-SERVER1` pattern in `SP_SERVERMON_XML_DIR`
- Cannot analyze servermon archives from different dates or locations
- No support for analyzing extracted zip archives

### 2. Limited Archive Management
- No ability to list available servermon archives
- No support for extracting specific archives by index/date
- Cannot work with servermon zip files directly

### 3. Basic Analysis
- Limited understanding of servermon command structure
- No knowledge of commands.ini configuration
- Missing context about what different XML files represent

## Requirements

### R1: User-Specified Path Support
**Priority:** HIGH

Users must be able to specify custom paths for servermon analysis:
- Absolute paths to extracted servermon directories
- Paths to servermon zip archives
- Relative paths within SP_SERVERMON_XML_DIR

**User Interface Options:**
1. **Tool Parameter** (Recommended)
   ```
   run_servermon(path="/opt/tivoli/tsmsvr01/servermon_issue_2/")
   run_servermon(archive="servermonFile-SERVER1-20250223.zip")
   ```

2. **Interactive Selection**
   ```
   list_servermon_archives()  # Returns available archives
   run_servermon(archive_index=42)  # Analyze specific archive
   ```

3. **Configuration Override**
   ```
   set_servermon_path("/custom/path")
   run_servermon()  # Uses custom path
   ```

### R2: Archive Management
**Priority:** HIGH

Implement servermon archive operations:

1. **List Archives**
   - Command: `servermon -list -instance=<instance_name>`
   - Output: Index, Date Created, Zipped Size
   - Tool: `list_servermon_archives(instance_name)`

2. **Extract Archives**
   - Command: `servermon -extract -id=<index> -instance=<instance_name>`
   - Output: Zip file in `<instance_dir>/srvmon/`
   - Tool: `extract_servermon_archive(index, instance_name)`

3. **Auto-Extract and Analyze**
   - Extract archive if needed
   - Analyze extracted content
   - Clean up temporary files (optional)

### R3: Enhanced Analysis Capabilities
**Priority:** MEDIUM

Incorporate knowledge from commands.ini structure:

#### File Type Understanding
Based on commands.ini stanzas:

| File Pattern | Frequency | Content Type | Analysis Focus |
|--------------|-----------|--------------|----------------|
| `*-10min-show.xml` | Every 10 min | Server sessions, locks, processes | Performance bottlenecks |
| `*-20min-show.xml` | Every 20 min | DB connections, instrumentation | Connection issues |
| `*-60min-show.xml` | Every 60 min | Allocations, replication, locks | Resource allocation |
| `*-daily.xml` | Daily start | Libraries, drives, schedules | Configuration issues |
| `*-db2.xml` | 20 min | DB2 snapshots, applications | Database performance |
| `*-db2pd.xml` | 20 min | DB2 diagnostics | Lock timeouts, buffer pools |
| `*-srtcvs-show.xml` | Daily end | CSV data for SRT analysis | Capacity planning |
| `*-iostat.txt` | Continuous | I/O statistics | Disk performance |
| `*-vmstat.txt` | Continuous | Virtual memory stats | Memory pressure |

#### Key Metrics to Extract

**From 10min files:**
- Active sessions and their states
- Lock waits and deadlocks
- Dedup thread status
- Mount requests and drive usage
- Running jobs and processes

**From 20min files:**
- Instrumentation data (INSTR BEGIN/END)
- DB connection pool status
- Network statistics (netstat)
- Long-running queries (>1 second)

**From daily files:**
- Total managed data growth
- Deduplication/compression ratios
- Storage pool occupancy
- Client platform distribution
- Backup success/failure rates
- Table sizes and reorg needs

**From db2pd files:**
- Lock timeouts
- Buffer pool hit ratios
- Transaction log usage
- Dirty pages
- Memory pool allocation

### R4: Issue Detection Patterns
**Priority:** HIGH

Implement automated detection for common issues:

#### Critical Issues
1. **Deduplication Failure**
   - Pattern: DEDUP_PCT = 0% for multiple days
   - Historical baseline: >70% typical
   - Alert: "Deduplication stopped working on <date>"

2. **Database Lock Contention**
   - Pattern: Lock timeouts > 0
   - Failed statement operations > 1000
   - Alert: "Database experiencing lock contention"

3. **Network Connectivity Problems**
   - Pattern: Failed connections > 100K
   - TCP timeouts > 10K
   - Listen queue overflows > 10K
   - Alert: "Severe network connectivity issues"

4. **Storage Pool Issues**
   - Pattern: Pool utilization > 90%
   - No scratch tapes available
   - Mount requests queued
   - Alert: "Storage pool capacity critical"

#### Warning Issues
1. **Performance Degradation**
   - Pattern: Average throughput < 50% of baseline
   - Session wait times increasing
   - Alert: "Performance degradation detected"

2. **Table Fragmentation**
   - Pattern: Allocated space > 2x used space
   - Last reorg > 30 days ago
   - Alert: "Tables need reorganization"

3. **Backup Failures**
   - Pattern: Failed backups > 5% of total
   - Specific clients failing repeatedly
   - Alert: "Backup failure rate elevated"

## Design Approach

### Architecture Changes

```
sp-mcp-server/
├── src/sp_mcp_server/
│   ├── commands/
│   │   └── servermon.py (NEW)
│   ├── analyzers/
│   │   ├── __init__.py (NEW)
│   │   ├── servermon_analyzer.py (NEW)
│   │   ├── dedup_analyzer.py (NEW)
│   │   ├── network_analyzer.py (NEW)
│   │   └── db_analyzer.py (NEW)
│   └── config/
│       └── servermon_patterns.yaml (NEW)
```

### New Components

#### 1. ServermonCommand Class
```python
class ServermonCommand:
    """Handle servermon archive operations"""
    
    def list_archives(self, instance_name: str) -> List[Archive]
    def extract_archive(self, index: int, instance_name: str) -> Path
    def find_results_dir(self, path: str) -> Path
    def validate_servermon_dir(self, path: Path) -> bool
```

#### 2. ServermonAnalyzer Class
```python
class ServermonAnalyzer:
    """Analyze servermon XML files"""
    
    def analyze_directory(self, path: Path) -> AnalysisReport
    def detect_issues(self) -> List[Issue]
    def generate_summary(self) -> Summary
    def extract_metrics(self, file_type: str) -> Dict
```

#### 3. Specialized Analyzers
```python
class DedupAnalyzer:
    """Analyze deduplication performance"""
    def check_dedup_ratio(self, daily_data: List) -> DedupStatus
    def detect_dedup_failure(self) -> Optional[Issue]

class NetworkAnalyzer:
    """Analyze network connectivity"""
    def check_connection_failures(self, netstat_data: Dict) -> NetworkStatus
    def detect_network_issues(self) -> List[Issue]

class DatabaseAnalyzer:
    """Analyze database performance"""
    def check_lock_timeouts(self, db2pd_data: Dict) -> DbStatus
    def check_table_fragmentation(self, daily_data: Dict) -> List[Table]
```

### Configuration File Structure

```yaml
# servermon_patterns.yaml
file_patterns:
  performance:
    - "*-10min-show.xml"
    - "*-20min-show.xml"
  database:
    - "*-db2.xml"
    - "*-db2pd.xml"
  daily:
    - "*-daily.xml"
  system:
    - "*-iostat.txt"
    - "*-vmstat.txt"

issue_thresholds:
  dedup_failure:
    min_ratio: 70.0
    consecutive_days: 2
  network:
    max_failed_connections: 100000
    max_tcp_timeouts: 10000
  database:
    max_lock_timeouts: 10
    max_failed_statements: 1000
  storage:
    max_pool_utilization: 90.0

metrics:
  dedup_ratio:
    query: "SELECT DEDUP_PCT FROM summary WHERE activity='BACKUP'"
    file: "*-daily.xml"
  network_stats:
    pattern: "failed connection attempts"
    file: "*-20min.xml"
```

## Implementation Plan

### Phase 1: Core Infrastructure (Week 1)
- [ ] Create servermon command wrapper
- [ ] Implement path validation and discovery
- [ ] Add archive listing functionality
- [ ] Support user-specified paths in run_servermon

### Phase 2: Enhanced Analysis (Week 2)
- [ ] Implement ServermonAnalyzer base class
- [ ] Add file type detection and routing
- [ ] Create metric extraction framework
- [ ] Build issue detection engine

### Phase 3: Specialized Analyzers (Week 3)
- [ ] Implement DedupAnalyzer
- [ ] Implement NetworkAnalyzer
- [ ] Implement DatabaseAnalyzer
- [ ] Add storage pool analyzer

### Phase 4: Integration & Testing (Week 4)
- [ ] Integrate with existing MCP tools
- [ ] Add comprehensive error handling
- [ ] Create unit tests
- [ ] Document new capabilities

## API Design

### Tool: run_servermon
```python
@mcp.tool()
async def run_servermon(
    path: Optional[str] = None,
    archive_index: Optional[int] = None,
    instance_name: Optional[str] = None,
    analysis_type: str = "full"
) -> str:
    """
    Analyze servermon logs from specified location.
    
    Args:
        path: Absolute path to servermon results directory
        archive_index: Index of archive to extract and analyze
        instance_name: SP instance name (required with archive_index)
        analysis_type: Type of analysis (full, quick, dedup, network, db)
    
    Returns:
        Analysis report with issues and recommendations
    """
```

### Tool: list_servermon_archives
```python
@mcp.tool()
async def list_servermon_archives(
    instance_name: str
) -> str:
    """
    List available servermon archives.
    
    Args:
        instance_name: SP instance name
    
    Returns:
        Table of archives with index, date, and size
    """
```

### Tool: extract_servermon_archive
```python
@mcp.tool()
async def extract_servermon_archive(
    index: int,
    instance_name: str,
    output_dir: Optional[str] = None
) -> str:
    """
    Extract servermon archive by index.
    
    Args:
        index: Archive index from list_servermon_archives
        instance_name: SP instance name
        output_dir: Optional output directory
    
    Returns:
        Path to extracted archive
    """
```

## Testing Strategy

### Unit Tests
- Path validation and discovery
- XML parsing for each file type
- Metric extraction accuracy
- Issue detection logic

### Integration Tests
- End-to-end analysis workflow
- Archive extraction and analysis
- Multiple path formats
- Error handling scenarios

### Test Data
- Sample servermon archives from different scenarios:
  - Normal operation
  - Dedup failure
  - Network issues
  - Database contention
  - Storage capacity issues

## Documentation Requirements

### User Documentation
1. **Quick Start Guide**
   - How to analyze servermon logs
   - Common use cases
   - Interpreting results

2. **Reference Guide**
   - All available tools
   - Parameters and options
   - Output format descriptions

3. **Troubleshooting Guide**
   - Common issues and solutions
   - Error messages explained
   - When to escalate to IBM support

### Developer Documentation
1. **Architecture Overview**
   - Component relationships
   - Data flow diagrams
   - Extension points

2. **Adding New Analyzers**
   - Analyzer interface
   - Pattern matching
   - Issue reporting

3. **Configuration Guide**
   - Pattern definitions
   - Threshold tuning
   - Custom metrics

## Success Criteria

### Functional Requirements
- ✅ Users can specify custom servermon paths
- ✅ Tool can list available archives
- ✅ Tool can extract and analyze archives
- ✅ Analysis detects critical issues automatically
- ✅ Reports include actionable recommendations

### Performance Requirements
- Analysis completes within 30 seconds for typical archive
- Memory usage < 500MB for large archives
- Supports archives up to 1GB compressed

### Quality Requirements
- 95% accuracy in issue detection
- Zero false positives for critical issues
- Clear, actionable error messages
- Comprehensive logging for debugging

## Future Enhancements

### Phase 2 Features
1. **Trend Analysis**
   - Compare multiple archives
   - Identify degradation patterns
   - Predict capacity issues

2. **Automated Remediation**
   - Generate fix scripts
   - Suggest configuration changes
   - Create support tickets

3. **Real-time Monitoring**
   - Watch active servermon session
   - Alert on threshold breaches
   - Dashboard integration

4. **Machine Learning**
   - Anomaly detection
   - Predictive maintenance
   - Workload optimization

## References

### IBM Documentation
- Spectrum Protect Server Administration Guide
- Servermon User Guide
- Performance Tuning Best Practices
- Container Storage Pool Best Practices

### Related Technotes
- 1683633: DB2 Table Analysis
- Servermon commands.ini structure
- Archive management procedures

### Internal Resources
- sp-mcp-server architecture
- MCP tool development guidelines
- Testing framework documentation

## Appendix A: Servermon File Types

### XML Files Generated by Servermon

| File Pattern | Stanza | Frequency | Key Content |
|--------------|--------|-----------|-------------|
| `*-10min-show.xml` | srv_10min | 10 min | QUERY PROCESS, SHOW LOCKS, QUERY DB, QUERY SESSION |
| `*-10min.xml` | servermon_10min | 10 min | Process performance metrics, file/byte counts |
| `*-20min-show.xml` | srv_20min | 20 min | INSTR END/BEGIN, SHOW DBCONN |
| `*-20min.xml` | servermon_20min | 20 min | netstat, df, long-running queries |
| `*-60min-show.xml` | srv_60min | 60 min | SHOW ALLOC, SHOW REPLICATION, SHOW LOCKS |
| `*-daily.xml` | srv_daily | Daily | QUERY LIBRARY, QUERY DRIVE, QUERY SCHEDULE |
| `*-24hour-show.xml` | srv_summary | Daily end | QUERY REPLFAIL, QUERY PROTECTS |
| `*-db2.xml` | db2commands | 20 min | DB2 snapshots, applications, config |
| `*-db2pd.xml` | db2pdcommands | 20 min | Buffer pools, locks, transactions, logs |
| `*-srtcvs-show.xml` | srv_srtcvs | Daily end | CSV data for SRT analysis |
| `*-iostat.txt` | servermon_stats | Continuous | I/O statistics (platform-specific) |
| `*-vmstat.txt` | servermon_stats | Continuous | Virtual memory statistics |
| `*-endOfDay.xml` | servermon_summary | Daily end | Reorg checks, system info, table stats |

### Key SQL Queries in commands.ini

**Deduplication Analysis:**
```sql
SELECT n.platform, DATE(s.START_TIME) AS Date,
       CAST(FLOAT(SUM(s.dedup_savings))/FLOAT(SUM(s.bytes_protected))*100 AS DECIMAL(5,2)) AS DEDUP_PCT
FROM summary s INNER JOIN nodes n ON s.entity = n.nodename
WHERE activity IN ('BACKUP','ARCHIVE','OBJECT CLIENT BACKUP')
GROUP BY n.platform, DATE(S.START_TIME)
```

**Storage Pool Occupancy:**
```sql
SELECT o.stgpool_name, s.pooltype, s.stg_type,
       SUM(o.reporting_mb)/1024/1024 AS Occupancy_TB,
       CAST(SUM(o.NUM_FILES) AS DECIMAL(12,0)) AS Number_of_files
FROM occupancy o JOIN stgpools s ON o.stgpool_name = s.stgpool_name
WHERE o.node_name != ''
GROUP BY o.stgpool_name, s.pooltype, s.stg_type
```

**Table Fragmentation:**
```sql
SELECT tu.name, CAST(rows_in_table AS BIGINT),
       CAST(table_used_mb AS BIGINT), CAST(table_alloc_mb AS BIGINT)
FROM (SELECT SUBSTR(tabname,1,28) AS name, BIGINT(card) AS rows_in_table,
      BIGINT(FLOAT(t.npages)/(1024/(b.pagesize/1024))) AS table_used_mb
      FROM syscat.tables t, syscat.tablespaces b
      WHERE t.tbspace=b.tbspace AND t.tabschema='TSMDB1') AS tu
WHERE (table_alloc_mb+index_alloc_mb) > 1024
ORDER BY table_alloc_mb DESC
```

## Appendix B: Issue Detection Algorithms

### Deduplication Failure Detection
```python
def detect_dedup_failure(daily_data: List[Dict]) -> Optional[Issue]:
    """
    Detect deduplication failure by analyzing historical ratios.
    
    Algorithm:
    1. Extract DEDUP_PCT for last 30 days
    2. Calculate baseline (median of first 20 days)
    3. Check if last 7 days < 10% of baseline
    4. Identify failure start date
    """
    ratios = [d['DEDUP_PCT'] for d in daily_data[-30:]]
    baseline = median(ratios[:20])
    recent = ratios[-7:]
    
    if baseline > 70 and all(r < baseline * 0.1 for r in recent):
        failure_date = find_first_low_ratio(ratios)
        return Issue(
            severity="CRITICAL",
            type="DEDUP_FAILURE",
            message=f"Deduplication stopped working on {failure_date}",
            baseline=baseline,
            current=mean(recent),
            recommendation="Check dedup pool status, verify client settings"
        )
    return None
```

### Network Issue Detection
```python
def detect_network_issues(netstat_data: Dict) -> List[Issue]:
    """
    Detect network connectivity problems.
    
    Checks:
    - Failed connection attempts > 100K
    - TCP timeouts > 10K
    - Listen queue overflows > 10K
    - Connection resets > 100K
    """
    issues = []
    
    if netstat_data['failed_connections'] > 100000:
        issues.append(Issue(
            severity="HIGH",
            type="NETWORK_CONNECTIVITY",
            message=f"{netstat_data['failed_connections']:,} failed connection attempts",
            recommendation="Review firewall rules, check network capacity"
        ))
    
    if netstat_data['tcp_timeouts'] > 10000:
        issues.append(Issue(
            severity="HIGH",
            type="NETWORK_TIMEOUT",
            message=f"{netstat_data['tcp_timeouts']:,} TCP timeout events",
            recommendation="Check network latency, review timeout settings"
        ))
    
    return issues
```

### Database Contention Detection
```python
def detect_db_contention(db2pd_data: Dict) -> Optional[Issue]:
    """
    Detect database lock contention.
    
    Checks:
    - Lock timeouts > 0
    - Failed statements > 1000
    - Lock timeout setting < 10 seconds
    """
    if db2pd_data['lock_timeouts'] > 0:
        return Issue(
            severity="MEDIUM",
            type="DB_LOCK_CONTENTION",
            message=f"{db2pd_data['lock_timeouts']} lock timeout events",
            details={
                'failed_statements': db2pd_data['failed_statements'],
                'timeout_setting': db2pd_data['lock_timeout_seconds']
            },
            recommendation="Increase lock timeout, review long-running queries"
        )
    return None
```

---

**Document Version:** 1.0  
**Last Updated:** 2026-03-19  
**Author:** SP-MCP-Server Development Team  
**Status:** Draft for Review
