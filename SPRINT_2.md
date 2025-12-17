# Sprint 2: Execution & Improvement

**Sprint Goal:** Persist data using PostgreSQL, add user engagement features (Likes/Comments), and implement monitoring.
**Status:** In Progress

---

## 1. Backlog & Task Breakdown
### **Process Improvements (Refactoring)**
- [ ] **Infrastructure:** Set up Docker Compose for PostgreSQL Database.
- [ ] **Backend:** Refactor `main.py` to use SQLAlchemy instead of in-memory list.

### **New Features**
- [ ] **US-4 (Likes):** Add API endpoint and UI to "like" a post.
- [ ] **US-5 (Comments):** Add API endpoint and UI to add comments.

### **DevOps & Monitoring**
- [ ] **Monitoring:** Add health check endpoint (`/health`) and basic logging.
- [ ] **CI/CD:** Ensure pipeline passes with new database tests.

---