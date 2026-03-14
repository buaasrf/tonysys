# CLAUDE.md — TonySys Codebase Guide

This file provides AI assistants with essential context about the TonySys codebase: its architecture, development workflow, and conventions.

---

## Project Overview

**TonySys** is a student dormitory and conduct management system built with Java and Spring MVC. It manages student information, dormitory assignments, and conduct scores with role-based access control.

- **Language:** Java (JDK 1.7)
- **Framework:** Spring MVC 3.0.5.RELEASE
- **Build:** Maven (WAR packaging)
- **Database:** MySQL
- **UI:** JSP + JSTL + Bootstrap, AJAX-driven interactions
- **Created:** November 2012 by buaasrf

---

## Repository Structure

```
tonysys/
├── pom.xml                              # Maven build descriptor
├── docs/
│   ├── readme.txt                       # Setup guide (Chinese)
│   └── db/
│       └── tonysysForMysql.sql          # Full database schema
└── src/main/
    ├── filters/
    │   ├── filter-dev.properties        # Dev DB credentials
    │   ├── filter-test.properties       # Test DB credentials
    │   └── filter-product.properties    # Production DB credentials
    ├── java/com/tonysys/
    │   ├── admin/
    │   │   ├── controller/              # Spring MVC controllers
    │   │   ├── dao/                     # DAO interfaces
    │   │   │   └── Impl/               # DAO implementations
    │   │   ├── model/                   # Domain model POJOs
    │   │   ├── rowMapper/              # JDBC RowMapper classes
    │   │   └── service/                # Service interfaces
    │   │       └── Impl/               # Service implementations
    │   ├── context/                     # Session constants & enums
    │   ├── converter/                   # HTTP message converters
    │   ├── filter/                      # Servlet filters
    │   └── util/                        # Utility classes
    ├── resources/
    │   ├── spring.xml                   # Root application context
    │   ├── config.properties            # DB connection properties (filtered)
    │   ├── logback.xml                  # Logging configuration
    │   └── ehcache.xml                  # Cache configuration
    └── webapp/
        ├── WEB-INF/
        │   ├── web.xml                  # Servlet deployment descriptor
        │   └── tonysys-servlet.xml      # Spring MVC dispatcher config
        ├── login.jsp
        ├── index.jsp
        ├── about.jsp
        ├── contactUs.jsp
        ├── userManage/                  # User management JSP pages
        ├── dormitoryManage/             # Dormitory management JSP pages
        ├── conductScoreManage/          # Conduct score JSP pages
        └── resource/                    # Static assets (Bootstrap, JS, CSS)
```

---

## Build Commands

```bash
# Build WAR package
mvn clean package

# Run locally with Jetty (port 80, context path /)
mvn jetty:run

# Build for a specific environment profile
mvn clean package -Dproject.environment=dev       # default
mvn clean package -Dproject.environment=test
mvn clean package -Dproject.environment=product
```

There is **no automated test suite**. There is no `src/test` directory. Manual testing via the web UI is required.

---

## Database Setup

1. Install MySQL and create the database:

```sql
CREATE DATABASE DB_TONYSYS CHARACTER SET utf8;
```

2. Import the schema:

```bash
mysql -u root -p DB_TONYSYS < docs/db/tonysysForMysql.sql
```

3. The schema creates three tables:
   - **`user`** — Student/user records (30+ fields: personal info, contact, family, dormitory reference)
   - **`dormitory`** — Room records (building, room number, bed count)
   - **`conduct_score`** — Conduct event records (type, score, date, place, remarks)
   - Foreign key: `user.dormitoryid → dormitory.id` (ON DELETE SET NULL)

**Default dev credentials (filter-dev.properties):**
- Host: `localhost:3306`
- Database: `DB_TONYSYS`
- Username: `root`
- Password: `root`

**Default application login:** `root` / `abc`

---

## Environment Configuration

Database credentials are injected via Maven resource filtering at build time. Select the environment by setting `project.environment` in `pom.xml` or via `-D` flag.

Filter files: `src/main/filters/filter-{dev,test,product}.properties`

The placeholder variables resolved into `src/main/resources/config.properties`:

| Variable | Description |
|---|---|
| `db_instance_ad` | `host:port/DB_NAME` |
| `db_username_ad` | Database username |
| `db_password_ad` | Database password |

To change the target database, edit the appropriate `filter-*.properties` file; **do not edit `config.properties` directly** — it is a filtered template.

---

## Architecture

### Request Flow

```
Browser → LoginFilter → DispatcherServlet (/admin/*)
       → Controller → Service → DAO (JdbcTemplate) → MySQL
       ← JSP View / JSON response ←
```

### Layer Responsibilities

| Layer | Package | Role |
|---|---|---|
| Controller | `com.tonysys.admin.controller` | Maps HTTP requests, calls services, returns views or JSON |
| Service | `com.tonysys.admin.service` | Business logic; transaction boundaries defined here |
| DAO | `com.tonysys.admin.dao` | SQL execution via `JdbcTemplate` |
| RowMapper | `com.tonysys.admin.rowMapper` | Maps `ResultSet` rows to model objects |
| Model | `com.tonysys.admin.model` | Plain POJOs representing domain entities |

### Controllers

| Class | URL Prefix | Responsibility |
|---|---|---|
| `LoginController` | `/signin` | Authentication; sets session attributes |
| `UserController` | `/admin/user/*` | Student CRUD, search, pagination |
| `DormitoryController` | `/admin/dormitory/*` | Dormitory and bed management |
| `ConductScoreController` | `/admin/conductScore/*` | Conduct score CRUD |

### Domain Models

