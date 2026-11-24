# Local Service Connect
### Local Service Problem Diagnosis and Matching System


---

## 1. Project Overview

Local Service Connect is a Python Flask web application that helps people describe household or equipment problems and connect with suitable local service providers.

A user may know that something is wrong but may not know which type of professional to contact. For example, a leaking kitchen sink may need a plumber, while a faulty light may need an electrician. The application accepts a problem description and uses a text-classification model to suggest a service category. The user can review the category and send the request to a suitable provider.

The application includes three user roles:

- **Local user/customer:** registers, submits service requests, reviews the suggested category, sends requests, tracks status, and submits feedback.
- **Service provider:** registers business details, selects service categories, receives requests, accepts or rejects them, and updates service status.
- **System administrator:** manages accounts, approves providers, manages service categories, and views service requests.

The Week 3 version connects the main customer, provider, administrator, classification, database, and feedback components. It is an academic prototype and is still being tested and improved.

## 2. Project Objectives

The project aims to:

- Accept household and equipment problem descriptions through a web interface.
- Predict a suitable service category from the submitted text.
- Allow the customer to review or change the suggested category.
- Store the original predicted category and the customer's final selected category.
- Match requests with approved providers based on service category and provider information.
- Allow customers to send requests and track their status.
- Allow providers to accept, reject, and complete service requests.
- Allow customers to submit ratings and written feedback after completion.
- Provide administrator functions for account, provider, category, and request management.
- Test the application using automated tests and browser-based workflows.
- Maintain source code, milestone documents, and evidence in GitHub.

## 3. Current Implementation Status

### Implemented and demonstrated in Week 3

- Flask application with a home page and role-based pages.
- Customer and service-provider registration.
- Login and logout.
- Administrator account setup through `seed_admin.py`.
- Administrator dashboard and provider approval.
- Provider profile and service information.
- Service request submission.
- TF-IDF and Logistic Regression category prediction.
- Display of predicted and selected categories.
- Storage of service requests in SQLite.
- Provider matching and sending a request to a selected provider.
- Provider request workspace.
- Provider acceptance and status updates, including **In Progress** and **Completed**.
- Customer request tracking.
- Customer rating and written feedback.
- Automated Week 3 workflow tests.

### Current test evidence

The Week 3 automated test run collected four tests and reported:

```text
4 passed in 5.08s
```

The browser-based test demonstrated one complete Plumbing request:

1. Customer Rahul Kumar submitted a kitchen sink pipe leakage problem.
2. The classifier displayed **Plumbing** as the predicted category.
3. The displayed model score was **0.24**.
4. The selected category was Plumbing.
5. The request was sent to Suresh Home Plumbing Services.
6. The provider accepted the request and updated it to In Progress.
7. The provider changed the status to Completed.
8. The customer submitted a 5/5 rating and written feedback.

The displayed score of 0.24 is the score shown for that prediction. It is **not** the model's overall accuracy.

### Work still requiring testing or development

- Test the classifier with more categories and a wider range of descriptions.
- Record and evaluate incorrect or uncertain category predictions.
- Complete browser tests for provider rejection, cancellation, profile updates, availability changes, and category management.
- Complete negative-input and role-access tests.
- Review the remaining partial functional requirements.
- Expand administrator reporting and provider-side service history/feedback views where required by the approved requirements.

A feature should be described as complete only when it is present in the code and has suitable test evidence.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Flask | Web application and route handling |
| HTML | Page structure and forms |
| CSS | Page layout and visual styling |
| SQLite | Application data storage |
| scikit-learn | Machine-learning classification |
| TF-IDF | Converts problem text into numerical features |
| Logistic Regression | Predicts a service category |
| pytest | Automated testing |
| Visual Studio Code | Development environment |
| Git and GitHub | Version control and project submission |

The current project uses a local SQLite database. A separate database server is not required.

## 5. Service Categories

The application is configured with these service categories:

1. Plumbing
2. Electrical
3. Appliance Repair
4. Carpentry
5. Painting
6. Cleaning
7. Other

The model's prediction depends on its training data and learned patterns. A category in the application's category list is not automatically guaranteed to be predicted correctly. Additional examples and evaluation are needed to assess the classifier for each category.

## 6. Repository Structure

The current project is organized with the application source inside `src/`. The main structure is:

