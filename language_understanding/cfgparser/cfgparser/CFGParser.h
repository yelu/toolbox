#pragma once

#include "NodeMatcher.h"

class Match
{
public:
	struct Comparator
	{
		bool operator()(const pair<int, int>& m1, const pair<int, int>& m2) const
		{
			if (m1.first != m2.first)
				return m1.first < m2.first;
			else
				return m1.second < m2.second;
		}
	};
};

class CFGParser
{
public:
	CFGParser() {}

	void LoadXml(const string& path);

	// print all [start, end) that match a compelte rule.
	map<string, vector<pair<int, int>>> Parse(const vector<string>& tokenizedQuery, bool merge = true);

	// get all dependent files of this cfg grammar file.
	vector<string> GetDependentFiles() { return _dependentFiles; }

	shared_ptr<NodeMatcher> _GenMatcherFromNode(const xml_node<>* node);

private:
	map<string, Rule> _rules;
	map<string, Rule> _publicRules;
	string _cfgFile;
	vector<string> _dependentFiles;
};

