'''
Created on 2015/06/02

:author: hubo
'''
from __future__ import print_function, absolute_import, division 
from collections import deque
from vlcp_event_cython.matchtree cimport MatchTree
from vlcp_event_cython.event cimport Event, EventMatcher
from vlcp_event_cython.event import withIndices

cdef int bisect_left(list a, int x, int lo=0, int hi=-1) except -1:
    """Return the index where to insert item x in list a, assuming a is sorted.
    The return value i is such that all e in a[:i] have e < x, and all e in
    a[i:] have e >= x.  So if x already appears in the list, a.insert(x) will
    insert just before the leftmost x already there.
    Optional args lo (default 0) and hi (default len(a)) bound the
    slice of a to be searched.
    """
    cdef int mid
    if lo < 0:
        raise ValueError('lo must be non-negative')
    if hi < 0:
        hi = len(a)
    while lo < hi:
        mid = (lo+hi)//2
        if a[mid] < x: lo = mid+1
        else: hi = mid
    return lo

cdef bint cmp_lt(x, y):
    # Use __lt__ if available; otherwise, try __le__.
    # In Py3.x, only __lt__ will be called.
    return (x < y) if hasattr(x, '__lt__') else (not y <= x)

cdef int _siftdown(list heap, int startpos, int pos) except -1:
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    cdef int parentpos
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if cmp_lt(newitem, parent):
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem

cdef int _siftup(list heap, int pos) except -1:
    cdef int endpos = len(heap)
    cdef int startpos = pos
    newitem = heap[pos]
    # Bubble up the smaller child until hitting a leaf.
    cdef int childpos = 2*pos + 1    # leftmost child position
    cdef int rightpos
    while childpos < endpos:
        # Set childpos to index of smaller child.
        rightpos = childpos + 1
        if rightpos < endpos and not cmp_lt(heap[childpos], heap[rightpos]):
            childpos = rightpos
        # Move the smaller child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2*pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    _siftdown(heap, startpos, pos)


cdef int heappush(list heap, item) except -1:
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    _siftdown(heap, 0, len(heap)-1)

cdef object heappop(list heap):
    """Pop the smallest item off the heap, maintaining the heap invariant."""
    lastelt = heap.pop()    # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        _siftup(heap, 0)
    else:
        returnitem = lastelt
    return returnitem


@withIndices('queue')
class QueueCanWriteEvent(Event):
    pass

@withIndices('queue')
class QueueIsEmptyEvent(Event):
    pass

@withIndices('newonly', 'firstonly')
class AutoClassQueueCanWriteEvent(QueueCanWriteEvent):
    pass

cdef class _MultiQueue

cdef class _SubQueue:
    cdef bint blocked
    cdef _MultiQueue parent
    cpdef append(self, value, bint force = False):
        raise NotImplementedError
    cpdef bint canAppend(self):
        raise NotImplementedError
    cpdef bint canPop(self):
        raise NotImplementedError
    cdef tuple _pop(self):
        raise NotImplementedError
    cpdef tuple clear(self):
        raise NotImplementedError
    cdef tuple _clear(self):
        raise NotImplementedError
    cpdef block(self, value):
        raise NotImplementedError
    cpdef unblock(self, value):
        raise NotImplementedError
    cpdef unblockall(self):
        raise NotImplementedError
    
    

'''
A multi-queue model with priority and balance.
When first created, there is a default queue with priority 0. More sub-queues maybe created with addSubQueue.
Each sub-queue is a CBQueue which accepts more sub-queues. Sub-queues are considered as black-box to the outer parent.
'''
cdef class _FifoQueue(_SubQueue):
    cdef:
        readonly object queue
        int maxlength
        bint isWaited
    def __cinit__(self):
        self.queue = deque()
    '''
    A wrapper for a FIFO queue
    '''
    def __init__(self, _MultiQueue parent = None, maxlength = None):
        self.parent = parent
        self.maxlength = -1 if maxlength is None else <int?>maxlength
        self.blocked = False
        if maxlength is not None and <int?>maxlength <= 0:
            self.maxlength = 1
        self.isWaited = False
    cpdef append(self, value, bint force = False):
        if not force and not self.canAppend():
            self.isWaited = True
            return QueueCanWriteEvent.createMatcher(self)
        if self.parent is not None:
            m = self.parent.notifyAppend(self, force)
            if m is not None:
                return m
        self.queue.append(value)
        return None
    cpdef bint canAppend(self):
        return self.maxlength < 0 or len(self.queue) < self.maxlength
    cpdef bint canPop(self):
        return self.queue and not self.blocked
    cpdef tuple pop(self):
        cdef tuple ret = self._pop()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self)
            ret[1].extend(pr[0])
            ret[2].extend(pr[1])
        return ret
    cdef tuple _pop(self):
        if self.blocked:
            raise IndexError('pop from a blocked queue')
        ret = self.queue.popleft()
        if self.isWaited and self.canAppend():
            self.isWaited = False
            return (ret, [QueueCanWriteEvent(self)], [])
        else:
            return (ret, [], [])
    cpdef tuple clear(self):
        cdef int l = len(self)
        cdef tuple ret = self._clear()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self, l)
            ret[0].extend(pr[0])
            ret[1].extend(pr[1])
        return ret
    cdef tuple _clear(self):
        if self.blocked:
            self.unblockall()
        self.queue.clear()
        if self.isWaited and self.canAppend():
            self.isWaited = False
            return ([QueueCanWriteEvent(self)], [])
        else:
            return ([], [])
    def __len__(self):
        return len(self.queue)
    cpdef block(self, value):
        if self.parent is not None:
            self.parent.notifyAppend(self, True)
        self.queue.appendleft(value)
        if not self.blocked:
            self.blocked = True
            if self.parent is not None:
                self.parent.notifyBlock(self, True)
    cpdef unblock(self, value):
        if self.blocked:
            self.blocked = False
            if self.parent is not None:
                self.parent.notifyBlock(self, False)
    cpdef unblockall(self):
        if self.blocked:
            self.blocked = False
            if self.parent is not None:
                self.parent.notifyBlock(self, False)

