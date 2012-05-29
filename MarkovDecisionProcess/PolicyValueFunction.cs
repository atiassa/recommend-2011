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

        public PolicyValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;
        }

        public double ValueAt(State s)
        {
            //your code here
            return 0.0;
        }


        public override Action GetAction(State s)
        {
            //your code here
            return null;
        }

        public void PolicyIteration(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting policy iteration");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;

            //your code here
            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished policy iteration");
        }

    }
}
