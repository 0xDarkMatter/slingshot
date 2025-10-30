# Implementation Plan: D1 Database & R2 Storage Integration

**Status:** In Progress
**Started:** 2024-10-31
**Priority:** D1 First, then R2
**Scope:** Full functionality (resource management + data operations)

---

## Overview

Adding complete support for Cloudflare D1 (SQL database) and R2 (object storage) to Slingshot.

### User Requirements
- ✅ Full functionality including data operations
- ✅ Grouped CLI commands (`slingshot d1 ...`, `slingshot r2 ...`)
- ✅ D1 implementation first, then R2
- ✅ Templates and examples for both features

---

## Progress Tracker

### Phase 1: D1 Database Support ⏳ Not Started
- [ ] 1.1 API Client Extensions
- [ ] 1.2 Configuration Support
- [ ] 1.3 CLI Commands
- [ ] 1.4 Templates & Examples
- [ ] 1.5 Documentation Updates
- [ ] 1.6 Testing

### Phase 2: R2 Storage Integration ⏳ Not Started
- [ ] 2.1 API Client Extensions
- [ ] 2.2 Configuration Support
- [ ] 2.3 CLI Commands
- [ ] 2.4 Templates & Examples
- [ ] 2.5 Documentation Updates
- [ ] 2.6 Testing

### Phase 3: Final Integration ⏳ Not Started
- [ ] 3.1 Update Existing Components
- [ ] 3.2 CHANGELOG Updates
- [ ] 3.3 Documentation Polish
- [ ] 3.4 Final Testing & Commit

---

## Phase 1: D1 Database Support

### 1.1 API Client Extensions
**File:** `src/slingshot/client.py`

Add these methods to `CloudflareClient` class:

```python
def list_d1_databases(self) -> List[Dict[str, Any]]:
    """List all D1 databases in account."""
    return self._request("GET", f"accounts/{self.account_id}/d1/database")

def create_d1_database(self, name: str) -> Dict[str, Any]:
    """Create a new D1 database."""
    return self._request("POST", f"accounts/{self.account_id}/d1/database",
                        data={"name": name})

def delete_d1_database(self, database_id: str) -> Dict[str, Any]:
    """Delete a D1 database."""
    return self._request("DELETE", f"accounts/{self.account_id}/d1/database/{database_id}")

def get_d1_database(self, database_id: str) -> Dict[str, Any]:
    """Get D1 database details."""
    return self._request("GET", f"accounts/{self.account_id}/d1/database/{database_id}")

def query_d1(self, database_id: str, sql: str, params: Optional[List] = None) -> Dict[str, Any]:
    """Execute SQL query on D1 database."""
    data = {"sql": sql}
    if params:
        data["params"] = params
    return self._request("POST", f"accounts/{self.account_id}/d1/database/{database_id}/query",
                        data=data)

def execute_d1_batch(self, database_id: str, statements: List[str]) -> Dict[str, Any]:
    """Execute multiple SQL statements."""
    return self._request("POST", f"accounts/{self.account_id}/d1/database/{database_id}/query",
                        data={"sql": statements})
```

**API Endpoints:**
- `GET /accounts/{account_id}/d1/database` - List databases
- `POST /accounts/{account_id}/d1/database` - Create database
- `GET /accounts/{account_id}/d1/database/{id}` - Get database info
- `DELETE /accounts/{account_id}/d1/database/{id}` - Delete database
- `POST /accounts/{account_id}/d1/database/{id}/query` - Execute queries

**Reference:** https://developers.cloudflare.com/d1/

---

### 1.2 Configuration Support

**Update `.slingshot.json` format:**
```json
{
  "worker_name": "my-worker",
  "main": "worker.js",
  "compatibility_date": "2024-01-01",
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-database",
      "database_id": "xxx-xxx-xxx"
    }
  ],
  "kv_namespaces": [],
  "r2_buckets": [],
  "vars": {}
}
```

**Files to update:**