cdef class _PriorityQueue(_SubQueue):
    cdef:
        readonly list queue
        readonly object deque
        int maxlength
        set blocks
        bint isWaited
        str key
        
    '''
    A queue with inner built priority. Event must have a "priority" property to use with this type of queue.
    For fail-safe, events without "priority" property have the lowest priority.
    NOTICE: different from the queue priority, the priority property is smaller-higher, and is not limited to integers.
    This allows datetime to be used as an increasing priority
    '''
    def __cinit__(self):
        self.deque = deque()
        self.queue = []
        self.blocks = set()
    def __init__(self, _MultiQueue parent = None, maxlength = None, str key = 'priority'):
        # a heap
        self.parent = parent
        self.maxlength = None if maxlength is None else <int?>maxlength
        if self.maxlength is not None and self.maxlength <= 0:
            self.maxlength = 1
        self.blocked = False
        self.isWaited = False
        self.key = key
    @classmethod
    def initHelper(cls, str key = 'priority'):
        def initer(_MultiQueue parent = None, maxlength = None):
            return cls(parent, maxlength, key)
        return initer
    cpdef append(self, value, bint force = False):
        if not force and not self.canAppend():
            self.isWaited = True
            return QueueCanWriteEvent.createMatcher(self)
        if self.parent is not None:
            m = self.parent.notifyAppend(self, force)
            if m is not None:
                return m
        if hasattr(value, self.key):
            heappush(self.queue, (getattr(value, self.key), value))
            # a priority push may change the block status
            if self.blocked and not self.queue[0][1] in self.blocks:
                self.blocked = False
                if self.parent is not None:
                    self.parent.notifyBlock(self, False)
        else:
            self.deque.append(value)
        return None
    cpdef bint canAppend(self):
        return self.maxlength < 0 or len(self.queue) + len(self.deque) < self.maxlength
    cpdef bint canPop(self):
        return len(self.queue) + len(self.deque) > 0 and not self.blocked
    cpdef pop(self):
        cdef tuple ret = self._pop()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self)
            ret[1].extend(pr[0])
            ret[2].extend(pr[1])
        return ret
    cdef tuple _pop(self):
        if self.blocked:
            raise IndexError('pop from a blocked queue')
        if self.queue:
            ret = heappop(self.queue)[1]
        else:
            ret = self.deque.popleft()
        cdef bint blocked
        if self.queue:
            blocked = self.queue[0][1] in self.blocks
        elif self.deque:
            blocked = self.deque[0] in self.blocks
        else:
            blocked = False
        if self.blocked != blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
        if self.isWaited and self.canAppend():
            self.isWaited = False
            return (ret, [QueueCanWriteEvent(self)], [])
        else:
            return (ret, [], [])
    cdef tuple _clear(self):
        if self.blocks:
            self.unblockall()
        del self.queue[:]
        self.deque.clear()
        if self.isWaited and self.canAppend():
            self.isWaited = False
            return ([QueueCanWriteEvent(self)], [])
        else:
            return ([], [])
    cpdef tuple clear(self):
        cdef int l = len(self)
        cdef tuple ret = self._clear()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self, l)
            ret[0].extend(pr[0])
            ret[1].extend(pr[1])
        return ret
    def __len__(self):
        return len(self.queue) + len(self.deque)
    cpdef block(self, value):
        self.blocks.add(value)
        if self.parent is not None:
            self.parent.notifyAppend(self, True)
        if hasattr(value, self.key):
            heappush(self.queue, (getattr(value, self.key), value))
        else:
            self.deque.appendleft(value)
        if self.queue:
            blocked = self.queue[0][1] in self.blocks
        elif self.deque:
            blocked = self.deque[0] in self.blocks
        else:
            blocked = False
        if self.blocked != blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
    cpdef unblock(self, value):
        self.blocks.remove(value)
        cdef bint blocked
        if self.queue:
            blocked = self.queue[0][1] in self.blocks
        elif self.deque:
            blocked = self.deque[0] in self.blocks
        else:
            blocked = False
        if self.blocked != blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
    cpdef unblockall(self):
        self.blocks.clear()
        cdef bint blocked = False
        if self.blocked != blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)

