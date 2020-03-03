#include "NodeMatcher.h"

set<int> StringNodeMatcher::Match(const std::vector<string>& tokenizedQuery, int start)
{
	set<int> ret;
	if ((int)(tokenizedQuery.size()) - start < (int)(_tokenizedItem.size())) { return ret; }

	for (size_t i = 0; i < _tokenizedItem.size(); i++)
	{
		if (_tokenizedItem[i] != tokenizedQuery[i + start])
		{
			return ret;
		}
	}
	ret.insert(start + (int)_tokenizedItem.size());
	return ret;
}

set<int> RegexNodeMatcher::Match(const std::vector<string>& tokenizedQuery, int start)
{
	set<int> ret;
	string query;
	for (size_t i = start; i < tokenizedQuery.size(); i++)
	{
		query += tokenizedQuery[i];
		query += " ";
	}
	rtrim(query);	
	if (query.size() == 0) { return ret; }

	std::smatch match;
	std::regex_search(query, match, _regex, std::regex_constants::match_continuous);	
 	if (match.size() == 0) { return ret; }
	string matchedPrefix = match[0].str();
	if (matchedPrefix.size() == 0) { return ret; }

	// check if the matched prefix are complete words.	
	size_t idx = query.find(matchedPrefix) + matchedPrefix.size();
	if (idx >= query.size()) { idx -= 1; }
	else if (query[idx] == ' ') { idx -= 1; }
	else if (query[idx - 1] == ' ') { idx -= 2; }
	else { return ret; }
	
	int end = start + 1;
	int i = idx;
	while (i >= 0)
	{
		if (query[i] == ' ') end += 1;
		i--;	
	}
	ret.insert(end);

	return ret;
}

set<int> SequenceNodeMatcher::Match(const std::vector<string>& tokenizedQuery, int start)
{
	auto ret = _Match(tokenizedQuery, start, 0);
	return ret;
}

set<int> SequenceNodeMatcher::_Match(const std::vector<string>& tokenizedQuery,
														int qStart, 
														int mStart)
{
	set<int> ret;
	if (mStart >= (int)_matchers.size())
	{
		ret.insert(qStart);
		return ret;
	}
	set<int> ends = _matchers[mStart]->Match(tokenizedQuery, qStart);
	for(int end:ends)
	{
		auto finalEnds = _Match(tokenizedQuery, end, mStart + 1);
		if (finalEnds.size() == 0) { continue; }
		else { ret.insert(finalEnds.begin(), finalEnds.end()); }
	}
	return ret;
}

set<int> OneOfNodeMatcher::Match(const std::vector<string>& tokenizedQuery, int start)
{
	set<int> ret;
	for(auto matcher = _matchers.begin(); matcher != _matchers.end(); matcher++)
	{
		auto ends = (*matcher)->Match(tokenizedQuery, start);
		ret.insert(ends.begin(), ends.end());
	}
	return ret;
}

set<int> OptionalNodeMatcher::Match(const std::vector<string>& tokenizedQuery, int start)
{
	set<int> ret;
	ret.insert(start);
	auto ends = _matcher->Match(tokenizedQuery, start);
	ret.insert(ends.begin(), ends.end());
	return ret;
}

set<int> RefNodeMatcher::Match(const std::vector<string>& tokenizedQuery, int start)
{
	if (!_matcher) { _matcher = _rules[_name].Matcher; }
	auto ret = _matcher->Match(tokenizedQuery, start);
	return ret;
}

set<int> LexiconNodeMatcher::Match(const std::vector<string>& tokenizedQuery, int start)
{
	set<int> ret;
	size_t end = (size_t)start;
	auto cur_lex_token = _trie_root;
	for( ; end < tokenizedQuery.size(); end++)
	{	
		if (cur_lex_token->children.count(tokenizedQuery[end]) == 0)
		{
			break;
		}
		auto next_token = cur_lex_token->children[tokenizedQuery[end]];
		if (next_token->is_lexicon_end) 
		{
			ret.insert(end + 1);
		}
		cur_lex_token = next_token;
	} 

	return ret;
}
