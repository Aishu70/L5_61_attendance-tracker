# Lab 5: Static Code Analysis

## Project Information

- **Project:** Attendance Tracker
- **File Analysed:** `attendance_tracker.py`
- **Tools Used:** Pylint, Bandit, Flake8
- **Objective:** Identify and fix code quality, security, and formatting issues using static code analysis.

---

## 1. Issues Identified and Fixes

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Line too long | Code Quality / Style | 60 | Pylint reported a line exceeding the recommended maximum length. | Split the statement across multiple lines. |
| Missing module docstring | Code Quality | 1 | The module does not contain a module-level docstring describing its purpose. | Add a descriptive docstring at the beginning of the file. |
| Missing function docstrings | Code Quality | 15, 18, 23, 29, 32, 41, 45, 49, 58, 63, 66, 69, 72, 75 | Multiple functions lack documentation explaining their purpose. | Add meaningful docstrings to all functions. |
| Invalid function naming | Code Quality | 15, 18, 23, 29, 32, 41, 45, 49, 58, 63, 66, 69, 72 | Function names use camelCase instead of Python's recommended snake_case convention. | Rename functions using snake_case and update their calls. |
| Mutable default argument | Potential Bug | 18 | The `register={}` default dictionary is shared across function calls and can retain unintended state. | Replace the default with `None` and initialize a new dictionary inside the function. |
| Simplifiable Boolean expression | Code Quality | 30 | The conditional expression returns `True` or `False` unnecessarily. | Return the comparison directly. |
| Boolean comparison | Code Quality | 35 | The code compares a Boolean result with `False` instead of using a direct Boolean expression. | Use `not` before the function call. |
| Unnecessary list comprehension | Code Quality | 43 | A list is created only to be consumed by `any()`. | Use a generator expression instead. |
| Unnecessary nested comprehension | Code Quality | 46 | The date list uses an unnecessary nested list comprehension. | Simplify the expression to iterate directly over the attendance records. |
| File opened without context manager | Code Quality | 50-55 | The CSV file is manually opened and closed, which is less robust if an error occurs. | Use a `with open(...)` statement. |
| Unspecified file encoding | Code Quality / Portability | 50 | The CSV file is opened without explicitly specifying an encoding. | Specify `encoding="utf-8"` when opening the file. |
| Dictionary iteration improvement | Code Quality | 53 | Pylint recommends iterating through dictionary items when both keys and values are needed. | Use `.items()` where appropriate. |
| Missing HTTP timeout | Security / Reliability | 60 | Bandit reported that the HTTP request does not specify a timeout. | Add an appropriate timeout to the request. |
| Disabled SSL certificate verification | Security | 60 | Bandit reported `verify=False`, which disables HTTPS certificate verification. | Enable certificate verification by removing `verify=False` or explicitly setting `verify=True`. |
| Subprocess module usage | Security | 5, 64 | Bandit reported the subprocess import and associated command execution for further security review. | Avoid unsafe shell execution and use explicit subprocess arguments. |
| Shell wildcard injection risk | Security | 64 | Bandit reported possible wildcard injection in the backup command. | Select CSV files explicitly and pass their paths as a list of arguments. |
| Partial executable path | Security | 64 | Bandit reported the use of a partial executable path for process execution. | Use a trusted executable and avoid relying on an uncontrolled executable search path where practical. |
| `shell=True` in subprocess | Security | 64 | Bandit reported subprocess execution with `shell=True`. | Use an argument list with `shell=False` instead. |
| Insecure TLS protocol default | Security | 66 | Bandit reported the explicit use of the legacy TLS 1.0 protocol. | Use `ssl.create_default_context()` to obtain a secure default TLS context. |
| Shell execution flag in job description | Security Review | 73 | Bandit reported a function call that passes `shell=True`. The function currently describes a command rather than executing it. | Represent the command as a list of arguments and set the shell flag to `False`. |
| Unused imports | Code Quality / Style | 1, 4, 6 | Flake8 reported unused imports for `os`, `json`, and `datetime`. | Remove unused imports or use them where required. |
| Insufficient blank lines | Code Quality / Style | 15, 18, 23, 29, 32, 41, 45, 49, 58, 63, 66, 69, 72, 75 | Flake8 reported that some top-level definitions do not have the required two blank lines between them. | Add the required blank lines between top-level definitions. |
| Invalid Boolean comparison style | Code Quality / Style | 35 | Flake8 reported an E712 violation for comparing a Boolean expression to `False`. | Use `if not condition:` instead. |
| Lines exceeding style limit | Code Quality / Style | 43, 54, 60, 78, 81, 82 | Flake8 reported lines exceeding 79 characters. | Wrap long expressions and function calls across multiple lines. |
| Missing blank lines after module-level definitions | Code Quality / Style | 96 | Flake8 reported an E305 violation because there are not enough blank lines before the module-level call. | Add the required blank lines before the final call. |

---

## 2. Additional Issues Observed During Code Inspection

The following issues were identified by inspecting the source code. They should not be treated as direct findings from the supplied reports unless a tool explicitly reports them.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| Hardcoded API credential | Security | 12 | The ERP API key is embedded directly in the Python source file. | Read the key from an environment variable and rotate it if it is a real credential. |
| Possible division by zero | Potential Bug | 24-27 | Attendance percentage calculation fails when a student has no records. | Return an appropriate value, such as zero, when the record list is empty. |
| Potential CSV formula injection | Security | 77, 54 | A student name beginning with a formula character may be interpreted as a formula by spreadsheet software. | Sanitize untrusted spreadsheet values before exporting them. |
| Empty attendance date list | Potential Bug | 45-47 | Calling `max()` on an empty list raises an exception. | Return `None` or another documented value when no attendance dates exist. |
| Attendance threshold boundary | Logic | 29-30 | The original condition rejects attendance equal to the configured minimum of 75%. | Confirm the intended rule and use `>=` if 75% is inclusive. |

---

## 3. Summary of Static Analysis Results

### Pylint
Pylint identified code quality issues involving naming conventions, missing docstrings, mutable default arguments, Boolean expressions, list comprehensions, file handling, and line length.

### Bandit
Bandit identified eight security findings:

- **High severity:** 2 findings.
- **Medium severity:** 3 findings.
- **Low severity:** 3 findings.

The findings include disabled SSL certificate verification, a missing HTTP timeout, subprocess usage, wildcard injection concerns, and an obsolete TLS protocol.

### Flake8
Flake8 identified unused imports, missing blank lines, an invalid Boolean comparison style, long lines, and a missing blank line before the final module-level call.

---

## 4. Corrective Actions

The following corrective actions will be performed:

1. Improve function naming and add documentation strings.
2. Remove mutable default arguments.
3. Improve Boolean expressions and simplify comprehensions.
4. Improve file handling and specify file encoding.
5. Enable HTTPS certificate verification and add an HTTP timeout.
6. Remove unsafe shell execution where possible.
7. Use a secure default TLS context.
8. Remove unused imports and correct formatting violations.
9. Review additional security and error-handling issues.
10. Rerun all three tools to verify the fixes.

---

## 5. Verification

After applying the corrections, the following commands will be used to verify the changes:

```bash
python -m pylint attendance_tracker.py
python -m bandit -r attendance_tracker.py
python -m flake8 attendance_tracker.py