```text
Local_Service_Connect/
│
├── .venv/                         # Local Python virtual environment (do not commit)
├── docs/
│   └── step_2/
│       ├── week_1/
│       ├── week_2/
│       └── week_3/
│           ├── integration_and_progress.pdf
│           └── screenshots/       # Week 3 browser and test evidence
│
├── src/
│   ├── app.py                     # Flask application and routes
│   ├── classifier.py              # TF-IDF and Logistic Regression classifier
│   ├── config.py                  # Application configuration
│   ├── database.py                # SQLite connection and database functions
│   ├── schema.sql                 # Database schema
│   ├── services.py                # Provider matching logic
│   ├── seed_admin.py              # Administrator account setup
│   ├── requirements.txt           # Python dependencies
│   ├── sample_training_data.csv   # Sample classifier training data
│   ├── instance/                  # Local application database/runtime data
│   ├── static/                    # CSS and static assets
│   ├── templates/                 # Flask HTML templates
│   └── tests/
│       ├── conftest.py
│       └── test_week3_workflow.py
│
└── README.md
```

This tree describes the current main layout. Keep the actual filenames and folders in the repository synchronized with this README when the project changes.

**Database and privacy note:** Do not commit a local database containing real user information, passwords, or other private records. Do not commit the `.venv` directory or secret environment values.

## 7. System Requirements

- Windows, Linux, or macOS.
- Python 3.13 or a Python version supported by the packages in `src/requirements.txt`.
- pip.
- Visual Studio Code or another Python editor.
- A current web browser.
- Git, if cloning or pushing the repository.

SQLite is included with standard Python installations in normal Python distributions.

## 8. Installation and Setup

### 8.1 Clone or open the repository

Clone the GitHub repository using its actual URL:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Local_Service_Connect
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with the repository URL. If the project is already on your computer, open the existing `Local_Service_Connect` folder in Visual Studio Code.

### 8.2 Create a virtual environment

Run this from the project root:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

The terminal should show `(.venv)` when activation succeeds.

If PowerShell blocks script activation, use the Python environment activation method permitted by your computer's policy, or activate it from Command Prompt:

```cmd
.venv\Scripts\activate.bat
```

### 8.3 Install dependencies

The `requirements.txt` file is inside `src`, so change to that folder before installing:

```powershell
cd .\src
python -m pip install -r requirements.txt
```

If the virtual environment is not active, activate it from the project root first.

## 9. Configuration and Administrator Setup

The application uses local configuration and SQLite. The administrator setup script requires an environment variable named `ADMIN_PASSWORD`.

From the `src` folder in PowerShell, set a strong password for the current terminal session:

```powershell
$env:ADMIN_PASSWORD = "ChooseYourOwnStrongPassword"
```

Then run:

```powershell
python seed_admin.py
```

The tested setup script reported that the administrator account was created for:

```text
admin@localservice.test
```

Use the password that you set in `ADMIN_PASSWORD` when logging in. Do not put the password in this README, source control, screenshots, or a public commit.

The environment variable is available only in the current PowerShell session. If the terminal is closed, set it again before running the setup script.

## 10. Running the Application

From the `src` folder, with the virtual environment activated, run:

```powershell
python app.py
```

Open the local address in a browser:

```text
http://127.0.0.1:5000
```

To stop the Flask development server, return to the terminal and press `Ctrl+C`.

Run the application from `src` so that relative paths and the project configuration resolve as expected.

## 11. Main Application Workflow

### 11.1 Customer workflow

1. Open the home page.
2. Register a local user account.
3. Log in.
4. Open the new service request form.
5. Enter a clear description of the household or equipment problem.
6. Submit the request.
7. Review the category predicted by the classifier.
8. Accept the suggested category or select another available category.
9. Review matching providers.
10. Send the request to a selected provider.
11. Track the request from the customer dashboard.
12. After the request is completed, submit a rating and written feedback.

### 11.2 Service provider workflow

1. Register using the Service Provider account type.
2. Enter the business name, service area, service description, availability, and service categories requested by the form.
3. Wait for administrator approval.
4. Log in after approval.
5. Open the provider area and review incoming requests.
6. Accept or reject a request.
7. For an accepted request, update the status as work progresses.
8. Mark the request Completed when the service is finished.

### 11.3 Administrator workflow

1. Create or confirm the administrator account using `seed_admin.py`.
2. Log in with the administrator credentials.
3. Open the Admin dashboard.
4. Review pending provider registrations.
5. Approve or deactivate providers as appropriate.
6. Review user accounts, categories, and service requests.
7. Use the available administration controls to manage supported records.

The exact controls available on the dashboard depend on the current implementation.

## 12. Example Problem Submission

The following description was used in the Week 3 browser workflow:

**Input:**

