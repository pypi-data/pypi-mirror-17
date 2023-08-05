# -*- coding: utf-8 -*-
"""elasticsearch_django apps module - includes config validation functions."""
import logging

from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.db.models import signals

from elasticsearch_django import settings

logger = logging.getLogger(__name__)


class ElasticAppConfig(AppConfig):

    """AppConfig for Search3."""

    name = 'elasticsearch_django'
    verbose_name = "Django Powered ElasticSearch"
    configs = []

    def ready(self):
        """Validate config and connect signals."""
        super(ElasticAppConfig, self).ready()
        _validate_config(settings.get_setting('strict_validation'))
        if settings.get_setting('auto_sync'):
            _connect_signals()
        else:
            logger.debug("SEARCH_AUTO_SYNC has been disabled.")


def _validate_config(strict=False):
    """Validate settings.SEARCH_SETTINGS."""
    for index in settings.get_index_names():
        _validate_mapping(index, strict=strict)
        for model in settings.get_index_models(index):
            _validate_model(model)


def _validate_mapping(index, strict=False):
    """Check that an index mapping JSON file exists."""
    try:
        settings.get_index_mapping(index)
    except IOError:
        if strict:
            raise ImproperlyConfigured("Index '%s' has no mapping file.")
        else:
            logger.warn("Index '%s' has no mapping, relying on ES instead.", index)


def _validate_model(model):
    """Check that a model configured for an index subclasses the required classes."""
    if not hasattr(model, 'as_search_document'):
        raise ImproperlyConfigured(
            "'%s' must implement `as_search_document`." % model
        )
    if not hasattr(model.objects, 'get_search_queryset'):
        raise ImproperlyConfigured(
            "'%s.objects must implement `get_search_queryset`." % model
        )


def _connect_signals():
    """Connect up post_save, post_delete signals for models."""
    for index in settings.get_index_names():
        for model in settings.get_index_models(index):
            dispatch_uid = '%s.post_save' % model._meta.model_name
            logger.debug("Connecting search index model sync signal: %s", dispatch_uid)
            signals.post_save.connect(_on_model_save, sender=model, dispatch_uid=dispatch_uid)
            dispatch_uid = '%s.post_delete' % model._meta.model_name
            logger.debug("Connecting search index model sync signal: %s", dispatch_uid)
            signals.post_delete.connect(_on_model_delete, sender=model, dispatch_uid=dispatch_uid)


def _on_model_save(sender, **kwargs):
    """Update documents in search index post_save."""
    _update_search_index(kwargs.get('instance'), 'index')


def _on_model_delete(sender, **kwargs):
    """Remove documents from search index post_delete."""
    _update_search_index(kwargs.get('instance'), 'delete')


def _update_search_index(instance, action):
    """Process generic search index update actions."""
    try:
        instance.update_search_index(action)
    except:
        logger.exception("Error handling '%s' signal for %s", action, instance)
