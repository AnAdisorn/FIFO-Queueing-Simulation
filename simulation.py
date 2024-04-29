# %%
import numpy as np
from numpy.random import uniform, exponential

import matplotlib.pyplot as plt


# %%
def main(K, lam, muf, muc, muw, p, q, r, T):
    """
    Simulates the Solar Panel Funding (SPF) application processing system
    for a specified number of applicants.

    Args:
        K (int): Number of applicants to simulate.
        lam (float): Arrival rate of applicants (per hour - Poisson process).
        muf (float): Service rate of Fingerprint server (per hour).
        muc (float): Service rate of Case Review server (per hour).
        muw (float): Service rate of Interview server (per hour).
        p (float): Probability of applicant using Application Checking Service (ACS).
        q (float): Probability of application approval in Case Review.
        r (float): Probability of application approval after Interview.
        T (float): Total simulation time (hours - SPF office hours).

    Returns:
        dict: Dictionary containing processing times for all (Ta),
              completed (Tc), and rejected (Tr) applications.
    """
    Times = {
        "c": [],  # times spent in office by completed application
        "r": [],  # times spent in office by rejected application
    }
    for _ in range(K):
        t_prev = 0
        applicant_arrival_times = poisson_process(lam, T)
        applicant_arrival_times.append(float("inf"))  # the last one is never arrive
        Servers = {
            "F": [],
            "C": [],
            "W": [],
        }
        for t in applicant_arrival_times:
            # calculate time until this applicant arrive relative to previus applicant
            time_till_applicant = t - t_prev

            # find process that require minimum time to process (FIFO)
            # including time_till_applicate
            while True:
                time_min_name = "time_till_applicant"
                time_min = time_till_applicant
                for name in Servers:
                    if Servers[name]:  # if list not empty
                        time_spent = Servers[name][0]["stages"][0][1]
                        if time_spent < time_min:
                            time_min_name = name
                            time_min = time_spent

                if time_min_name == "time_till_applicant":
                    break
                else:
                    time_spent = Servers[time_min_name][0]["stages"][0][1]
                    time_till_applicant -= time_spent
                    for name in Servers:
                        for i in range(len(Servers[name])):
                            Servers[name][i]["time_spent_total"] += time_spent
                            if i == 0:  # active applicant
                                Servers[name][i]["stages"][0][1] -= time_spent
                    Servers[time_min_name][0]["stages"].pop(
                        0
                    )  # complete this stage, pop off
                    applicant = Servers[time_min_name].pop(
                        0
                    )  # pop the applicant off the Server (done with whis Server)
                    if applicant["stages"]:  # still has more stages to go
                        Servers[applicant["stages"][0][0]].append(
                            applicant
                        )  # move applicant to the next stage
                    else:  # applicant complete every stages
                        if applicant["rejection"]:  # is rejected
                            Times["r"].append(applicant["time_spent_total"])
                        else:  # is completed
                            Times["c"].append(applicant["time_spent_total"])

            applicant = process_application(muf, muc, muw, p, q, r)
            Servers[applicant["stages"][0][0]].append(applicant)

            t_prev = t

    return Times


def poisson_process(lam, T):
    """
    Simulate a Poisson process with rate lambda for a time period T.

    Args:
        lam (float): The rate of the Poisson process.
        T (float): The time period to simulate.

    Returns:
        times (list): List of event times.
    """
    times = []
    t = 0.0  # start time
    while t < T:
        u = uniform()  # random unform [0,1]
        dt = -np.log(u) / lam  # time to get one event
        t += dt  # current time
        if t < T:  # if event happens before time limit
            times.append(t)

    return times


def process_application(muf, muc, muw, p, q, r):
    """
    Simulates the processing stages for a single application.

    Args:
        muf (float): Service rate of Fingerprint server (per hour).
        muc (float): Service rate of Case Review server (per hour).
        muw (float): Service rate of Interview server (per hour).
        p (float): Probability of applicant using Application Checking Service (ACS).
        q (float): Probability of application approval in Case Review.
        r (float): Probability of application approval after Interview.

    Returns:
        dict: Dictionary containing information about the processed application:
            stages (list): List of stages the application went through with time spent at each stage.
                Each element is a list containing server name and service time.
            rejection (bool): True if the application was rejected, False otherwise.
            time_spent_total (float): Total time spent by the applicant in the SPF office.
    """
    stages = []
    rejection = False
    if uniform() < p:  # ACS is used, sent to Sf
        stages.append(["F", exponential(1 / muf)])
    else:  # ACS is not used, sent to Sc
        stages.append(["C", exponential(1 / muc)])
        if uniform() < q:  # satisfied with application, sent to Sf
            stages.append(["F", exponential(1 / muf)])
        else:  # not satisfied with application, sent to Sw
            stages.append(["W", exponential(1 / muw)])
            if uniform() < r:  # satisfied with interview, sent to Sf
                stages.append(["F", exponential(1 / muf)])
            else:  # reject the application
                rejection = True
    return {"stages": stages, "rejection": rejection, "time_spent_total": 0.0}


# %%
if __name__ == "__main__":
    """
    This block is executed only when the script is run directly (not imported as a module).
    """

    # Define simulation parameters
    K = 500  # Number of applicants to simulate
    lam = 8  # Arrival rate of applicants (per hour)
    muf = 6  # Service rate of Fingerprint server (per hour)
    muc = 5  # Service rate of Case Review server (per hour)
    muw = 4  # Service rate of Interview server (per hour)
    p = 0.5  # Probability of applicant using ACS
    q = 0.6  # Probability of application approval in Case Review
    r = 0.4  # Probability of application approval after Interview
    T = 17 - 9  # Simulation time (hours - SPF office hours)

    # Simulate the application processing system
    Times = main(K=K, lam=lam, muf=muf, muc=muc, muw=muw, p=p, q=q, r=r, T=T)

    # Calculate total processing time (applicant)
    Times["a"] = Times["c"] + Times["r"]  # Combine completed and rejected times

    # Print average processing times
    print(f"E[Ta] = {np.mean(Times['a'])}")  # Average total processing time
    print(f"E[Tc] = {np.mean(Times['c'])}")  # Average completed processing time
    print(f"E[Tr] = {np.mean(Times['r'])}")  # Average rejected processing time

    # Plot histograms for processing times
    fig, axes = plt.subplots(3)
    for i, name in enumerate(["a", "c", "r"]):
        axes[i].hist(Times[name], bins=np.linspace(0, 15, 100), density=True)
        axes[i].set_xlabel(f"T{name}")  # Label for each histogram (total, completed, rejected)
        axes[i].set_ylabel(f'{name}')

    plt.subplots_adjust(hspace=1)  # Adjust spacing between subplots
    plt.show()


# %%