1. **`src/slingshot/config.py`** - Add D1 property:
   ```python
   @property
   def d1_databases(self) -> List[Dict[str, Any]]:
       """Get D1 database bindings."""
       return self.get("d1_databases", [])
   ```

2. **`src/slingshot/deployer.py`** - Update `prepare_metadata()`:
   ```python
   # D1 Databases
   d1_databases = self.config.get("d1_databases", [])
   for d1 in d1_databases:
       bindings.append({
           "type": "d1",
           "name": d1.get("binding"),
           "id": d1.get("database_id")
       })
   ```

3. **Update all template `.slingshot.json` files** to include empty `d1_databases` array

---

### 1.3 CLI Commands

**File:** `src/slingshot/cli.py`

Create D1 command group:

```python
@main.group()
def d1():
    """Manage Cloudflare D1 databases."""
    pass

@d1.command()
@click.argument('name')
@click.option('--save-config', is_flag=True, help='Save database ID to .slingshot.json')
def create(name: str, save_config: bool):
    """Create a new D1 database."""
    # Implementation

@d1.command()
def list():
    """List all D1 databases."""
    # Display table with: Name, ID, Created, Size

@d1.command()
@click.argument('database')  # name or ID
def info(database: str):
    """Show detailed database information."""
    # Implementation

@d1.command()
@click.argument('database')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation')
def delete(database: str, yes: bool):
    """Delete a D1 database."""
    # Implementation with confirmation

@d1.command()
@click.argument('database')
@click.argument('sql')
@click.option('--params', '-p', multiple=True, help='Query parameters')
def query(database: str, sql: str, params: tuple):
    """Execute a SQL query."""
    # Implementation

@d1.command()
@click.argument('database')
@click.option('--file', '-f', required=True, type=click.Path(exists=True))
def execute(database: str, file: str):
    """Execute SQL from a file."""
    # Implementation

@d1.command()
@click.argument('database')
def schema(database: str):
    """Show database schema (tables and columns)."""
    # Query sqlite_master table
```

**Commands to implement:**
- `slingshot d1 create <name>` - Create database
- `slingshot d1 list` - List all databases
- `slingshot d1 info <name|id>` - Show database info
- `slingshot d1 delete <name|id>` - Delete database
- `slingshot d1 query <name|id> "<sql>"` - Execute SQL
- `slingshot d1 execute <name|id> --file <path>` - Execute SQL file
- `slingshot d1 schema <name|id>` - Show schema

---

### 1.4 Templates & Examples

#### Template: `templates/d1-api/`

**Files:**
- `worker.js` - REST API with CRUD operations
- `.slingshot.json` - Config with D1 binding
- `schema.sql` - Database schema setup
- `README.md` - Usage instructions

**`schema.sql`:**
```sql
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, email) VALUES
  ('Alice', 'alice@example.com'),
  ('Bob', 'bob@example.com');
```

**`worker.js`:** REST API with routes:
- `GET /api/users` - List all users
- `GET /api/users/:id` - Get user by ID
- `POST /api/users` - Create user
- `PUT /api/users/:id` - Update user
- `DELETE /api/users/:id` - Delete user

#### Example: `examples/d1-todo-app/`

Complete todo list application with:
- `worker.js` - Full CRUD API
- `schema.sql` - Todos table schema
- `.slingshot.json` - D1 binding configured
- `README.md` - Setup and deployment guide

**Schema:**
```sql
CREATE TABLE todos (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  completed BOOLEAN DEFAULT 0,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

### 1.5 Documentation Updates

**README.md additions:**
```markdown
## D1 Database Support

Slingshot provides full support for Cloudflare D1 SQL databases.

### Quick Start

```bash
# Create a database
slingshot d1 create my-database

# List databases
slingshot d1 list

# Execute a query
slingshot d1 query my-database "SELECT * FROM users"

# Execute SQL file
slingshot d1 execute my-database --file schema.sql
```

### Configuration

Add D1 bindings to `.slingshot.json`:

