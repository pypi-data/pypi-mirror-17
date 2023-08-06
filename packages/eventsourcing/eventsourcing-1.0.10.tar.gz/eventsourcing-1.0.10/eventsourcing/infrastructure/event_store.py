import six

from eventsourcing.domain.model.events import DomainEvent
from eventsourcing.exceptions import ConcurrencyError
from eventsourcing.infrastructure.stored_events.base import StoredEventRepository


class EventStore(object):

    def __init__(self, stored_event_repo):
        assert isinstance(stored_event_repo, StoredEventRepository), stored_event_repo
        self.stored_event_repo = stored_event_repo

    def append(self, domain_event):
        assert isinstance(domain_event, DomainEvent)
        # Serialize the domain event.
        stored_event = self.stored_event_repo.serialize(domain_event)

        # Optimistic concurrency control.
        if domain_event.entity_version:
            last_event = self.get_most_recent_event(stored_event.stored_entity_id)
            if last_event is not None:
                assert isinstance(last_event, DomainEvent), last_event
                last_version = last_event.entity_version
                this_version = domain_event.entity_version
                if this_version - 1 != last_version:
                    raise ConcurrencyError("Can't append event at version {}, last stored version is {}"
                                           "".format(this_version, last_version))

        # Append the stored event to the stored event repo.
        self.stored_event_repo.append(stored_event)

    def get_entity_events(self, stored_entity_id, after=None, until=None,
                          limit=None, is_ascending=True, page_size=None, is_short=False):
        # Get the events that have been stored for the entity.
        if page_size:
            stored_events = self.stored_event_repo.iterate_entity_events(
                stored_entity_id=stored_entity_id,
                after=after,
                until=until,
                limit=limit,
                is_ascending=is_ascending,
                page_size=page_size
            )
        elif is_short:
            stored_events = self.stored_event_repo.get_entity_events(
                stored_entity_id=stored_entity_id,
                after=after,
                until=until,
                limit=limit,
                query_ascending=False,  # Speed up for Cassandra, assuming primary TimeUUID key is stored descending.
                results_ascending=False,  # Still need to return the events in ascending order.
            )
            stored_events = reversed(stored_events)
        else:
            stored_events = self.stored_event_repo.get_entity_events(
                stored_entity_id=stored_entity_id,
                after=after,
                until=until,
                limit=limit,
                query_ascending=is_ascending,
                results_ascending=is_ascending,
            )

        # Deserialize all the stored event objects into domain event objects.
        return six.moves.map(self.stored_event_repo.deserialize, stored_events)

    def get_most_recent_event(self, stored_entity_id, until=None):
        """Returns last event for given entity ID.

        :rtype: DomainEvent, NoneType
        """
        stored_event = self.stored_event_repo.get_most_recent_event(stored_entity_id, until=until)
        return None if stored_event is None else self.stored_event_repo.deserialize(stored_event)
