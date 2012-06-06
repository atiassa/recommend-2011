using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Diagnostics;
using System.Threading;
using System.Windows.Forms;

namespace MarkovDecisionProcess
{
    class ValueFunction : Policy
    {

        //more data structures here
        private Domain m_dDomain;
        public double MaxValue { get; private set; }
        public double MinValue { get; private set; }

        private Dictionary<int, Dictionary<State, double>> ViByS;
        private Dictionary<State, Action> ViBySActions;

        public ValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<int, Dictionary<State, double>>();
            ViBySActions = new  Dictionary<State, Action>();
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

        public void ValueIteration(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting value iteration");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;

            //your code here
            initV0();

            bool stop = true;
            int i = 0;
            do
            {
                stop = true;
                i++;
                Dictionary<State, double> Vi = new Dictionary<State, double>();
                ViByS.Add(i, Vi);
                foreach (State s in m_dDomain.States)
                {
                    update(i,s);
                    cUpdates++;
                    if (stop && Math.Abs(ViByS[i][s] - ViByS[i-1][s]) > dEpsilon)
                        stop = false;
                }
            } while (!stop);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished value iteration");
        }

        // calc the formula for Vi(s)
        private void update(int i,State s)
        {
            bool first = true;
            ViByS[i].Add(s, 0);
            foreach (Action a in m_dDomain.Actions)
            {
                // clac formula for action a
                double sum = 0;
                if (i != 1)
                {
                    foreach (State stag in s.Successors(a))
                         sum += s.TransitionProbability(a, stag) *ViByS[i-1][stag]; 
                }
                double tmp = s.Reward(a) + m_dDomain.DiscountFactor * sum;

                // save max
                if (first)
                {
                    ViByS[i][s] = tmp;
                    ViBySActions[s] = a;
                    first = false;
                }
                else if(ViByS[i][s] < tmp)
                {
                    ViByS[i][s] = Math.Max(ViByS[i][s], tmp);
                    ViBySActions[s] = a;
                }
            }
        }

     
		
	    public void Sarsa(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting SARSA");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;
            Application.DoEvents();
            //your code here
            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished SARSA");
        }

    }
}
