#pragma once
#include <fstream>
#include <algorithm>
#include <string>
#include <vector>
#include <memory>
#include <map>
#include <set>
#include <list>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <regex>
#include <stdexcept>
#include "Str.h"
#include "RapidXml/rapidxml.hpp"
using std::wstring;
using std::vector;
using std::set;
using std::map;
using std::list;
using std::tuple;
using std::pair;
using std::string;
using std::unordered_map;
using std::unordered_set;
using std::shared_ptr;
using std::regex;
using namespace rapidxml;

class NodeMatcher
{
public:
	virtual set<int> Match(const std::vector<string>& tokenizedQuery, int start) = 0;
	virtual void Aggregate(shared_ptr<NodeMatcher> childMatcher) {};
};

class Rule
{
public:
	Rule()
	{
		IsPublic = true;
	}
	shared_ptr<NodeMatcher> Matcher;
	bool IsPublic;
	string Name;
};

class StringNodeMatcher : public NodeMatcher
{
public:
	StringNodeMatcher(const char* str)
	{
		string content(str);
		_tokenizedItem = split(content);
		if (_tokenizedItem.size() == 0)
		{
			string msg("Empty string is not allowed");
			throw std::runtime_error(msg.c_str());
		}
	}

	set<int> Match(const std::vector<string>& tokenizedQuery, int start);
private:
	vector<string> _tokenizedItem;
};

class RegexNodeMatcher : public NodeMatcher
{
public:
	RegexNodeMatcher(const char* str) :_regex(str)
	{
	}

	set<int> Match(const std::vector<string>& tokenizedQuery, int start);
private:
	regex _regex;
};

class SequenceNodeMatcher : public NodeMatcher
{
public:
	SequenceNodeMatcher()
	{

	}

	void Aggregate(shared_ptr<NodeMatcher> childMatcher)
	{
		_matchers.push_back(childMatcher);
	}

	set<int> Match(const std::vector<string>& tokenizedQuery, int start);
private:
	vector<shared_ptr<NodeMatcher>> _matchers;

	set<int> _Match(const std::vector<string>& tokenizedQuery,
		int qStart,
		int mStart);
};

class OneOfNodeMatcher : public NodeMatcher
{
public:
	OneOfNodeMatcher()
	{

	}

	void Aggregate(shared_ptr<NodeMatcher> childMatcher)
	{
		_matchers.push_back(childMatcher);
	}

	set<int> Match(const std::vector<string>& tokenizedQuery, int start);
private:
	vector<shared_ptr<NodeMatcher>> _matchers;
};

class OptionalNodeMatcher : public NodeMatcher
{
public:
	OptionalNodeMatcher()
	{
	}

	void Aggregate(shared_ptr<NodeMatcher> childMatcher)
	{
		_matcher = childMatcher;
	}

	set<int> Match(const vector<string>& tokenizedQuery, int start);
private:
	shared_ptr<NodeMatcher> _matcher;
};

class RefNodeMatcher : public NodeMatcher
{
public:
	RefNodeMatcher(map<string, Rule>& rules, const char* name) :_rules(rules), _name(name)
	{
	}

	set<int> Match(const vector<string>& tokenizedQuery, int start);
private:
	shared_ptr<NodeMatcher> _matcher;
	map<string, Rule>& _rules;
	string _name;
};

struct LexiconToken
{
	LexiconToken()
	{
		is_lexicon_end = false;
	}

public:
	bool is_lexicon_end;
	unordered_map<string, shared_ptr<LexiconToken>> children;
};

class LexiconNodeMatcher : public NodeMatcher
{
public:
	LexiconNodeMatcher(const char* lexiconFile):_lexicon_file(lexiconFile),
		_trie_root(new LexiconToken())
	{
		std::ifstream infile(_lexicon_file);
		if (!infile.is_open())
		{
			string msg = "failed to open lexion file ";
			msg += string(_lexicon_file);
			throw std::runtime_error(msg.c_str());
		}
		string line;
		while (std::getline(infile, line))
		{
			auto words = split(line);
			if (words.size() == 0)
			{
				continue;
			}
			shared_ptr<LexiconToken> cur_trie_node = _trie_root;
			for (auto ite = words.begin(); ite != words.end(); ite++)
			{
				if (cur_trie_node->children.count(*ite) == 0)
				{
					// is_lexicon_end is set to false by default, 
					// don't need to set it here again.
					cur_trie_node->children[*ite] = 
						shared_ptr<LexiconToken>(new LexiconToken());
				}
				cur_trie_node = cur_trie_node->children[*ite];
			}
			cur_trie_node->is_lexicon_end = true;
		}
		infile.close();
	}

	set<int> Match(const std::vector<string>& tokenizedQuery, int start);

private:
	string _lexicon_file;
	shared_ptr<LexiconToken> _trie_root;
};
