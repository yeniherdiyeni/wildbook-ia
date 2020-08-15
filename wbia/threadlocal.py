# -*- coding: utf-8 -*-
"""
Thread-Local - management of data between threads and parallel processes
"""
import threading


__all__ = (
    'get_current_db',
    'get_current_settings',
    'manager',
)


class ThreadLocalManager(threading.local):
    def __init__(self):
        self.stack = []

    def push(self, info):
        self.stack.append(info)

    def pop(self):
        if self.stack:
            return self.stack.pop()

    def get(self):
        return self.stack[-1]

    def clear(self):
        self.stack[:] = []


manager = ThreadLocalManager()


def get_current_db():
    """Return the active controller"""
    return manager.get()['db']


def get_current_settings():
    """Return the active settings"""
    return manager.get()['settings']