cdef class _CircleListNode:
    cdef:
        _CircleListNode _prev
        _CircleListNode _next
        readonly object value

    @property
    def prev(self):
        return self._prev

    @property
    def next(self):
        return self._next

    '''
    Circle link list
    '''
    def __init__(self, value):
        self._prev = self
        self.value = value
        self._next = self
    cdef _CircleListNode insertprev(self, _CircleListNode node):
        self._prev._next = node
        node._prev = self._prev
        node._next = self
        self._prev = node
        return self
    cdef _CircleListNode remove(self):
        if self.next is self:
            return None
        self._prev._next = self._next
        self._next._prev = self._prev
        ret = self._next
        self._next = self
        self._prev = self
        return ret


cdef class _CircleList:
    cdef readonly _CircleListNode current
    def __init__(self):
        self.current = None
    cpdef remove(self, _CircleListNode node):
        if self.current is node:
            self.current = node.remove()
        else:
            node.remove()
    cpdef insertprev(self, _CircleListNode node):
        if self.current is None:
            self.current = node
        else:
            self.current.insertprev(node)
    cpdef insertcurrent(self, _CircleListNode node):
        self.insertprev(node)
        self.current = node
    cpdef _CircleListNode next(self):
        cdef _CircleListNode ret = self.current
        if self.current is not None:
            self.current = self.current.next
        return ret
    cpdef clear(self):
        self.current = None

cdef class CBQueue

cdef class _MultiQueue:
    CircleListNode = _CircleListNode
    CircleList = _CircleList
    cdef:
        bint blocked
        _CircleList queues
        dict queueDict
        dict queueStat
        object statseq
        CBQueue parent
        int priority
        int totalSize
    '''
    A multi-queue container, every queue in a multi-queue has the same priority, and is popped in turn.
    '''
    def __cinit__(self):
        self.queues = _CircleList()
        self.queueDict = {}
        self.queueStat = {}
        self.statseq = deque()
    def __init__(self, parent = None, priority = 0):
        self.parent = parent
        self.priority = priority
        self.totalSize = 0
        self.blocked = True
    cpdef bint canPop(self):
        return bool(self.queues.current)
    cdef tuple _pop(self):
        if not self.canPop():
            raise IndexError('pop from an empty or blocked queue')
        cdef _CircleListNode c = self.queues.next()
        cdef _SubQueue cvalue = <_SubQueue>c.value
        cdef tuple ret = cvalue._pop()
        self.queueStat[cvalue] = self.queueStat.get(cvalue, 0) + 1
        cdef _SubQueue o
        while len(self.statseq) >= 10 * len(self.queueDict) + 10:
            o = self.statseq.popleft()
            if o in self.queueStat:
                self.queueStat[o] = self.queueStat[o] - 1
                if self.queueStat[o] <= 0 and not o in self.queueDict:
                    del self.queueStat[o]
        self.statseq.append(cvalue)
        if not cvalue.canPop():
            self.queues.remove(c)
            self.queueDict[cvalue] = None
        self.totalSize = self.totalSize - 1
        if not self.canPop():
            if not self.blocked:
                self.blocked = True
                if self.parent is not None:
                    self.parent.notifyBlock(self, True)
        return ret            
    cpdef addSubQueue(self, _SubQueue queue):
        self.totalSize = self.totalSize + len(queue)
        queue.parent = self
        cdef _CircleListNode node
        if queue.canPop():
            # Activate this queue
            node = _CircleListNode(queue)
            self.queues.insertprev(node)
            self.queueDict[queue] = node
            self.queueStat[queue] = 0
        else:
            self.queueDict[queue] = None
        if self.canPop():
            if self.blocked:
                self.blocked = False
                if self.parent is not None:
                    self.parent.notifyBlock(self, False)
    cpdef removeSubQueue(self, _SubQueue queue):
        self.totalSize = self.totalSize - len(queue)
        cdef _CircleListNode node = self.queueDict[queue]
        if node is not None:
            self.queues.remove(node)
        del self.queueDict[queue]
        if queue in self.queueStat:
            del self.queueStat[queue]
        if not self.canPop():
            if not self.blocked:
                self.blocked = True
                if self.parent is not None:
                    self.parent.notifyBlock(self, True)
    cpdef notifyAppend(self, _SubQueue queue, bint force):
        if self.parent is not None:
            m = self.parent.notifyAppend(self, force)
            if m is not None:
                return m
        self.totalSize = self.totalSize + 1
        cdef _CircleListNode node
        cdef int qs
        if not queue.blocked:
            if self.queueDict[queue] is None:
                # Activate this queue
                node = _CircleListNode(queue)
                qs = self.queueStat.setdefault(queue, 0)
                if qs * len(self.queueStat) >= len(self.statseq):
                    self.queues.insertprev(node)
                else:
                    self.queues.insertcurrent(node)
                self.queueDict[queue] = node
        if self.canPop():
            if self.blocked:
                self.blocked = False
                if self.parent is not None:
                    self.parent.notifyBlock(self, False)
        return None
    def __len__(self):
        return self.totalSize
    cpdef notifyBlock(self, _SubQueue queue, bint blocked):
        cdef _CircleListNode node
        cdef int qs
        if queue.canPop():
            if self.queueDict[queue] is None:
                # Activate this queue
                node = _CircleListNode(queue)
                qs = self.queueStat.setdefault(queue, 0)
                if qs * len(self.queueStat) >= len(self.statseq):
                    self.queues.insertprev(node)
                else:
                    self.queues.insertcurrent(node)
                self.queueDict[queue] = node
        else:
            if self.queueDict[queue] is not None:
                self.queues.remove(self.queueDict[queue])
                self.queueDict[queue] = None
        cdef bint selfblocked = not self.canPop()
        if selfblocked != self.blocked:
            self.blocked = selfblocked
            if self.parent is not None:
                self.parent.notifyBlock(self, selfblocked)
    cpdef tuple notifyPop(self, _SubQueue queue, int length = 1):
        self.totalSize = self.totalSize - length
        if not queue.canPop():
            if self.queueDict[queue] is not None:
                self.queues.remove(self.queuDict[queue])
                self.queueDict[queue] = None
        cdef tuple ret = ([], [])
        if self.parent is not None:
            ret = self.parent.notifyPop(self, length)
        cdef bint blocked = not self.canPop()
        if blocked != self.blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
        return ret
        
    cpdef unblockall(self):
        cdef _SubQueue q
        for q in self.queueDict.keys():
            q.unblockall()
    cdef tuple _clear(self):
        cdef tuple ret = ([],[])
        cdef _SubQueue q
        cdef tuple pr
        for q in self.queueDict.keys():
            pr = q._clear()
            ret[0].extend(pr[0])
            ret[1].extend(pr[1])
        self.totalSize = 0
        self.queues.clear()
        if not self.blocked:
            self.blocked = True
            if self.parent is not None:
                self.parent.notifyBlock(self, True)
        return ret

