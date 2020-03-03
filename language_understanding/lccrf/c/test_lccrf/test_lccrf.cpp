#include "stdafx.h"
#include "CppUnitTest.h"
#include <memory>
#include <iostream>
#define private public
#include "../lib_lccrf/FWBW.h"
#include "../lib_lccrf/LCCRF.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;


namespace test_lccrf
{		
	TEST_CLASS(TestFWBW)
	{
	public:

		static void MakeDocument(X& x, Y& y, LCCRFFeatures& lccrfFeatures)
		{
			x.AddFeature(0, 0);
			x.AddFeature(1, 1);

			y.SetTag(0, 0);
			y.SetTag(1, 1);

			lccrfFeatures.AddSample(x, y);
		}

		static void PrintMatrix(MultiArray<double, 2>& alphaMatrix)
		{
			for (int i = 0; i < alphaMatrix.Dim1(); i++)
			{
				for (int j = 0; j < alphaMatrix.Dim2(); j++)
				{
					std::cout << alphaMatrix[i][j] << "\t";
				}
				std::cout << std::endl;
			}
		}
	
		TEST_METHOD(TestCalc)
		{
			static X x(2);
			static Y y(2);
			LCCRFFeatures lccrfFeatures;

			MakeDocument(x, y, lccrfFeatures);
			std::vector<double> weights(3, 1.0);
			FWBW fwbw(x, y, lccrfFeatures, weights);

			PrintMatrix(fwbw._alphaMatrix);
			Assert::AreEqual(fwbw._alphaMatrix.Dim1(), 2);
			Assert::AreEqual(fwbw._alphaMatrix.Dim2(), 2);

			// alpha matrix.
			Assert::AreEqual(0.731058, fwbw._alphaMatrix[0][0], 1e-4);
			Assert::AreEqual(0.268941, fwbw._alphaMatrix[0][1], 1e-4);
			Assert::AreEqual(0.140195, fwbw._alphaMatrix[1][0], 1e-4);
			Assert::AreEqual(0.859804, fwbw._alphaMatrix[1][1], 1e-4);

			Assert::AreEqual(3.718281, fwbw._alphaScales[0], 1e-4);
			Assert::AreEqual(7.132891, fwbw._alphaScales[1], 1e-4);

			PrintMatrix(fwbw._betaMatrix);
			Assert::AreEqual(fwbw._betaMatrix.Dim1(), 2);
			Assert::AreEqual(fwbw._betaMatrix.Dim2(), 2);

			// beta matrix.
			Assert::AreEqual(0.859804, fwbw._betaMatrix[0][0], 1e-4);
			Assert::AreEqual(0.140195, fwbw._betaMatrix[0][1], 1e-4);
			Assert::AreEqual(0.268941, fwbw._betaMatrix[1][0], 1e-4);
			Assert::AreEqual(0.731058, fwbw._betaMatrix[1][1], 1e-4);

			Assert::AreEqual(7.132891, fwbw._betaScales[0], 1e-4);
			Assert::AreEqual(3.718281, fwbw._betaScales[1], 1e-4);
		}
	};

	TEST_CLASS(TestLCCRF)
	{
	public:
		void MakeDocument(vector<X>& xs, vector<Y>& ys, LCCRFFeatures& lccrfFeatures)
		{
			X x(2);
			x.AddFeature(0, 0);
			x.AddFeature(1, 1);

			xs.push_back(x);

			Y y(2);
			y.SetTag(0, 0);
			y.SetTag(1, 1);

			ys.push_back(y);

			lccrfFeatures.AddSample(x, y);
		}

		TEST_METHOD(TestPredict)
		{
			vector<X> xs;
			vector<Y> ys;
			LCCRFFeatures lccrfFeatures;

			MakeDocument(xs, ys, lccrfFeatures);
			LCCRF lccrf;

			// fit
			lccrf.Fit(xs, ys, 1000, 0.1, 0.1);
			Assert::AreEqual(0.76578, lccrf._weights[0], 1e-4);
			Assert::AreEqual(0.76578, lccrf._weights[1], 1e-4);
			Assert::AreEqual(1.7396, lccrf._weights[2], 1e-4);
			string weightsFile = "./lccrf.weights.txt";
			lccrf.Save(weightsFile);

			// check likelihood, without regularization.
			FWBW fwbw(xs.front(), ys.front(), lccrfFeatures, lccrf._weights);
			double likehoold = fwbw.CalcLikelihood(xs.front(), ys.front());
			Assert::AreEqual(-0.18334, likehoold, 1e-4);

			// predit
			Y res = lccrf.Predict(xs.front());
			Assert::AreEqual(res.Tags[0], 0);
			Assert::AreEqual(res.Tags[1], 1);
		}
	};


	TEST_CLASS(TestLoadWeights)
	{
	public:
		TEST_METHOD(TestLoad)
		{
			LCCRF lccrf;
			lccrf.Load("D:\\Bitbucket\\work\\devbox\\language_understanding\\scenario\\movie\\slot_output\\model\\lccrf.weights.txt");
			X x(6);
			x.AddFeature(48,2);
			x.AddFeature(59, 3);
			x.AddFeature(61, 1);
			x.AddFeature(64, 4);
			x.AddFeature(66, 0);
			Y y = lccrf.Predict(x);
		}
	};
}