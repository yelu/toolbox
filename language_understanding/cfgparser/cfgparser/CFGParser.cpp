#include "CFGParser.h"

void CFGParser::LoadXml(const string& path)
{
	if (path.find_last_of('/') == string::npos &&
		path.find_last_of('\\') == string::npos)
	{
		throw std::runtime_error("invalid cfg file path.");
	}
	_cfgFile = path;
	xml_document<> doc;
	xml_node<> * rootNode;
	// Read the xml file into a vector
	std::ifstream theFile(path);
	vector<char> buffer((std::istreambuf_iterator<char>(theFile)), std::istreambuf_iterator<char>());
	buffer.push_back('\0');
	// Parse the buffer using the xml file parsing library into doc 
	doc.parse<0>(&buffer[0]);
	// Find our root node
	rootNode = doc.first_node("root");

	// Iterate over the children
	for (xml_node<>* ruleNode = rootNode->first_node("rule"); ruleNode != NULL; 
		ruleNode = ruleNode->next_sibling("rule"))
	{
		Rule rule;
		string name(ruleNode->first_attribute("name")->value());
		rule.Name = name;
		auto scopeAttr = ruleNode->first_attribute("scope");
		if (scopeAttr != 0 && strcmp(scopeAttr->value(), "private") == 0)
		{
			rule.IsPublic = false;
		}
		auto first_node = ruleNode->first_node();
		rule.Matcher = _GenMatcherFromNode(first_node);
		// If there is only one node under rule, and it is not "sequence" node.
		// we allow you omit "sequence" node. Otherwise, you have to provide it.
		// Therefore, there is always only one node under rule.
		if (NULL != first_node->next_sibling())
		{
			throw std::runtime_error("root rule can have only one child.");
		}
		// if it is empty rule, ignore it.
		if (!rule.Matcher) { continue; }
		_rules[rule.Name] = rule;
		if (rule.IsPublic)
		{
			_publicRules[name] = rule;
		}
	}
}

shared_ptr<NodeMatcher> CFGParser::_GenMatcherFromNode(const xml_node<>* node)
{
	shared_ptr<NodeMatcher> ret;

	if (strcmp(node->name(), "sequence") == 0)
	{
		ret.reset(new SequenceNodeMatcher());
		for (xml_node<>* child = node->first_node();child; child = child->next_sibling())
		{
			ret->Aggregate(_GenMatcherFromNode(child));
		}
	}
	else if (strcmp(node->name(), "one-of") == 0)
	{
		ret.reset(new OneOfNodeMatcher());
		for (xml_node<>* child = node->first_node(); child; child = child->next_sibling())
		{
			ret->Aggregate(_GenMatcherFromNode(child));
		}
	}
	else if (strcmp(node->name(), "string") == 0)
	{
		ret.reset(new StringNodeMatcher(node->value()));
	}
	else if (strcmp(node->name(), "reference") == 0)
	{
		auto ruleAttr = node->first_attribute("rule");
		if (ruleAttr == NULL)
		{
			string msg("attribute \"rule\" is missing in reference node");
			throw std::runtime_error(msg.c_str());
		}
		ret.reset(new RefNodeMatcher(_rules, ruleAttr->value()));
	}
	else if (strcmp(node->name(), "regex") == 0)
	{
		if (node->value() == NULL)
		{
			string msg("regex can't be empty");
			throw std::runtime_error(msg.c_str());
		}
		string pattern(node->value());
		trim(pattern);
		if(pattern.size() == 0)
		{
			throw std::runtime_error("regex can't be empty");
		}
		ret.reset(new RegexNodeMatcher(pattern.c_str()));
	}
	else if(strcmp(node->name(), "lexicon") == 0)
	{
		auto fileAttr = node->first_attribute("file");
		if (fileAttr == NULL)
		{
			string msg("attribute \"file\" is missing in lexicon node");
			throw std::runtime_error(msg.c_str());
		}

		// deal with relative file path.
		string lexiconFilePath = fileAttr->value();
		if (lexiconFilePath[0] == '.')
		{
			size_t last_slash = 0;
			auto last_slash_1 = _cfgFile.find_last_of('\\');
			auto last_slash_2 = _cfgFile.find_last_of('/');
			if (last_slash_1 == string::npos)
			{
				last_slash = last_slash_2;
			}
			else if(last_slash_2 == string::npos)
			{
				last_slash = last_slash_1;
			}
			else
			{
				last_slash = last_slash_1 > last_slash_2 ? last_slash_1 : last_slash_2;
			}
			string cfgFileDir = _cfgFile.substr(0, last_slash + 1);
			lexiconFilePath = cfgFileDir + lexiconFilePath;
		}
		_dependentFiles.push_back(lexiconFilePath);
		ret.reset(new LexiconNodeMatcher(lexiconFilePath.c_str()));
	}
	else
	{
		char msg[100];
		sprintf(msg, "unknown node \"%s\"", node->name());
		throw std::runtime_error(msg);
	}

	// if it is optioanl
	auto optianalAttr = node->first_attribute("optional");
	if (optianalAttr != NULL && strcmp(optianalAttr->value(), "true") == 0)
	{
		shared_ptr<OptionalNodeMatcher> optionalMatcher(new OptionalNodeMatcher());
		optionalMatcher->Aggregate(ret);
		ret = optionalMatcher;
	}
	return ret;
}

map<string, vector<pair<int, int>>> CFGParser::Parse(const vector<string>& tokenizedQuery, bool merge)
{
	map<string, vector<pair<int, int>>> matches;
	for (size_t start = 0; start < tokenizedQuery.size(); start++)
	{
		for(auto rule = _publicRules.begin(); rule != _publicRules.end(); rule++)
		{
			if (!rule->second.IsPublic) { continue; }
			auto ends = rule->second.Matcher->Match(tokenizedQuery, (int)start);
			for (auto end = ends.begin(); end != ends.end(); end++)
			{
				if (matches.count(rule->second.Name) == 0)
				{
					matches[rule->second.Name] = vector<pair<int, int>>();
				}
				matches[rule->second.Name].push_back(pair<int, int>(start, *end));
			}
		}
	}

	if (!merge) { return matches; }
	// merge intervals of the same rule.
	for (auto ite  = matches.begin(); ite != matches.end(); ite++)
	{	
		sort(ite->second.begin(), ite->second.end(), Match::Comparator());
		int preStart = 0;
		int preEnd = 0;
		auto last = ite->second.begin();
		for (auto match = ite->second.begin(); match != ite->second.end(); match++)
		{
			if (match->first > preEnd)
			{
				if (preEnd != 0)
				{
					last->first = preStart;
					last->second = preEnd;
					last++;
				}
				preStart = match->first;
				preEnd = match->second;
			}
			else
			{
				preEnd = match->second < preEnd ? preEnd : match->second;
			}
		}
		if (preEnd != 0)
		{
			last->first = preStart;
			last->second = preEnd;
			last++;
		}
		ite->second.erase(last, ite->second.end());
	}
	return matches;
}



