﻿﻿using System;
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
        private Dictionary<State ,Dictionary<Action, double>> Q;

        public ValueFunction(Domain d)
        {
            //your code here
            m_dDomain = d;
            MaxValue = 0.0;
            MinValue = 0.0;

            ViByS = new Dictionary<State, double>();
            Vi_1ByS = new Dictionary<State, double>();
            ViBySActions = new Dictionary<State, Action>();

            Q = new Dictionary<State, Dictionary<Action, double>>();
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
            double delta, maxDelta;
            do
            {
                maxDelta = Double.MinValue;
                foreach (State s in m_dDomain.States)
                {
                    delta = updateValueIter(s);
                    cUpdates++;
                    maxDelta = Math.Max(delta, maxDelta);
                }
               // Console.WriteLine(maxDelta);
                ViByS = new Dictionary<State, double>(Vi_1ByS);
            } while (maxDelta >= dEpsilon);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished value iteration");
        }

        // calc the formula for Vi+1(s)
        private double updateValueIter(State s)
        {
            double maxV = Double.MinValue;
            Action maxA = null;
            foreach (Action a in m_dDomain.Actions)
            {
                // clac formula for action a
                double sum = 0;
                foreach (State stag in s.Successors(a))
                    sum += s.TransitionProbability(a, stag) * ViByS[stag];
                double tmp = s.Reward(a) + m_dDomain.DiscountFactor * sum;
                // save max
                if((tmp >= maxV)){
                    maxV = tmp;
                    maxA = a;
                }
            }
            if (maxA != null)
            {
                Vi_1ByS[s] = maxV;
                ViBySActions[s] = maxA;
                return Math.Abs(Vi_1ByS[s] - ViByS[s]);
            }
            return 0;
        }

        public double LearningQ(double dEpsilon, int cTrials, int cStepsPerTrial)
        {
            double dSumRewards = 0.0;
            
            //your code here
            initV0();
            initQ();
            for (int j = 0; j < cTrials; j++)
            {
                double alpha = 0.7;
                State s = m_dDomain.StartState, stag;
                int t = 1;
                while (!m_dDomain.IsGoalState(s) && t <= cStepsPerTrial)
                {
                    Action a = epsilonGreedy(s, dEpsilon);
                    double r = s.Reward(a);
                    dSumRewards += r;
                    stag = s.Apply(a);
                    Q[s][a] =  Q[s][a] + alpha * (r + m_dDomain.DiscountFactor * MaxR(stag) - Q[s][a]);
                    s = stag;
                    t++;
                   // alpha = alpha /t;
                }

            }
            foreach (State ss in m_dDomain.States)
                ViBySActions[ss] = findMaxQA(ss);

            Debug.WriteLine("\nDone computing ADR");
            return dSumRewards;
        }

        private double MaxR(State stag)
        {
            double maxR = double.MinValue;
            foreach (Action a in m_dDomain.Actions)
                maxR = Math.Max(maxR,Q[stag][a] );
            return maxR;
        }

        private void initQ()
        {
            foreach (State s in m_dDomain.States)
            {
                Q.Add(s, new Dictionary<Action, double>());
                foreach (Action a in m_dDomain.Actions)
                    Q[s].Add(a, 0);
            }
        }

        private Action findMaxQA(State j)
        {
            List<Action> actions = new List<Action>();
            double maxQA = double.MinValue;
            foreach (Action a in m_dDomain.Actions)
                if (Q[j][a] > maxQA)
                    maxQA = Q[j][a];
            foreach (Action a in m_dDomain.Actions)
                if (Q[j][a] == maxQA)
                    actions.Add(a);
            int idx = RandomGenerator.Next(actions.Count);
            return actions[idx];
        }

        private Action epsilonGreedy(State s,double depsilon)
        {
            if ( RandomGenerator.NextDouble() > depsilon)
                return m_dDomain.Actions.ElementAt(RandomGenerator.Next(m_dDomain.Actions.Count()));
            else
                return findMaxQA(s);
        }

        public double Sarsa(double dEpsilon, int cTrials, int cStepsPerTrial)
        {
            double dSumRewards = 0.0;
            //your code here
            initV0();
            initQ();
            for (int j = 0; j < cTrials; j++)
            {
                State s = m_dDomain.StartState, stag;
                Action a = epsilonGreedy(s, dEpsilon);
                double alpha = 0.7;
                int t = 1;
                while (!m_dDomain.IsGoalState(s) && t <= cStepsPerTrial)
                {
                    double r = s.Reward(a);
                    dSumRewards += r;
                    stag = s.Apply(a);
                    Action atag = epsilonGreedy(stag,dEpsilon);
                    Q[s][a] = Q[s][a] + alpha * (r + m_dDomain.DiscountFactor * Q[stag][atag] - Q[s][a]);
                    s = stag;
                    a = atag;
                    t++;
                    // alpha = alpha /t;
                }

            }
            foreach (State ss in m_dDomain.States)
                ViBySActions[ss] = findMaxQA(ss);

            Debug.WriteLine("\nDone computing ADR");
            return dSumRewards;
        }

    }
}