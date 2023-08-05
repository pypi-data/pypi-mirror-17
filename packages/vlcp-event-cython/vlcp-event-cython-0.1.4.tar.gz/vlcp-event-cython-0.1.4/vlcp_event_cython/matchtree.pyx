'''
Created on 2015/06/01

:author: hubo
'''
from __future__ import print_function, absolute_import, division 
from vlcp_event_cython.event cimport Event, EventMatcher


cdef class MatchTree:
    '''
    A dictionary tree for fast event match
    '''
    @property
    def index(self):
        return self._index

    @property
    def matchers(self):
        return self._matchers

    @property
    def any(self):
        if self._any is None:
            raise AttributeError
        else:
            return self._any
    
    def __cinit__(self):
        self._index = {}
        self._matchers = []
        self.parent = None
        self._any = None
    def __init__(self, MatchTree parent = None):
        '''
        Constructor
        '''
        self.parent = parent
        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
    cpdef MatchTree subtree(self, EventMatcher matcher, bint create = False):
        '''
        Find a subtree from a matcher
        :param matcher: the matcher to locate the subtree. If None, return the root of the tree.
        :param create: if True, the subtree is created if not exists; otherwise return None if not exists
        '''
        if matcher is None:
            return self
        cdef MatchTree current = self
        cdef int i
        cdef MatchTree cany, current2, cind
        for i in range(self.depth, len(matcher.indices)):
            ind = matcher.indices[i]
            if ind is None:
                # match Any
                if current._any is not None:
                    current = current._any
                else:
                    if create:
                        cany = MatchTree(current)
                        cany.parentIndex = None
                        current._any = cany
                        current = cany
                    else:
                        return None
            else:
                current2 = current._index.get(ind)
                if current2 is None:
                    if create:
                        cind = MatchTree(current)
                        cind.parentIndex = ind 
                        current._index[ind] = cind
                        current = cind
                    else:
                        return None
                else:
                    current = current2
        return current        
    cpdef insert(self, EventMatcher matcher, obj):
        '''
        Insert a new matcher
        :param matcher: an EventMatcher
        :param obj: object to return
        '''
        cdef MatchTree current = self.subtree(matcher, True)
        current._matchers.append((matcher, obj))
        return current
    cpdef remove(self, EventMatcher matcher, obj):
        '''
        Remove the matcher
        :param matcher: an EventMatcher
        :param obj: the object to remove
        '''
        cdef MatchTree current = self.subtree(matcher, False)
        if current is None:
            return
        cdef tuple t
        cdef MatchTree p
        current._matchers[:] = [t for t in current._matchers if t[1] is not obj]
        while not current._matchers and current._any is None \
                and not current._index and current.parent is not None:
            # remove self from parents
            ind = current.parentIndex
            if ind is None:
                current.parent._any = None
            else:
                del current.parent._index[ind]
            p = current.parent
            current.parent = None
            current = p
    cpdef tuple matchesWithMatchers(self, Event event):
        '''
        Return all matches for this event. The first matcher is also returned for each matched object.
        :param event: an input event
        '''
        cdef list ret = []
        cdef set s = set()
        self._matches(event, s, ret)
        return tuple(ret)
    cpdef tuple matches(self, Event event):
        '''
        Return all matches for this event. The first matcher is also returned for each matched object.
        :param event: an input event
        '''
        cdef list ret = []
        cdef set s = set()
        self._matches(event, s, ret)
        cdef tuple r
        return tuple([r[0] for r in ret])
    cdef int _matches(self, Event event, set duptest, list retlist) except -1:
        # 1. matches(self.index[ind], event)
        # 2. matches(self.any, event)
        # 3. self.matches
        cdef MatchTree subtree
        if self.depth < len(event.indices):
            ind = event.indices[self.depth]
            if ind in self._index:
                subtree = self._index[ind]
                subtree._matches(event, duptest, retlist)
            if self._any is not None:
                self._any._matches(event, duptest, retlist)
        cdef EventMatcher m
        for m,o in self._matchers:
            if o not in duptest and m.judge(event):
                duptest.add(o)
                retlist.append((o, m))
    cpdef matchfirst(self, Event event):
        '''
        Return first match for this event
        :param event: an input event
        '''
        # 1. matches(self.index[ind], event)
        # 2. matches(self.any, event)
        # 3. self.matches
        cdef MatchTree subtree
        if self.depth < len(event.indices):
            ind = event.indices[self.depth]
            if ind in self._index:
                subtree = self._index[ind]
                m = subtree.matchfirst(event)
                if m is not None:
                    return m
            if self._any is not None:
                m = self._any.matchfirst(event)
                if m is not None:
                    return m
        cdef EventMatcher m2
        for m2,o in self._matchers:
            if m2 is None or m2.judge(event):
                return o
            node = node._next