nokey = object()

cdef class _AutoClassQueue(_SubQueue):
    '''
    A queue classify events into virtual sub-queues by key
    '''
    cdef:
        _CircleList queues
        dict queueDict
        dict queueStat
        object statseq
        int maxlength
        int maxstat
        set waited
        str key
        int preserve
        int totalSize
        set blockKeys
        int subqueuelimit
    def __cinit__(self):
        self.queues = _CircleList()
        self.queueDict = {}
        self.queueStat = {}
        self.statseq = deque()
        self.waited = set()
        self.blockKeys = set()
    def __init__(self, _MultiQueue parent = None, maxlength = None, str key = 'owner', preserveForNew = 1, maxstat = None, subqueuelimit = None):
        self.maxlength = -1 if maxlength is None else <int?>maxlength
        self.blocked = False
        if maxlength is not None and maxlength <= 0:
            self.maxlength = 1
        if maxstat is None:
            if self.maxlength < 0:
                self.maxstat = 10240
            else:
                self.maxstat = self.maxlength * 10
        else:
            self.maxstat = <int?>maxstat
        if self.maxstat >= 10240:
            self.maxstat = 10240
        self.key = key
        self.preserve = <int?>preserveForNew
        self.totalSize = 0
        self.subqueuelimit = -1 if subqueuelimit is None else <int?>subqueuelimit
    @classmethod
    def initHelper(cls, str key = 'owner', preserveForNew = 1, maxstat = None, subqueuelimit = None):
        def initer(_MultiQueue parent = None, maxlength = None):
            return cls(parent, maxlength, key, preserveForNew, maxstat, subqueuelimit)
        return initer
    cpdef append(self, value, bint force = False):
        key = getattr(value, self.key, nokey)
        # We use hash instead of reference or weakref, this may cause problem, but better than leak.
        kid = hash(key)
        if not force:
            w = self._tryAppend(key, kid)
            if w is not None:
                return w
        if self.parent is not None:
            m = self.parent.notifyAppend(self, force)
            if m is not None:
                return m
        cdef _CircleListNode node
        cdef int qs
        if key in self.queueDict:
            (<tuple>((<_CircleListNode>(self.queueDict[key])).value))[1].append(value)
        else:
            node = _CircleListNode((key,deque()))
            (<tuple>(node.value))[1].append(value)
            qs = self.queueStat.setdefault(kid, 0)
            if qs * len(self.queueStat) >= len(self.statseq):
                self.queues.insertprev(node)
            else:
                self.queues.insertcurrent(node)
            self.queueDict[key] = node
        self.totalSize += 1
        cdef bint blocked = not self.canPop() and self.totalSize > 0
        if blocked != self.blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
        return None
    cdef _tryAppend(self, key, kid):
        if self.maxlength < 0:
            if self.subqueuelimit < 0 or not key in self.queueDict:
                return None
            elif len((<tuple>((<_CircleListNode>(self.queueDict[key])).value))[1]) >= self.subqueuelimit:
                self.waited.add((False, False, key))
                return AutoClassQueueCanWriteEvent.createMatcher(self, _ismatch = lambda x: x.key == key or x.key is nokey)
            else:
                return None
        cdef _CircleListNode node
        cdef tuple nvalue
        if key in self.queueDict:
            node = self.queueDict[key]
            nvalue = node.value
            if self.subqueuelimit >= 0 and len(nvalue[1]) >= self.subqueuelimit:
                self.waited.add((False, False, key))
                return AutoClassQueueCanWriteEvent.createMatcher(self, _ismatch = lambda x: x.key == key or x.key is nokey)
            elif self.totalSize < self.maxlength - self.preserve - len(self.queueStat) + len(self.queueDict):
                return None
            else:
                if len(nvalue[1]) <= 1:
                    self.waited.add((False, True, key))
                    return AutoClassQueueCanWriteEvent.createMatcher(self, False, _ismatch = lambda x: not (x.firstonly and x.key != key))
                else:
                    self.waited.add((False, False))
                    return AutoClassQueueCanWriteEvent.createMatcher(self, False, False)
        elif kid in self.queueStat:
            if self.totalSize < self.maxlength - self.preserve:
                return None
            else:
                self.waited.add((False, True))
                return AutoClassQueueCanWriteEvent.createMatcher(self, False)
        else:
            if self.totalSize < self.maxlength:
                return None
            else:
                self.waited.add((True, True))
                return AutoClassQueueCanWriteEvent.createMatcher(self)
    cpdef bint canAppend(self):
        return self.maxlength is None or self.totalSize < self.maxlength
    cpdef bint canPop(self):
        return self.queues.current is not None
    cpdef tuple pop(self):
        cdef tuple ret = self._pop()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self)
            ret[1].extend(pr[0])
            ret[2].extend(pr[1])
        return ret
    cdef tuple _pop(self):
        if not self.canPop():
            raise IndexError('pop from a blocked or empty queue')
        cdef _CircleListNode c = self.queues.next()
        cdef tuple cvalue = c.value
        key = cvalue[0]
        kid = hash(key)
        ret = cvalue[1].popleft()
        self.totalSize -= 1
        self.queueStat[kid] = self.queueStat.get(kid, 0) + 1
        while len(self.statseq) >= min(self.maxstat, 10 * len(self.queueStat) + 10):
            k1 = self.statseq.popleft()
            self.queueStat[k1] = self.queueStat[k1] - 1
            if self.queueStat[k1] <= 0:
                del self.queueStat[k1]
        self.statseq.append(kid)
        if not cvalue[1]:
            del self.queueDict[cvalue[0]]
            self.queues.remove(c)
        cdef bint blocked = not self.canPop() and self.totalSize > 0
        if blocked != self.blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
        cdef int subsize
        cdef tuple w
        if self.waited:
            if key not in self.queueDict:
                subsize = 0
            else:
                subsize = len(self.queueDict[key].value[1])
            if self.maxlength < 0:
                if self.subqueuelimit >= 0 and subsize < self.subqueuelimit and (False, False, key) in self.waited:
                    return (ret, [AutoClassQueueCanWriteEvent(self, False, False, key=key)], [])
            elif self.totalSize < self.maxlength - self.preserve - len(self.queueStat) + len(self.queueDict):
                self.waited = {w for w in self.waited if len(w) == 3 and w[1] == False and w[2] != key}
                return (ret, [AutoClassQueueCanWriteEvent(self, False, False, key=key)], [])
            elif self.totalSize < self.maxlength - self.preserve:
                if (False, True) in self.waited or (False, True, key) in self.waited or (True, True) in self.waited or \
                        (False, False, key) in self.waited:
                    self.waited.discard((False, True))
                    self.waited.discard((False, True, key))
                    self.waited.discard((True, True))
                    self.waited.discard((False, False, key))
                    return (ret, [AutoClassQueueCanWriteEvent(self, False, True, key=key)], [])
            elif self.totalSize < self.maxlength:
                if (True, True) in self.waited or (False, False, key) in self.waited or (False, True, key) in self.waited:
                    self.waited.discard((True, True))
                    self.waited.discard((False, False, key))
                    if (False, True, key) in self.waited:
                        self.waited.discard((False, True, key))
                        return (ret, [AutoClassQueueCanWriteEvent(self, False, True, key=key)], [])
                    else:
                        return (ret, [AutoClassQueueCanWriteEvent(self, True, True, key=key)], [])
            elif self.subqueuelimit >= 0 and subsize < self.subqueuelimit and (False, False, key) in self.waited:
                # If we don't wake up the sub-queue waiter now, it may wait forever.
                # The sub-queue waiter won't be able to send events in, but they will get a new matcher
                # Some waiters might wake up mistakenly, they will wait again when they try to append the event. 
                self.waited.discard((True, True))
                self.waited.discard((False, False, key))
                return (ret, [AutoClassQueueCanWriteEvent(self, True, True, key=key)], [])
        return (ret, [], [])
    cpdef tuple clear(self):
        cdef int l = len(self)
        cdef tuple ret = self._clear()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self, l)
            ret[0].extend(pr[0])
            ret[1].extend(pr[1])
        return ret
    cdef tuple _clear(self):
        self.queues.clear()
        self.blockKeys.clear()
        self.queueDict.clear()
        self.totalSize = 0
        cdef bint blocked = not self.canPop() and self.totalSize > 0
        if blocked != self.blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
        if self.waited:
            self.waited.clear()
            return ([AutoClassQueueCanWriteEvent(self, False, False, key=nokey)], [])
        else:
            return ([], [])
    def __len__(self):
        return self.totalSize
    cpdef block(self, value):
        if self.parent is not None:
            self.parent.notifyAppend(self, True)
        key = getattr(value, self.key, nokey)
        cdef _CircleListNode node
        cdef tuple nvalue
        if key in self.queueDict:
            node = self.queueDict[key]
            nvalue = node.value
            nvalue[1].appendleft(value)
            self.queues.remove(self.queueDict[key])
        else:
            nvalue = (key, deque())
            node = _CircleListNode(nvalue)
            nvalue[1].append(value)
            self.queueDict[key] = node
        self.blockKeys.add(key)
        self.totalSize += 1
        cdef bint blocked = not self.canPop() and self.totalSize > 0
        if blocked != self.blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)
    cpdef unblock(self, value):
        key = getattr(value, self.key, nokey)
        cdef bint blocked
        if key in self.blockKeys:
            self._unblock(key)
            blocked = not self.canPop() and self.totalSize > 0
            if blocked != self.blocked:
                self.blocked = blocked
                if self.parent is not None:
                    self.parent.notifyBlock(self, blocked)
    def _unblock(self, key):
        self.blockKeys.remove(key)
        cdef _CircleListNode node = self.queueDict[key]
        cdef int qs = self.queueStat.setdefault(hash(key), 0)
        if qs * len(self.queueStat) >= len(self.statseq):
            self.queues.insertprev(node)
        else:
            self.queues.insertcurrent(node)            
    cpdef unblockall(self):
        for k in list(self.blockKeys):
            self._unblock(k)
        cdef bint blocked = not self.canPop() and self.totalSize > 0
        if blocked != self.blocked:
            self.blocked = blocked
            if self.parent is not None:
                self.parent.notifyBlock(self, blocked)


