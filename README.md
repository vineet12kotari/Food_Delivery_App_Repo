# 🚀 Food Delivery Analytics Portal: Real-Time Strategy with Streamlit & Cortex AI

**A full-stack analytics solution seamlessly deployed and running adjacent to the data inside the Snowflake Data Cloud.** This project integrates real-time operational data with Generative AI to provide executives with immediate, actionable insights into platform profitability, restaurant performance, and customer loyalty.

[![Built with Streamlit](https://img.shields.io/badge/Streamlit-Powered-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Data Source: Snowflake](https://img.shields.io/badge/Data%20Source-Snowflake%20Cloud-0099E6?logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![AI Engine: Cortex](https://img.shields.io/badge/AI%20Engine-Snowflake%20Cortex-2EA44F)](https://www.snowflake.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status: Live Demo](https://img.shields.io/badge/Status-Deployed%20in%20Snowflake-2EA44F)](<LINK_TO_YOUR_SNOWSIGHT_APP_HERE>)

---

## 💡 Core Idea / Project Purpose

This project directly addresses the need for **real-time, granular strategic decisions** in the high-velocity food delivery industry. It showcases an innovative, enterprise-grade architecture where **analytics are performed where the data lives**, eliminating latency and data transfer costs.

**The primary goal is to unlock actionable intelligence to inform strategic decisions:**

* **Profitability Optimization:** Identify top-grossing restaurants, commission revenue, and net profit to optimize commission rates and menu offerings.
* **Customer Loyalty:** Track customer demographics, join dates, and order frequency to develop targeted marketing campaigns and loyalty programs.
* **Operational Excellence:** Analyze ratings, cuisine types, and commission rates to inform restaurant selection and menu optimization.

By leveraging these insights, users can: **Optimize menu offerings and pricing strategies, enhance customer retention and loyalty programs,** and **inform strategic business decisions to drive growth and profitability.**

---

## 🛠️ Technical Stack: Cloud-Native & AI-Driven

This project leverages a cutting-edge, integrated suite of tools for secure and efficient analytics.

| Component | Technology | Showcase Skill / Purpose |
| :--- | :--- | :--- |
| **Application Hosting** | **Streamlit in Snowflake (SiS)** | Demonstrates **zero data egress**, high performance, and automatic scaling within the data cloud perimeter. |
| **Data Engine** | **Snowflake Data Cloud** | Unified platform for data warehousing, compute, and application execution. |
| **NL2SQL / AI** | **Snowflake Cortex AI** | Implements secure **Natural Language Query** functionality (Tab 4) and dynamic text summarization (Tab 1). |
| **Frontend/Logic** | **Python 3.9+** | Used for dashboard logic, data manipulation, and utilizing Streamlit/Plotly libraries. |

---

## 📊 Dashboard Structure & Functionality

The portal provides a multi-dimensional view designed for strategic navigation:

| Tab | Icon | Core Focus |
| :--- | :--- | :--- |
| **1. Portal Summary** | 📰 | **AI-Generated Context** explaining the dashboard's objective and core data structure. |
| **2. Executive Dashboard**| 🚀 | High-level financial (**GMV, Profit**) and operational KPIs. |
| **3. Restaurant Deep Dive**| 🍽️ | Analysis of profitability, **commission impact**, and rating correlation. |
| **4. AI Analyst** | 🧠 | **NL2SQL Engine:** Ask business questions; Cortex generates and executes SQL live. |
| **5. Customer Insights** | 👥 | Metrics on **customer loyalty, repeat rate**, and satisfaction distribution. |
| **6. Conclusion & Recs** | 🧩 | **Executive Action Plan** combining insights into data-backed next steps. |

---

## ⚙️ Key Technical Achievements

This section highlights the specific software engineering and data governance skills demonstrated in the project:

* **NL2SQL Integration:** Designed and implemented a secure AI workflow (Tab 4) where user text is dynamically passed to `SNOWFLAKE.CORTEX.COMPLETE()` to instantly generate and execute complex SQL queries against the underlying tables.
* **Strategic Conclusion Synthesis:** Developed logic (Tab 6) to run multiple aggregate queries and use Python conditional statements (`if/then`) to generate **contextual, data-driven strategic recommendations**.
* **Data Model & Source:** Built upon a clear structure encompassing six core files (e.g., `FACT_ORDER_STREAMLIT.csv`, `DIM_RESTAURANT_STREAMLIT.csv`) for a comprehensive view of the business.
* **Custom UI & State Management:** Utilized Streamlit's `st.session_state` for managing custom features like the **Dark/Light Mode toggle** and complex filter states.
* **Secure Git Synchronization:** Established a secure connection between the internal Snowflake environment and this public GitHub repository, demonstrating proficiency in cloud-native **version control** and CI/CD preparation via Snowflake's Git Integration DDL.

---

## 📁 Repository Structure

The repository is structured to enable immediate deployment within the Streamlit in Snowflake environment. It contains the following core files, with the CSV files simulating the data tables:

| Source File | Type | Purpose |
| :--- | :--- | :--- |
| `FACT_ORDER_STREAMLIT.csv` | **FACT** | Core order transactions, GMV, and profit metrics. |
| `DIM_CUSTOMERS_STREAMLIT.csv` | **DIM** | Customer demographics and loyalty metrics. |
| `DIM_RESTAURANT_STREAMLIT.csv` | **DIM** | Restaurant details, ratings, cuisine type, and commission rates. |
| `DIM_FACT_ORDER_ITEMS_STREAMLIT.csv` | **FACT** | Detailed breakdown of items within each order. |
| `DIM_MENU_ITEM_STREAMLIT.csv` | **DIM** | Menu category and item pricing details. |
| `DIM_COUPON_STREAMLIT.csv` | **DIM** | Coupon usage and discount information. |

### Repository Files

* `streamlit_app.py`: The core application logic.
* `environment.yml`: Defines Python dependencies.
* `Data/` (Folder): Contains the six core CSV data files.

---

### Screenshots / Demos
Example: ![Dashboard Preview](https://github.com/vineet12kotari/Food_Delivery_App_Repo/blob/main/Snapshot.png)

--- 

## 📜 License

Distributed under the MIT License.

