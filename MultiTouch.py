'''
CursorTracker.py will maintain a real-time list of all cursors 
and their respective positions. It is updated via a tuio "thread"

Modified from Python Input Module for NumptyPhysics 
'''

import sys
import collections
import math

WIDTH = 680
HEIGHT = 460

class CursorTracker(object):
    def __init__(self, max_cursors):
        self._seen = {}
        self._coords = {}
        self._prevCoords = {}
        self._startCoords = {}
        self._freeslots = collections.deque(range(max_cursors))
        
    '''
    FINGER DETECTION
    '''

    def update(self, cursors):
        vanished = list(self._seen)
        for cursor in cursors:
            id, x, y = cursor.sessionid, cursor.xpos, cursor.ypos
            x, y = self.convert_coords(x, y)
            
            if id in self._seen:
                # cursor still active
                vanished.remove(id)
                if self._coords[id] != (x, y):
                    self._prevCoords[id] = self._coords[id]
                    self._coords[id] = (x, y)
                else:
                    self._prevCoords[id] = self._coords[id]
            else:
                # found a new cursor
                taken_slot = self.grabslot()
                if taken_slot is None:
                    print 'IGNORING EXCESSIVE CURSOR'
                    continue
                self._seen[id] = taken_slot
                self._startCoords[id] = (x,y)
                self._prevCoords[id] = (x,y)
                self._coords[id] = (x, y)

        for id in vanished:
            # the cursor vanished
            self._startCoords[id] = (self._startCoords[id][0]+2, self._startCoords[id][1]+2)
            self._prevCoords[id] = (self._prevCoords[id][0]+2, self._prevCoords[id][1]+2)
            self._coords[id] = (self._coords[id][0]+2, self._coords[id][1]+2)
            self.freeslot(self._seen[id])
            del self._startCoords[id]
            del self._prevCoords[id]
            del self._coords[id]
            del self._seen[id]
            
    def grabslot(self):
        try:
            return self._freeslots.pop()
        except IndexError:
            return None

    def freeslot(self, slot):
        self._freeslots.appendleft(slot)

    def convert_coords(self, x, y):
        return (int(x*WIDTH), int(HEIGHT-y*HEIGHT))
            
    def fingers_detected(self):
        return len(self._seen)
        