cdef allSubqueues(set subqueues, CBQueue q):
    subqueues.add(q)
    cdef list v
    for v in q.queueindex.values():
        if len(v) == 3:
            allSubqueues(subqueues, v[1])


cdef class CBQueue(_SubQueue):
    FifoQueue = _FifoQueue
    PriorityQueue = _PriorityQueue
    MultiQueue = _MultiQueue
    AutoClassQueue = _AutoClassQueue
    cdef:
        dict queues
        dict queueindex
        list prioritySet
        MatchTree tree
        readonly _SubQueue defaultQueue
        int totalSize
        int maxtotal
        readonly dict blockEvents
        bint isWaited
        bint isWaitEmpty
        int outputStat
    def __cinit__(self):
        self.queues = {}
        self.queueindex = {}
        self.prioritySet = []
    def __init__(self, MatchTree tree = None, _MultiQueue parent = None, maxdefault = None, maxtotal = None, defaultQueueClass = _FifoQueue, int defaultQueuePriority = 0):
        '''
        Constructor
        '''
        if tree is None:
            self.tree = MatchTree()
        else:
            self.tree = tree
        self.parent = parent
        cdef _MultiQueue defaultPriority = _MultiQueue(self, defaultQueuePriority)
        cdef _SubQueue defaultQueue = defaultQueueClass(defaultPriority, maxdefault)
        defaultPriority.addSubQueue(defaultQueue)
        self.queues[defaultQueuePriority] = defaultPriority
        self.tree.insert(None, defaultQueue)
        self.defaultQueue = defaultQueue
        self.totalSize = 0
        self.maxtotal = -1 if maxtotal is None else <int?>maxtotal
        self.blocked = True
        self.blockEvents = {}
        self.isWaited = False
        self.isWaitEmpty = False
        self.outputStat = 0
    cdef _removeFromTree(self):
        cdef list v
        for v in self.queueindex.values():
            if len(v) == 3:
                (<CBQueue>v[1])._removeFromTree()
        self.tree.remove(None, self.defaultQueue)
        self.tree = None
    cpdef bint canAppend(self):
        '''
        Whether the queue is full or not. Only check the total limit. Sub-queue may still be full (even default).
        :returns: False if the queue is full, True if not.
        If there are sub-queues, append() may still fail if the sub-queue is full. 
        '''
        return self.maxtotal < 0 or self.totalSize < self.maxtotal
    cpdef append(self, event, bint force = False):
        '''
        Append an event to queue. The events are classified and appended to sub-queues
        :param event: input event
        :param force: if True, the event is appended even if the queue is full
        :returns: None if appended successfully, or a matcher to match a QueueCanWriteEvent otherwise
        '''
        if self.tree is None:
            if self.parent is None:
                raise IndexError('The queue is removed')
            else:
                return self.parent.parent.append(event, force)
        cdef _SubQueue q = self.tree.matchfirst(<Event>event)
        return q.append(event, force)
    cpdef waitForEmpty(self):
        '''
        Make this queue generate a QueueIsEmptyEvent when it is empty
        :returns: matcher for QueueIsEmptyEvent, or None if the queue is already empty
        '''
        if not self:
            return None
        self.isWaitEmpty = True
        return QueueIsEmptyEvent.createMatcher(self)
    cpdef block(self, event, emptyEvents = ()):
        '''
        Return a recently popped event to queue, and block all later events until unblock.
        Only the sub-queue directly containing the event is blocked, so events in other queues may still be processed.
        It is illegal to call block and unblock in different queues with a same event.
        :param event: the returned event. When the queue is unblocked later, this event will be popped again.
        :param emptyEvents: reactivate the QueueIsEmptyEvents
        '''
        cdef _SubQueue q = self.tree.matchfirst(event)
        q.block(event)
        self.blockEvents[event] = q
        for ee in emptyEvents:
            (<CBQueue>ee.queue).waitForEmpty()
    cpdef unblock(self, event):
        '''
        Remove a block 
        '''
        if event not in self.blockEvents:
            return
        (<_SubQueue>(self.blockEvents[event])).unblock(event)
        del self.blockEvents[event]
    cpdef unblockqueue(self, CBQueue queue):
        '''
        Remove blocked events from the queue and all subqueues. Usually used after queue clear/unblockall to prevent leak.
        :returns: the cleared events
        '''
        cdef set subqueues = set()
        allSubqueues(subqueues, queue)
        cdef CBQueue v
        events = [k for k,v in self.blockEvents.items() if v in subqueues]
        for e in events:
            del self.blockEvents[e]
        return events
    cpdef unblockall(self):
        '''
        Remove all blocks from the queue and all sub-queues
        '''
        cdef _MultiQueue q
        for q in self.queues.values():
            q.unblockall()
        self.blockEvents.clear()
    cpdef notifyAppend(self, _MultiQueue queue, bint force):
        '''
        Internal notify for sub-queues
        :returns: If the append is blocked by parent, an EventMatcher is returned, None else.
        '''
        if not force and not self.canAppend():
            self.isWaited = True
            return QueueCanWriteEvent.createMatcher(self)
        if self.parent is not None:
            m = self.parent.notifyAppend(self, force)
            if m is not None:
                return m
        self.totalSize = self.totalSize + 1
        return None
    cpdef notifyBlock(self, _MultiQueue queue, bint blocked):
        '''
        Internal notify for sub-queues been blocked
        '''
        cdef int pindex
        if blocked:
            if self.prioritySet[-1] == queue.priority:
                self.prioritySet.pop()
            else:
                pindex = bisect_left(self.prioritySet, queue.priority)
                if pindex < len(self.prioritySet) and self.prioritySet[pindex] == queue.priority:
                    del self.prioritySet[pindex]
        else:
            if queue.canPop():
                pindex = bisect_left(self.prioritySet, queue.priority)
                if pindex >= len(self.prioritySet) or self.prioritySet[pindex] != queue.priority:
                    self.prioritySet.insert(pindex, queue.priority)
        cdef bint newblocked =  not self.canPop()
        if newblocked != self.blocked:
            self.blocked = newblocked
            if self.parent is not None:
                self.parent.notifyBlock(self, newblocked)
    cpdef tuple notifyPop(self, queue, length = 1):
        '''
        Internal notify for sub-queues been poped
        :returns: List of any events generated by this pop
        '''
        self.totalSize = self.totalSize - length
        cdef list ret1 = []
        cdef list ret2 = []
        if self.isWaited and self.canAppend():
            self.isWaited = False
            ret1.append(QueueCanWriteEvent(self))
        if self.isWaitEmpty and not self:
            self.isWaitEmpty = False
            ret2.append(QueueIsEmptyEvent(self))
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self, length)
            ret1.extend(pr[0])
            ret2.extend(pr[1])
        cdef bint newblocked =  not self.canPop()
        if newblocked != self.blocked:
            self.blocked = newblocked
            if self.parent is not None:
                self.parent.notifyBlock(self, newblocked)
        return (ret1, ret2)
    cpdef bint canPop(self):
        '''
        Whether the queue is empty/blocked or not
        :returns: False if the queue is empty or blocked, or True otherwise
        '''
        return bool(self.prioritySet)
    cpdef tuple pop(self):
        '''
        Pop an event from the queue. The event in the queue with higher priority is popped before ones in lower priority.
        If there are multiple queues with the same priority, events are taken in turn from each queue.
        May return some queueEvents indicating that some of the queues can be written into.
        :returns: (obj, (queueEvents,...), (queueEmptyEvents,...)) where obj is the popped event, queueEvents are QueueCanWriteEvents generated by this pop
                and queueEmptyEvents are QueueIsEmptyEvents generated by this pop
        '''
        cdef tuple ret = self._pop()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self)
            ret[1].extend(pr[0])
            ret[2].extend(pr[1])
        return ret
    cdef tuple _pop(self):
        '''
        Actual pop
        '''
        if not self.canPop():
            raise IndexError('pop from an empty or blocked queue')
        cdef int priority = self.prioritySet[-1]
        cdef tuple ret = (<_MultiQueue>self.queues[priority])._pop()
        self.outputStat = self.outputStat + 1
        self.totalSize = self.totalSize - 1
        if self.isWaited and self.canAppend():
            self.isWaited = False
            ret[1].append(QueueCanWriteEvent(self))
        if self.isWaitEmpty and not self:
            self.isWaitEmpty = False
            ret[2].append(QueueIsEmptyEvent(self))
        return ret
    cpdef tuple clear(self):
        '''
        Clear all the events in this queue, including any sub-queues.
        :returns: ((queueEvents,...), (queueEmptyEvents,...)) where queueEvents are QueueCanWriteEvents generated by clearing.
        '''
        cdef int l = len(self)
        cdef tuple ret = self._clear()
        cdef tuple pr
        if self.parent is not None:
            pr = self.parent.notifyPop(self, l)
            ret[0].extend(pr[0])
            ret[1].extend(pr[1])
        return ret
    cdef tuple _clear(self):
        '''
        Actual clear
        '''
        cdef tuple ret = ([],[])
        cdef _MultiQueue q
        cdef tuple pr
        for q in self.queues.values():
            pr = q._clear()
            ret[0].extend(pr[0])
            ret[1].extend(pr[1])
        self.totalSize = 0
        del self.prioritySet[:]
        if self.isWaited and self.canAppend():
            self.isWaited = False
            ret[0].append(QueueCanWriteEvent(self))
        if self.isWaitEmpty and not self:
            self.isWaitEmpty = False
            ret[1].append(QueueIsEmptyEvent(self))
        self.blockEvents.clear()
        return ret
    def __contains__(self, name):
        return name in self.queueindex
    def __getitem__(self, name):
        '''
        Get a sub-queue through q['sub-queue-name']
        '''
        return self.queueindex[name][1]
    def getPriority(self, queue):
        '''
        get priority of a sub-queue
        '''
        return self.queueindex[queue][0]
    def setPriority(self, queue, priority):
        '''
        Set priority of a sub-queue
        '''
        cdef list q = self.queueindex[queue]
        self.queues[q[0]].removeSubQueue(q[1])
        newPriority = self.queues.setdefault(priority, CBQueue.MultiQueue(self, priority))
        q[0] = priority
        newPriority.addSubQueue(q[1])
        
    cpdef addSubQueue(self, int priority, EventMatcher matcher, name = None, maxdefault = None, maxtotal = None, defaultQueueClass = FifoQueue):
        '''
        add a sub queue to current queue, with a priority and a matcher
        :param priority: priority of this queue. Larger is higher, 0 is lowest.
        :param matcher: an event matcher to catch events. Every event match the criteria will be stored in this queue.
        :param name: a unique name to identify the sub-queue. If none, the queue is anonymous. It can be any hashable value.
        :param maxdefault: max length for default queue.
        :param maxtotal: max length for sub-queue total, including sub-queues of sub-queue
        '''
        if name is not None and name in self.queueindex:
            raise IndexError("Duplicated sub-queue name '" + str(name) + "'")
        cdef MatchTree subtree = self.tree.subtree(matcher, True)
        cdef _MultiQueue newPriority = self.queues.setdefault(priority, _MultiQueue(self, priority))
        cdef CBQueue newQueue = CBQueue(subtree, newPriority, maxdefault, maxtotal, defaultQueueClass)
        newPriority.addSubQueue(newQueue)
        cdef list qi = [priority, newQueue, name]
        if name is not None:
            self.queueindex[name] = qi
        self.queueindex[newQueue] = qi
        return newQueue
    cpdef removeSubQueue(self, queue):
        '''
        remove a sub queue from current queue.
        This unblock the sub-queue, retrieve all events from the queue and put them back to the parent.
        Call clear on the sub-queue first if the events are not needed any more.
        :param queue: the name or queue object to remove
        :returns: ((queueevents,...), (queueEmptyEvents,...)) Possible queue events from removing sub-queues
        '''
        cdef list q = self.queueindex[queue]
        cdef CBQueue cbq = q[1]
        cbq.unblockall()
        cbq._removeFromTree()
        cdef tuple ret = ([],[])
        cdef tuple r
        while cbq.canPop():
            r = cbq.pop()
            self.append(r[0], True)
            ret[0].extend(r[1])
            ret[1].extend(r[2])
        cdef int qpriority = q[0]
        self.queues[qpriority].removeSubQueue(cbq)
        # Remove from index
        if q[2] is not None:
            del self.queueindex[q[2]]
        del self.queueindex[cbq]
        cdef bint newblocked =  not self.canPop()
        if newblocked != self.blocked:
            self.blocked = newblocked
            if self.parent is not None:
                self.parent.notifyBlock(self, newblocked)
        return ret
    def __len__(self):
        return self.totalSize
        
