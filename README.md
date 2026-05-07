# Blockchain Smart Contract QA Automation Framework

## Project Summary
This project is a QA automation framework for testing Solidity smart contracts using Hardhat, PyTest, Web3.py, and GitHub Actions.

The sample contract is `TokenEscrow`, where a buyer can deposit ETH into escrow, release funds to a seller, or refund funds back to themselves.

It demonstrates practical blockchain QA responsibilities:
- Functional smart contract testing
- Negative and security testing
- Event/log validation
- Gas usage measurement
- CI/CD regression automation

## Why This Project Was Built
This repository is designed to mirror real Blockchain Test Engineer workflows for roles requiring:
- Solidity contract testing
- Ethereum transaction lifecycle validation
- Access-control and security-focused checks
- Web3.py-driven API-style test automation
- CI/CD test orchestration and artifact reporting

## Tech Stack
| Area                       | Tool                                                 |
|----------------------------|------------------------------------------------------|
| Smart Contract             | Solidity                                             |
| Blockchain Dev Environment | Hardhat                                              |
| Local Blockchain           | Hardhat Network (Ganache-style local chain behavior) |
| Automation Framework       | PyTest                                               |
| Blockchain API Layer       | Web3.py                                              |
| CI/CD                      | GitHub Actions                                       |
| Reports                    | PyTest HTML + JSON Gas Report                        |
| Languages                  | Python, JavaScript                                   |

## Repository Structure
```text
blockchain-smart-contract-qa-framework/
|-- contracts/
|   `-- TokenEscrow.sol
|-- scripts/
|   `-- deploy.js
|-- deployments/
|   `-- local.json                  # generated after deploy
|-- tests/
|   |-- conftest.py
|   |-- test_escrow_functional.py
|   |-- test_escrow_negative_security.py
|   `-- test_gas_usage.py
|-- reports/
|   `-- gas_report.json             # generated after gas test
|-- .github/
|   `-- workflows/
|       `-- ci.yml
|-- hardhat.config.js
|-- package.json
|-- requirements.txt
|-- pytest.ini
|-- .gitignore
`-- README.md
```

## Smart Contract Requirements
### Functional Requirements
1. Buyer can deposit ETH into escrow for a seller.
2. Buyer can approve the release of escrow funds to the seller.
3. Buyers can refund escrow funds.
4. Contract records buyer, seller, amount, and escrow state.
5. Contract emits events for deposit, release, and refund.

### Negative/Security Requirements
1. User cannot deposit zero ETH.
2. Buyer cannot also be a seller.
3. Duplicate order IDs are rejected.
4. Non-buyers cannot release funds.
5. Non-buyers cannot refund funds.
6. Released/refunded escrow cannot be reused.

## Test Strategy
### Functional Testing
- Deposit funds into escrow
- Release funds to seller
- Refund funds to the buyer
- Validate contract state after each transaction

### Event and Log Validation
- Validate `EscrowCreated` event
- Validate `EscrowReleased` event
- Validate `EscrowRefunded` event
- Assert expected event arguments
y
### Negative and Security Testing
- Invalid seller and zero-value deposit checks
- Duplicate order ID rejection
- Unauthorized release and refund prevention
- State transition constraints

### Gas Usage Testing
- Capture gas for deposit/release/refund
- Export report to `reports/gas_report.json`

### CI/CD Regression Testing
GitHub Actions automatically:
1. Installs Node and Python dependencies
2. Compiles Solidity contracts
3. Starts a local Hardhat blockchain node
4. Deploys the smart contract
5. Runs the full PyTest regression suite
6. Uploads reports as workflow artifacts

## Test Cases
| Test Case ID | Scenario                                     | Type            |
|--------------|----------------------------------------------|-----------------|
| TC-001       | Buyer deposits funds into escrow             | Functional      |
| TC-002       | Buyer releases funds to seller               | Functional      |
| TC-003       | Buyer refunds escrow                         | Functional      |
| TC-004       | Attacker cannot release funds                | Security        |
| TC-005       | Attacker cannot refund funds                 | Security        |
| TC-006       | Cannot deposit zero amount                   | Negative        |
| TC-007       | Cannot reuse existing order ID               | Negative        |
| TC-008       | Buyer cannot also be seller                  | Negative        |
| TC-009       | Capture gas usage for deposit/release/refund | Performance/Gas |

## Local Setup

### 1) Clone the Repository
```bash
git clone https://github.com/JUnelus/blockchain-smart-contract-qa-framework.git
cd blockchain-smart-contract-qa-framework
```

### 2) Install Node Dependencies
```bash
npm install
```

### 3) Install Python Dependencies
macOS/Linux:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 4) Compile Smart Contract
```bash
npm run compile
```

### 5) Start Local Blockchain (Terminal 1)
```bash
npm run node
```

### 6) Deploy Contract (Terminal 2)
```bash
npm run deploy:local
```

### 7) Run Full Test Suite
```bash
pytest -v
```

### 8) Generate HTML Report
```bash
pytest -v --html=reports/pytest_report.html --self-contained-html
```

### 9) Focused Test Runs
```bash
pytest -m functional -v
pytest -m security -v
pytest -m gas -v
```

## CI/CD Pipeline
Workflow file: `.github/workflows/ci.yml`

Runs on pushes to `main`/`develop` and PRs to `main`.

Artifacts uploaded:
- `reports/pytest_report.html`
- `reports/gas_report.json`
- `hardhat-node.log`

## Sample Defect Examples
### Defect 1: Unauthorized User Can Release Funds
- Severity: Critical
- Expected: Only the buyer can release escrow funds.
- Actual: The unauthorized account can call `approveRelease`.
- Impact: Escrow theft risk.
- Test Coverage: `test_attacker_cannot_release_buyer_escrow`

### Defect 2: Duplicate Order ID Accepted
- Severity: High
- Expected: Duplicate escrow order IDs should be rejected.
- Actual: Contract allows duplicate order IDs.
- Impact: Escrow records/funds could be overwritten.
- Test Coverage: `test_cannot_reuse_existing_order_id`

### Defect 3: Zero ETH Deposit Accepted
- Severity: Medium
- Expected: Deposit amount must be greater than zero.
- Actual: Contract accepts zero-value deposits.
- Impact: Invalid escrow records can be created.
- Test Coverage: `test_cannot_deposit_zero_amount`
