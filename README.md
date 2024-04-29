This code simulates the queuing system for processing applications at the World Kingdom (WK) Solar Panel Funding (SPF) department. The government aims to understand why citizens experience long wait times when submitting applications.

Description of the System

Citizens arrive according to a Poisson process to the SPF offices, which are open from 9 AM to 5 PM. They can utilize an optional Application Checking Service (ACS) for a fee to reduce processing time.

There are three stages an application can go through:

Fingerprint (F): Mandatory stage for all applicants.
Case Review (C): For applicants who didn't use ACS, their application is reviewed here. They can either be approved or sent for an interview.
Interview (W): Applicants who aren't approved in the Case Review stage go for an interview. They can be approved after the interview or be rejected.
The code calculates:

Average time spent by all applicants (Ta)
Average time spent by completed applications (Tc)
Average time spent by rejected applications (Tr)
These metrics help identify bottlenecks in the application processing workflow.

Model Parameters

The code allows you to define various parameters to simulate different scenarios:

Arrival rate (λ): Number of applicants arriving per hour (Poisson process).
Service times:
μF: Fingerprint server processing rate per hour.
μC: Case Review server processing rate per hour.
μW: Interview server processing rate per hour.
Probabilities:
p: Probability an applicant used ACS.
q: Probability of application approval in Case Review.
r: Probability of application approval after the Interview.
Number of applicants (K): Total number of applicants simulated.
Simulation time (T): Total hours the SPF offices are open (9 AM to 5 PM = 8 hours).
