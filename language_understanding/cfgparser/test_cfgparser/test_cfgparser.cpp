#include "stdafx.h"
#include "CppUnitTest.h"
#include "../cfgparser/CFGParser.h"

using namespace Microsoft::VisualStudio::CppUnitTestFramework;

namespace test_cfgparser
{		
	TEST_CLASS(TestCFGParser)
	{
	public:
		
		TEST_METHOD(TestMatch)
		{
			CFGParser parser;
			parser.LoadXml("../../test_cfgparser/cfg.xml");
			string query = "thursday september   8 2016";
			vector<string> tokenizeQuery = split(query);
			auto ret = parser.Parse(tokenizeQuery);
			
			Assert::AreEqual((int)ret.size(), 3);
			Assert::AreEqual(ret["MonthDay"][0].first, 1);
			Assert::AreEqual(ret["MonthDay"][0].second, 3);
			Assert::AreEqual(ret["YearMonthDay"][0].first, 0);
			Assert::AreEqual(ret["YearMonthDay"][0].second, 4);
			Assert::AreEqual(ret["Lexicon_Date"][0].first, 2);
			Assert::AreEqual(ret["Lexicon_Date"][0].second, 4);
		}
	};
}