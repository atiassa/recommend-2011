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
            double sumRewards = 0.0;
            for(int j=0; j<cTrials; j++){
                sumRewards += CompOneExperimant(p, cStepsPerTrial);
            }
            dSumRewards = (1.0 / cTrials) * sumRewards;

            Debug.WriteLine("\nDone computing ADR");
            return dSumRewards;
        }

        private double CompOneExperimant(Policy p, int cStepsPerTrial)
        {
            State s = StartState;
            double r = 0;
            int i = 0;
            while (!IsGoalState(s) && i <= cStepsPerTrial)
            {
                Action a = p.GetAction(s);
                r += Math.Pow(DiscountFactor, i) * s.Reward(a);
                i++;
                foreach (State stag in States)
                    if (s.TransitionProbability(a, stag) != 0)
                        s = stag;
            }
            return r;
        }
		
		
    }
}