> Water is leaking continuously from the kitchen sink pipe. The area under the sink is becoming wet. I need a plumber to inspect the pipe and repair the leakage.

**Observed application output:**

| Field | Observed value |
|---|---|
| Predicted category | Plumbing |
| Model score displayed | 0.24 |
| Selected category | Plumbing |
| Service area | Garland, Texas |
| Matched provider | Suresh Home Plumbing Services |
| Request ID | 1 |
| Final request status | Completed |
| Customer rating | 5/5 |

This example confirms that the tested description passed through the main workflow. It does not establish the overall classification accuracy of the model.

## 13. Database Information

SQLite stores the application's records. The current database schema includes data for:

- Users and account roles.
- Service categories.
- Provider profiles.
- Provider service categories.
- Service requests.
- Customer feedback.

The service request workflow stores the predicted category and the final selected category. This allows the project to compare the classifier's suggestion with the category retained by the customer.

The database is initialized by the application/database setup code. The actual database file is kept under the application's local runtime/instance area. Do not assume that a displayed request ID alone proves every database field was saved correctly; verify the record when performing database tests.

### Database inspection

For a database check:

1. Start the application and submit a test request.
2. Identify the database path configured by the application.
3. Open the SQLite database using a SQLite viewer or Python's `sqlite3` module.
4. Inspect the relevant user, provider, service request, and feedback records.
5. Compare the stored values with the information shown in the browser.

Do not publish a database containing real personal information.

## 14. Automated Testing

The project uses pytest. Run the tests from the `src` folder:

```powershell
python -m pytest -v
```

The Week 3 test run collected four tests and reported:

| Test | Purpose | Recorded result |
|---|---|---|
| `test_user_submit_predict_store_and_match` | Checks customer request submission, category prediction, database storage, and provider matching. | PASSED |
| `test_invalid_short_problem_is_rejected` | Checks rejection of a short problem description. | PASSED |
| `test_provider_accept_and_complete_then_user_feedback` | Checks provider acceptance/completion and customer feedback. | PASSED |
| `test_admin_approves_provider` | Checks administrator provider approval. | PASSED |

**Recorded Week 3 result:**

```text
4 passed in 5.08s
```

This result applies to the test run captured on November 24, 2026. Run the tests again after making code changes and use the new terminal output as the current result.

### Browser-based integration test

The following end-to-end workflow was also demonstrated in the browser:

| Step | Action | Observed result |
|---|---|---|
| 1 | Register customer and provider | Accounts created |
| 2 | Approve provider as administrator | Provider approval updated |
| 3 | Submit a plumbing problem as customer | Request created |
| 4 | Review classifier output | Plumbing predicted |
| 5 | Send request to provider | Request sent |
| 6 | Open provider workspace | Incoming request displayed |
| 7 | Update service status | In Progress |
| 8 | Complete service | Completed |
| 9 | Submit customer feedback | Confirmation displayed; 5/5 rating shown |

Additional tests are still needed for other categories, invalid inputs, role restrictions, provider rejection, request cancellation, and other administration functions.

## 15. Functional Requirement Status

The following is a high-level summary of the approved functional requirement groups. The detailed requirement-by-requirement tracker is maintained in the Week 3 milestone document.

| Requirement group | Main functions | Current status |
|---|---|---|
| FR-01 to FR-18 – Local user | Registration, login, profile, problem submission, category review, provider matching, request tracking, cancellation, feedback | Main request and feedback workflow demonstrated; profile, cancellation, and some history functions need further testing |
| FR-19 to FR-31 – Service provider | Provider registration/profile, service categories, availability, incoming requests, accept/reject, status updates, completion, service history | Registration, approval-dependent request receipt, acceptance, status update, and completion demonstrated; rejection and some profile/history functions need testing |
| FR-32 to FR-38 – Administrator | Admin access, user/provider management, provider approval, category management, request monitoring, reports | Admin access and provider approval demonstrated; several management controls need browser testing; full reporting is not implemented |
| FR-39 to FR-42 – NLP/ML | Process text, predict category, use category in matching, store predicted and final category | Main Plumbing prediction and category-based matching demonstrated; broader model evaluation remains in progress |

### Known requirement work still to review

- **FR-10:** Verify the full category acceptance/change workflow against the approved requirement wording.
- **FR-12:** Verify that all required provider details, availability, and ratings are displayed.
- **FR-17 and FR-31:** Verify the full customer and provider service-history views.
- **FR-37:** Extend testing of invalid, duplicate, and inappropriate records.
- **FR-38:** A full system reporting view remains to be implemented.

