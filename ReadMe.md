#Project Proposal

**In a paragraph: what is the scope of your project?**

The proposed project aims to leverage the capabilities of LLM technology within the pharmacy domain. Specifically, it focuses on utilizing LLM to extract and analyze patient notes and metadata from an Electronic Health Records database. By cross-referencing this information with the prescribed medication’s documentation, the project aims to minimize the occurrence of pharmacists calling for adjustments on prescribed medications due to potential drug mismatches with the patient's ongoing profile. This solution intends to enhance patient safety and optimize medication fulfillment processes within the US healthcare system.

**In a few bullets: What is the impact of your project?**
i.e what problem are you solving/who is the end user?

The project addresses the problem of potential medication prescription errors and delays in prescription fulfillment from pharmacies within the United States healthcare system.
Current EHR features utilize Clinical Decision Support (CDS) systems to verify drug prescriptions, reducing adverse effects of multiple medications by 80%. However, studies indicate that doctors override approximately 60% of the alerts, leading to alert fatigue and increased risks of Adverse Drug Events (ADEs).
The end users of our proposed solution would be doctors, who are ultimately responsible for prescribing medications, and pharmacies/medical facilities that handle medication dispensing.
The existing CDS systems heavily rely on rule-based approaches to generate recommendations, often resulting in alerts triggered by subjective word interpretation and lacking comprehensive data analysis.
The primary impact of the project is to improve prescription accuracy and reduce delays in prescription fulfillment. This will enhance efficiency within the healthcare system, allowing patients to receive their prescribed medications promptly while minimizing the risk of errors or adverse health effects caused by drug mismatches.

**List the resources you plan to use?**
Datasets, GPUs, API's, pre-trained models, etc. (we realize this will be subject to change)

Datasets: EPIC Sample EHR DB (Self Provided- Free)
APIs: GPT-4, Anthropic, Vercel, DailyMed (Self Provided- Free)

**In a few bullets: How do you plan to distribute your project and get it in front of your end user?**
i.e front-end interfaces, spreading on twitter or GitHub, which workflows you might integrate into, etc.
API Integration: The project will focus on developing an API that integrates with healthcare systems like EPIC. This will enable doctors and healthcare professionals to access the LLM-powered medication verification system within their existing workflows.
Online Presence and Documentation: A dedicated website will be created to provide comprehensive documentation, tutorials, and examples for developers. It will offer guidance on integrating the API into their systems