```json
{
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-database",
      "database_id": "xxx-xxx-xxx"
    }
  ]
}
```

### Using D1 in Workers

```javascript
export default {
  async fetch(request, env, ctx) {
    // Query the database
    const { results } = await env.DB.prepare(
      "SELECT * FROM users WHERE email = ?"
    ).bind("alice@example.com").all();

    return Response.json(results);
  }
};
```
```

**QUICKSTART.md:** Add D1 section after KV storage

**cloudflare-expert.md:** Add D1 patterns section with:
- Query patterns (prepared statements)
- CRUD operations
- Transaction handling
- Schema migrations
- Security (SQL injection prevention)
- Common issues

---

### 1.6 Testing

**New file: `tests/test_d1.py`**
```python
"""Tests for D1 database operations."""

import pytest
import responses
from slingshot.client import CloudflareClient

@pytest.fixture
def client():
    return CloudflareClient("test_account", "test_token")

@responses.activate
def test_list_d1_databases(client):
    responses.add(
        responses.GET,
        "https://api.cloudflare.com/client/v4/accounts/test_account/d1/database",
        json={"success": True, "result": [{"name": "test-db", "uuid": "123"}]},
        status=200
    )
    result = client.list_d1_databases()
    assert len(result) == 1
    assert result[0]["name"] == "test-db"

# More tests...
```

**Update existing test files:**
- `tests/test_deployer.py` - Test D1 binding generation
- `tests/test_cli.py` - Test D1 commands
- `tests/conftest.py` - Add D1 fixtures

---

## Phase 2: R2 Storage Integration

### 2.1 API Client Extensions
**File:** `src/slingshot/client.py`

Add R2 methods:
```python
def list_r2_buckets(self) -> List[Dict[str, Any]]
def create_r2_bucket(self, name: str, location_hint: Optional[str] = None) -> Dict[str, Any]
def delete_r2_bucket(self, name: str) -> Dict[str, Any]
def get_r2_bucket(self, name: str) -> Dict[str, Any]
def list_r2_objects(self, bucket: str, prefix: Optional[str] = None, limit: int = 1000)
def upload_r2_object(self, bucket: str, key: str, content: bytes, content_type: str)
def download_r2_object(self, bucket: str, key: str) -> bytes
def delete_r2_object(self, bucket: str, key: str)
def get_r2_object_metadata(self, bucket: str, key: str)
```

**API Endpoints:**
- `/accounts/{account_id}/r2/buckets` - Bucket management
- S3-compatible API for object operations

**Reference:** https://developers.cloudflare.com/r2/

---

### 2.2 Configuration Support

**`.slingshot.json` format:**
```json
{
  "r2_buckets": [
    {
      "binding": "BUCKET",
      "bucket_name": "my-bucket"
    }
  ]
}
```

Update same files as D1 (config.py, deployer.py, templates)

---

### 2.3 CLI Commands

```bash
slingshot r2 create <name>          # Create bucket
slingshot r2 list                   # List buckets
slingshot r2 info <name>           # Bucket details
slingshot r2 delete <name>         # Delete bucket
slingshot r2 upload <bucket> <file> [--key <key>]
slingshot r2 download <bucket> <key> [--output <path>]
slingshot r2 ls <bucket> [--prefix <prefix>]
slingshot r2 rm <bucket> <key>
```

---

### 2.4 Templates & Examples

**Template: `templates/r2-cdn/`**
- Static file server using R2
- Cache headers
- Directory listing
- CORS support

**Example: `examples/r2-image-host/`**
- Image upload API
- Public gallery
- Image serving with cache

---

### 2.5 Documentation Updates

Similar structure to D1:
- README.md R2 section
- QUICKSTART.md R2 guide
- cloudflare-expert.md R2 patterns

---

### 2.6 Testing

**New file: `tests/test_r2.py`**
- Test all R2 client methods
- Mock API responses
- Test object upload/download

Update existing tests as needed.

---

## Phase 3: Final Integration & Polish

### 3.1 Update Existing Components
- [ ] Update all template configs to include `d1_databases` and `r2_buckets` arrays
- [ ] Add migration guide for existing users
- [ ] Verify all examples work end-to-end

### 3.2 CHANGELOG Updates
```markdown
## [Unreleased]

