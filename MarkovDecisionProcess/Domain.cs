using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;

namespace MarkovDecisionProcess
{
    abstract class Domain
    {
        public abstract IEnumerable<State> States { get; }
        public abstract IEnumerable<Action> Actions { get; }
        public abstract double MaxReward { get; }
        public abstract State StartState{ get; }
        public abstract bool IsGoalState(State s);
        public double DiscountFactor { get; protected set; }
        public double ComputeAverageDiscountedReward(Policy p, int cTrials, int cStepsPerTrial)
        {
            Debug.WriteLine("Started computing ADR");
            double dSumRewards = 0.0;
            //your code here
            Debug.WriteLine("\nDone computing ADR");
            return dSumRewards;
        }
		
		
    }
}
