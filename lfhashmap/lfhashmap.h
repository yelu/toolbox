/***************************************************************************
 * 
 * Copyright (c) 2013 Baidu.com, Inc. All Rights Reserved
 * lfhashmap.h,v 1.11 2013-05-31 2013-05-31
 * 
 **************************************************************************/
 
/**
 * @file lfhashmap.h
 * @author yelu(yelu01@baidu.com)
 * @brief lock free hashmap when there is only one concurrent writing.
 *  
 **/

#ifndef  _LFHASHMAP_H_
#define  _LFHASHMAP_H_
#include <list>
#include <mutex>

namespace ems{

template <class _Key,							//hash key
		  class _Value,							//hash value
          class _HashFun = xhash<_Key>,			//hash function
          class _Equl = std::equal_to<_Key>		//key cmp function.
          >
class lfhashmap
{
public:
	enum HASH_STATUS
	{
		HASH_ERROR = -1,
		HASH_EXIST = 1,
		HASH_NOT_EXIST,
		HASH_INSERT_SEC,
		HASH_OVERWRITE,
		HASH_INSERT_SEC
	};

	struct node_t
	{
		node_t(){next = NULL;}
		_Key key;
		_Value value;
		node_t* next;
	};

	struct deleted_node_t
	{
		deleted_node_t(){node = NULL; timestamp = 0;}
		long timestamp;
		node_t* node;
	};

	size_t size()
	{
		return _size;
	}

	lfhashmap()
	{
		_bucket = NULL;
		_bucket_size = 0;
		_size = 0;
	}

	~lfhashmap()
	{
		destroy();
	}

	int create(size_t bucket_size)
	{
		_bucket_size = bucket_size;
		_bucket = new(std::nothrow) node_t*[_bucket_size];
		if (NULL == _bucket)
		{
			return -1;
		}
		memset(_bucket, 0, sizeof(node_t*) * _bucket_size);

		_size = 0;

		return 0;
	}

	/**
	 * @param [in] k. the key to set.
	 * @param [in] val. the value set to.
	 * @param [in] flag. if a flag with 0 indicates if key exists, return 
	 *  with value unchanged. otherwise, if key exists, value will be replaced.
	 * @return. HASH_OVERWRITE indicates value overwritten(when flag!=0).
	 * 			HASH_INSERT_SEC	indicates new node inserted.
	 * 			HASH_EXIST	indicates key exists(when flag=0).
	 * @brief add key to set.
	 *
	 **/
	HASH_STATUS set(const _Key& k, const _Value v, int flag = 0)
	{
		std::lock_guard<std::mutex> lock(_wlock);
		_delete_expired_node();
		size_t key = _hashfun(k);
		uint64_t bucket_idx = key % _bucket_size;
		node_t* node = _bucket[bucket_idx];

		while(node)
		{
			if(_equl((node)->key, k))
			{
				if(flag) {node->value = v; return HASH_OVERWRITE;}
				else { return HASH_EXIST; }
			}
			node = node->next;
		}
		// not found, add it.
		node_t* new_node = new node_t();
		new_node->key = k;
		new_node->value = v;
		new_node->next = _bucket[bucket_idx];
		_bucket[bucket_idx] = new_node;
		_size++;
		return HASH_INSERT_SEC;
	}

	HASH_STATUS erase(const _Key& k)
	{
		std::lock_guard<std::mutex> lock(_wlock);
		size_t key = _hashfun(k);
		uint64_t bucket_idx = key % _bucket_size;
		node_t** pnode = &(_bucket[bucket_idx]);

		while(*pnode)
		{
			if(_equl((*pnode)->key, k))
			{
				node_t* tmp = (*pnode);
				(*pnode) = tmp->next;

				// save deleted node and deleting time in sec for future deleting.
				deleted_node_t deleted_node;
				deleted_node.node = tmp;
				timeval t;
				gettimeofday(&t, NULL);
				long now = t.tv_sec;	// current time in second.
				deleted_node.timestamp = now;
				_deleted.push_back(deleted_node);
				_size--;
				return HASH_EXIST;
			}
			pnode = &((*pnode)->next);
		}
		// not found
		return HASH_NOT_EXIST;
	}

	/**
	 * @brief add key to set.
	 * @param [in] k. the key to find
	 * @param [in/out] val. address to store the value we get.
	 *  if it is not null, *v will be set to value we get.
	 * @return  HASH_EXIST indicates key exists. 
	 *	HASH_NOEXIST indicates key doesn't exist.
	 *
	 **/
	HASH_STATUS get(const _Key& k, _Value* v = 0)
	{
		size_t key = _hashfun(k);
		uint64_t bucket_idx = key % _bucket_size;
		node_t* node = _bucket[bucket_idx];

		while(node)
		{
			if(_equl((node)->key, k))
			{
				if(v) {*v = node->value;}
				return HASH_EXIST;
			}
			node = node->next;
		}
		return HASH_NOT_EXIST;
	}

	/**
	 * @brief destroy hashmap. not thread safe.
	 *
	 * @return  int 0:succeed, otherwise:error. 
	**/
	int destroy()
	{
		if(NULL == _bucket) return 0;
		for(size_t i = 0; i < _bucket_size; i++)
		{
			node_t** node = &(_bucket[i]);
			while(*node)
			{
				node_t* tmp = (*node);
				*node = tmp->next;
				delete tmp;
			}
		}
		delete []_bucket;
		_bucket = NULL;
		_bucket_size = 0;
		_size = 0;

		typename std::list<deleted_node_t>::iterator ite = _deleted.begin();
		while(ite != _deleted.end())
		{
			delete ite->node;
			ite = _deleted.erase(ite);
		}

		return 0;
	}


private:
	std::mutex _wlock;

	std::list<deleted_node_t> _deleted;

	void _delete_expired_node()
	{
		static const uint64_t DELETE_DELAY = 600;
		// delete if _deleted has more than 10000 node to avoid calling
		// to gettimeofday too much frequently.
		if(_deleted.size() < 10000) {return;}

		// get current time in second.
		timeval t;
		gettimeofday(&t, NULL);
		long now = t.tv_sec;

		typename std::list<deleted_node_t>::iterator ite = _deleted.begin();
		while(ite != _deleted.end())
		{
			if(now - (ite->timestamp) > DELETE_DELAY)
			{
				delete ite->node;
				ite = _deleted.erase(ite);
			}
			else
			{
				break;
			}
		}
	}

	node_t** _bucket;
	size_t _bucket_size;
	_HashFun _hashfun;
	_Equl _equl;
	size_t _size;

};

} // namespace ems

#endif  //_HASHMAP_H_

