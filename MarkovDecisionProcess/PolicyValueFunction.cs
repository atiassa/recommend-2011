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
        private Dictionary<State, Action> ViBySActions;

        public PolicyValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<State, double>();
            ViBySActions = new Dictionary<State, Action>();
        }

        public double ValueAt(State s)
        {
            //your code here
            return ViByS[s];
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
            double maxDelta, delta;
            initV0();
            RandomPolicy rp = new RandomPolicy(m_dDomain);
            foreach (State s in m_dDomain.States)
                ViBySActions.Add(s, rp.GetAction(s));
            do
            {
                maxDelta = Double.MinValue;
                foreach (State s in m_dDomain.States)
                {
                    delta = update(s);
                    cUpdates++;
                    maxDelta = Math.Max(delta, maxDelta);
                }
               // Console.WriteLine(maxDelta);
            } while (maxDelta >= dEpsilon);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished policy iteration");
        }

        private double update(State s)
        {
            double maxV = ViByS[s];
            Action maxA = null;
            foreach (Action a in m_dDomain.Actions)
            {
                double sum = 0;
                foreach (State stag in s.Successors(a))
                    sum += s.TransitionProbability(a, stag) * ViByS[stag];
                double tmp = s.Reward(a) + (m_dDomain.DiscountFactor * sum);

               // save max
                if ((tmp >= maxV) && (!s.Apply(a).Equals(s)))
                {
                    maxV = tmp;
                    maxA = a;
                }
            }
            if (maxA != null)
            {
                double delta = maxV - ViByS[s];
                ViByS[s] = maxV;
                ViBySActions[s] = maxA;
                return Math.Abs(delta);
            }
            return 0;
        }

        // init all V0(s) to 0
        private void initV0()
        {
            foreach (State s in m_dDomain.States)
                ViByS.Add(s, 0);
        }    
    }
}
