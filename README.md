# SOC Behavioural Anomaly Detection System

A behavioural anomaly detection system designed to simulate a **Security Operations Centre (SOC)** monitoring environment.

The project analyses SSH authentication activity and web traffic behaviour to detect suspicious IP activity using **unsupervised machine learning**.

The system builds behavioural profiles per IP address and uses **Isolation Forest** to identify anomalous behaviour patterns consistent with brute-force attacks and web scanning.

---

# Project Overview

Traditional intrusion detection systems often rely on signatures of known attacks.  
This project explores a **behavioural anomaly detection approach**, where the model learns patterns of normal behaviour and flags unusual activity.

The pipeline simulates a SOC workflow:
Network Activity
↓
Feature Engineering
↓
Behaviour Profiles (per IP)
↓
Baseline Model Training
↓
Anomaly Detection
↓
Ranked Suspicious IPs


---

# Features

The system extracts behavioural indicators from simulated SSH and web activity.

## SSH Behaviour Features

- Total login attempts
- Failed login attempts
- Successful logins
- Login failure ratio
- Number of unique usernames attempted

These features help capture **SSH brute force patterns**.

---

## Web Activity Features

- Total HTTP requests
- Error response count
- POST request count
- Unique endpoints accessed
- Error response ratio
- POST request ratio

These features help detect **web scanning behaviour**.

---

## Cross-Source Behaviour Features

Additional metrics combine SSH and web behaviour:

- Total activity per IP
- SSH activity ratio
- Seen in SSH logs
- Seen in web logs

Each row in the dataset represents **a behavioural profile of one IP address**.

---

# Synthetic Behaviour Generator

Since labelled attack data can be difficult to obtain, the project includes a **synthetic behaviour generator** that simulates different types of activity.

### Normal Users
- Low SSH activity
- Low failure ratios
- Typical browsing patterns

### SSH Brute Force Attackers
- High login attempt volume
- Very high failure ratios
- Many usernames targeted

### Web Scanners
- High request volume
- Large numbers of endpoints accessed
- High error response rates

Generated dataset size:
200 Normal IPs
20 SSH Attackers
20 Web Scanners


Total: **240 behavioural profiles**

---

# Baseline vs Detection Window

To simulate real-world SOC deployment, the dataset is split into two time windows.

### Baseline Window
Historical activity used to train the anomaly detection model.  
This dataset contains mostly normal behaviour with minimal attack contamination.

### Detection Window
New incoming activity where attacks occur.  
The trained model analyses this window to detect anomalies.

This mirrors real-world systems where models learn **historical behaviour before detecting new threats**.

---

# Machine Learning Model

The project uses **Isolation Forest**, an unsupervised anomaly detection algorithm.

Isolation Forest works by isolating data points in random decision trees.  
Points that are easier to isolate are considered anomalous.

Pipeline steps:

1. Generate synthetic behavioural dataset
2. Split baseline vs detection windows
3. Standardise feature values
4. Train Isolation Forest on baseline behaviour
5. Score detection window IPs
6. Rank IPs by anomaly score

Higher anomaly scores indicate more suspicious behaviour.

---

# Evaluation Metrics

Since synthetic attackers are labelled, the system can compute detection performance.

Metrics implemented:

## Recall (Detection Rate)

Percentage of attackers correctly detected.

## False Positive Rate

Percentage of normal IPs incorrectly flagged as anomalies.

Example results:
Total Attackers: 34
Total Normals: 20
True Positives: 34
False Positives: 2

Recall: 1.00
False Positive Rate: 0.10


This indicates the model detected all attackers while maintaining a low false positive rate.

---

## Project Structure

```
src/
│
├── data/
├── generator.py
├── feature_engineering/
├── parsers/
├── pipeline/
└── train_and_detect.py
```


### Key Components

**generator.py**  
Synthetic behavioural dataset generator.

**train_and_detect.py**  
Main anomaly detection pipeline.

---

## Running the Project

### 1. Create a virtual environment

```bash
python -m venv venv
```

### 2. Activate the environment

Windows (PowerShell):

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install pandas scikit-learn numpy
```

### 4. Run the anomaly detection pipeline

```bash
python -m src.pipeline.train_and_detect
```

Example output:

```
Top 20 Most Suspicious IPs

SSH_ATTACK_*
WEB_ATTACK_*
```

---
## 📊 Analytics & Dashboard

The anomaly detection results are visualised through an interactive **Tableau dashboard**, enabling clear interpretation of model performance and network behaviour.

### Dashboard Components
![Dashboard](docs/images/dashboard.png)

**Anomaly Score Distribution**
- Histogram showing the distribution of anomaly scores across network flows
- Allows comparison between **benign traffic and attack traffic**
- Demonstrates how abnormal traffic produces significantly higher anomaly scores

**Confusion Matrix**
- Evaluates model performance by comparing **predicted anomalies vs actual attack labels**
- Highlights true positives, false positives, true negatives, and false negatives

**Performance Metrics**
- Detection Rate (Recall): percentage of attacks successfully identified
- False Positive Rate: percentage of normal traffic incorrectly flagged as malicious

**Average Anomaly Score by Label**
- Shows the difference in anomaly scores between benign traffic and attack traffic
- Confirms that malicious traffic consistently produces higher anomaly scores

These visualisations allow the system to function similarly to a **Security Operations Center (SOC) monitoring dashboard**, enabling analysts to quickly identify suspicious network activity.

---

## 🗄️ Data Storage

Detected anomalies and model outputs are stored in a **SQLite database** for persistence and further analysis.

### Stored Fields

- Network flow features
- Anomaly score
- Predicted anomaly label
- Ground truth attack label

### Benefits

- Historical anomaly tracking
- Data export for analytics
- Integration with dashboard visualisation tools

## Future Improvements

In order of priority:

1. Integration with real intrusion detection datasets (e.g. CICIDS2017) to evaluate the model on real network traffic. - Completed
2. Database storage via SQLite to persist detection results and enable querying by IP address. - Completed
3. Tableau / analytics dashboards for analyst-facing monitoring and anomaly investigation.
4. Score distribution visualisation and evaluation plots (e.g. anomaly score distributions and confusion matrices) to analyse separation between normal and malicious behaviour.
5. Containerisation using Docker and scalable deployment via Kubernetes.
