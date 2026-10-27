# FA26_Pitts_David_COMP_699_A
# Local Service Problem Diagnosis and Matching System

## 1. Project Overview

The Local Service Problem Diagnosis and Matching System is a Python-based project designed to help users identify suitable service categories for household and equipment problems.

People often have difficulty deciding which type of service provider to contact when something stops working. For example, a leaking kitchen pipe may require a plumber, while a faulty electrical switch may require an electrician. This project aims to reduce that confusion by processing a problem description and suggesting a relevant service category.

The initial version is a technical proof of concept. It accepts a problem description through a web page, uses a machine-learning classification model to predict a category, and stores the request in an SQLite database. The project will be expanded to support service provider matching and request management.

## 2. Project Objectives

The main objectives are:

- Accept household and equipment problem descriptions through a web interface.
- Process submitted text and predict a suitable service category.
- Store problem descriptions and classification results in a database.
- Match submitted requests with service providers based on their service categories.
- Allow users to review previous requests.
- Support request status updates as the system develops.
- Evaluate the classification model using appropriate testing methods.
- Maintain source code and documentation in a GitHub repository.

## 3. Current Implementation Status

The project is being developed in stages.

### Implemented in the technical proof of concept

- A web interface for entering a problem description.
- A Python Flask application that processes submitted descriptions.
- Text classification using TF-IDF and Logistic Regression.
- SQLite storage for submitted requests.
- Display of the predicted category, model confidence value, and request ID.
- Local execution through a web browser.

### Planned for later development

- A larger and more representative labeled training dataset.
- Improved classification and model evaluation.
- Service provider registration and management.
- Matching requests with eligible service providers.
- Request history and status management.
- Authentication and access control, if required by the final design.
- Additional functional, performance, security, and usability testing.

These planned features will be marked as complete only after they have been implemented and tested.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language for the application and classification logic. |
| Flask | Handles web requests and connects the user interface with the Python code. |
| HTML | Provides the structure of the web interface. |
| CSS | Provides styling for the interface. |
| scikit-learn | Provides the text-classification algorithms and evaluation tools. |
| TF-IDF | Converts text descriptions into numerical features for classification. |
| Logistic Regression | Predicts a service category from the processed text. |
| SQLite | Stores submitted requests and their classification results. |
| pandas | Supports working with tabular data where needed. |
| Visual Studio Code | Development environment. |
| Git and GitHub | Source code management and project documentation. |

## 5. Service Categories

The initial classification model uses three example categories:

1. **Plumbing:** Problems involving pipes, taps, sinks, leaks, and related equipment.
2. **Electrical:** Problems involving electrical switches, wiring, lights, and related equipment.
3. **Appliance Repair:** Problems involving household appliances such as refrigerators and washing machines.

These categories are intended for the initial prototype. Additional categories may be added after the training data and classification approach have been evaluated.

## 6. Project Repository Structure

The repository should contain the following files and folders, adjusted to match the actual files in the project.

```text
Local-Service-Problem-Diagnosis-and-Matching/
│
├── app.py
├── classifier.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── sample_training_data.csv
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
├── tests/
│   └── test_app.py
│
├── docs/
│   ├── architecture.md
│   ├── testing-plan.md
│   └── screenshots/
│
└── service_requests.db
```

**Note:** This is a suggested structure, not a statement that every file already exists. Keep the files that are actually part of your project and update the README when you add new components. Do not commit a generated SQLite database containing real or sensitive user information.

## 7. System Requirements

The following software is required to run the current proof of concept:

- Windows, Linux, or macOS.
- Python 3.13 or another Python version compatible with the installed dependencies.
- Visual Studio Code or another Python development environment.
- pip for installing Python packages.
- A web browser.
- Git for repository management.

The current prototype uses SQLite, which is included with standard Python installations. A separate database server is not required.

## 8. Installation Instructions

### Step 1: Clone the repository