Use the Week 3 `integration_and_progress.pdf` tracker as the detailed status record. Update both documents when requirement status changes.

## 16. Design Changes and Current Limitations

The project continues to use the planned technology stack: Python, Flask, SQLite, HTML/CSS, scikit-learn, TF-IDF, and Logistic Regression.

During Week 3 integration, two issues were corrected:

- A SQLite database-lock issue occurred in the test fixture. The fixture setup was changed so that test users were created before opening the database connection used for provider setup.
- The administrator category page expected category records with fields such as ID, name, and active status, but the route initially supplied category-name strings. The route/template data was corrected, and the administrator approval test subsequently passed.

Current limitations and work to review:

- The browser evidence demonstrates one complete Plumbing request. Other service categories still need browser tests.
- The model score shown for the Plumbing example was 0.24. More labeled data and held-out evaluation are needed before judging model performance.
- Provider rejection, customer cancellation, profile changes, availability changes, and category administration need additional browser testing.
- Full administrator reports are not yet implemented.
- Customer and provider service-history and feedback views need further verification.
- The project is an academic prototype and has not been assessed as a production service.

## 17. Troubleshooting

### `ModuleNotFoundError`

Activate the project virtual environment and install the packages from the `src` folder:

```powershell
python -m pip install -r requirements.txt
```

### `Set ADMIN_PASSWORD before running this script`

Set the environment variable in the current PowerShell terminal and run the script again:

```powershell
$env:ADMIN_PASSWORD = "ChooseYourOwnStrongPassword"
python seed_admin.py
```

### Training data cannot be found

Check that the training data file exists and that the application is being run from the `src` folder. Confirm that the file path used by `classifier.py` matches the actual file location.

### SQLite database is locked

Stop duplicate application or test processes that may be using the same database. Close database viewer connections and rerun the test. Check that test fixtures close connections after use.

### Port 5000 is already in use

Stop the other process using port 5000 or change the Flask development port in the local run configuration.

### A predicted category is unexpected

The model can make incorrect predictions. Record the description and actual result, compare it with the expected category, and include the case in model evaluation. Do not change a recorded result just to make it match the expected category.

## 18. GitHub and Milestone Submission

Before committing, check the files that Git will include:

```powershell
git status
```

Add the relevant source code, tests, documentation, and approved evidence:

```powershell
git add README.md src docs
git status
git commit -m "Update Local Service Connect Week 3 integration"
git push
```

Check the staged files before committing. Do not add:

- `.venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.env` files or passwords
- Local databases containing personal information
- Temporary files or editor caches

A suitable `.gitignore` should include at least:

```gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.env
*.db
instance/
```

If a non-sensitive database template or required sample database is intentionally part of the project, decide separately whether it should be tracked. Do not commit the live local database with test-user information.

## 19. Next Development Tasks

The next development tasks are:

1. Test the classifier with Electrical, Appliance Repair, Carpentry, Cleaning, Painting, and Other descriptions. Record actual predictions and review incorrect results.
2. Test invalid inputs and access restrictions, including blank descriptions, duplicate registration, invalid login, and customer access to administrator/provider pages.
3. Test provider rejection, request cancellation, profile updates, availability changes, and administrator category management.
4. Review and complete the remaining partial requirements, especially FR-10, FR-12, FR-17, FR-31, FR-37, and FR-38.
5. Update the requirement tracker, complete final testing and documentation, and prepare the final project submission.

## 20. Project Schedule

The planned final project date is December 8, 2026.

| Milestone | Planned date |
|---|---|
| Architecture and design | October 30, 2026 |
| Technical proof of concept | October 31, 2026 |
| Core implementation | November 10, 2026 |
| Component integration | November 16, 2026 |
| Minimum viable product | November 20, 2026 |
| Testing and evaluation | November 27, 2026 |
| Refinement | December 1, 2026 |
| Documentation | December 4, 2026 |
| Final system and presentation | December 8, 2026 |

Dates are project targets and should be updated if the course schedule or development plan changes.

## 21. Conclusion

Local Service Connect now connects the main customer, service provider, administrator, classification, database, and feedback functions in one Flask application. The Week 3 browser test demonstrated a Plumbing request from submission through provider completion and customer feedback. The automated test suite also reported four passing tests.

The next stage is to test more service categories, check negative and access-control cases, finish the remaining requirements, and evaluate the classifier with a larger and more representative dataset. The repository and milestone evidence will be updated as the project moves toward the planned December 8, 2026 completion date.
