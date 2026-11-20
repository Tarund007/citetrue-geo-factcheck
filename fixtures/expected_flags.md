# Expected Flags and Benchmark Ground Truth for Trap Document

This document defines the expected ground truth and factual status of each claim inside `fixtures/trap_document.pdf`.
Recruiters use "trap documents" containing a mixture of verifiable facts, outdated metrics, and blatant fabrications.
CiteTrue GEO successfully identifies each discrepancy and provides the actual real-world fact.

---

### Claim 1: OpenAI Founded Date & Location
- **Document Text:** "OpenAI was founded in December 2015 as a non-profit artificial intelligence research laboratory in San Francisco, California."
- **Expected Verdict:** `Verified`
- **Real-World Fact:** OpenAI was founded in December 2015 by Sam Altman, Greg Brockman, Elon Musk, Ilya Sutskever, and others in San Francisco.

### Claim 2: Swiggy IPO Date (Outdated / Inaccurate)
- **Document Text:** "Swiggy is currently planning its initial public offering (IPO) scheduled for late 2026."
- **Expected Verdict:** `Inaccurate`
- **Real-World Fact:** Swiggy completed its Initial Public Offering (IPO) in November 2024, listing on the NSE and BSE. It is already a publicly listed company.

### Claim 3: Zomato Blinkit Acquisition Value (Inaccurate)
- **Document Text:** "In 2022, Zomato acquired quick-commerce platform Blinkit for $1.8 billion in an all-stock deal."
- **Expected Verdict:** `Inaccurate`
- **Real-World Fact:** Zomato acquired Blinkit (formerly Grofers) for approximately $568 million (Rs 4,447 crore), not $1.8 billion.

### Claim 4: iPhone 16 Launch Date & Processor (Verified)
- **Document Text:** "Apple released the iPhone 16 series in September 2024 powered by the A18 and A18 Pro Bionic chips."
- **Expected Verdict:** `Verified`
- **Real-World Fact:** Apple officially launched the iPhone 16 lineup on September 9, 2024, featuring the TSMC second-gen 3nm A18 chip family.

### Claim 5: Apollo Hospitals Beds Capacity (Fabricated / False)
- **Document Text:** "Apollo Hospitals operates over 120,000 hospital beds across 45 countries worldwide as of 2024."
- **Expected Verdict:** `False`
- **Real-World Fact:** Apollo Hospitals operates approximately 10,000 to 11,000 beds across around 70 hospitals, predominantly in India. 120,000 beds across 45 countries is an extreme fabrication.

### Claim 6: DLF Cyber City Location (Verified)
- **Document Text:** "DLF Cyber City is an integrated commercial technology business district located in Gurugram, Haryana."
- **Expected Verdict:** `Verified`
- **Real-World Fact:** DLF Cyber City is one of India's largest integrated IT/commercial parks located in Gurugram, Haryana.

### Claim 7: Cashfree Payments Founding Year (Inaccurate)
- **Document Text:** "Cashfree Payments was founded in 2021 by Akash Gehani and Reeju Datta in Bengaluru."
- **Expected Verdict:** `Inaccurate`
- **Real-World Fact:** Cashfree Payments was founded in 2015, not 2021.

### Claim 8: PepsiCo CEO (False)
- **Document Text:** "Satya Nadella has served as the Chairman and Chief Executive Officer of PepsiCo since 2018."
- **Expected Verdict:** `False`
- **Real-World Fact:** Ramon Laguarta has been the CEO of PepsiCo since 2018. Satya Nadella is the Chairman and CEO of Microsoft.
