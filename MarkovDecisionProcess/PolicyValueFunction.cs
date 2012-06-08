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

        private Dictionary<int, Dictionary<State, double>> ViByS;
        private Dictionary<State, Action> ViBySActions;

        public PolicyValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<int, Dictionary<State, double>>();
            ViBySActions = new Dictionary<State, Action>();
        }

        public double ValueAt(State s)
        {
            //your code here
            return ViByS[ViByS.Count][s];
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
            ValueFunction v = new ValueFunction(m_dDomain);
            TimeSpan t;
            int up;
            v.ValueIteration(dEpsilon, out up,out  t);
            double maxDelta = Double.MinValue , delta;
            int i = 0;
            do
            {
                i++;
                Dictionary<State, double> Vi = new Dictionary<State, double>();
                ViByS.Add(i, Vi);
                foreach (State s in m_dDomain.States)
                {
                    delta = update(s,i,v);
                    cUpdates++;
                    if (maxDelta < delta)
                        maxDelta = delta;
                }
            } while (maxDelta < dEpsilon);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished policy iteration");
        }

        private double update(State s, int i,ValueFunction v)
        {
            ViByS[i].Add(s, Double.MinValue);
            foreach (Action a in m_dDomain.Actions)
            {
                double sum = 0;
                foreach (State stag in s.Successors(a))
                    sum += s.TransitionProbability(a, stag) * ViByS[i - 1][stag];
                double tmp = s.Reward(v.GetAction(s)) + (m_dDomain.DiscountFactor * sum);

               // save max
                if(ViByS[i][s] < tmp)
                {
                    ViByS[i][s] = tmp;
                    ViBySActions[s] = a;
                }
            }
            
            return Math.Abs(ViByS[i][s] - ViByS[i - 1][s]);
        }

        // init all V0(s) to 0
        private void initV0()
        {
            Dictionary<State, double> tmpD = new Dictionary<State, double>();
            foreach (State s in m_dDomain.States)
            {
                tmpD.Add(s, 0.0);
                ViBySActions.Add(s, null);
            }
            ViByS.Add(0, tmpD);
        }

    }   
}