### Added
- **D1 Database Support**: Full D1 integration with CLI, bindings, and data operations
  - New command group: `slingshot d1` (create, list, delete, query, execute, schema)
  - D1 database bindings in worker configuration
  - SQL query execution and schema management
- **R2 Storage Support**: Full R2 integration with CLI, bindings, and data operations
  - New command group: `slingshot r2` (create, list, delete, upload, download, ls, rm)
  - R2 bucket bindings in worker configuration
  - Object upload/download and management
- New templates: `d1-api` (REST API with D1), `r2-cdn` (CDN with R2)
- New examples: `d1-todo-app`, `r2-image-host`
- Enhanced cloudflare-expert agent with D1 and R2 patterns and best practices

### Changed
- Configuration format now supports `d1_databases` and `r2_buckets` arrays
- Updated all templates to include new binding placeholders
```

### 3.3 Documentation Polish
- [ ] Add troubleshooting sections for D1 and R2
- [ ] Security considerations (SQL injection, R2 access control)
- [ ] Update roadmap to mark features complete
- [ ] Review all code examples

### 3.4 Final Testing
- [ ] Run full test suite: `pytest --cov=slingshot`
- [ ] Manual test all D1 commands
- [ ] Manual test all R2 commands
- [ ] Test template deployments
- [ ] Test example projects end-to-end
- [ ] Commit and push to GitHub

---

## Technical Notes

### D1 Query Patterns (for templates)
```javascript
// Basic query
const { results } = await env.DB.prepare("SELECT * FROM users").all();

// Prepared statement (prevents SQL injection)
const stmt = env.DB.prepare("SELECT * FROM users WHERE id = ?");
const { results } = await stmt.bind(userId).all();

// Insert
await env.DB.prepare("INSERT INTO users (name, email) VALUES (?, ?)")
  .bind(name, email)
  .run();

// Transaction (multiple statements)
const result = await env.DB.batch([
  env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Alice"),
  env.DB.prepare("INSERT INTO users (name) VALUES (?)").bind("Bob")
]);
```

### R2 Usage Patterns (for templates)
```javascript
// Store object
await env.BUCKET.put("file.txt", "Hello, World!");

// Retrieve object
const object = await env.BUCKET.get("file.txt");
if (object) {
  const text = await object.text();
}

// List objects
const list = await env.BUCKET.list({ prefix: "images/" });

// Delete object
await env.BUCKET.delete("file.txt");

// Get metadata
const object = await env.BUCKET.head("file.txt");
```

---

## Estimated Effort

- **Phase 1 (D1):** 8-12 hours
  - Client methods: 2h
  - Config/Deployer: 1h
  - CLI commands: 3h
  - Templates/Examples: 3h
  - Docs: 2h
  - Tests: 2h

- **Phase 2 (R2):** 8-12 hours
  - Similar breakdown to D1

- **Phase 3 (Polish):** 2-4 hours
  - Integration testing
  - Documentation review
  - CHANGELOG and commit

**Total: 18-28 hours**

---

## Resources

- **D1 Documentation:** https://developers.cloudflare.com/d1/
- **D1 API Reference:** https://developers.cloudflare.com/api/operations/cloudflare-d1-create-database
- **R2 Documentation:** https://developers.cloudflare.com/r2/
- **R2 API Reference:** https://developers.cloudflare.com/api/operations/r2-list-buckets
- **Workers Bindings:** https://developers.cloudflare.com/workers/configuration/bindings/

---

## Next Steps

When resuming:
1. Check the todo list in the codebase
2. Start with Phase 1.1 (D1 API client methods)
3. Work through each phase sequentially
4. Test thoroughly before moving to next phase
5. Commit after each major phase completion

**Current Status:** Ready to begin Phase 1.1
