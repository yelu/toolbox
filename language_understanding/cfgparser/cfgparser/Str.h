#pragma once

#include <string>
#include <sstream>
#include <vector>
#include <algorithm> 
#include <functional> 
#include <cctype>
#include <regex>

static std::vector<std::string> split(const std::string &s, 
	                  const char* delim_reg = "\\s+") 
{
	std::regex re(delim_reg);

	return std::vector<std::string>(
		std::sregex_token_iterator(s.begin(), s.end(), re, -1),
		std::sregex_token_iterator()
		);
}

// trim from start
static inline std::string &ltrim(std::string &s) {
	s.erase(s.begin(), std::find_if(s.begin(), s.end(),
		std::not1(std::ptr_fun<int, int>(std::isspace))));
	return s;
}

// trim from end
static std::string &rtrim(std::string &s) {
	s.erase(std::find_if(s.rbegin(), s.rend(),
		std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
	return s;
}

// trim from both ends
static inline std::string &trim(std::string &s) {
	return ltrim(rtrim(s));
}