- **`UserBean`** — Student entity with ~30 fields (id, number, name, password, class, grade, gender, phone, address, dormitory, etc.)
- **`Dormitory`** — Room entity (id, building, roomNumber, doorNumber, bedCount)
- **`Bed`** — Bed entity linking a user to a dormitory
- **`ConductScore`** — Conduct event (userId, type, score, date, place, remarks)
- **`ResultMSG`** — Generic API response wrapper (code, message, data)

### Authentication & Session

- `LoginFilter` intercepts all requests except the exclusion list and redirects unauthenticated users to `/login.jsp`.
- Excluded URLs: `/login.jsp`, `/about.jsp`, `/contactUs.jsp`, `/resource/**`, `/admin/login*`
- After successful login, the following attributes are stored in `HttpSession`:
  - `UserContext.USER_TOKEN` — Full `UserBean` object
  - `UserContext.USER_ID` — User ID
  - `UserContext.USER_NUMBER` — Student number
  - `UserContext.USER_NAME` — User name
  - `UserContext.LOGIN_TIME` — Login timestamp

---

## Spring Configuration

### Root Context (`spring.xml`)

- **Component scan packages:** `com.tonysys.admin.dao`, `com.tonysys.admin.controller`, `com.tonysys.admin.service`, `com.tonysys.admin.rowMapper`
- **DataSource:** C3P0 connection pool (`tonysysDataSource`), min/max pool size 1–5
- **JDBC:** `tonysysJdbcTemplate` bean injected into DAOs by name (`default-autowire="byName"`)
- **Transactions:** AOP-based declarative transactions on all service methods matching `insert*`, `del*`, `update*`, `add*`
- **Cache:** EhCache via `ehcache-spring-annotations` (`@Cacheable` / `@TriggersRemove`)
- **Scheduler:** `task:scheduler` with 2 threads for `@Scheduled` tasks

### MVC Context (`tonysys-servlet.xml`)

- **Component scan:** `com.tonysys.admin.controller`
- **View resolver:** JSP suffix `.jsp` via `InternalResourceViewResolver`
- **Content negotiation:** Supports both JSON and JSP view resolution
- **Message converter:** `UTF8StringHttpMessageConverter` for `text/plain` and `text/html` responses

---

## Key Conventions

### Naming

- Controller methods return a `String` view name (e.g., `"redirect:/index.jsp"`, `"/login"`) or a `ModelAndView`.
- DAO implementations are in `dao/Impl/` and named `XxxDAOImpl`.
- Service implementations are in `service/Impl/` and named `XxxServiceImpl`.
- RowMapper classes are named `XxxRowMapper` or `XxxNoDormitoryRowMapper` for variant projections.

### Dependency Injection

- Wiring is `byName` in the root context; use `@Resource` (JSR-250) for field injection in controllers and services.
- The `JdbcTemplate` bean is named `tonysysJdbcTemplate` — inject it by this exact name.

### Transaction Handling

- Transactions are applied automatically at the service layer for methods prefixed with `insert`, `del`, `update`, or `add`.
- Do not manually manage transactions in DAOs or controllers.

### JSON Responses

- Use `ResultMSG` as the response wrapper for all API-style endpoints.
- JSON serialization uses both Jackson (`jackson-mapper-asl`) and Alibaba FastJSON (`FastJsonHelper`).
- For JSONP responses, use `MappingJacksonJsonpView`.

### Caching

Three named EhCache caches (24-hour TTL, 10,000 max entries each):
- `userCache`
- `dormitoryCache`
- `conductScoreCache`

Annotate service methods with `@Cacheable` and `@TriggersRemove` to use them.

### Logging

- Uses SLF4J + Logback.
- Logger names follow package paths (e.g., `com.tonysys.admin.dao`, `com.tonysys.admin.service`).
- Log files are written to `/ROOT/logs/tonysys.com/business.log`.
- Debug level is enabled for all `com.tonysys.admin.*` packages.

### Character Encoding

- All HTTP input/output uses UTF-8.
- The `CharacterEncodingFilter` in `web.xml` enforces UTF-8 at the servlet level.
- The custom `UTF8StringHttpMessageConverter` handles string responses.

---

## Dependencies Summary

| Library | Version | Purpose |
|---|---|---|
| Spring Framework | 3.0.5.RELEASE | Core MVC, JDBC, AOP, TX |
| MySQL Connector/J | 5.1.15 | JDBC driver |
| C3P0 | 0.9.1.2 | Connection pooling |
| EhCache Spring Annotations | 1.2.0 | Declarative caching |
| Logback | 1.0.7 | Logging implementation |
| SLF4J | 1.7.1 | Logging facade |
| Alibaba FastJSON | 1.1.21 | JSON serialization |
| Jackson | 1.9.2 | JSON serialization (Spring MVC) |
| Apache HttpComponents | 4.2.1 | HTTP client utilities |
| Apache Commons Lang | 2.6 | String utilities |
| Google Guava | 13.0.1 | General utilities |
| AspectJ Weaver | 1.6.9 | AOP support |
| Servlet API | 2.5 | Servlet container contract |
| JSTL | 1.2 | JSP tag libraries |

---

## Known Limitations

- **No automated tests** — the project has no test directory or test classes.
- **Outdated dependencies** — Spring 3.0.5 (2010), MySQL driver 5.1.15; do not upgrade without thorough regression testing.
- **Plain-text password comparison** — `LoginController` compares passwords with `.equals()`; no hashing.
- **Hardcoded dev credentials** — `filter-dev.properties` uses `root/root`; never use in production.
- **No CI/CD pipeline** — builds and deployments are manual.
- **Chinese comments and UI** — all JSP pages, comments, and error messages are in Chinese.