Open a terminal and run:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd YOUR_PROJECT_FOLDER
```

Replace the example placeholders with the actual GitHub repository URL and project directory name.

Alternatively, download the repository from GitHub and open its folder in Visual Studio Code.

### Step 2: Create a virtual environment

Run:

```bash
python -m venv .venv
```

Activate the environment in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If activation is successful, the terminal should display `(.venv)`.

For Windows Command Prompt, use:

```cmd
.venv\Scripts\activate.bat
```

### Step 3: Install dependencies

Run the following command from the project root:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file should list the dependencies required by the actual application. If the file is missing, create it using the packages used by your source code.

To verify the main dependencies, run:

```bash
python -c "import flask, pandas, sklearn; print('Dependencies installed successfully')"
```

## 9. Configuration Instructions

The current proof of concept runs locally and does not require external API keys or cloud services.

Before running the application, check the following:

1. The Python virtual environment is activated.
2. The required packages are installed.
3. The application source files are in the expected locations.
4. The training data file is available if the classifier loads data from a file.
5. The application has permission to create or write to its SQLite database location.

If the database is created automatically by the application, make sure the configured database path is writable. If the database is initialized through a separate script, run that script before starting the application.

No passwords, API keys, database credentials, or other secrets should be included in this README or committed to GitHub.

## 10. Running the Application

From the project directory, activate the virtual environment and run:

```bash
python app.py
```

If Flask starts successfully, the terminal should display a local address similar to:

```text
http://127.0.0.1:5000
```

Open the address in a web browser.

To stop the local server, return to the terminal and press `Ctrl+C`.

## 11. How to Use the Proof of Concept

1. Open the application in a web browser.
2. Enter a description of a household or equipment problem.
3. Select **Classify and Save**.
4. Review the predicted service category.
5. Check the displayed confidence value and request ID.
6. Inspect the SQLite database to verify that the request was saved.

For example, the following description was tested:

**Input:** The kitchen sink pipe is leaking.

**Observed result:**

- Predicted category: Plumbing
- Model confidence: 0.51
- Saved request ID: 1

This result demonstrates the basic classification and request-saving workflow. It does not establish the model's overall accuracy or prove that all types of problem descriptions will be classified correctly.

## 12. Database Information

SQLite is used to store information submitted through the application.

The initial database implementation stores request information, including the problem description, predicted category, confidence value, and creation time, as supported by the current implementation.

As the project develops, the database may be expanded to include tables for:

- Users and their accounts.
- Service providers and their service categories.
- Submitted service requests.
- Classification results.
- Request status updates and service history.

The final database structure will follow the approved system design. The additional tables and functions should not be considered implemented until they have been created and tested.

### Database verification

To verify a saved request:

1. Run the application and submit a test description.
2. Identify the SQLite database file used by the application.
3. Open the database with a SQLite viewer or Python's `sqlite3` module.
4. Inspect the relevant request table.
5. Compare the stored description and category with the result displayed by the application.

A database record should be checked directly rather than assuming that a displayed request ID alone proves that all stored fields are correct.

## 13. Testing Instructions

Testing will be performed as additional features are implemented.

### Current proof-of-concept tests

| Test | Input or action | Expected result |
|---|---|---|
| Application startup | Run `python app.py`. | Flask starts without an application error. |
| Valid problem submission | Enter a household problem description. | The application accepts the input. |
| Classification | Submit a known example. | The model returns a service category. |
| Database storage | Submit a valid request and inspect SQLite. | The corresponding request record is present. |
| Empty input | Submit the form without a description. | The application displays a validation message and does not save an invalid request. |

Record the actual results of each test before marking it as passed.

### Planned tests

Additional testing will cover:

- Unit testing of classification and validation functions.
- Integration testing between Flask, the classifier, and SQLite.
- Evaluation using a held-out classification dataset.
- Provider-matching tests.
- Request-history and status-update tests.
- Performance testing using a defined workload.
- Security testing for input validation and access control.
- Usability testing with representative users.

The classification model will be evaluated using accuracy, precision, recall, and F1-score. Any target values will be treated as evaluation goals until actual results have been collected.

## 14. Troubleshooting

### Error: `ModuleNotFoundError: No module named 'flask'`

Activate the virtual environment and install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Then run:

```bash
python app.py
```

### Error: The application cannot find the training dataset

Check whether the dataset exists at the path expected by the classifier. If the code uses a relative path, run the application from the correct project directory.

### Error: The database cannot be opened or updated

Check the database path, folder permissions, and database initialization code. Confirm that the application is using the intended SQLite file.

### Error: The port is already in use

Another application may already be using port 5000. Stop the other Flask process or configure an available port through the application's development settings.

### Unexpected classification result

The current model uses a small illustrative dataset. Incorrect predictions are possible. Record the input and result, compare the prediction with the expected category, and investigate the issue during model evaluation.

## 15. Git and GitHub Workflow

GitHub will be used to maintain the source code, documentation, and development history.

After completing a meaningful change, use the following commands:

```bash
git status
git add app.py requirements.txt README.md
git commit -m "Update proof of concept and documentation"
git push
```

Add other relevant source files to the commit when they change. Before committing, inspect `git status` to make sure that secrets, virtual-environment files, temporary files, and sensitive database contents are not included.

A `.gitignore` file should exclude generated files that do not belong in the repository.

For example:

```gitignore
.venv/
__pycache__/
*.py[cod]
.env
*.db
.pytest_cache/
```

If the project intentionally includes a non-sensitive, empty database template or a database initialization script, manage it separately rather than committing a database containing private records.

Use regular commits to document the development process instead of waiting until the end of the project to upload all files.

## 16. Project Schedule

The planned completion date is December 8, 2026.

| Milestone | Planned completion |
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

These are planned dates and will be updated as development progresses.

## 17. Limitations

The current proof of concept uses a small illustrative dataset. Its predictions have not yet been validated against a sufficiently large, representative test dataset.

The current implementation demonstrates problem submission, classification, and database storage. It is not yet a complete service marketplace. Provider matching, account management, request history, and status updates require further implementation and testing if they are included in the final approved requirements.

The system should therefore be treated as an academic prototype until its classification quality, security, reliability, and other requirements have been evaluated.

## 18. Future Improvements

Possible improvements include:

- Expanding the labeled dataset to cover more problem types and descriptions.
- Improving classification quality through model evaluation and refinement.
- Implementing provider registration and category-based matching.
- Adding request history and status tracking.
- Improving input validation and access control.
- Evaluating performance with a larger number of requests.
- Improving the interface based on user feedback.
- Preparing clearer installation and database initialization instructions.

These improvements will be prioritized according to the project requirements and the available development time.

## 19. Conclusion

The Local Service Problem Diagnosis and Matching System is being developed to help users identify suitable service categories for household and equipment problems. The current proof of concept demonstrates a basic connection between a Flask web application, a text-classification model, and an SQLite database.

The next stages will focus on improving the classification model, implementing provider matching and request-management features, and testing the completed system against its requirements. The GitHub repository will be updated throughout development to maintain the source code, instructions, documentation, and evidence of progress.

The final objective is to deliver a working minimum viable product with documented test results by December 8, 2026.