cdef class EventTree:
    '''
    Store events; match matchers
    '''
    @property
    def events(self):
        return self._events

    @property
    def subevents(self):
        if self.hassubtree:
            raise AttributeError
        else:
            return self._subevents

    @property
    def index(self):
        if self.hassubtree:
            return self._index
        else:
            raise AttributeError
    
    def __cinit__(self):
        self._events = []
        self._subevents = []
        self._index = {}
        self.hassubtree = False
    def __init__(self, EventTree parent = None, int branch = 5):
        '''
        Constructor
        '''
        self.parent = parent
        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.branch = branch
    cpdef EventTree subtree(self, Event event, bint create = False):
        '''
        Find a subtree from an event
        '''
        cdef EventTree current = self
        cdef EventTree current2
        cdef int i
        for i in range(self.depth, len(event.indices)):
            if not current.hassubtree:
                return current
            ind = event.indices[i]
            current2 = current._index.get(ind)
            if current2 is None:
                if create:
                    current2 = EventTree(current, self.branch)
                    current._index[ind] = current2
                    current2.parentIndex = ind
                else:
                    return None
            current = current2
        return current
    cpdef insert(self, Event event):
        cdef EventTree current = self.subtree(event, True)
        if current.depth == len(event.indices):
            current._events.append(event)
        else:
            current._subevents.append(event)
            if len(current._subevents) > current.branch:
                current.hassubtree = True
                for e in current._subevents:
                    current.insert(e)
                del current._subevents[:]
    cdef int _returnAll(self, list ret) except -1:
        ret.extend(self._events)
        cdef EventTree st
        if self.hassubtree:
            for st in self.index.values():
                st._returnAll(ret)
        else:
            ret.extend(self._subevents)
    cdef int _removeFromParent(self) except -1:
        cdef EventTree current = self
        cdef EventTree p
        while current.parent is not None:
            del current.parent._index[current.parentIndex]
            p = current.parent
            current.parent = None
            current = p
            if current._index or current.events:
                break
        if current.hassubtree and not current._index:
            current.hassubtree = False
    cdef int _findAndRemove(self, EventMatcher matcher, list ret) except -1:
        cdef EventTree current = self
        cdef list newsub = []
        cdef EventTree st
        cdef Event e
        while current.depth < len(matcher.indices):
            ind = matcher.indices[current.depth]
            if not current.hassubtree:
                del newsub[:]
                for e in current._subevents:
                    if matcher.isMatch(e, current.depth):
                        ret.append(e)
                    else:
                        newsub.append(e)
                current._subevents[:] = newsub
                if not current._subevents and not current._events:
                    current._removeFromParent()
                return 0
            elif ind is None:
                for st in current._index.values():
                    st._findAndRemove(matcher, ret)
                return 0
            else:
                if ind not in current._index:
                    return 0
                current = current._index[ind]
        current._returnAll(ret)
        current._removeFromParent()
    cpdef findAndRemove(self, EventMatcher matcher):
        cdef list ret = []
        self._findAndRemove(matcher, ret)
        return tuple(ret)
    cpdef remove(self, Event event):
        cdef EventTree current = self.subtree(event)
        if current.depth == len(event.indices):
            current._events.remove(event)
        else:
            current._subevents.remove(event)

            
