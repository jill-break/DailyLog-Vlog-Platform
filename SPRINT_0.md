# Sprint 0: Planning (Setup)

**Project Name:** DailyLog Vlog Platform

**Sprint Goal:** Prepare the project vision, backlog, and standards for execution.

---

## 1. Product Vision
The **DailyLog** is a lightweight vlogging platform that allows the creator to share daily updates via video links and text, while fostering community engagement through real-time reactions and comments.

---

## 2. Product Backlog
*Estimation Scale: Story Points (1, 2, 3, 5, 8)*

| ID | Priority | User Story | Acceptance Criteria (AC) | Estimate |
|:---|:---|:---|:---|:---|
| **US-1** | **High** | **As a Vlogger,** I want to **create a new post** so that I can share my daily activities. | 1. API endpoint `/posts` accepts `title`, `content`, and `video_url`.<br>2. Data is saved successfully to the PostgreSQL database.<br>3. Frontend displays a success notification upon submission.<br>4. Unit test validates that a post with valid data returns HTTP 201. | **5** |
| **US-2** | **High** | **As a Viewer,** I want to **view a list of all vlogs** so that I can see recent updates. | 1. Homepage fetches data from `/posts` API.<br>2. Posts are displayed in reverse chronological order (newest first).<br>3. Each card displays the Title, Date, and a short snippet of content. | **3** |
| **US-3** | **Medium** | **As a Viewer,** I want to **view the details of a single post** to read the full content. | 1. Clicking a post card navigates to `/post/[id]`.<br>2. The video URL renders in a clickable link or embedded player.<br>3. If the ID does not exist, a 404 error page is displayed. | **3** |
| **US-4** | **Medium** | **As a Viewer,** I want to **'like' a post** to show my appreciation. | 1. A 'Like' button is visible on the post detail page.<br>2. Clicking the button increments the count immediately in the UI.<br>3. The new count persists in the database after a page reload. | **3** |
| **US-5** | **Low** | **As a Viewer,** I want to **comment on a post** to engage with the vlogger. | 1. A comment form is available below the post details.<br>2. Submitted comments appear in the list without a full page refresh.<br>3. Empty comments are rejected with an error message. | **5** |

---

## 3. Definition of Done (DoD)
For any User Story to be considered "Done" in this project, it must meet the following standards:

- [ ] **Code Complete:** Feature is implemented in Python (FastAPI) and Next.js.
- [ ] **Version Controlled:** All code is committed and pushed to the `main` branch on GitHub.
- [ ] **Tested:** At least one passing Unit Test exists for the backend logic.
- [ ] **Clean:** Code follows standard linting rules (no obvious errors or debug print statements).
- [ ] **Buildable:** The application runs locally (e.g., via Docker) without crashing.

---

## 4. Sprint 1 Plan
*Goal: Deliver the "Walking Skeleton" (MVP) and establish the CI/CD pipeline.*

I have selected the following stories for Sprint 1 Execution:

1.  **US-1 (Create Post):** Essential for inputting data into the system.
2.  **US-2 (View List):** Essential for displaying data to the user.
3.  **US-3 (View Details):** Essential for basic navigation.

**Total Story Points committed:** 11 Points.