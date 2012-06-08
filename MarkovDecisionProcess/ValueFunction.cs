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

        private Dictionary<State, double> ViByS;
        private Dictionary<State, double> Vi_1ByS;
        private Dictionary<State, Action> ViBySActions;

        public ValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<State, double>();
            Vi_1ByS = new Dictionary<State, double>();
            ViBySActions = new  Dictionary<State, Action>();
        }

        // init all V0(s) to 0
        private void initV0()
        {
            foreach (State s in m_dDomain.States)
            {
                ViByS.Add(s, 0.0);
                Vi_1ByS.Add(s, 0);
                ViBySActions.Add(s, null);
            }
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
                foreach (State s in m_dDomain.States)
                {
                    update(i,s);
                    cUpdates++;
                    if (stop && Math.Abs(Vi_1ByS[s] - ViByS[s]) > dEpsilon)
                        stop = false;
                }
                ViByS = new Dictionary<State,double>(Vi_1ByS);
            } while (!stop);

            updatePI();
            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished value iteration");
        }

        // calc the formula for Vi+1(s)
        private void update(int i, State s)
        {
            bool first = true;
            foreach (Action a in m_dDomain.Actions)
            {
                if (i == 1)
                {
                    Vi_1ByS[s] = s.Reward(a);
                    continue;
                }
                
                // clac formula for action a
                double sum = 0;
                foreach (State stag in s.Successors(a))
                        sum += s.TransitionProbability(a, stag) * ViByS[stag]; 
                double tmp = s.Reward(a) + m_dDomain.DiscountFactor * sum;

                // save max
                if (first)
                {
                    Vi_1ByS[s] = tmp;
                    first = false;
                }
                else Vi_1ByS[s] = Math.Max(tmp, ViByS[s]);
            }
        }

        private void updatePI()
        {
            foreach (State s in m_dDomain.States)
            {
                bool first = true;
                double max = 0;
                foreach (Action a in m_dDomain.Actions)
                {
                    // clac formula for action a
                    double sum = 0;
                    foreach (State stag in s.Successors(a))
                        sum += s.TransitionProbability(a, stag) * Vi_1ByS[stag];
                    double tmp = s.Reward(a) + m_dDomain.DiscountFactor * sum;

                    // save max
                    if (first)
                    {
                        max = tmp;
                        ViBySActions[s] = a;
                        first = false;
                    }
                    else if (max < tmp)
                    {
                        max =  tmp;
                        ViBySActions[s] = a;
                    }
                }
            }
        }

        public void LearningQ(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting learning-q");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;
            Application.DoEvents();
            //your code here
            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished learning-q");
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
