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
        private Dictionary<State, Dictionary<State, Dictionary<Action, double>>> sums;

        public ValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<int, Dictionary<State, double>>();
            initV0();
            sums = new Dictionary<State, Dictionary<State, Dictionary<Action, double>>>();
        }

        // init all V0(s) to 0
        private void initV0()
        {
            Dictionary<State, double> tmpD = new Dictionary<State, double>();
            foreach (State s in m_dDomain.States)
                tmpD.Add(s, 0.0);
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

            return null;
        }

        public void ValueIteration(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting value iteration");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;

            //your code here
            bool stop = true;
            int i = 0;
            do
            {
                Console.WriteLine("cupdates = " + cUpdates);
                stop = true;
                i++;
                Dictionary<State, double> Vi = new Dictionary<State, double>();
                ViByS.Add(i, Vi);
                foreach (State s in m_dDomain.States)
                {
                    ViByS[i].Add(s,calcMaxVal(i,s));
                    if (stop && Math.Abs(ViByS[i][s] - ViByS[i-1][s]) > dEpsilon)
                        stop = false;
                    cUpdates++;
                }
            } while (!stop);
            Console.WriteLine("Finished value iteration");

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished value iteration");
        }

        // calc the formula for Vi(s)
        private double calcMaxVal(int i,State s)
        {
            bool first = true;
            double max = 0;
            double tmp, sum,sss;
            foreach (Action a in m_dDomain.Actions)
            {
                // clac formula for action a
                if (i == 1)
                    tmp = s.Reward(a);
                else
                {
                    sum = 0;
                    foreach (State stag in m_dDomain.States)
                    {
                        //if ((sss = getSum(s, a, stag)) == 0)
                        //{   
                        //    sss = s.TransitionProbability(a, stag);
                        //    setSum(s, a,stag, sss);
                        //    s.TransitionProbability(a, stag);
                        //}
                        //sum +=  sss * ViByS[i-1][stag];
                        sum += s.TransitionProbability(a, stag) *ViByS[i - 1][stag]; 
                    }
                    tmp = s.Reward(a) + m_dDomain.DiscountFactor * sum;
                }

                // save max
                if (first)
                {
                    max = tmp;
                    first = false;
                }
                else max = Math.Max(max, tmp); 
            }
            return max;
        }

        private void setSum(State s, Action a, State stag, double sum)
        {
            if (sums.ContainsKey(stag))
            {
                if (sums[stag].ContainsKey(s))
                {
                    if (!sums[stag][s].ContainsKey(a))
                        sums[stag][s].Add(a, sum);
                    else if (sums[stag][s][a] != sum)
                            Console.WriteLine("not good");
                }
                else
                {
                    Dictionary<Action, double> sa = new Dictionary<Action, double>();
                    sa.Add(a, sum);
                    sums[stag].Add(s, sa);
                }
            }
            else
            {
                Dictionary<State, Dictionary<Action, double>> iss = new Dictionary<State,Dictionary<Action,double>>();
                Dictionary<Action, double> sa = new Dictionary<Action, double>();
                sa.Add(a,sum);
                iss.Add(s,sa);
                sums.Add(stag, iss);
            }
        }

        private double getSum(State s, Action a, State stag)
        {
            if (sums.ContainsKey(stag))
                if (sums[stag].ContainsKey(s))
                    if (sums[stag][s].ContainsKey(a))
                        return sums[stag][s][a];
            return 0;
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
