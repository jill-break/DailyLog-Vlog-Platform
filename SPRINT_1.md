# Sprint 1: Execution (The Walking Skeleton)

**Sprint Goal:** Deliver a working MVP where users can Create and View posts, and establish a CI/CD pipeline.
**Status:** In Progress
**Selected User Stories:** US-1 (Create Post), US-2 (View List), US-3 (View Details)

---

## 1. Task Breakdown & Status
*This section tracks the technical tasks required to complete the selected User Stories.*

### **Backend (Python/FastAPI)**
- [x] Initialize Project Structure & Virtual Environment
- [x] Create In-Memory "Database" (List)
- [x] **Feature (US-1):** Implement `POST /posts` endpoint
- [x] **Feature (US-2):** Implement `GET /posts` endpoint
- [x] **Testing:** Write Unit Tests (`test_main.py`)
- [ ] **Refactor:** Switch from In-Memory List to PostgreSQL (Planned for end of Sprint 1 or Sprint 2)

### **Frontend (Next.js)**
- [x] Initialize Next.js Project
- [ ] **Feature (US-2):** Create Homepage to fetch and display posts
- [ ] **Feature (US-1):** Create "New Post" Form
- [ ] **Feature (US-3):** Create Post Detail Page (Dynamic Route)
- [ ] **Integration:** Connect Frontend to Backend API

### **DevOps & Infrastructure**
- [x] Initialize Git Repository & Push to Main
- [ ] **CI Pipeline:** Create GitHub Actions workflow (`ci.yml`) to run tests automatically
- [ ] **Containerization:** Add `Dockerfile` for Backend (Optional for local dev, good for bonus)

---

## 2. CI/CD Evidence
*Documentation of the pipeline setup as required by the grading rubric.*

* **Pipeline Tool:** GitHub Actions
* **Triggers:** Push to `main`, Pull Requests
* **Stages:**
    1.  Checkout Code
    2.  Install Python Dependencies
    3.  Run `pytest`
* **Status:** (To be updated after setting up `.github/workflows/main.yml`)

---

## 3. Sprint Review (Demo)
*To be filled at the end of the sprint.*

* **Screenshot 1:** (Insert screenshot of Swagger UI showing successful API calls)
* **Screenshot 2:** (Insert screenshot of Next.js Homepage showing the list of vlogs)
* **Accomplishments:**
    * Successfully connected Python Backend to Next.js Frontend.
    * CI pipeline catches errors on every push.

---

## 4. Retrospective
*Required reflection on the process.*

**What went well?**
* (Example: Separating backend and frontend allowed for clear testing of the API.)

**What could be improved?**
* (Example: I forgot to add CORS headers initially and spent an hour debugging connection errors.)

**Action Plan for Sprint 2:**
* (Example: Automate the database setup using Docker Compose.)