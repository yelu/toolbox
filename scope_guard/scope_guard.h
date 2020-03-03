/***************************************************************************
 *
 * Copyright (c) 2012 Baidu.com, Inc. All Rights Reserved
 * common.h,v 1.0 2012-09-08 12:39 yelu01
 *
 **************************************************************************/



/**
 * @file scope_guard.h
 * @author yelu01(yelu01@baidu.com)
 * @date 2012-08-22 10:25
 * @version 1.0
 * @brief make use of RAII to make sure resource release when functions return.
 *
 **/

#pragma once

#include <boost/function.hpp>
#include <boost/lambda/lambda.hpp>

class scope_guard_t
{
public:
    explicit scope_guard_t(boost::function<void()> on_exit)
        : _on_exit(on_exit)
    { }

    ~scope_guard_t()
    {
    	_on_exit();
    }

private:
    boost::function<void()> _on_exit;

private:
    // noncopyable
    scope_guard_t(scope_guard_t const&);
    scope_guard_t& operator=(scope_guard_t const&);
};

#define SCOPEGUARD_LINENAME_CAT(name, line) name##line
#define SCOPEGUARD_LINENAME(name, line) SCOPEGUARD_LINENAME_CAT(name, line)

#define ON_SCOPE_EXIT(callback) scope_guard_t \
	SCOPEGUARD_LINENAME(EXIT, __LINE__)(callback)
