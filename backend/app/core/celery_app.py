#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
功能描述: 
作者: ly
版本: 1.0.0
"""

from celery import Celery

celery_app = Celery(
    "worker",
    broker="redis://localhost:6379/1",
    backend="redis://localhost:6379/2",
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)


celery_app.autodiscover_tasks([
    "app.workers",
])