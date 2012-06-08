using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Threading;
using System.Windows.Forms;

namespace MarkovDecisionProcess
{
    class PolicyValueFunction : Policy
    {

        //more data structures here
        private Domain m_dDomain;
        public double MaxValue { get; private set; }
        public double MinValue { get; private set; }

        private Dictionary<State, double> ViByS;
        private Dictionary<State, double> Vi_1ByS;
        private Dictionary<State, Action> ViBySActions;

        public PolicyValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<State, double>();
            Vi_1ByS = new Dictionary<State, double>();
            ViBySActions = new Dictionary<State, Action>();
        }

        public double ValueAt(State s)
        {
            //your code here
            return Vi_1ByS[s];
        }


        public override Action GetAction(State s)
        {
            //your code here
            return ViBySActions[s];
        }

        public void PolicyIteration(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting policy iteration");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;

            //your code here
            initV0();
            //ValueFunction rp = new ValueFunction(m_dDomain);
            //TimeSpan t;
            //int up;
            //rp.ValueIteration(dEpsilon, out up, out  t);
            RandomPolicy rp = new RandomPolicy(m_dDomain);
            double maxDelta = Double.MinValue, delta;
            int i = 0;
            do
            {
                i++;
                foreach (State s in m_dDomain.States)
                {
                    delta = update(s, i, rp);
                    cUpdates++;
                    maxDelta = Math.Max(delta, maxDelta);
                }
                ViByS = new Dictionary<State, double>(Vi_1ByS);
            } while (maxDelta >= dEpsilon);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished policy iteration");
        }

        private double update(State s, int i, Policy v)
        {
            bool first = true;
            foreach (Action a in m_dDomain.Actions)
            {
                if (i == 1)
                {
                    Vi_1ByS[s] = s.Reward(v.GetAction(s));
                    ViBySActions[s] = a;
                    continue;
                }
                double sum = 0;
                foreach (State stag in s.Successors(a))
                    sum += s.TransitionProbability(a, stag) * ViByS[stag];
                double tmp = s.Reward(v.GetAction(s)) + (m_dDomain.DiscountFactor * sum);

                // save max
                if (first)
                {
                    Vi_1ByS[s] = tmp;
                    ViBySActions[s] = a;
                    first = false;
                }
                else if (Vi_1ByS[s] < tmp)
                {
                    Vi_1ByS[s] = tmp;
                    ViBySActions[s] = a;
                }
            }

            return Math.Abs(Vi_1ByS[s] - ViByS[s]);
        }

        // init all V0(s) to 0
        private void initV0()
        {
            foreach (State s in m_dDomain.States)
            {
                ViByS.Add(s, 0);
                Vi_1ByS.Add(s, 0);
                ViBySActions.Add(s, null);
            }
        }
    }
}
