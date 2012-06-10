﻿using System;
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

        public void LearningQ(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting learning-q");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;
            Application.DoEvents();
            
            //your code here
            initV0();
            initQ();
            
            State s = m_dDomain.StartState , stag;
            Action chosenA = null;
            do
            {
                chosenA = findMaxQA(s);
                double r = s.Reward(chosenA);
                stag = s.Apply(chosenA);
                Q[s][chosenA] = (1-dEpsilon)*Q[s][chosenA] + dEpsilon*(r + m_dDomain.DiscountFactor *Q[stag][findMaxQA(stag)] - Q[s][chosenA]);
                s = stag;
            } while (!m_dDomain.IsGoalState(s));
             
            foreach (State ss in m_dDomain.States)
                ViBySActions[ss] = findMaxQA(ss);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished learning-q");
        }

        private void initQ()
        {
            foreach (State s in m_dDomain.States)
            {
                Dictionary<Action, double> d = new Dictionary<Action, double>();
                foreach (Action a in m_dDomain.Actions)
                    d.Add(a, double.MinValue);
                Q.Add(s, d);
            }
        }

        private Action findMaxQA(State j)
        {
            List<Action> actions = new List<Action>();
            double maxQA = double.MinValue;
            foreach (Action a in m_dDomain.Actions)
                if (Q[j][a] >= maxQA)
                    maxQA = Q[j][a];
            foreach (Action a in m_dDomain.Actions)
                if (Q[j][a] == maxQA)
                    actions.Add(a);
            int idx = RandomGenerator.Next(actions.Count);
            return actions[idx];
        }

        public void Sarsa(double dEpsilon, out int cUpdates, out TimeSpan tsExecutionTime)
        {
            Debug.WriteLine("Starting SARSA");
            DateTime dtBefore = DateTime.Now;
            cUpdates = 0;
            Application.DoEvents();
            
            //your code here
            initV0();
            initQ();
            State s = m_dDomain.StartState, stag;
            Action a = findMaxQA(s) , atag;
            do
            {
                double r = s.Reward(a);
                stag = s.Apply(a);
                atag = findMaxQA(stag);
                Q[s][a] = (1-dEpsilon)*Q[s][a] + dEpsilon*(r + m_dDomain.DiscountFactor*Q[stag][atag] - Q[s][a]);
                s = stag;
                a = atag;
            } while (!m_dDomain.IsGoalState(s));

            foreach (State ss in m_dDomain.States)
                ViBySActions[ss] = findMaxQA(ss);

            tsExecutionTime = DateTime.Now - dtBefore;
            Debug.WriteLine("\nFinished SARSA");
        }

    }
}